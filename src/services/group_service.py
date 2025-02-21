import string
import random
from datetime import datetime
from src.models.group import (
    StudyGroup,
    GroupMembership,
    GroupResource,
    GroupMessage,
    GroupEvent,
    GroupEventParticipant,
    db
)

class GroupService:
    def generate_join_code(self, length=8):
        """Generate a unique join code for private groups"""
        chars = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choices(chars, k=length))
            if not StudyGroup.query.filter_by(join_code=code).first():
                return code

    def create_group(self, user_id, data):
        """Create a new study group"""
        group = StudyGroup(
            name=data['name'],
            description=data.get('description', ''),
            language=data['language'],
            creator_id=user_id,
            max_members=data.get('max_members', 10),
            is_private=data.get('is_private', False)
        )
        
        if group.is_private:
            group.join_code = self.generate_join_code()
            
        db.session.add(group)
        
        # Add creator as admin
        membership = GroupMembership(
            user_id=user_id,
            group=group,
            role='admin'
        )
        db.session.add(membership)
        
        db.session.commit()
        return self._format_group(group)

    def join_group(self, user_id, group_id, join_code=None):
        """Join a study group"""
        group = StudyGroup.query.get_or_404(group_id)
        
        # Check if user is already a member
        if GroupMembership.query.filter_by(
            user_id=user_id, group_id=group_id
        ).first():
            raise ValueError('Already a member of this group')
            
        # Check join code for private groups
        if group.is_private and group.join_code != join_code:
            raise ValueError('Invalid join code')
            
        # Check member limit
        current_members = GroupMembership.query.filter_by(
            group_id=group_id
        ).count()
        if current_members >= group.max_members:
            raise ValueError('Group is full')
            
        membership = GroupMembership(
            user_id=user_id,
            group=group
        )
        db.session.add(membership)
        db.session.commit()
        
        return self._format_group(group)

    def add_resource(self, user_id, group_id, data):
        """Add a resource to the group"""
        membership = GroupMembership.query.filter_by(
            user_id=user_id,
            group_id=group_id
        ).first_or_404()
        
        resource = GroupResource(
            group_id=group_id,
            user_id=user_id,
            title=data['title'],
            resource_type=data['resource_type'],
            content=data.get('content'),
            url=data.get('url')
        )
        
        db.session.add(resource)
        db.session.commit()
        
        return self._format_resource(resource)

    def send_message(self, user_id, group_id, data):
        """Send a message in the group chat"""
        membership = GroupMembership.query.filter_by(
            user_id=user_id,
            group_id=group_id
        ).first_or_404()
        
        message = GroupMessage(
            group_id=group_id,
            user_id=user_id,
            content=data['content'],
            message_type=data.get('message_type', 'text'),
            parent_id=data.get('parent_id')
        )
        
        db.session.add(message)
        db.session.commit()
        
        return self._format_message(message)

    def create_event(self, user_id, group_id, data):
        """Create a group study event"""
        membership = GroupMembership.query.filter_by(
            user_id=user_id,
            group_id=group_id
        ).first_or_404()
        
        event = GroupEvent(
            group_id=group_id,
            creator_id=user_id,
            title=data['title'],
            description=data.get('description', ''),
            event_type=data['event_type'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']),
            video_link=data.get('video_link')
        )
        
        db.session.add(event)
        
        # Add creator as participant
        participant = GroupEventParticipant(
            event=event,
            user_id=user_id,
            status='accepted'
        )
        db.session.add(participant)
        
        db.session.commit()
        return self._format_event(event)

    def get_group_details(self, group_id):
        """Get detailed information about a group"""
        group = StudyGroup.query.get_or_404(group_id)
        return self._format_group(group, include_details=True)

    def search_groups(self, query=None, language=None, page=1, per_page=20):
        """Search for study groups"""
        groups_query = StudyGroup.query
        
        if query:
            groups_query = groups_query.filter(
                StudyGroup.name.ilike(f'%{query}%') |
                StudyGroup.description.ilike(f'%{query}%')
            )
            
        if language:
            groups_query = groups_query.filter_by(language=language)
            
        groups = groups_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'groups': [self._format_group(g) for g in groups.items],
            'total': groups.total,
            'pages': groups.pages,
            'current_page': groups.page
        }

    def _format_group(self, group, include_details=False):
        """Format group data for response"""
        data = {
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'language': group.language,
            'is_private': group.is_private,
            'member_count': len(group.members),
            'created_at': group.created_at.isoformat()
        }
        
        if include_details:
            data.update({
                'members': [self._format_member(m) for m in group.members],
                'resources': [self._format_resource(r) for r in group.resources],
                'events': [self._format_event(e) for e in group.events]
            })
            
        return data

    def _format_member(self, membership):
        """Format member data for response"""
        return {
            'id': membership.user.id,
            'name': membership.user.name,
            'role': membership.role,
            'joined_at': membership.joined_at.isoformat()
        }

    def _format_resource(self, resource):
        """Format resource data for response"""
        return {
            'id': resource.id,
            'title': resource.title,
            'resource_type': resource.resource_type,
            'url': resource.url,
            'created_at': resource.created_at.isoformat(),
            'created_by': {
                'id': resource.user.id,
                'name': resource.user.name
            }
        }

    def _format_message(self, message):
        """Format message data for response"""
        return {
            'id': message.id,
            'content': message.content,
            'message_type': message.message_type,
            'created_at': message.created_at.isoformat(),
            'user': {
                'id': message.user.id,
                'name': message.user.name
            },
            'parent_id': message.parent_id
        }

    def _format_event(self, event):
        """Format event data for response"""
        return {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'event_type': event.event_type,
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat(),
            'video_link': event.video_link,
            'created_at': event.created_at.isoformat(),
            'creator': {
                'id': event.creator.id,
                'name': event.creator.name
            },
            'participants': [
                {
                    'user_id': p.user_id,
                    'name': p.user.name,
                    'status': p.status
                }
                for p in event.participants
            ]
        }
