from flask import Blueprint, request, jsonify
from src.services.group_service import GroupService
from src.routes.auth import auth_required

groups_bp = Blueprint('groups', __name__)
group_service = GroupService()

@groups_bp.route('/api/groups', methods=['POST'])
@auth_required
def create_group(current_user):
    """Create a new study group"""
    try:
        data = request.get_json()
        group = group_service.create_group(current_user.id, data)
        return jsonify(group), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create group'}), 500

@groups_bp.route('/api/groups/search', methods=['GET'])
@auth_required
def search_groups(current_user):
    """Search for study groups"""
    try:
        query = request.args.get('q')
        language = request.args.get('language')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        results = group_service.search_groups(
            query=query,
            language=language,
            page=page,
            per_page=per_page
        )
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': 'Search failed'}), 500

@groups_bp.route('/api/groups/<int:group_id>/join', methods=['POST'])
@auth_required
def join_group(current_user, group_id):
    """Join a study group"""
    try:
        data = request.get_json()
        join_code = data.get('join_code')
        group = group_service.join_group(current_user.id, group_id, join_code)
        return jsonify(group)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to join group'}), 500

@groups_bp.route('/api/groups/<int:group_id>/resources', methods=['POST'])
@auth_required
def add_resource(current_user, group_id):
    """Add a resource to the group"""
    try:
        data = request.get_json()
        resource = group_service.add_resource(current_user.id, group_id, data)
        return jsonify(resource), 201
    except Exception as e:
        return jsonify({'error': 'Failed to add resource'}), 500

@groups_bp.route('/api/groups/<int:group_id>/messages', methods=['POST'])
@auth_required
def send_message(current_user, group_id):
    """Send a message in the group chat"""
    try:
        data = request.get_json()
        message = group_service.send_message(current_user.id, group_id, data)
        return jsonify(message), 201
    except Exception as e:
        return jsonify({'error': 'Failed to send message'}), 500

@groups_bp.route('/api/groups/<int:group_id>/events', methods=['POST'])
@auth_required
def create_event(current_user, group_id):
    """Create a group study event"""
    try:
        data = request.get_json()
        event = group_service.create_event(current_user.id, group_id, data)
        return jsonify(event), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create event'}), 500

@groups_bp.route('/api/groups/<int:group_id>', methods=['GET'])
@auth_required
def get_group(current_user, group_id):
    """Get group details"""
    try:
        group = group_service.get_group_details(group_id)
        return jsonify(group)
    except Exception as e:
        return jsonify({'error': 'Failed to get group details'}), 500

@groups_bp.route('/api/groups/<int:group_id>/events/<int:event_id>/join', methods=['POST'])
@auth_required
def join_event(current_user, group_id, event_id):
    """Join a group event"""
    try:
        data = request.get_json()
        event = group_service.join_event(current_user.id, group_id, event_id)
        return jsonify(event)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to join event'}), 500
