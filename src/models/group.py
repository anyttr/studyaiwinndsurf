from datetime import datetime
from src.models import db

class StudyGroup(db.Model):
    __tablename__ = 'study_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(10), nullable=False)  # 'en' or 'ro'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Group settings
    max_members = db.Column(db.Integer, default=10)
    is_private = db.Column(db.Boolean, default=False)
    join_code = db.Column(db.String(20), unique=True)
    
    # Relationships
    members = db.relationship('GroupMembership', back_populates='group')
    resources = db.relationship('GroupResource', back_populates='group')
    messages = db.relationship('GroupMessage', back_populates='group')
    events = db.relationship('GroupEvent', back_populates='group')

class GroupMembership(db.Model):
    __tablename__ = 'group_memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('study_groups.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # admin, moderator, member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='group_memberships')
    group = db.relationship('StudyGroup', back_populates='members')

class GroupResource(db.Model):
    __tablename__ = 'group_resources'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('study_groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)  # flashcard_deck, note, link, etc.
    content = db.Column(db.Text)
    url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('StudyGroup', back_populates='resources')
    user = db.relationship('User')

class GroupMessage(db.Model):
    __tablename__ = 'group_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('study_groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, system, file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('StudyGroup', back_populates='messages')
    user = db.relationship('User')
    replies = db.relationship('GroupMessage',
        backref=db.backref('parent', remote_side=[id]))

class GroupEvent(db.Model):
    __tablename__ = 'group_events'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('study_groups.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)  # study_session, quiz, discussion
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    video_link = db.Column(db.String(500))  # For video conferencing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('StudyGroup', back_populates='events')
    creator = db.relationship('User')
    participants = db.relationship('GroupEventParticipant', back_populates='event')

class GroupEventParticipant(db.Model):
    __tablename__ = 'group_event_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('group_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    event = db.relationship('GroupEvent', back_populates='participants')
    user = db.relationship('User')
