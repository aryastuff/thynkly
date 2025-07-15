from models import User
from app import db

def calculate_compatibility(user1, user2):
    """
    Calculate compatibility score between two users based on:
    - Field of work similarity
    - Keyword overlap
    - Interest overlap
    """
    if not user1 or not user2 or user1.id == user2.id:
        return 0
    
    score = 0
    
    # Field of work similarity (30% weight)
    if user1.field_of_work and user2.field_of_work:
        if user1.field_of_work.lower() == user2.field_of_work.lower():
            score += 30
        elif 'tech' in user1.field_of_work.lower() and 'tech' in user2.field_of_work.lower():
            score += 15  # Partial match for tech fields
    
    # Keywords overlap (40% weight)
    if user1.keywords and user2.keywords:
        keywords1 = set(k.strip().lower() for k in user1.keywords.split(',') if k.strip())
        keywords2 = set(k.strip().lower() for k in user2.keywords.split(',') if k.strip())
        
        if keywords1 and keywords2:
            overlap = len(keywords1.intersection(keywords2))
            total_unique = len(keywords1.union(keywords2))
            if total_unique > 0:
                score += (overlap / total_unique) * 40
    
    # Interests overlap (30% weight)
    if user1.interests and user2.interests:
        interests1 = set(i.strip().lower() for i in user1.interests.split(',') if i.strip())
        interests2 = set(i.strip().lower() for i in user2.interests.split(',') if i.strip())
        
        if interests1 and interests2:
            overlap = len(interests1.intersection(interests2))
            total_unique = len(interests1.union(interests2))
            if total_unique > 0:
                score += (overlap / total_unique) * 30
    
    return min(100, max(0, round(score)))

def get_compatible_users(current_user, search_keyword=None):
    """
    Get all users with compatibility scores, optionally filtered by search keyword
    """
    query = User.query.filter(User.id != current_user.id)
    
    if search_keyword:
        search_term = f"%{search_keyword.lower()}%"
        query = query.filter(
            db.or_(
                User.keywords.ilike(search_term),
                User.interests.ilike(search_term),
                User.field_of_work.ilike(search_term),
                User.full_name.ilike(search_term),
                User.bio.ilike(search_term)
            )
        )
    
    users = query.all()
    
    # Calculate compatibility scores and sort
    user_scores = []
    for user in users:
        score = calculate_compatibility(current_user, user)
        user_scores.append((user, score))
    
    # Sort by compatibility score (descending)
    user_scores.sort(key=lambda x: x[1], reverse=True)
    
    return user_scores
