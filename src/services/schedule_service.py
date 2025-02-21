from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm.session import Session
import numpy as np
from collections import defaultdict

from src.models import (
    User, LearningGoal, StudySession, StudySessionType,
    LearningProgress, AnalysisResult
)
from src import db

class ScheduleService:
    def __init__(self, db_session: Session = None):
        self.db = db_session or db.session
        self.DIFFICULTY_WEIGHTS = {
            1: 15,  # Easy: 15 minutes
            2: 20,  # Medium-Easy: 20 minutes
            3: 30,  # Medium: 30 minutes
            4: 45,  # Medium-Hard: 45 minutes
            5: 60   # Hard: 60 minutes
        }
        self.SESSION_TYPE_WEIGHTS = {
            StudySessionType.FLASHCARDS: 0.2,
            StudySessionType.QUIZ: 0.3,
            StudySessionType.MICROLEARNING: 0.3,
            StudySessionType.READING: 0.2
        }

    def generate_schedule(self, user_id: int, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Generate a personalized study schedule based on user's goals and learning patterns."""
        user = self.db.query(User).get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Get active goals and their associated topics
        goals = self.db.query(LearningGoal).filter(
            LearningGoal.user_id == user_id,
            LearningGoal.status == 'active'
        ).all()

        if not goals:
            return []

        # Get user's learning progress and patterns
        learning_progress = self.db.query(LearningProgress).filter(
            LearningProgress.user_id == user_id
        ).all()

        # Calculate available study slots
        available_slots = self._calculate_available_slots(start_date, end_date)
        
        # Generate schedule
        schedule = []
        for slot in available_slots:
            session = self._create_study_session(slot, goals, learning_progress)
            if session:
                schedule.append(session)

        return self._optimize_schedule(schedule)

    def _calculate_available_slots(self, start_date: datetime, end_date: datetime) -> List[datetime]:
        """Calculate available study time slots based on date range."""
        slots = []
        current_date = start_date
        
        while current_date <= end_date:
            # Default study hours: 9 AM - 9 PM
            study_start = current_date.replace(hour=9, minute=0)
            study_end = current_date.replace(hour=21, minute=0)
            
            # Create 2-hour slots
            slot_time = study_start
            while slot_time < study_end:
                slots.append(slot_time)
                slot_time += timedelta(hours=2)
            
            current_date += timedelta(days=1)
        
        return slots

    def _create_study_session(
        self, 
        time_slot: datetime,
        goals: List[LearningGoal],
        learning_progress: List[LearningProgress]
    ) -> Optional[Dict[str, Any]]:
        """Create a study session for a specific time slot."""
        # Prioritize goals based on deadline and progress
        prioritized_goals = self._prioritize_goals(goals)
        if not prioritized_goals:
            return None

        # Select goal and topics for this session
        selected_goal = prioritized_goals[0]
        topics = self._get_topics_for_goal(selected_goal)
        
        # Calculate session difficulty and duration
        avg_difficulty = np.mean([topic.difficulty_level for topic in topics]) if topics else 3
        duration = self.DIFFICULTY_WEIGHTS[round(avg_difficulty)]
        
        # Select session type based on learning patterns and spaced repetition
        session_type = self._select_session_type(selected_goal, learning_progress)
        
        return {
            'start_time': time_slot,
            'end_time': time_slot + timedelta(minutes=duration),
            'goal_id': selected_goal.id,
            'goal_title': selected_goal.title,
            'session_type': session_type.value,
            'topics': [{'name': topic.concept_name, 'difficulty': topic.difficulty_level} for topic in topics],
            'duration': duration,
            'difficulty_level': round(avg_difficulty)
        }

    def _prioritize_goals(self, goals: List[LearningGoal]) -> List[LearningGoal]:
        """Prioritize goals based on deadline and progress."""
        def priority_score(goal):
            days_until_deadline = (goal.target_date - datetime.utcnow()).days
            progress_remaining = 100 - goal.progress
            return (progress_remaining / 100) * (1 + 1/max(days_until_deadline, 1))

        return sorted(goals, key=priority_score, reverse=True)

    def _get_topics_for_goal(self, goal: LearningGoal) -> List[LearningProgress]:
        """Get relevant topics for a goal based on metadata and analysis results."""
        if not goal.goal_metadata or 'topics' not in goal.goal_metadata:
            return []

        return self.db.query(LearningProgress).filter(
            LearningProgress.user_id == goal.user_id,
            LearningProgress.concept_name.in_(goal.goal_metadata['topics'])
        ).all()

    def _select_session_type(
        self,
        goal: LearningGoal,
        learning_progress: List[LearningProgress]
    ) -> StudySessionType:
        """Select appropriate session type based on learning patterns and spaced repetition."""
        # Get recent sessions for this goal
        recent_sessions = self.db.query(StudySession).filter(
            StudySession.goal_id == goal.id,
            StudySession.created_at >= datetime.utcnow() - timedelta(days=7)
        ).all()

        # Count session types
        session_counts = defaultdict(int)
        for session in recent_sessions:
            session_counts[session.session_type] += 1

        # Calculate session type scores based on weights and variety
        scores = {}
        total_sessions = sum(session_counts.values()) or 1
        
        for session_type in StudySessionType:
            # Base score from predefined weights
            base_score = self.SESSION_TYPE_WEIGHTS[session_type]
            
            # Adjust based on frequency (prefer less frequent types)
            frequency = session_counts[session_type] / total_sessions
            variety_score = 1 - frequency
            
            # Adjust based on goal type
            if goal.goal_type.name == 'EXAM_PREP' and session_type == StudySessionType.QUIZ:
                base_score *= 1.5
            elif goal.goal_type.name == 'TOPIC_MASTERY' and session_type == StudySessionType.MICROLEARNING:
                base_score *= 1.5
            
            scores[session_type] = base_score * variety_score

        # Return session type with highest score
        return max(scores.items(), key=lambda x: x[1])[0]

    def _optimize_schedule(self, schedule: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize the schedule using spaced repetition and learning patterns."""
        if not schedule:
            return schedule

        # Sort by start time
        schedule.sort(key=lambda x: x['start_time'])
        
        # Ensure variety in consecutive sessions
        for i in range(1, len(schedule)):
            prev_session = schedule[i-1]
            curr_session = schedule[i]
            
            # If consecutive sessions are of the same type, try to swap with next different type
            if curr_session['session_type'] == prev_session['session_type']:
                for j in range(i+1, len(schedule)):
                    if schedule[j]['session_type'] != curr_session['session_type']:
                        schedule[i], schedule[j] = schedule[j], schedule[i]
                        break
        
        # Implement spaced repetition
        topic_last_studied = {}
        for i, session in enumerate(schedule):
            for topic in session['topics']:
                topic_name = topic['name']
                if topic_name in topic_last_studied:
                    # Calculate days since last study
                    days_diff = (session['start_time'] - topic_last_studied[topic_name]).days
                    
                    # If too soon, try to swap with a later session
                    if days_diff < 2:  # Minimum 2 days between same topic
                        for j in range(i+1, len(schedule)):
                            can_swap = True
                            for swap_topic in schedule[j]['topics']:
                                if swap_topic['name'] in topic_last_studied:
                                    swap_days = (session['start_time'] - topic_last_studied[swap_topic['name']]).days
                                    if swap_days < 2:
                                        can_swap = False
                                        break
                            if can_swap:
                                schedule[i], schedule[j] = schedule[j], schedule[i]
                                break
                
                topic_last_studied[topic_name] = session['start_time']
        
        return schedule

    def save_schedule(self, user_id: int, schedule: List[Dict[str, Any]]) -> List[StudySession]:
        """Save generated schedule to database."""
        sessions = []
        for session_data in schedule:
            session = StudySession(
                user_id=user_id,
                goal_id=session_data['goal_id'],
                session_type=session_data['session_type'],
                start_time=session_data['start_time'],
                end_time=session_data['end_time'],
                duration=session_data['duration']
            )
            self.db.add(session)
            sessions.append(session)
        
        self.db.commit()
        return sessions

    def get_user_schedule(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get user's saved study schedule."""
        query = self.db.query(StudySession).filter(StudySession.user_id == user_id)
        
        if start_date:
            query = query.filter(StudySession.start_time >= start_date)
        if end_date:
            query = query.filter(StudySession.end_time <= end_date)
            
        sessions = query.order_by(StudySession.start_time).all()
        
        return [{
            'id': session.id,
            'start_time': session.start_time,
            'end_time': session.end_time,
            'goal_id': session.goal_id,
            'goal_title': session.learning_goal.title if session.learning_goal else None,
            'session_type': session.session_type.value,
            'duration': session.duration,
            'completed': session.completed,
            'performance_score': session.performance_score
        } for session in sessions]
