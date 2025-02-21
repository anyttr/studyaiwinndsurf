"""Quiz models"""
from datetime import datetime
from src.extensions import db

class Quiz(db.Model):
    """Quiz model"""
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.Integer, default=1)  # 1-5
    time_limit = db.Column(db.Integer)  # Time limit in minutes, null for no limit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('created_quizzes', lazy=True))
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True)
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True)

    def __repr__(self):
        return f'<Quiz {self.title}>'

class QuizQuestion(db.Model):
    """Quiz Question model"""
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # multiple_choice, true_false, open_ended
    correct_answer = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON)  # For multiple choice questions
    points = db.Column(db.Integer, default=1)
    
    # Foreign keys
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    
    # Relationships
    answers = db.relationship('QuizAnswer', backref='question', lazy=True)

    def __repr__(self):
        return f'<QuizQuestion {self.id}>'

class QuizAttempt(db.Model):
    """Quiz Attempt model"""
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    score = db.Column(db.Integer)
    max_score = db.Column(db.Integer)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, abandoned
    
    # Foreign keys
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_session_id = db.Column(db.Integer, db.ForeignKey('study_sessions.id'))
    
    # Relationships
    user = db.relationship('User', backref=db.backref('quiz_attempts', lazy=True))
    answers = db.relationship('QuizAnswer', backref='attempt', lazy=True)
    study_session = db.relationship('StudySession', backref=db.backref('quiz_attempts', lazy=True))

    def __repr__(self):
        return f'<QuizAttempt {self.id}>'

class QuizAnswer(db.Model):
    """Quiz Answer model"""
    __tablename__ = 'quiz_answers'

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean)
    points_earned = db.Column(db.Integer)
    
    # Foreign keys
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), nullable=False)

    def __repr__(self):
        return f'<QuizAnswer {self.id}>'
