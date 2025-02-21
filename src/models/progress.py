"""Learning Progress models"""
from datetime import datetime
from src.extensions import db

class LearningProgress(db.Model):
    """Learning Progress model"""
    __tablename__ = 'learning_progress'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    level = db.Column(db.Integer, default=1)  # 1-5 indicating proficiency level
    progress = db.Column(db.Integer, default=0)  # 0-100
    last_reviewed = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('learning_goals.id'))
    
    # Relationships
    user = db.relationship('User', backref=db.backref('learning_progress', lazy=True))
    goal = db.relationship('LearningGoal', backref=db.backref('progress_records', lazy=True))

    def __repr__(self):
        return f'<LearningProgress {self.topic}>'
