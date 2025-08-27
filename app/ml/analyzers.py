from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None

try:
    import nltk
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    nltk = None
from loguru import logger
import pickle
import os

class BaseAnalyzer(ABC):
    """Base class for all analyzers"""
    
    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze the provided data"""
        pass

class SentimentAnalyzer(BaseAnalyzer):
    """Sentiment analysis using pre-trained transformers model"""
    
    def __init__(self):
        if TRANSFORMERS_AVAILABLE:
            try:
                # Initialize the sentiment analysis pipeline
                self.sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    return_all_scores=True
                )
                logger.info("Sentiment analyzer initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to load transformer model: {e}")
                # Fallback to basic sentiment analysis
                self.sentiment_pipeline = None
                self._init_basic_model()
        else:
            logger.info("Transformers not available, using basic sentiment analysis")
            self.sentiment_pipeline = None
            self._init_basic_model()
    
    def _init_basic_model(self):
        """Initialize basic sentiment model as fallback"""
        self.basic_model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        self.is_basic = True
        logger.info("Basic sentiment model initialized as fallback")
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            if self.sentiment_pipeline:
                return self._analyze_with_transformer(text)
            else:
                return self._analyze_with_basic_model(text)
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _analyze_with_transformer(self, text: str) -> Dict[str, Any]:
        """Analyze using transformer model"""
        results = self.sentiment_pipeline(text)
        
        # Process results
        sentiment_scores = {}
        for result in results[0]:
            sentiment_scores[result['label'].lower()] = result['score']
        
        # Determine primary sentiment
        primary_sentiment = max(sentiment_scores.keys(), key=lambda k: sentiment_scores[k])
        confidence = sentiment_scores[primary_sentiment]
        
        return {
            "sentiment": primary_sentiment,
            "confidence": confidence,
            "all_scores": sentiment_scores,
            "model": "transformer"
        }
    
    def _analyze_with_basic_model(self, text: str) -> Dict[str, Any]:
        """Analyze using basic model (mock implementation)"""
        # This is a simplified mock implementation
        word_count = len(text.split())
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'hate']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, 0.5 + (positive_count * 0.1))
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, 0.5 + (negative_count * 0.1))
        else:
            sentiment = "neutral"
            confidence = 0.5
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "word_count": word_count,
            "model": "basic"
        }

class TextAnalyzer(BaseAnalyzer):
    """Comprehensive text analysis"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        if NLTK_AVAILABLE:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
            except:
                logger.warning("Failed to download NLTK data")
        else:
            logger.info("NLTK not available, using basic text analysis")
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """Perform comprehensive text analysis"""
        analysis = {
            "text_length": len(text),
            "word_count": len(text.split()),
            "character_count": len(text),
            "sentence_count": len(text.split('.')),
        }
        
        # Add sentiment analysis
        sentiment_result = self.sentiment_analyzer.analyze(text)
        analysis.update(sentiment_result)
        
        # Add basic text statistics
        analysis.update(self._get_text_statistics(text))
        
        return analysis
    
    def _get_text_statistics(self, text: str) -> Dict[str, Any]:
        """Get basic text statistics"""
        words = text.split()
        
        return {
            "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "unique_words": len(set(words)),
            "readability_score": self._calculate_readability(text)
        }
    
    def _calculate_readability(self, text: str) -> float:
        """Simple readability score calculation"""
        words = text.split()
        sentences = text.split('.')
        
        if not words or not sentences:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Simple readability formula
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_word_length / 100)
        return max(0, min(100, readability))

class DataFormatAnalyzer(BaseAnalyzer):
    """Analyzer for different data formats"""
    
    def analyze(self, data: Any, format_type: str = "auto") -> Dict[str, Any]:
        """Analyze data based on format"""
        try:
            if format_type == "csv" or (format_type == "auto" and self._is_csv(data)):
                return self._analyze_csv(data)
            elif format_type == "json" or (format_type == "auto" and self._is_json(data)):
                return self._analyze_json(data)
            else:
                return self._analyze_text(data)
        except Exception as e:
            logger.error(f"Error in data format analysis: {e}")
            return {"error": str(e), "format": "unknown"}
    
    def _is_csv(self, data: str) -> bool:
        """Check if data appears to be CSV"""
        lines = data.strip().split('\n')
        if len(lines) < 2:
            return False
        
        # Check if it has comma separation and consistent number of fields
        try:
            first_line_parts = lines[0].split(',')
            if len(first_line_parts) < 2:
                return False
            
            # Check if most lines have similar number of parts
            similar_parts = 0
            for line in lines[1:]:
                if len(line.split(',')) == len(first_line_parts):
                    similar_parts += 1
            
            return similar_parts >= len(lines) * 0.7  # At least 70% of lines should match
        except:
            return False
    
    def _is_json(self, data: str) -> bool:
        """Check if data appears to be JSON"""
        data = data.strip()
        if not data:
            return False
        try:
            import json
            json.loads(data)
            return True
        except:
            return False
    
    def _analyze_csv(self, data: str) -> Dict[str, Any]:
        """Analyze CSV data"""
        try:
            import io
            df = pd.read_csv(io.StringIO(data))
            
            # Convert data types to serializable format
            data_types = {}
            for col, dtype in df.dtypes.items():
                data_types[col] = str(dtype)
            
            # Convert sample data to serializable format
            sample_data = df.head(3).to_dict('records')
            
            return {
                "format": "csv",
                "rows": int(len(df)),
                "columns": int(len(df.columns)),
                "column_names": df.columns.tolist(),
                "data_types": data_types,
                "sample_data": sample_data
            }
        except Exception as e:
            return {"format": "csv", "error": str(e)}
    
    def _analyze_json(self, data: str) -> Dict[str, Any]:
        """Analyze JSON data"""
        try:
            import json
            parsed = json.loads(data)
            return {
                "format": "json",
                "type": type(parsed).__name__,
                "size": len(parsed) if isinstance(parsed, (list, dict)) else 1,
                "keys": list(parsed.keys()) if isinstance(parsed, dict) else None,
                "sample": parsed if len(str(parsed)) < 500 else str(parsed)[:500] + "..."
            }
        except Exception as e:
            return {"format": "json", "error": str(e)}
    
    def _analyze_text(self, data: str) -> Dict[str, Any]:
        """Analyze plain text data"""
        text_analyzer = TextAnalyzer()
        result = text_analyzer.analyze(data)
        result["format"] = "text"
        return result