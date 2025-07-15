from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_socketio import emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, socketio
from models import User, CollaborationRequest, Message, Project
from compatibility import get_compatible_users
import logging

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('signin.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f'Welcome to Thynkly, {user.full_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('signin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        field_of_work = request.form.get('field_of_work')
        keywords = request.form.get('keywords')
        interests = request.form.get('interests')
        bio = request.form.get('bio')
        
        # Validation
        if not all([username, email, password, confirm_password, full_name, field_of_work]):
            flash('All required fields must be filled.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            field_of_work=field_of_work,
            keywords=keywords,
            interests=interests,
            bio=bio
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash(f'Welcome to Thynkly, {user.full_name}! Your account has been created.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('signin'))

@app.route('/dashboard')
@login_required
def dashboard():
    search_keyword = request.args.get('search', '')
    user_scores = get_compatible_users(current_user, search_keyword)
    return render_template('dashboard.html', user_scores=user_scores, search_keyword=search_keyword)

@app.route('/profile')
@login_required
def profile():
    # Get user's projects
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.created_at.desc()).all()
    return render_template('profile.html', user=current_user, projects=projects)

@app.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    current_user.full_name = request.form.get('full_name', current_user.full_name)
    current_user.field_of_work = request.form.get('field_of_work', current_user.field_of_work)
    current_user.keywords = request.form.get('keywords', current_user.keywords)
    current_user.interests = request.form.get('interests', current_user.interests)
    current_user.bio = request.form.get('bio', current_user.bio)
    
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/request_collaboration', methods=['POST'])
@login_required
def request_collaboration():
    recipient_id = request.form.get('recipient_id')
    message = request.form.get('message', '')
    
    if not recipient_id:
        flash('Invalid recipient.', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if request already exists
    existing_request = CollaborationRequest.query.filter_by(
        requester_id=current_user.id,
        recipient_id=recipient_id
    ).first()
    
    if existing_request:
        flash('You have already sent a collaboration request to this user.', 'error')
        return redirect(url_for('dashboard'))
    
    # Create new request
    new_request = CollaborationRequest(
        requester_id=current_user.id,
        recipient_id=recipient_id,
        message=message
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    flash('Collaboration request sent!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/notifications')
@login_required
def notifications():
    pending_requests = CollaborationRequest.query.filter_by(
        recipient_id=current_user.id,
        status='pending'
    ).order_by(CollaborationRequest.created_at.desc()).all()
    
    sent_requests = CollaborationRequest.query.filter_by(
        requester_id=current_user.id
    ).order_by(CollaborationRequest.created_at.desc()).all()
    
    return render_template('notifications.html', 
                         pending_requests=pending_requests,
                         sent_requests=sent_requests)

@app.route('/respond_request', methods=['POST'])
@login_required
def respond_request():
    request_id = request.form.get('request_id')
    action = request.form.get('action')  # 'approve' or 'decline'
    
    collab_request = CollaborationRequest.query.get_or_404(request_id)
    
    if collab_request.recipient_id != current_user.id:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('notifications'))
    
    if action == 'approve':
        collab_request.status = 'approved'
        flash('Collaboration request approved!', 'success')
    elif action == 'decline':
        collab_request.status = 'declined'
        flash('Collaboration request declined.', 'info')
    
    db.session.commit()
    return redirect(url_for('notifications'))

@app.route('/chat')
@login_required
def chat():
    # Get approved collaborations
    approved_requests = db.session.query(CollaborationRequest).filter(
        db.or_(
            db.and_(CollaborationRequest.requester_id == current_user.id, CollaborationRequest.status == 'approved'),
            db.and_(CollaborationRequest.recipient_id == current_user.id, CollaborationRequest.status == 'approved')
        )
    ).all()
    
    # Get unique users current user can chat with
    chat_users = set()
    for req in approved_requests:
        if req.requester_id == current_user.id:
            chat_users.add(req.recipient)
        else:
            chat_users.add(req.requester)
    
    selected_user_id = request.args.get('user_id')
    selected_user = None
    messages = []
    
    if selected_user_id:
        selected_user = User.query.get(selected_user_id)
        if selected_user and selected_user in chat_users:
            # Get messages between current user and selected user
            messages = Message.query.filter(
                db.or_(
                    db.and_(Message.sender_id == current_user.id, Message.recipient_id == selected_user.id),
                    db.and_(Message.sender_id == selected_user.id, Message.recipient_id == current_user.id)
                )
            ).order_by(Message.timestamp.asc()).all()
            
            # Mark messages as read
            Message.query.filter_by(
                sender_id=selected_user.id,
                recipient_id=current_user.id,
                is_read=False
            ).update({'is_read': True})
            db.session.commit()
    
    return render_template('chat.html', 
                         chat_users=list(chat_users),
                         selected_user=selected_user,
                         messages=messages)

# New route for detailed user view
@app.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return redirect(url_for('profile'))
    
    # Get user's projects
    projects = Project.query.filter_by(user_id=user_id).order_by(Project.created_at.desc()).all()
    
    # Check if there's an existing collaboration request
    existing_request = CollaborationRequest.query.filter_by(
        requester_id=current_user.id,
        recipient_id=user_id
    ).first()
    
    # Check if users are already collaborating
    is_collaborating = CollaborationRequest.query.filter(
        db.or_(
            db.and_(CollaborationRequest.requester_id == current_user.id, 
                   CollaborationRequest.recipient_id == user_id,
                   CollaborationRequest.status == 'approved'),
            db.and_(CollaborationRequest.requester_id == user_id, 
                   CollaborationRequest.recipient_id == current_user.id,
                   CollaborationRequest.status == 'approved')
        )
    ).first() is not None
    
    return render_template('user_detail.html', 
                         user=user, 
                         projects=projects,
                         existing_request=existing_request,
                         is_collaborating=is_collaborating)

# Route for adding projects
@app.route('/add_project', methods=['POST'])
@login_required
def add_project():
    title = request.form.get('title')
    description = request.form.get('description')
    project_type = request.form.get('project_type')
    project_url = request.form.get('project_url')
    thumbnail_url = request.form.get('thumbnail_url')
    tags = request.form.get('tags')
    
    if not title or not project_url or not project_type:
        flash('Title, project URL, and type are required.', 'error')
        return redirect(url_for('profile'))
    
    # Validate project type
    if project_type not in ['replit', 'gdrive']:
        flash('Invalid project type.', 'error')
        return redirect(url_for('profile'))
    
    # Create new project
    project = Project(
        user_id=current_user.id,
        title=title,
        description=description,
        project_type=project_type,
        project_url=project_url,
        thumbnail_url=thumbnail_url,
        tags=tags
    )
    
    db.session.add(project)
    db.session.commit()
    
    flash('Project added successfully!', 'success')
    return redirect(url_for('profile'))

# Route for deleting projects
@app.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if project.user_id != current_user.id:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('profile'))
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('profile'))

# Socket.IO events
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    logging.debug(f"User {current_user.id} joined room {room}")

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    logging.debug(f"User {current_user.id} left room {room}")

@socketio.on('send_message')
def handle_message(data):
    recipient_id = data['recipient_id']
    content = data['content']
    room = data['room']
    
    # Verify users can chat
    approved_request = CollaborationRequest.query.filter(
        db.or_(
            db.and_(CollaborationRequest.requester_id == current_user.id, 
                   CollaborationRequest.recipient_id == recipient_id,
                   CollaborationRequest.status == 'approved'),
            db.and_(CollaborationRequest.recipient_id == current_user.id, 
                   CollaborationRequest.requester_id == recipient_id,
                   CollaborationRequest.status == 'approved')
        )
    ).first()
    
    if not approved_request:
        return
    
    # Save message
    message = Message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()
    
    # Emit message to room
    emit('receive_message', {
        'sender_id': current_user.id,
        'sender_name': current_user.full_name,
        'content': content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }, room=room)
