"""Resource Library service for managing learning resources"""
from datetime import datetime
from sqlalchemy import func, desc
from src.extensions import db
from src.models.resource_library import Resource, ResourceCategory, ResourceRating

class ResourceLibraryService:
    def create_resource(self, user_id, data):
        """Create a new learning resource"""
        resource = Resource(
            title=data['title'],
            description=data['description'],
            content=data['content'],
            resource_type=data['resource_type'],
            language=data['language'],
            difficulty_level=data['difficulty_level'],
            user_id=user_id
        )
        
        # Add to categories
        for category_id in data.get('categories', []):
            category = ResourceCategory.query.get_or_404(category_id)
            resource.categories.append(category)
            
        db.session.add(resource)
        db.session.commit()
        
        return self._format_resource(resource)

    def search_resources(self, query=None, categories=None, language=None, difficulty=None, page=1, per_page=20):
        """Search resources with filters"""
        resources = Resource.query
        
        if query:
            resources = resources.filter(
                Resource.title.ilike(f'%{query}%') |
                Resource.description.ilike(f'%{query}%') |
                Resource.content.ilike(f'%{query}%')
            )
            
        if categories:
            for category_id in categories:
                resources = resources.join(Resource.categories).filter(
                    ResourceCategory.id == category_id
                )
                
        if language:
            resources = resources.filter(Resource.language == language)
            
        if difficulty:
            resources = resources.filter(Resource.difficulty_level == difficulty)
            
        # Order by rating and recency
        resources = resources.order_by(
            desc(Resource.average_rating),
            desc(Resource.created_at)
        )
        
        # Paginate results
        paginated = resources.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'resources': [self._format_resource(r) for r in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': paginated.page
        }

    def get_resource_details(self, resource_id):
        """Get detailed resource info"""
        resource = Resource.query.get_or_404(resource_id)
        return self._format_resource(resource, include_content=True)

    def rate_resource(self, user_id, resource_id, rating, comment=None):
        """Rate a resource"""
        if rating < 1 or rating > 5:
            raise ValueError('Rating must be between 1 and 5')
            
        resource = Resource.query.get_or_404(resource_id)
        
        # Check if user has already rated
        existing_rating = ResourceRating.query.filter_by(
            user_id=user_id,
            resource_id=resource_id
        ).first()
        
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.comment = comment
            existing_rating.updated_at = datetime.utcnow()
        else:
            rating = ResourceRating(
                rating=rating,
                comment=comment,
                user_id=user_id,
                resource=resource
            )
            db.session.add(rating)
            
        # Update resource average rating
        resource.average_rating = db.session.query(
            func.avg(ResourceRating.rating)
        ).filter(
            ResourceRating.resource_id == resource_id
        ).scalar() or 0.0
        
        db.session.commit()
        
        return self._format_resource(resource)

    def get_categories(self):
        """Get all resource categories"""
        categories = ResourceCategory.query.all()
        return [self._format_category(c) for c in categories]

    def create_category(self, name, description=None):
        """Create a new resource category"""
        category = ResourceCategory(
            name=name,
            description=description
        )
        
        db.session.add(category)
        db.session.commit()
        
        return self._format_category(category)

    def get_trending_resources(self, limit=10):
        """Get trending resources based on recent ratings"""
        resources = Resource.query.order_by(
            desc(Resource.average_rating),
            desc(Resource.created_at)
        ).limit(limit).all()
        
        return [self._format_resource(r) for r in resources]

    def _format_resource(self, resource, include_content=False):
        """Format resource data"""
        data = {
            'id': resource.id,
            'title': resource.title,
            'description': resource.description,
            'resource_type': resource.resource_type,
            'language': resource.language,
            'difficulty_level': resource.difficulty_level,
            'average_rating': float(resource.average_rating or 0.0),
            'rating_count': len(resource.ratings),
            'created_at': resource.created_at.isoformat(),
            'updated_at': resource.updated_at.isoformat(),
            'categories': [self._format_category(c) for c in resource.categories],
            'user': {
                'id': resource.user.id,
                'name': resource.user.name
            }
        }
        
        if include_content:
            data['content'] = resource.content
            data['ratings'] = [self._format_rating(r) for r in resource.ratings]
            
        return data

    def _format_category(self, category):
        """Format category data"""
        return {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'resource_count': len(category.resources)
        }

    def _format_rating(self, rating):
        """Format rating data"""
        return {
            'id': rating.id,
            'rating': rating.rating,
            'comment': rating.comment,
            'created_at': rating.created_at.isoformat(),
            'updated_at': rating.updated_at.isoformat(),
            'user': {
                'id': rating.user.id,
                'name': rating.user.name
            }
        }
