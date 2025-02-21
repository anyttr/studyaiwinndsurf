from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm.session import Session

from src.models import LearningGoal, GoalType, User
from src import db

class GoalService:
    def __init__(self, db_session: Session = None):
        self.db = db_session or db.session

    def create_goal(self, user_id: int, goal_data: Dict[str, Any]) -> LearningGoal:
        """Create a new learning goal for a user."""
        goal = LearningGoal(
            user_id=user_id,
            goal_type=GoalType[goal_data['goal_type']],
            title=goal_data['title'],
            description=goal_data.get('description'),
            start_date=datetime.utcnow(),
            target_date=goal_data['target_date'],
            target_score=goal_data.get('target_score'),
            goal_metadata=goal_data.get('metadata', {})
        )
        self.db.add(goal)
        self.db.commit()
        return goal

    def get_user_goals(self, user_id: int, status: Optional[str] = None) -> List[LearningGoal]:
        """Get all learning goals for a user, optionally filtered by status."""
        query = self.db.query(LearningGoal).filter(LearningGoal.user_id == user_id)
        if status:
            query = query.filter(LearningGoal.status == status)
        return query.order_by(LearningGoal.created_at.desc()).all()

    def get_goal(self, goal_id: int) -> Optional[LearningGoal]:
        """Get a specific learning goal by ID."""
        return self.db.query(LearningGoal).get(goal_id)

    def update_goal_progress(self, goal_id: int, progress: float) -> LearningGoal:
        """Update the progress of a learning goal."""
        goal = self.get_goal(goal_id)
        if not goal:
            raise ValueError(f"Goal with ID {goal_id} not found")
        
        goal.progress = min(max(progress, 0.0), 100.0)  # Ensure progress is between 0-100%
        
        # Update status if goal is completed
        if goal.progress >= 100.0:
            goal.status = 'completed'
        
        self.db.commit()
        return goal

    def update_goal(self, goal_id: int, updates: Dict[str, Any]) -> LearningGoal:
        """Update a learning goal's details."""
        goal = self.get_goal(goal_id)
        if not goal:
            raise ValueError(f"Goal with ID {goal_id} not found")

        # Update allowed fields
        allowed_fields = ['title', 'description', 'target_date', 'target_score', 'status', 'goal_metadata']
        for field in allowed_fields:
            if field in updates:
                setattr(goal, field, updates[field])

        self.db.commit()
        return goal

    def delete_goal(self, goal_id: int) -> bool:
        """Delete a learning goal."""
        goal = self.get_goal(goal_id)
        if not goal:
            return False
        
        self.db.delete(goal)
        self.db.commit()
        return True

    def get_goal_suggestions(self, user_id: int) -> List[Dict[str, Any]]:
        """Generate goal suggestions based on user's learning history."""
        user = self.db.query(User).get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Get user's learning progress and analysis results
        learning_progress = user.learning_progress
        
        suggestions = []
        
        # Suggest exam preparation goals based on difficult concepts
        difficult_topics = [lp for lp in learning_progress if lp.confidence_level < 0.7]
        if difficult_topics:
            suggestions.append({
                'goal_type': GoalType.EXAM_PREP.value,
                'title': 'Master Challenging Topics',
                'description': f'Focus on improving understanding of {len(difficult_topics)} challenging concepts',
                'target_date': datetime.utcnow() + timedelta(weeks=2),
                'metadata': {
                    'topics': [topic.concept_name for topic in difficult_topics],
                    'current_confidence': sum(t.confidence_level for t in difficult_topics) / len(difficult_topics)
                }
            })

        # Suggest topic mastery goals for related concepts
        topic_clusters = self._cluster_related_topics(learning_progress)
        for cluster in topic_clusters[:3]:  # Suggest up to 3 topic clusters
            suggestions.append({
                'goal_type': GoalType.TOPIC_MASTERY.value,
                'title': f'Master {cluster["main_topic"]}',
                'description': f'Deep dive into {cluster["main_topic"]} and related concepts',
                'target_date': datetime.utcnow() + timedelta(weeks=4),
                'metadata': {
                    'topics': cluster['related_topics'],
                    'prerequisites': cluster['prerequisites']
                }
            })

        return suggestions

    def _cluster_related_topics(self, learning_progress: List[Any]) -> List[Dict[str, Any]]:
        """Helper method to cluster related topics based on learning progress."""
        # This is a placeholder implementation
        # TODO: Implement actual topic clustering using NLP and graph analysis
        clusters = []
        seen_topics = set()
        
        for progress in learning_progress:
            if progress.concept_name in seen_topics:
                continue
                
            cluster = {
                'main_topic': progress.concept_name,
                'related_topics': [progress.concept_name],  # In real impl, find related topics
                'prerequisites': []  # In real impl, identify prerequisites
            }
            clusters.append(cluster)
            seen_topics.add(progress.concept_name)
            
        return clusters
