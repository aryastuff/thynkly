from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    field_of_work = db.Column(db.String(100), nullable=False)
    keywords = db.Column(db.Text)  # Comma-separated keywords
    interests = db.Column(db.Text)  # Comma-separated interests
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sent_requests = db.relationship('CollaborationRequest', foreign_keys='CollaborationRequest.requester_id', backref='requester', lazy='dynamic')
    received_requests = db.relationship('CollaborationRequest', foreign_keys='CollaborationRequest.recipient_id', backref='recipient', lazy='dynamic')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    projects = db.relationship('Project', backref='user', lazy='dynamic', cascade='all, delete-orphan')

class CollaborationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, declined
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_type = db.Column(db.String(50), nullable=False)  # 'replit' or 'gdrive'
    project_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500))
    tags = db.Column(db.Text)  # Comma-separated tags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
