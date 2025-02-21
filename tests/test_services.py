import pytest
import os
from src.services.concept_extractor import ConceptExtractor
from src.services.visualizer import Visualizer
from src.services.difficulty_assessor import DifficultyAssessor
from src.services.summarizer import Summarizer
from src.services.goal_service import GoalService
from src.services.schedule_service import ScheduleService
from src.services.analytics_service import AnalyticsService
from datetime import datetime, timedelta

# Sample text for testing
SAMPLE_TEXT_EN = """
Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience
without being explicitly programmed. Deep learning, a more specialized form of machine learning, uses neural 
networks with multiple layers to analyze various factors of data.

Key concepts in machine learning include:
1. Supervised Learning: Training with labeled data
2. Unsupervised Learning: Finding patterns in unlabeled data
3. Reinforcement Learning: Learning through trial and error
"""

SAMPLE_TEXT_RO = """
Învățarea automată este o subramură a inteligenței artificiale care permite sistemelor să învețe și să se
îmbunătățească din experiență fără a fi programate explicit. Învățarea profundă, o formă mai specializată
de învățare automată, utilizează rețele neurale cu mai multe straturi pentru a analiza diverși factori ai datelor.

Concepte cheie în învățarea automată includ:
1. Învățarea supervizată: Antrenament cu date etichetate
2. Învățarea nesupervizată: Găsirea tiparelor în date neetichetate
3. Învățarea prin întărire: Învățarea prin încercare și eroare
"""

@pytest.fixture
def concept_extractor():
    return ConceptExtractor()

@pytest.fixture
def visualizer():
    return Visualizer()

@pytest.fixture
def difficulty_assessor():
    return DifficultyAssessor()

@pytest.fixture
def summarizer():
    return Summarizer()

@pytest.fixture
def goal_service():
    return GoalService()

@pytest.fixture
def schedule_service():
    return ScheduleService()

@pytest.fixture
def analytics_service():
    return AnalyticsService()

def test_concept_extraction_english(concept_extractor):
    """Test concept extraction for English text"""
    concepts = concept_extractor.extract_concepts(SAMPLE_TEXT_EN, 'en')
    
    # Check if basic concept categories are present
    assert 'terms' in concepts
    assert 'entities' in concepts
    assert 'definitions' in concepts
    assert 'relationships' in concepts
    
    # Check if key terms were extracted
    terms = [term['term'].lower() for term in concepts['terms']]
    assert 'machine learning' in terms
    assert 'deep learning' in terms
    assert 'neural networks' in terms

def test_concept_extraction_romanian(concept_extractor):
    """Test concept extraction for Romanian text"""
    concepts = concept_extractor.extract_concepts(SAMPLE_TEXT_RO, 'ro')
    
    # Check if basic concept categories are present
    assert 'terms' in concepts
    assert 'entities' in concepts
    assert 'definitions' in concepts
    assert 'relationships' in concepts
    
    # Check if key terms were extracted
    terms = [term['term'].lower() for term in concepts['terms']]
    assert 'învățarea automată' in terms
    assert 'învățarea profundă' in terms
    assert 'rețele neurale' in terms

def test_visualization_generation(concept_extractor, visualizer):
    """Test visualization generation"""
    # Extract concepts
    concepts = concept_extractor.extract_concepts(SAMPLE_TEXT_EN, 'en')
    
    # Generate mind map
    mind_map = visualizer.create_mind_map(concepts, "Test Topic")
    assert mind_map is not None
    
    # Generate knowledge graph
    graph = concept_extractor.generate_knowledge_graph(concepts)
    knowledge_graph = visualizer.create_knowledge_graph(graph)
    assert knowledge_graph is not None

def test_difficulty_assessment(difficulty_assessor):
    """Test difficulty assessment"""
    # Test English text
    en_assessment = difficulty_assessor.assess_difficulty(SAMPLE_TEXT_EN, 'en')
    assert 'difficulty_level' in en_assessment
    assert 'metrics' in en_assessment
    assert 'recommendations' in en_assessment
    
    # Test Romanian text
    ro_assessment = difficulty_assessor.assess_difficulty(SAMPLE_TEXT_RO, 'ro')
    assert 'difficulty_level' in ro_assessment
    assert 'metrics' in ro_assessment
    assert 'recommendations' in ro_assessment

def test_summarization(summarizer):
    """Test text summarization"""
    # Test English summarization
    en_summary = summarizer.generate_summary(SAMPLE_TEXT_EN, 'en', summary_type='paragraph')
    assert en_summary['type'] == 'paragraph'
    assert len(en_summary['summary']) > 0
    
    en_bullets = summarizer.generate_summary(SAMPLE_TEXT_EN, 'en', summary_type='bullet_points')
    assert en_bullets['type'] == 'bullet_points'
    assert len(en_bullets['points']) > 0
    
    # Test Romanian summarization
    ro_summary = summarizer.generate_summary(SAMPLE_TEXT_RO, 'ro', summary_type='paragraph')
    assert ro_summary['type'] == 'paragraph'
    assert len(ro_summary['summary']) > 0
    
    ro_bullets = summarizer.generate_summary(SAMPLE_TEXT_RO, 'ro', summary_type='bullet_points')
    assert ro_bullets['type'] == 'bullet_points'
    assert len(ro_bullets['points']) > 0

# Phase 2 Service Tests

def test_goal_creation(goal_service):
    """Test goal creation and suggestion"""
    # Test creating a new learning goal
    goal_data = {
        'title': 'Master Python Basics',
        'description': 'Learn fundamental Python concepts',
        'deadline': (datetime.now() + timedelta(days=30)).isoformat(),
        'goal_type': 'topic_mastery',
        'target_score': 90
    }
    
    goal = goal_service.create_goal(1, goal_data)
    assert goal['title'] == goal_data['title']
    assert goal['goal_type'] == goal_data['goal_type']
    
    # Test goal suggestions
    suggestions = goal_service.get_goal_suggestions(1)
    assert len(suggestions) > 0
    assert all('title' in s and 'description' in s for s in suggestions)

def test_schedule_generation(schedule_service):
    """Test study schedule generation"""
    # Test creating a study schedule
    schedule_params = {
        'start_date': datetime.now().isoformat(),
        'end_date': (datetime.now() + timedelta(days=7)).isoformat(),
        'daily_study_hours': 2,
        'preferred_times': ['morning', 'evening']
    }
    
    schedule = schedule_service.generate_schedule(1, schedule_params)
    assert len(schedule['sessions']) > 0
    assert all('start_time' in s and 'duration' in s for s in schedule['sessions'])
    
    # Test schedule optimization
    optimized = schedule_service.optimize_schedule(1, schedule['id'])
    assert optimized['optimization_score'] > 0

def test_analytics_dashboard(analytics_service):
    """Test analytics dashboard data generation"""
    dashboard = analytics_service.get_user_dashboard(1)
    
    # Test performance stats
    assert 'performance' in dashboard
    assert all(key in dashboard['performance'] for key in ['flashcards', 'quizzes', 'sessions'])
    
    # Test progress tracking
    assert 'goals' in dashboard
    assert len(dashboard['goals']) > 0
    assert all('date' in g and 'progress' in g for g in dashboard['goals'])
    
    # Test topic analysis
    assert 'topics' in dashboard
    assert len(dashboard['topics']) > 0
    assert all('topic' in t and 'confidence' in t for t in dashboard['topics'])
    
    # Test study time analysis
    assert 'study_time' in dashboard
    assert all(key in dashboard['study_time'] for key in ['total_time', 'average_daily_time', 'time_by_type'])

def test_goal_progress_tracking(goal_service):
    """Test goal progress tracking and updates"""
    # Create a test goal
    goal_data = {
        'title': 'Complete Python Course',
        'description': 'Finish all Python course modules',
        'deadline': (datetime.now() + timedelta(days=14)).isoformat(),
        'goal_type': 'course_completion',
        'target_score': 100
    }
    
    goal = goal_service.create_goal(1, goal_data)
    
    # Update progress
    updated_goal = goal_service.update_goal_progress(1, goal['id'], 50)
    assert updated_goal['progress'] == 50
    
    # Check goal status
    status = goal_service.get_goal_status(1, goal['id'])
    assert 'progress' in status
    assert 'remaining_time' in status
    assert 'on_track' in status

def test_study_session_tracking(schedule_service):
    """Test study session tracking and analytics"""
    # Create a test session
    session_data = {
        'start_time': datetime.now().isoformat(),
        'duration': 60,  # minutes
        'topic': 'Python Basics',
        'session_type': 'learning'
    }
    
    session = schedule_service.create_session(1, session_data)
    
    # Complete the session
    completion_data = {
        'end_time': (datetime.now() + timedelta(minutes=60)).isoformat(),
        'performance_score': 85,
        'topics_covered': ['variables', 'control_flow'],
        'notes': 'Completed basic Python concepts'
    }
    
    completed = schedule_service.complete_session(1, session['id'], completion_data)
    assert completed['status'] == 'completed'
    assert completed['performance_score'] == 85
    
    # Get session analytics
    analytics = schedule_service.get_session_analytics(1, session['id'])
    assert 'duration' in analytics
    assert 'performance_score' in analytics
    assert 'topics_covered' in analytics
