"""Schedule models"""
from datetime import datetime
from src.extensions import db

class StudySessionType(db.Model):
    """Study Session Type model"""
    __tablename__ = 'study_session_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # Duration in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StudySessionType {self.name}>'

class StudySession(db.Model):
    """Study Session model"""
    __tablename__ = 'study_sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_type_id = db.Column(db.Integer, db.ForeignKey('study_session_types.id'))
    
    # Relationships
    user = db.relationship('User', backref=db.backref('study_sessions', lazy=True))
    session_type = db.relationship('StudySessionType', backref=db.backref('sessions', lazy=True))

    def __repr__(self):
        return f'<StudySession {self.title}>'
