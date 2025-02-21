"""Accessibility service for managing user accessibility preferences"""
from src.extensions import db
from src.models.user import User, AccessibilitySettings

class AccessibilityService:
    def get_settings(self, user_id):
        """Get accessibility settings for a user"""
        user = User.query.get_or_404(user_id)
        settings = user.accessibility_settings or AccessibilitySettings()
        
        return {
            'font_size': settings.font_size,
            'high_contrast': settings.high_contrast,
            'reduced_motion': settings.reduced_motion,
            'dyslexic_font': settings.dyslexic_font,
            'line_spacing': settings.line_spacing,
            'preferred_language': settings.preferred_language,
            'keyboard_navigation': settings.keyboard_navigation,
            'screen_reader': settings.screen_reader,
            'focus_indicators': settings.focus_indicators,
            'skip_links': settings.skip_links
        }

    def update_settings(self, user_id, settings_data):
        """Update accessibility settings for a user"""
        user = User.query.get_or_404(user_id)
        
        if not user.accessibility_settings:
            user.accessibility_settings = AccessibilitySettings()
            
        settings = user.accessibility_settings
        
        # Update each setting if provided
        if 'font_size' in settings_data:
            settings.font_size = settings_data['font_size']
        if 'high_contrast' in settings_data:
            settings.high_contrast = settings_data['high_contrast']
        if 'reduced_motion' in settings_data:
            settings.reduced_motion = settings_data['reduced_motion']
        if 'dyslexic_font' in settings_data:
            settings.dyslexic_font = settings_data['dyslexic_font']
        if 'line_spacing' in settings_data:
            settings.line_spacing = settings_data['line_spacing']
        if 'preferred_language' in settings_data:
            settings.preferred_language = settings_data['preferred_language']
        if 'keyboard_navigation' in settings_data:
            settings.keyboard_navigation = settings_data['keyboard_navigation']
        if 'screen_reader' in settings_data:
            settings.screen_reader = settings_data['screen_reader']
        if 'focus_indicators' in settings_data:
            settings.focus_indicators = settings_data['focus_indicators']
        if 'skip_links' in settings_data:
            settings.skip_links = settings_data['skip_links']
            
        db.session.commit()
        
        return self.get_settings(user_id)

    def apply_settings_to_response(self, response, user_id):
        """Apply accessibility settings to an API response"""
        settings = self.get_settings(user_id)
        
        # Add accessibility metadata to response
        response['accessibility'] = {
            'font_size': settings['font_size'],
            'high_contrast': settings['high_contrast'],
            'reduced_motion': settings['reduced_motion'],
            'dyslexic_font': settings['dyslexic_font'],
            'line_spacing': settings['line_spacing'],
            'preferred_language': settings['preferred_language']
        }
        
        # Add ARIA attributes and keyboard shortcuts if needed
        if settings['keyboard_navigation']:
            response['accessibility']['keyboard_shortcuts'] = self._get_keyboard_shortcuts()
            
        if settings['screen_reader']:
            response['accessibility']['aria_labels'] = self._get_aria_labels()
            
        return response

    def _get_keyboard_shortcuts(self):
        """Get keyboard shortcuts for navigation"""
        return {
            'search': 'Ctrl+K',
            'create_question': 'Ctrl+Q', 
            'my_questions': 'Ctrl+M',
            'settings': 'Ctrl+,',
            'help': 'Ctrl+H'
        }

    def _get_aria_labels(self):
        """Get ARIA labels for screen readers"""
        return {
            'search': 'Search questions and resources',
            'create_question': 'Create a new question',
            'my_questions': 'View my questions',
            'settings': 'Accessibility settings',
            'help': 'Help and documentation'
        }
