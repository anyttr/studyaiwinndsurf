"""Resource Library models"""
from datetime import datetime
from src.extensions import db
from src.models.user import User

class Resource(db.Model):
    """Resource model"""
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en')  # ISO language code
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ratings = db.relationship('ResourceRating', backref='resource', lazy=True)
    categories = db.relationship('ResourceCategory', secondary='resource_category_association', backref=db.backref('resources', lazy=True))
    user = db.relationship('User', backref=db.backref('resources', lazy=True))
    
    def to_dict(self):
        """Convert resource to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'language': self.language,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'categories': [category.name for category in self.categories],
            'average_rating': sum(rating.value for rating in self.ratings) / len(self.ratings) if self.ratings else 0,
            'rating_count': len(self.ratings)
        }

class ResourceRating(db.Model):
    """Resource rating model"""
    __tablename__ = 'resource_ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)  # 1-5 rating
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'resource_id', name='unique_resource_rating'),
    )
    
    def to_dict(self):
        """Convert rating to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'resource_id': self.resource_id,
            'value': self.value,
            'comment': self.comment,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ResourceCategory(db.Model):
    """Resource category model"""
    __tablename__ = 'resource_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert category to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

# Association table for resource categories
resource_category_association = db.Table('resource_category_association',
    db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('resource_categories.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)
