from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy import func, and_
from collections import defaultdict

from src.models import (
    User, LearningGoal, StudySession, LearningProgress,
    FlashcardReview, QuizAttempt, StudySessionType
)
from src import db

class AnalyticsService:
    def __init__(self):
        self.db = db.session

    def get_user_dashboard(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive dashboard data for a user."""
        return {
            'goals': self._get_goals_progress(user_id),
            'study_time': self._get_study_time_stats(user_id),
            'performance': self._get_performance_stats(user_id),
            'activity': self._get_activity_heatmap(user_id),
            'topics': self._get_topic_stats(user_id),
            'strengths_weaknesses': self._get_strengths_weaknesses(user_id)
        }

    def _get_goals_progress(self, user_id: int) -> List[Dict[str, Any]]:
        """Get progress data for all active learning goals."""
        goals = self.db.query(LearningGoal).filter(
            LearningGoal.user_id == user_id,
            LearningGoal.status != 'abandoned'
        ).all()

        return [{
            'id': goal.id,
            'title': goal.title,
            'type': goal.goal_type.value,
            'progress': goal.progress,
            'target_date': goal.target_date.isoformat(),
            'days_remaining': (goal.target_date - datetime.utcnow()).days,
            'status': goal.status
        } for goal in goals]

    def _get_study_time_stats(self, user_id: int) -> Dict[str, Any]:
        """Get study time statistics by session type and topic."""
        # Get all completed sessions in the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        sessions = self.db.query(StudySession).filter(
            StudySession.user_id == user_id,
            StudySession.completed == True,
            StudySession.created_at >= thirty_days_ago
        ).all()

        # Calculate total study time and breakdown by session type
        total_time = sum(session.duration for session in sessions)
        time_by_type = defaultdict(int)
        for session in sessions:
            time_by_type[session.session_type.value] += session.duration

        # Calculate daily study time for the last 30 days
        daily_time = defaultdict(int)
        for session in sessions:
            date_key = session.start_time.date().isoformat()
            daily_time[date_key] += session.duration

        return {
            'total_time': total_time,
            'average_daily_time': total_time / 30 if total_time > 0 else 0,
            'time_by_type': dict(time_by_type),
            'daily_time': dict(daily_time)
        }

    def _get_performance_stats(self, user_id: int) -> Dict[str, Any]:
        """Get performance statistics across different learning activities."""
        # Get flashcard performance
        flashcard_stats = self.db.query(
            func.count(FlashcardReview.id).label('total_reviews'),
            func.avg(FlashcardReview.performance).label('avg_performance')
        ).filter(
            FlashcardReview.user_id == user_id
        ).first()

        # Get quiz performance
        quiz_stats = self.db.query(
            func.count(QuizAttempt.id).label('total_attempts'),
            func.avg(QuizAttempt.score).label('avg_score')
        ).filter(
            QuizAttempt.user_id == user_id
        ).first()

        # Get session performance
        session_stats = self.db.query(
            func.count(StudySession.id).label('total_sessions'),
            func.avg(StudySession.performance_score).label('avg_performance')
        ).filter(
            StudySession.user_id == user_id,
            StudySession.completed == True
        ).first()

        return {
            'flashcards': {
                'total_reviews': flashcard_stats.total_reviews or 0,
                'avg_performance': float(flashcard_stats.avg_performance or 0)
            },
            'quizzes': {
                'total_attempts': quiz_stats.total_attempts or 0,
                'avg_score': float(quiz_stats.avg_score or 0)
            },
            'sessions': {
                'total_sessions': session_stats.total_sessions or 0,
                'avg_performance': float(session_stats.avg_performance or 0)
            }
        }

    def _get_activity_heatmap(self, user_id: int) -> Dict[str, int]:
        """Generate activity heatmap data for the last 365 days."""
        year_ago = datetime.utcnow() - timedelta(days=365)
        
        # Get all study activities
        activities = self.db.query(
            StudySession.start_time,
            StudySession.duration
        ).filter(
            StudySession.user_id == user_id,
            StudySession.start_time >= year_ago
        ).all()

        # Create heatmap data
        heatmap = defaultdict(int)
        for activity in activities:
            date_key = activity.start_time.date().isoformat()
            heatmap[date_key] += activity.duration

        return dict(heatmap)

    def _get_topic_stats(self, user_id: int) -> List[Dict[str, Any]]:
        """Get statistics for each studied topic."""
        progress_items = self.db.query(LearningProgress).filter(
            LearningProgress.user_id == user_id
        ).all()

        return [{
            'topic': item.concept_name,
            'confidence': item.confidence_level * 100,
            'review_count': item.review_count,
            'last_reviewed': item.last_reviewed.isoformat() if item.last_reviewed else None
        } for item in progress_items]

    def _get_strengths_weaknesses(self, user_id: int) -> Dict[str, List[Dict[str, Any]]]:
        """Identify user's strengths and weaknesses based on performance."""
        progress_items = self.db.query(LearningProgress).filter(
            LearningProgress.user_id == user_id
        ).all()

        # Sort topics by confidence level
        sorted_topics = sorted(
            progress_items,
            key=lambda x: x.confidence_level
        )

        # Get top 5 strengths and weaknesses
        strengths = sorted_topics[-5:] if len(sorted_topics) >= 5 else sorted_topics
        weaknesses = sorted_topics[:5] if len(sorted_topics) >= 5 else sorted_topics

        return {
            'strengths': [{
                'topic': item.concept_name,
                'confidence': item.confidence_level * 100,
                'mastered_date': item.last_reviewed.isoformat() if item.confidence_level >= 0.9 else None
            } for item in reversed(strengths)],
            'weaknesses': [{
                'topic': item.concept_name,
                'confidence': item.confidence_level * 100,
                'review_count': item.review_count
            } for item in weaknesses]
        }

    def get_goal_details(self, goal_id: int) -> Dict[str, Any]:
        """Get detailed analytics for a specific learning goal."""
        goal = self.db.query(LearningGoal).get(goal_id)
        if not goal:
            raise ValueError(f"Goal with ID {goal_id} not found")

        # Get all sessions for this goal
        sessions = self.db.query(StudySession).filter(
            StudySession.goal_id == goal_id
        ).all()

        # Calculate session statistics
        total_time = sum(session.duration for session in sessions if session.completed)
        completed_sessions = [s for s in sessions if s.completed]
        avg_performance = (
            sum(s.performance_score for s in completed_sessions) / len(completed_sessions)
            if completed_sessions else 0
        )

        # Get performance trend
        performance_trend = [{
            'date': session.end_time.isoformat(),
            'performance': session.performance_score
        } for session in completed_sessions]

        # Calculate time spent by session type
        time_by_type = defaultdict(int)
        for session in sessions:
            if session.completed:
                time_by_type[session.session_type.value] += session.duration

        return {
            'goal': {
                'id': goal.id,
                'title': goal.title,
                'type': goal.goal_type.value,
                'progress': goal.progress,
                'target_date': goal.target_date.isoformat(),
                'status': goal.status
            },
            'statistics': {
                'total_time': total_time,
                'total_sessions': len(sessions),
                'completed_sessions': len(completed_sessions),
                'avg_performance': avg_performance,
                'time_by_type': dict(time_by_type)
            },
            'performance_trend': performance_trend
        }
