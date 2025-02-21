"""Tests for the resource library service"""
import pytest
from src.models.resource_library import (
    Resource, ResourceCategory, ResourceRating
)
from src.services.resource_library_service import ResourceLibraryService

@pytest.fixture
def resource_service():
    return ResourceLibraryService()

@pytest.fixture
def test_user(db):
    from src.models.user import User
    user = User(
        name='Test User',
        email='test@example.com',
        password_hash='hash123'
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_category(db):
    category = ResourceCategory(
        name='Test Category',
        description='Test category description'
    )
    db.session.add(category)
    db.session.commit()
    return category

@pytest.fixture
def test_resource(db, test_user, test_category):
    resource = Resource(
        title='Test Resource',
        description='Test resource description',
        content='Test resource content',
        resource_type='document',
        language='en',
        difficulty_level='intermediate',
        user=test_user
    )
    resource.categories.append(test_category)
    db.session.add(resource)
    db.session.commit()
    return resource

class TestResourceLibraryService:
    def test_create_resource(self, resource_service, test_user, test_category):
        """Test creating a new resource"""
        data = {
            'title': 'New Resource',
            'description': 'A test resource',
            'content': 'This is the content',
            'resource_type': 'document',
            'language': 'en',
            'difficulty_level': 'beginner',
            'categories': [test_category.id]
        }
        
        result = resource_service.create_resource(test_user.id, data)
        
        assert result['title'] == data['title']
        assert result['description'] == data['description']
        assert result['resource_type'] == data['resource_type']
        assert len(result['categories']) == 1
        assert result['categories'][0]['id'] == test_category.id

    def test_search_resources(self, resource_service, test_resource):
        """Test searching resources"""
        result = resource_service.search_resources(
            query='test',
            categories=None,
            language='en'
        )
        
        assert result['total'] >= 1
        assert any(r['title'] == test_resource.title for r in result['resources'])

    def test_get_resource_details(self, resource_service, test_resource):
        """Test getting resource details"""
        result = resource_service.get_resource_details(test_resource.id)
        
        assert result['id'] == test_resource.id
        assert result['title'] == test_resource.title
        assert result['content'] == test_resource.content
        assert len(result['categories']) > 0

    def test_rate_resource(self, resource_service, test_user, test_resource):
        """Test rating a resource"""
        result = resource_service.rate_resource(
            user_id=test_user.id,
            resource_id=test_resource.id,
            rating=5,
            comment='Great resource!'
        )
        
        assert result['average_rating'] == 5.0
        assert result['rating_count'] == 1

    def test_get_categories(self, resource_service, test_category):
        """Test getting all categories"""
        result = resource_service.get_categories()
        
        assert len(result) >= 1
        assert any(c['name'] == test_category.name for c in result)

    def test_create_category(self, resource_service):
        """Test creating a new category"""
        result = resource_service.create_category(
            name='New Category',
            description='A new test category'
        )
        
        assert result['name'] == 'New Category'
        assert result['description'] == 'A new test category'

    def test_get_trending_resources(self, resource_service, test_resource):
        """Test getting trending resources"""
        result = resource_service.get_trending_resources(limit=10)
        
        assert len(result) >= 1
        assert any(r['id'] == test_resource.id for r in result)

    def test_error_handling(self, resource_service, test_user):
        """Test error handling in resource service"""
        with pytest.raises(ValueError):
            resource_service.rate_resource(
                user_id=test_user.id,
                resource_id=999,  # Non-existent resource
                rating=6  # Invalid rating
            )
