from transformers import pipeline
import spacy
import re
from collections import defaultdict
import networkx as nx

class ConceptExtractor:
    def __init__(self):
        # Load models for English and Romanian
        self.ner_pipeline_en = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
        # For Romanian, we'll use a multilingual model
        self.ner_pipeline_ro = pipeline("ner", model="xlm-roberta-large-finetuned-conll03-romanian")
        
        # Load SpaCy models
        self.nlp_en = spacy.load("en_core_web_sm")
        # For Romanian, we'll use the multilingual model
        self.nlp_ro = spacy.load("xx_ent_wiki_sm")

    def extract_concepts(self, text, language='en'):
        """Extract key concepts from text"""
        # Choose appropriate models based on language
        ner_pipeline = self.ner_pipeline_en if language == 'en' else self.ner_pipeline_ro
        nlp = self.nlp_en if language == 'en' else self.nlp_ro

        # Process text with SpaCy
        doc = nlp(text)

        # Extract different types of concepts
        concepts = {
            'terms': self._extract_key_terms(doc),
            'entities': self._process_named_entities(ner_pipeline(text)),
            'definitions': self._extract_definitions(text),
            'relationships': self._extract_relationships(doc)
        }

        return concepts

    def _extract_key_terms(self, doc):
        """Extract key terms using linguistic patterns"""
        key_terms = []
        
        # Extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Limit to phrases of 3 words or less
                key_terms.append({
                    'term': chunk.text,
                    'type': 'noun_phrase'
                })

        # Extract technical terms (words with specific patterns)
        technical_pattern = re.compile(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b')  # CamelCase words
        technical_terms = technical_pattern.findall(doc.text)
        for term in technical_terms:
            key_terms.append({
                'term': term,
                'type': 'technical'
            })

        return key_terms

    def _process_named_entities(self, entities):
        """Process named entities from the NER pipeline"""
        processed_entities = defaultdict(list)
        
        for entity in entities:
            processed_entities[entity['entity']].append({
                'text': entity['word'],
                'score': entity['score']
            })

        return dict(processed_entities)

    def _extract_definitions(self, text):
        """Extract definitions using pattern matching"""
        definition_patterns = [
            r'(?P<term>[^.]*?)\s+(?:is|are|refers to|means)\s+(?P<definition>[^.]*\.)',
            r'(?P<term>[^.]*?)\s+(?:can be defined as|is defined as)\s+(?P<definition>[^.]*\.)'
        ]

        definitions = []
        for pattern in definition_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                definitions.append({
                    'term': match.group('term').strip(),
                    'definition': match.group('definition').strip()
                })

        return definitions

    def _extract_relationships(self, doc):
        """Extract relationships between concepts"""
        graph = nx.DiGraph()

        # Add nodes for each named entity
        for ent in doc.ents:
            graph.add_node(ent.text, type=ent.label_)

        # Add edges for subject-verb-object relationships
        for token in doc:
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                subject = token.text
                verb = token.head.text
                
                # Find object
                for child in token.head.children:
                    if child.dep_ in ["dobj", "pobj"]:
                        obj = child.text
                        graph.add_edge(subject, obj, relation=verb)

        # Convert graph to dictionary format
        relationships = {
            'nodes': [{'id': node, 'type': data.get('type', 'concept')} 
                     for node, data in graph.nodes(data=True)],
            'edges': [{'source': u, 'target': v, 'relation': data['relation']} 
                     for u, v, data in graph.edges(data=True)]
        }

        return relationships

    def generate_knowledge_graph(self, concepts):
        """Generate a knowledge graph from extracted concepts"""
        graph = nx.DiGraph()

        # Add nodes for terms and entities
        for term in concepts['terms']:
            graph.add_node(term['term'], type='term')

        for entity_type, entities in concepts['entities'].items():
            for entity in entities:
                graph.add_node(entity['text'], type=entity_type)

        # Add nodes and edges for definitions
        for definition in concepts['definitions']:
            graph.add_node(definition['term'], type='term')
            graph.add_node(definition['definition'], type='definition')
            graph.add_edge(definition['term'], definition['definition'], relation='is_defined_as')

        # Add relationships from the relationship extraction
        for edge in concepts['relationships']['edges']:
            graph.add_edge(edge['source'], edge['target'], relation=edge['relation'])

        return graph
