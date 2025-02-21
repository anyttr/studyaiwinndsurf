"""Initialize routes"""
from src.routes.qa import qa_bp
from src.routes.resource_library import resource_library_bp
from src.routes.accessibility import accessibility_bp

def init_routes(app):
    """Initialize routes for the application"""
    app.register_blueprint(qa_bp, url_prefix='/api')
    app.register_blueprint(resource_library_bp, url_prefix='/api')
    app.register_blueprint(accessibility_bp, url_prefix='/api')
