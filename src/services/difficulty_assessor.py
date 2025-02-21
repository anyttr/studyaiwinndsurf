import spacy
import textstat
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class DifficultyAssessor:
    def __init__(self):
        # Load SpaCy models for both languages
        self.nlp_en = spacy.load('en_core_web_sm')
        self.nlp_ro = spacy.load('xx_ent_wiki_sm')  # Multilingual model for Romanian
        
        # Initialize TF-IDF vectorizer
        self.tfidf = TfidfVectorizer(max_features=1000)
        
        # Technical term patterns
        self.technical_patterns = {
            'en': [
                r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b',  # CamelCase
                r'\b[A-Z]{2,}\b',  # Acronyms
                r'\b\w+(?:ology|ization|isation|ment)\b'  # Words with technical suffixes
            ],
            'ro': [
                r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b',
                r'\b[A-Z]{2,}\b',
                r'\b\w+(?:ologie|izare|ment)\b'
            ]
        }

    def assess_difficulty(self, text, language='en'):
        """Assess the difficulty of a text and return a comprehensive analysis"""
        # Choose appropriate NLP model
        nlp = self.nlp_en if language == 'en' else self.nlp_ro
        doc = nlp(text)

        # Calculate various metrics
        metrics = {
            'linguistic_complexity': self._calculate_linguistic_complexity(doc, language),
            'concept_density': self._calculate_concept_density(doc),
            'technical_complexity': self._calculate_technical_complexity(text, language),
            'prerequisite_concepts': self._identify_prerequisites(doc)
        }

        # Determine overall difficulty level
        difficulty_level = self._determine_difficulty_level(metrics)

        return {
            'difficulty_level': difficulty_level,
            'metrics': metrics,
            'recommendations': self._generate_recommendations(metrics, difficulty_level)
        }

    def _calculate_linguistic_complexity(self, doc, language):
        """Calculate linguistic complexity based on various factors"""
        # Basic metrics
        avg_sentence_length = len([token for token in doc if not token.is_punct]) / len(list(doc.sents))
        avg_word_length = np.mean([len(token.text) for token in doc if token.is_alpha])
        
        # Calculate readability score
        if language == 'en':
            readability_score = textstat.flesch_reading_ease(doc.text)
        else:
            # For Romanian, use a simplified metric
            readability_score = 100 - (avg_sentence_length * 0.39 + avg_word_length * 11.8)

        return {
            'readability_score': readability_score,
            'avg_sentence_length': avg_sentence_length,
            'avg_word_length': avg_word_length,
            'complexity_score': self._normalize_score(
                (100 - readability_score) * 0.4 +
                (avg_sentence_length / 20) * 0.3 +
                (avg_word_length / 6) * 0.3
            )
        }

    def _calculate_concept_density(self, doc):
        """Calculate the density of key concepts in the text"""
        # Count named entities
        entity_count = len(doc.ents)
        
        # Count noun phrases
        noun_phrase_count = len(list(doc.noun_chunks))
        
        # Calculate density per 100 words
        total_words = len([token for token in doc if token.is_alpha])
        entity_density = (entity_count / total_words) * 100
        noun_phrase_density = (noun_phrase_count / total_words) * 100

        return {
            'entity_density': entity_density,
            'noun_phrase_density': noun_phrase_density,
            'density_score': self._normalize_score(
                entity_density * 0.5 + noun_phrase_density * 0.5
            )
        }

    def _calculate_technical_complexity(self, text, language):
        """Calculate the complexity based on technical terms and vocabulary"""
        # Get word frequencies
        words = [token.text.lower() for token in self.nlp_en(text) if token.is_alpha]
        word_freq = Counter(words)
        
        # Calculate vocabulary richness
        vocab_richness = len(word_freq) / len(words)
        
        # Count technical terms
        technical_terms = []
        for pattern in self.technical_patterns[language]:
            technical_terms.extend(re.findall(pattern, text))
        
        technical_density = len(technical_terms) / len(words) * 100

        return {
            'vocab_richness': vocab_richness,
            'technical_term_density': technical_density,
            'complexity_score': self._normalize_score(
                vocab_richness * 0.4 + (technical_density / 10) * 0.6
            )
        }

    def _identify_prerequisites(self, doc):
        """Identify potential prerequisite concepts"""
        prerequisites = []
        
        # Look for specific patterns indicating prerequisites
        for sent in doc.sents:
            if any(token.text.lower() in ['requires', 'needs', 'assumes', 'prerequisite']
                   for token in sent):
                prerequisites.append(sent.text)

        return prerequisites

    def _determine_difficulty_level(self, metrics):
        """Determine overall difficulty level based on metrics"""
        # Calculate weighted average of different scores
        overall_score = (
            metrics['linguistic_complexity']['complexity_score'] * 0.3 +
            metrics['concept_density']['density_score'] * 0.4 +
            metrics['technical_complexity']['complexity_score'] * 0.3
        )

        # Map score to difficulty level
        if overall_score < 0.3:
            return 'Beginner'
        elif overall_score < 0.7:
            return 'Intermediate'
        else:
            return 'Advanced'

    def _generate_recommendations(self, metrics, difficulty_level):
        """Generate recommendations based on the analysis"""
        recommendations = []

        # Add recommendations based on metrics
        if metrics['linguistic_complexity']['avg_sentence_length'] > 25:
            recommendations.append("Consider breaking down long sentences for better readability")

        if metrics['concept_density']['density_score'] > 0.7:
            recommendations.append("High concept density detected. Consider introducing concepts more gradually")

        if metrics['technical_complexity']['technical_term_density'] > 10:
            recommendations.append("High number of technical terms. Consider adding a glossary")

        if len(metrics['prerequisite_concepts']) > 0:
            recommendations.append("Ensure prerequisites are clearly explained before introducing new concepts")

        return recommendations

    def _normalize_score(self, score):
        """Normalize a score to be between 0 and 1"""
        return max(0, min(1, score))
