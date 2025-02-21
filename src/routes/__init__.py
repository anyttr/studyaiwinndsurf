"""Initialize routes"""
from src.routes.qa import qa_bp
from src.routes.resource_library import resource_library_bp
from src.routes.accessibility import accessibility_bp
from flask import Blueprint, jsonify

# Create a basic blueprint for testing
test_bp = Blueprint('test', __name__)

@test_bp.route('/health')
def health_check():
    return jsonify({"status": "ok", "message": "Server is running"})

def init_routes(app):
    """Initialize routes for the application"""
    # Register the test blueprint first
    app.register_blueprint(test_bp, url_prefix='/api')
    app.register_blueprint(qa_bp, url_prefix='/api')
    app.register_blueprint(resource_library_bp, url_prefix='/api')
    app.register_blueprint(accessibility_bp, url_prefix='/api')
