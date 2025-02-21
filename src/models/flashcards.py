"""Flashcard models"""
from datetime import datetime
from src.extensions import db

class Flashcard(db.Model):
    """Flashcard model"""
    __tablename__ = 'flashcards'

    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)
    hint = db.Column(db.Text)
    difficulty = db.Column(db.Integer, default=1)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('flashcard_decks.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('flashcards', lazy=True))
    deck = db.relationship('FlashcardDeck', backref=db.backref('flashcards', lazy=True))
    reviews = db.relationship('FlashcardReview', backref='flashcard', lazy=True)

    def __repr__(self):
        return f'<Flashcard {self.id}>'

class FlashcardDeck(db.Model):
    """Flashcard Deck model"""
    __tablename__ = 'flashcard_decks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('flashcard_decks', lazy=True))

    def __repr__(self):
        return f'<FlashcardDeck {self.name}>'

class FlashcardReview(db.Model):
    """Flashcard Review model"""
    __tablename__ = 'flashcard_reviews'

    id = db.Column(db.Integer, primary_key=True)
    confidence = db.Column(db.Integer, nullable=False)  # 1-5
    time_taken = db.Column(db.Integer)  # Time taken in seconds
    review_date = db.Column(db.DateTime, default=datetime.utcnow)
    next_review_date = db.Column(db.DateTime)
    
    # Foreign keys
    flashcard_id = db.Column(db.Integer, db.ForeignKey('flashcards.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_session_id = db.Column(db.Integer, db.ForeignKey('study_sessions.id'))
    
    # Relationships
    user = db.relationship('User', backref=db.backref('flashcard_reviews', lazy=True))
    study_session = db.relationship('StudySession', backref=db.backref('flashcard_reviews', lazy=True))

    def __repr__(self):
        return f'<FlashcardReview {self.id}>'
