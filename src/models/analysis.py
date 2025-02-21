"""Analysis models"""
from datetime import datetime
from src.extensions import db

class AnalysisResult(db.Model):
    """Analysis Result model"""
    __tablename__ = 'analysis_results'

    id = db.Column(db.Integer, primary_key=True)
    analysis_type = db.Column(db.String(100), nullable=False)  # e.g., 'learning_pattern', 'performance_trend'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    data = db.Column(db.JSON)  # Store analysis data in JSON format
    recommendations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_session_id = db.Column(db.Integer, db.ForeignKey('study_sessions.id'))
    learning_goal_id = db.Column(db.Integer, db.ForeignKey('learning_goals.id'))
    
    # Relationships
    user = db.relationship('User', backref=db.backref('analysis_results', lazy=True))
    study_session = db.relationship('StudySession', backref=db.backref('analysis_results', lazy=True))
    learning_goal = db.relationship('LearningGoal', backref=db.backref('analysis_results', lazy=True))

    def __repr__(self):
        return f'<AnalysisResult {self.title}>'
