"""API Tests"""
import pytest
from flask import url_for
from src.models.user import User, AccessibilitySettings
from src.models.qa import Question, Answer, Tag, QuestionVote, AnswerVote
from src.models.resource_library import Resource, ResourceCategory, ResourceRating

@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        name='Test User',
        email='test@example.com',
        password_hash='hash123'
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_question(db_session, test_user):
    """Create a test question"""
    question = Question(
        title='Test Question',
        content='Test content',
        language='en',
        user=test_user
    )
    db_session.add(question)
    db_session.commit()
    return question

@pytest.fixture
def test_resource(db_session, test_user):
    """Create a test resource"""
    resource = Resource(
        title='Test Resource',
        description='Test description',
        content='Test content',
        language='en',
        user=test_user
    )
    db_session.add(resource)
    db_session.commit()
    return resource

@pytest.fixture
def test_accessibility_settings(db_session, test_user):
    """Create test accessibility settings"""
    settings = AccessibilitySettings(
        user=test_user,
        font_size=18,
        high_contrast=True,
        reduced_motion=True,
        dyslexic_font=False
    )
    db_session.add(settings)
    db_session.commit()
    return settings

class TestQAAPI:
    """Test QA API endpoints"""
    
    def test_create_question(self, client, test_user):
        """Test creating a question"""
        data = {
            'title': 'Test Question',
            'content': 'Test content',
            'language': 'en',
            'user_id': test_user.id
        }
        response = client.post('/api/qa/questions', json=data)
        assert response.status_code == 201
        assert response.json['title'] == data['title']
        assert response.json['content'] == data['content']
        assert response.json['language'] == data['language']
        assert response.json['user_id'] == test_user.id
    
    def test_search_questions(self, client, test_question):
        """Test searching questions"""
        response = client.get('/api/qa/questions?query=Test')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['title'] == test_question.title
    
    def test_create_answer(self, client, test_user, test_question):
        """Test creating an answer"""
        data = {
            'content': 'Test answer',
            'user_id': test_user.id,
            'question_id': test_question.id
        }
        response = client.post('/api/qa/answers', json=data)
        assert response.status_code == 201
        assert response.json['content'] == data['content']
        assert response.json['user_id'] == test_user.id
        assert response.json['question_id'] == test_question.id

class TestResourceLibraryAPI:
    """Test Resource Library API endpoints"""
    
    def test_create_resource(self, client, test_user):
        """Test creating a resource"""
        data = {
            'title': 'Test Resource',
            'description': 'Test description',
            'content': 'Test content',
            'language': 'en',
            'user_id': test_user.id
        }
        response = client.post('/api/resources', json=data)
        assert response.status_code == 201
        assert response.json['title'] == data['title']
        assert response.json['description'] == data['description']
        assert response.json['content'] == data['content']
        assert response.json['language'] == data['language']
        assert response.json['user_id'] == test_user.id
    
    def test_search_resources(self, client, test_resource):
        """Test searching resources"""
        response = client.get('/api/resources?query=Test')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['title'] == test_resource.title
    
    def test_rate_resource(self, client, test_user, test_resource):
        """Test rating a resource"""
        data = {
            'user_id': test_user.id,
            'resource_id': test_resource.id,
            'value': 5,
            'comment': 'Test comment'
        }
        response = client.post(f'/api/resources/{test_resource.id}/rate', json=data)
        assert response.status_code == 201
        assert response.json['value'] == data['value']
        assert response.json['comment'] == data['comment']
        assert response.json['user_id'] == test_user.id
        assert response.json['resource_id'] == test_resource.id

class TestAccessibilityAPI:
    """Test Accessibility API endpoints"""
    
    def test_get_accessibility_settings(self, client, test_user, test_accessibility_settings):
        """Test getting accessibility settings"""
        response = client.get(f'/api/users/{test_user.id}/accessibility')
        assert response.status_code == 200
        assert response.json['font_size'] == test_accessibility_settings.font_size
        assert response.json['high_contrast'] == test_accessibility_settings.high_contrast
        assert response.json['reduced_motion'] == test_accessibility_settings.reduced_motion
        assert response.json['dyslexic_font'] == test_accessibility_settings.dyslexic_font
    
    def test_update_accessibility_settings(self, client, test_user, test_accessibility_settings):
        """Test updating accessibility settings"""
        data = {
            'font_size': 20,
            'high_contrast': False,
            'reduced_motion': True,
            'dyslexic_font': True
        }
        response = client.put(f'/api/users/{test_user.id}/accessibility', json=data)
        assert response.status_code == 200
        assert response.json['font_size'] == data['font_size']
        assert response.json['high_contrast'] == data['high_contrast']
        assert response.json['reduced_motion'] == data['reduced_motion']
        assert response.json['dyslexic_font'] == data['dyslexic_font']
