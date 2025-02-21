"""Test configuration and fixtures"""
import os
import pytest
from src import create_app, db
from src.models.user import User, AccessibilitySettings
from src.models.qa import Question, Answer, Tag, QuestionVote, AnswerVote
from src.models.resource_library import Resource, ResourceCategory, ResourceRating

@pytest.fixture(scope='session')
def app():
    """Create test app"""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test'
    })
    return app

@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    """Create database and tables"""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_user(db_session):
    """Create test user"""
    user = User(
        name='Test User',
        email='test@example.com',
        password_hash='password_hash'
    )
    db_session.session.add(user)
    db_session.session.commit()
    return user

@pytest.fixture
def test_accessibility_settings(db_session, test_user):
    """Create test accessibility settings"""
    settings = AccessibilitySettings(
        user_id=test_user.id,
        font_size=18,
        high_contrast=True,
        reduced_motion=True,
        dyslexic_font=False
    )
    db_session.session.add(settings)
    db_session.session.commit()
    return settings

@pytest.fixture
def test_question(db_session, test_user):
    """Create test question"""
    question = Question(
        title='Test Question',
        content='Test content',
        language='en',
        user_id=test_user.id
    )
    db_session.session.add(question)
    db_session.session.commit()
    return question

@pytest.fixture
def test_answer(db_session, test_user, test_question):
    """Create test answer"""
    answer = Answer(
        content='Test answer',
        user_id=test_user.id,
        question_id=test_question.id
    )
    db_session.session.add(answer)
    db_session.session.commit()
    return answer

@pytest.fixture
def test_resource(db_session, test_user):
    """Create test resource"""
    resource = Resource(
        title='Test Resource',
        description='Test description',
        content='Test content',
        language='en',
        user_id=test_user.id
    )
    db_session.session.add(resource)
    db_session.session.commit()
    return resource

@pytest.fixture
def test_category(db_session):
    """Create test resource category"""
    category = ResourceCategory(
        name='Test Category',
        description='Test description'
    )
    db_session.session.add(category)
    db_session.session.commit()
    return category

@pytest.fixture
def test_rating(db_session, test_user, test_resource):
    """Create test resource rating"""
    rating = ResourceRating(
        user_id=test_user.id,
        resource_id=test_resource.id,
        value=5,
        comment='Test comment'
    )
    db_session.session.add(rating)
    db_session.session.commit()
    return rating
