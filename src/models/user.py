"""User models"""
from datetime import datetime
from src.extensions import db

class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    questions = db.relationship('Question', backref='user', lazy=True)
    answers = db.relationship('Answer', backref='user', lazy=True)
    resources = db.relationship('Resource', backref='user', lazy=True)
    accessibility_settings = db.relationship('AccessibilitySettings', backref='user', uselist=False, lazy=True)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

    def __repr__(self):
        return f'<User {self.name}>'

class AccessibilitySettings(db.Model):
    """User accessibility settings"""
    __tablename__ = 'accessibility_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    font_size = db.Column(db.Integer, default=16)  # in pixels
    high_contrast = db.Column(db.Boolean, default=False)
    reduced_motion = db.Column(db.Boolean, default=False)
    dyslexic_font = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert settings to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'font_size': self.font_size,
            'high_contrast': self.high_contrast,
            'reduced_motion': self.reduced_motion,
            'dyslexic_font': self.dyslexic_font,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<AccessibilitySettings for User {self.user_id}>'
