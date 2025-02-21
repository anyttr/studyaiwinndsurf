import pytest
import os
from src.services.concept_extractor import ConceptExtractor
from src.services.visualizer import Visualizer
from src.services.difficulty_assessor import DifficultyAssessor
from src.services.summarizer import Summarizer

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
