from flask import Blueprint, jsonify
from src.services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__)
analytics_service = AnalyticsService()

@analytics_bp.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard():
    """Get comprehensive dashboard data for the current user."""
    try:
        # TODO: Get user_id from auth session
        user_id = 1  # Placeholder
        dashboard_data = analytics_service.get_user_dashboard(user_id)
        return jsonify(dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/api/analytics/goals/<int:goal_id>', methods=['GET'])
def get_goal_analytics(goal_id):
    """Get detailed analytics for a specific learning goal."""
    try:
        goal_data = analytics_service.get_goal_details(goal_id)
        return jsonify(goal_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
