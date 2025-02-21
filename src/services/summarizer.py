from transformers import pipeline
import spacy
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from heapq import nlargest
from string import punctuation
import re

class Summarizer:
    def __init__(self):
        # Initialize models for both languages
        self.summarizer_en = pipeline("summarization", model="facebook/bart-large-cnn")
        self.summarizer_ro = pipeline("summarization", model="facebook/mbart-large-cc25")
        
        # Load SpaCy models
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_ro = spacy.load("xx_ent_wiki_sm")  # Multilingual model for Romanian
        
        # Load stopwords
        self.stopwords_en = set(stopwords.words('english'))
        # Romanian stopwords (basic set, should be expanded)
        self.stopwords_ro = set(['și', 'în', 'la', 'de', 'pe', 'cu', 'pentru', 'dar', 'sau', 'care'])

    def generate_summary(self, text, language='en', max_length=150, min_length=50, summary_type='paragraph'):
        """Generate a summary of the given text"""
        if summary_type == 'bullet_points':
            return self._generate_bullet_points(text, language)
        else:
            return self._generate_paragraph_summary(text, language, max_length, min_length)

    def _generate_paragraph_summary(self, text, language='en', max_length=150, min_length=50):
        """Generate a paragraph summary using the appropriate model"""
        # Choose the appropriate summarizer based on language
        summarizer = self.summarizer_en if language == 'en' else self.summarizer_ro
        
        # Clean and prepare text
        cleaned_text = self._clean_text(text)
        
        # Split text into chunks if it's too long
        chunks = self._split_into_chunks(cleaned_text, max_length=1024)
        
        summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, 
                               max_length=max_length,
                               min_length=min_length,
                               do_sample=False)[0]['summary_text']
            summaries.append(summary)
        
        # Combine summaries if there are multiple chunks
        final_summary = ' '.join(summaries)
        
        return {
            'type': 'paragraph',
            'summary': final_summary,
            'length': len(final_summary.split())
        }

    def _generate_bullet_points(self, text, language='en', num_points=5):
        """Generate bullet points from the text"""
        # Choose appropriate NLP model and stopwords
        nlp = self.nlp_en if language == 'en' else self.nlp_ro
        stop_words = self.stopwords_en if language == 'en' else self.stopwords_ro
        
        # Process the text
        doc = nlp(text)
        
        # Tokenize into sentences
        sentences = [sent.text.strip() for sent in doc.sents]
        
        # Calculate sentence scores based on word frequency
        word_freq = self._calculate_word_frequency(text, stop_words)
        sentence_scores = self._score_sentences(sentences, word_freq)
        
        # Get the top sentences
        summary_sentences = nlargest(num_points, sentence_scores, key=sentence_scores.get)
        
        # Convert to bullet points
        bullet_points = []
        for sent in summary_sentences:
            # Clean and format the sentence
            point = sent.strip()
            # Remove redundant information and make more concise
            point = self._format_bullet_point(point)
            bullet_points.append(point)
        
        return {
            'type': 'bullet_points',
            'points': bullet_points,
            'count': len(bullet_points)
        }

    def _clean_text(self, text):
        """Clean and prepare text for summarization"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters and formatting
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        return text

    def _split_into_chunks(self, text, max_length=1024):
        """Split text into chunks of specified maximum length"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_chunk.append(word)
                current_length += len(word) + 1
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def _calculate_word_frequency(self, text, stop_words):
        """Calculate word frequency excluding stop words"""
        # Tokenize and clean words
        words = word_tokenize(text.lower())
        words = [word for word in words 
                if word not in stop_words 
                and word not in punctuation
                and not word.isnumeric()]
        
        # Calculate frequency
        freq_dist = FreqDist(words)
        
        # Normalize frequencies
        max_freq = max(freq_dist.values())
        return {word: freq/max_freq for word, freq in freq_dist.items()}

    def _score_sentences(self, sentences, word_freq):
        """Score sentences based on word frequency"""
        sentence_scores = {}
        
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            score = sum(word_freq.get(word, 0) for word in words)
            # Normalize by sentence length
            sentence_scores[sentence] = score / (len(words) + 1)
        
        return sentence_scores

    def _format_bullet_point(self, sentence):
        """Format a sentence as a concise bullet point"""
        # Remove certain phrases that often start sentences but add little value
        removable_starts = [
            'it is', 'there is', 'there are', 'this is', 'these are',
            'however', 'moreover', 'furthermore', 'in addition'
        ]
        
        sentence = sentence.strip()
        sentence_lower = sentence.lower()
        
        for start in removable_starts:
            if sentence_lower.startswith(start):
                sentence = sentence[len(start):].strip()
                # Capitalize the first letter
                sentence = sentence[0].upper() + sentence[1:]
        
        # Ensure the sentence ends with proper punctuation
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'
        
        return sentence
