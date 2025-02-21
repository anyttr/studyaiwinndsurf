"""Learning Goal models"""
from datetime import datetime
from src.extensions import db

class GoalType(db.Model):
    """Goal Type model"""
    __tablename__ = 'goal_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GoalType {self.name}>'

class LearningGoal(db.Model):
    """Learning Goal model"""
    __tablename__ = 'learning_goals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, completed, abandoned
    progress = db.Column(db.Integer, default=0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal_type_id = db.Column(db.Integer, db.ForeignKey('goal_types.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('learning_goals', lazy=True))
    goal_type = db.relationship('GoalType', backref=db.backref('learning_goals', lazy=True))

    def __repr__(self):
        return f'<LearningGoal {self.title}>'
