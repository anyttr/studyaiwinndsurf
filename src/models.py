from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from src import db

class GoalType(enum.Enum):
    EXAM_PREP = "exam_preparation"
    TOPIC_MASTERY = "topic_mastery"
    GENERAL_UNDERSTANDING = "general_understanding"

class QuestionType(enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_IN_BLANK = "fill_in_blank"
    SHORT_ANSWER = "short_answer"

class StudySessionType(enum.Enum):
    FLASHCARDS = "flashcards"
    QUIZ = "quiz"
    MICROLEARNING = "microlearning"
    READING = "reading"

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    uploads = relationship('Upload', back_populates='user')
    learning_progress = relationship('LearningProgress', back_populates='user')
    learning_goals = relationship('LearningGoal', back_populates='user')
    study_sessions = relationship('StudySession', back_populates='user')
    flashcard_decks = relationship('FlashcardDeck', back_populates='user')
    flashcard_reviews = relationship('FlashcardReview', back_populates='user')
    quizzes = relationship('Quiz', back_populates='user')
    quiz_attempts = relationship('QuizAttempt', back_populates='user')
    videos = relationship('StudyTokVideo', back_populates='user')

class Upload(db.Model):
    __tablename__ = 'uploads'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    content_length = Column(Integer)
    upload_date = Column(DateTime, default=datetime.utcnow)
    language = Column(String(10))
    analysis_results = relationship('AnalysisResult', back_populates='upload')
    user = relationship('User', back_populates='uploads')

class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    
    id = Column(Integer, primary_key=True)
    upload_id = Column(Integer, ForeignKey('uploads.id'), nullable=False)
    concepts = Column(JSON)  # Stores extracted concepts
    difficulty_assessment = Column(JSON)  # Stores difficulty metrics
    summaries = Column(JSON)  # Stores generated summaries
    visualization_paths = Column(JSON)  # Stores paths to generated visualizations
    created_at = Column(DateTime, default=datetime.utcnow)
    upload = relationship('Upload', back_populates='analysis_results')
    video = relationship('StudyTokVideo', back_populates='concept')

class LearningProgress(db.Model):
    __tablename__ = 'learning_progress'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    concept = Column(String(255), nullable=False)
    confidence_level = Column(Float, default=0.0)
    last_reviewed = Column(DateTime, default=datetime.utcnow)
    review_count = Column(Integer, default=0)
    user = relationship('User', back_populates='learning_progress')

class LearningGoal(db.Model):
    __tablename__ = 'learning_goals'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_type = Column(Enum(GoalType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, default=datetime.utcnow)
    target_date = Column(DateTime, nullable=False)
    target_score = Column(Float)  # For exam preparation
    progress = Column(Float, default=0.0)  # 0-100%
    status = Column(String(50), default='active')  # active, completed, abandoned
    goal_metadata = Column(JSON)  # Store additional goal-specific data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('User', back_populates='learning_goals')
    study_sessions = relationship('StudySession', back_populates='learning_goal')
    flashcard_decks = relationship('FlashcardDeck', back_populates='learning_goal')

class StudySession(db.Model):
    __tablename__ = 'study_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_id = Column(Integer, ForeignKey('learning_goals.id'))
    session_type = Column(Enum(StudySessionType), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration = Column(Integer)  # in minutes
    completed = Column(Boolean, default=False)
    performance_score = Column(Float)  # 0-100%
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='study_sessions')
    learning_goal = relationship('LearningGoal', back_populates='study_sessions')

class FlashcardDeck(db.Model):
    __tablename__ = 'flashcard_decks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_id = Column(Integer, ForeignKey('learning_goals.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    language = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_reviewed = Column(DateTime)
    review_count = Column(Integer, default=0)
    
    user = relationship('User', back_populates='flashcard_decks')
    learning_goal = relationship('LearningGoal', back_populates='flashcard_decks')
    flashcards = relationship('Flashcard', back_populates='deck')

class Flashcard(db.Model):
    __tablename__ = 'flashcards'
    
    id = Column(Integer, primary_key=True)
    deck_id = Column(Integer, ForeignKey('flashcard_decks.id'), nullable=False)
    front_content = Column(Text, nullable=False)
    back_content = Column(Text, nullable=False)
    media_urls = Column(JSON)  # Store URLs for images, audio, video
    difficulty_level = Column(Integer, default=1)  # 1-5
    box_number = Column(Integer, default=1)  # For Leitner system
    next_review = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    deck = relationship('FlashcardDeck', back_populates='flashcards')
    review_history = relationship('FlashcardReview', back_populates='flashcard')

class FlashcardReview(db.Model):
    __tablename__ = 'flashcard_reviews'
    
    id = Column(Integer, primary_key=True)
    flashcard_id = Column(Integer, ForeignKey('flashcards.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    review_date = Column(DateTime, default=datetime.utcnow)
    performance = Column(Integer)  # 1-5 rating
    time_taken = Column(Integer)  # in seconds
    
    flashcard = relationship('Flashcard', back_populates='review_history')
    user = relationship('User', back_populates='flashcard_reviews')

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_id = Column(Integer, ForeignKey('learning_goals.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    difficulty_level = Column(Integer, default=1)  # 1-5
    time_limit = Column(Integer)  # in minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='quizzes')
    questions = relationship('QuizQuestion', back_populates='quiz')
    attempts = relationship('QuizAttempt', back_populates='quiz')

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON)  # For multiple choice questions
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text)
    points = Column(Integer, default=1)
    
    quiz = relationship('Quiz', back_populates='questions')

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    score = Column(Float)
    answers = Column(JSON)  # Store user's answers
    
    quiz = relationship('Quiz', back_populates='attempts')
    user = relationship('User', back_populates='quiz_attempts')

class StudyTokVideo(db.Model):
    __tablename__ = 'studytok_videos'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    concept_id = Column(Integer, ForeignKey('analysis_results.id'))
    script = Column(Text)
    video_url = Column(String(255))
    thumbnail_url = Column(String(255))
    duration = Column(Integer)  # in seconds
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='videos')
    concept = relationship('AnalysisResult', back_populates='video')
