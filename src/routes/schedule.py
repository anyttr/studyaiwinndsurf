from datetime import datetime
from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError

from src.services.schedule_service import ScheduleService

schedule_bp = Blueprint('schedule', __name__)
schedule_service = ScheduleService()

class ScheduleRequestSchema(Schema):
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)

schedule_request_schema = ScheduleRequestSchema()

@schedule_bp.route('/api/schedule/generate', methods=['POST'])
def generate_schedule():
    """Generate a new study schedule."""
    try:
        data = schedule_request_schema.load(request.json)
        # TODO: Get user_id from auth session
        user_id = 1  # Placeholder
        
        schedule = schedule_service.generate_schedule(
            user_id,
            data['start_date'],
            data['end_date']
        )
        
        if not schedule:
            return jsonify({
                'message': 'No schedule could be generated. Please create some learning goals first.',
                'schedule': []
            }), 200
            
        # Save the generated schedule
        saved_sessions = schedule_service.save_schedule(user_id, schedule)
        
        return jsonify({
            'message': 'Schedule generated successfully',
            'schedule': schedule
        })
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@schedule_bp.route('/api/schedule', methods=['GET'])
def get_schedule():
    """Get user's study schedule."""
    try:
        # TODO: Get user_id from auth session
        user_id = 1  # Placeholder
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            
        schedule = schedule_service.get_user_schedule(user_id, start_date, end_date)
        
        return jsonify({'schedule': schedule})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@schedule_bp.route('/api/schedule/sessions/<int:session_id>/complete', methods=['POST'])
def complete_session(session_id):
    """Mark a study session as completed."""
    try:
        data = request.json
        performance_score = data.get('performance_score')
        
        # TODO: Get user_id from auth session
        user_id = 1  # Placeholder
        
        session = schedule_service.complete_session(
            user_id,
            session_id,
            performance_score
        )
        
        return jsonify({
            'message': 'Session marked as completed',
            'session': {
                'id': session.id,
                'completed': session.completed,
                'performance_score': session.performance_score
            }
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
