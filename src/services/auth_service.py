from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User, db

class AuthService:
    def __init__(self, secret_key='your-secret-key'):  # In production, use environment variable
        self.secret_key = secret_key

    def register_user(self, email, password, name):
        """Register a new user"""
        if User.query.filter_by(email=email).first():
            raise ValueError('Email already registered')
        
        user = User(
            email=email,
            password_hash=generate_password_hash(password),
            name=name,
            created_at=datetime.utcnow()
        )
        
        db.session.add(user)
        db.session.commit()
        
        return self._create_user_response(user)

    def login_user(self, email, password):
        """Authenticate a user and return token"""
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError('Invalid email or password')
        
        return self._create_user_response(user)

    def validate_token(self, token):
        """Validate JWT token and return user"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            user = User.query.get(payload['sub'])
            
            if not user:
                raise ValueError('User not found')
                
            return user
            
        except jwt.ExpiredSignatureError:
            raise ValueError('Token has expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token')

    def _create_user_response(self, user):
        """Create standardized user response with token"""
        token = self._generate_token(user)
        
        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'created_at': user.created_at.isoformat()
            },
            'token': token
        }

    def _generate_token(self, user):
        """Generate JWT token for user"""
        payload = {
            'sub': user.id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
