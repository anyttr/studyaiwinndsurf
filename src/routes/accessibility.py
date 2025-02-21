"""Accessibility routes"""
from flask import Blueprint, jsonify, request
from src.models.user import AccessibilitySettings
from src.services.accessibility_service import AccessibilityService
from src.extensions import db

accessibility_bp = Blueprint('accessibility', __name__)
accessibility_service = AccessibilityService()

@accessibility_bp.route('/accessibility/settings', methods=['GET'])
def get_accessibility_settings():
    """Get user's accessibility settings"""
    try:
        settings = accessibility_service.get_settings(request.user.id)
        return jsonify(settings.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@accessibility_bp.route('/accessibility/settings', methods=['PUT'])
def update_accessibility_settings():
    """Update user's accessibility settings"""
    data = request.get_json()
    
    try:
        settings = accessibility_service.update_settings(
            user_id=request.user.id,
            font_size=data.get('font_size'),
            high_contrast=data.get('high_contrast'),
            reduced_motion=data.get('reduced_motion'),
            dyslexic_font=data.get('dyslexic_font')
        )
        return jsonify(settings.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
