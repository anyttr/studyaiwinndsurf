"""Question and Answer models"""
from datetime import datetime
from src.extensions import db

class Question(db.Model):
    """Question model"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en')  # ISO language code
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    answers = db.relationship('Answer', backref='question', lazy=True)
    votes = db.relationship('QuestionVote', backref='question', lazy=True)
    tags = db.relationship('Tag', secondary='question_tags', backref=db.backref('questions', lazy=True))
    
    def to_dict(self):
        """Convert question to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'language': self.language,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tags': [tag.name for tag in self.tags],
            'vote_count': sum(vote.value for vote in self.votes),
            'answer_count': len(self.answers)
        }

class Answer(db.Model):
    """Answer model"""
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_accepted = db.Column(db.Boolean, default=False)
    
    # Relationships
    votes = db.relationship('AnswerVote', backref='answer', lazy=True)
    
    def to_dict(self):
        """Convert answer to dictionary"""
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_accepted': self.is_accepted,
            'vote_count': sum(vote.value for vote in self.votes)
        }

class QuestionVote(db.Model):
    """Question vote model"""
    __tablename__ = 'question_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)  # 1 for upvote, -1 for downvote
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'question_id', name='unique_question_vote'),
    )
    
    def to_dict(self):
        """Convert vote to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'value': self.value,
            'created_at': self.created_at.isoformat()
        }

class AnswerVote(db.Model):
    """Answer vote model"""
    __tablename__ = 'answer_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)  # 1 for upvote, -1 for downvote
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'answer_id', name='unique_answer_vote'),
    )
    
    def to_dict(self):
        """Convert vote to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'answer_id': self.answer_id,
            'value': self.value,
            'created_at': self.created_at.isoformat()
        }

class Tag(db.Model):
    """Tag model"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert tag to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }

# Association table for question tags
question_tags = db.Table('question_tags',
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)
