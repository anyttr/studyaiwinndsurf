"""Resource Library routes"""
from flask import Blueprint, jsonify, request
from src.models.resource_library import Resource, ResourceCategory
from src.services.resource_library_service import ResourceLibraryService
from src.extensions import db

resource_library_bp = Blueprint('resource_library', __name__)
resource_library_service = ResourceLibraryService()

@resource_library_bp.route('/resources', methods=['POST'])
def create_resource():
    """Create a new resource"""
    data = request.get_json()
    
    try:
        resource = resource_library_service.create_resource(
            title=data['title'],
            description=data['description'],
            content=data['content'],
            resource_type=data['resource_type'],
            language=data['language'],
            difficulty_level=data['difficulty_level'],
            categories=data.get('categories', []),
            user_id=request.user.id
        )
        return jsonify(resource.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@resource_library_bp.route('/resources', methods=['GET'])
def search_resources():
    """Search resources"""
    query = request.args.get('query', '')
    language = request.args.get('language', 'en')
    resource_type = request.args.get('type')
    difficulty_level = request.args.get('difficulty')
    category_ids = request.args.getlist('categories')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    resources = resource_library_service.search_resources(
        query=query,
        language=language,
        resource_type=resource_type,
        difficulty_level=difficulty_level,
        category_ids=category_ids,
        page=page,
        per_page=per_page
    )
    
    return jsonify({
        'resources': [r.to_dict() for r in resources.items],
        'total': resources.total,
        'pages': resources.pages,
        'current_page': resources.page
    }), 200

@resource_library_bp.route('/resources/<int:resource_id>/rate', methods=['POST'])
def rate_resource(resource_id):
    """Rate a resource"""
    data = request.get_json()
    
    try:
        rating = resource_library_service.rate_resource(
            resource_id=resource_id,
            user_id=request.user.id,
            rating=data['rating'],
            comment=data.get('comment')
        )
        return jsonify(rating.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@resource_library_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all resource categories"""
    categories = resource_library_service.get_categories()
    return jsonify([c.to_dict() for c in categories]), 200
