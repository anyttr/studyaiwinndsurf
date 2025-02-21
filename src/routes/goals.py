from datetime import datetime
from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError

from src.services.goal_service import GoalService
from src.models import GoalType

goals_bp = Blueprint('goals', __name__)
goal_service = GoalService()

class GoalSchema(Schema):
    goal_type = fields.String(required=True, validate=validate.OneOf([gt.name for gt in GoalType]))
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String()
    target_date = fields.DateTime(required=True)
    target_score = fields.Float()
    metadata = fields.Dict()

goal_schema = GoalSchema()

@goals_bp.route('/api/goals', methods=['POST'])
def create_goal():
    """Create a new learning goal."""
    try:
        data = goal_schema.load(request.json)
        # TODO: Get user_id from auth session
        user_id = 1  # Placeholder
        goal = goal_service.create_goal(user_id, data)
        return jsonify({
            'message': 'Goal created successfully',
            'goal': {
                'id': goal.id,
                'title': goal.title,
                'goal_type': goal.goal_type.value,
                'target_date': goal.target_date.isoformat()
            }
        }), 201
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/api/goals', methods=['GET'])
def get_goals():
    """Get all goals for the current user."""
    try:
        # TODO: Get user_id from auth session
        user_id = 1  # Placeholder
        status = request.args.get('status')
        goals = goal_service.get_user_goals(user_id, status)
        return jsonify({
            'goals': [{
                'id': goal.id,
                'title': goal.title,
                'goal_type': goal.goal_type.value,
                'progress': goal.progress,
                'status': goal.status,
                'target_date': goal.target_date.isoformat()
            } for goal in goals]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/api/goals/<int:goal_id>', methods=['GET'])
def get_goal(goal_id):
    """Get a specific goal by ID."""
    try:
        goal = goal_service.get_goal(goal_id)
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
            
        return jsonify({
            'id': goal.id,
            'title': goal.title,
            'goal_type': goal.goal_type.value,
            'description': goal.description,
            'progress': goal.progress,
            'status': goal.status,
            'target_date': goal.target_date.isoformat(),
            'target_score': goal.target_score,
            'metadata': goal.goal_metadata
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/api/goals/<int:goal_id>', methods=['PUT'])
def update_goal(goal_id):
    """Update a specific goal."""
    try:
        updates = request.json
        goal = goal_service.update_goal(goal_id, updates)
        return jsonify({
            'message': 'Goal updated successfully',
            'goal': {
                'id': goal.id,
                'title': goal.title,
                'progress': goal.progress,
                'status': goal.status
            }
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/api/goals/<int:goal_id>/progress', methods=['PUT'])
def update_goal_progress(goal_id):
    """Update the progress of a specific goal."""
    try:
        progress = request.json.get('progress')
        if progress is None:
            return jsonify({'error': 'Progress value is required'}), 400
            
        goal = goal_service.update_goal_progress(goal_id, float(progress))
        return jsonify({
            'message': 'Progress updated successfully',
            'goal': {
                'id': goal.id,
                'title': goal.title,
                'progress': goal.progress,
                'status': goal.status
            }
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/api/goals/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    """Delete a specific goal."""
    try:
        if goal_service.delete_goal(goal_id):
            return jsonify({'message': 'Goal deleted successfully'})
        return jsonify({'error': 'Goal not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/api/goals/suggestions', methods=['GET'])
def get_goal_suggestions():
    """Get personalized goal suggestions."""
    try:
        # TODO: Get user_id from auth session
        user_id = 1  # Placeholder
        suggestions = goal_service.get_goal_suggestions(user_id)
        return jsonify({'suggestions': suggestions})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
