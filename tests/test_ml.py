import pytest
from app.ml.analyzers import SentimentAnalyzer, TextAnalyzer, DataFormatAnalyzer

def test_sentiment_analyzer():
    """Test sentiment analyzer"""
    analyzer = SentimentAnalyzer()
    
    # Test positive sentiment
    result = analyzer.analyze("I love this product! It's amazing!")
    assert "sentiment" in result
    assert result["sentiment"] in ["positive", "LABEL_2"]  # Different models may return different labels
    assert "confidence" in result
    assert 0 <= result["confidence"] <= 1
    
    # Test negative sentiment
    result = analyzer.analyze("This is terrible! I hate it!")
    assert "sentiment" in result
    assert result["sentiment"] in ["negative", "LABEL_0"]
    
    # Test neutral sentiment
    result = analyzer.analyze("This is a chair.")
    assert "sentiment" in result

def test_text_analyzer():
    """Test comprehensive text analyzer"""
    analyzer = TextAnalyzer()
    
    text = "This is a sample text for testing. It has multiple sentences and words."
    result = analyzer.analyze(text)
    
    assert "word_count" in result
    assert "character_count" in result
    assert "sentence_count" in result
    assert "sentiment" in result
    assert "avg_word_length" in result
    assert "unique_words" in result
    assert "readability_score" in result
    
    assert result["word_count"] > 0
    assert result["character_count"] > 0
    assert result["sentence_count"] >= 1

def test_data_format_analyzer():
    """Test data format analyzer"""
    analyzer = DataFormatAnalyzer()
    
    # Test CSV format
    csv_data = "name,age,city\nJohn,25,NYC\nJane,30,LA"
    result = analyzer.analyze(csv_data, "csv")
    assert result["format"] == "csv"
    assert "rows" in result
    assert "columns" in result
    
    # Test JSON format
    json_data = '{"name": "John", "age": 25, "city": "NYC"}'
    result = analyzer.analyze(json_data, "json")
    assert result["format"] == "json"
    assert "type" in result
    
    # Test plain text
    text_data = "This is plain text content."
    result = analyzer.analyze(text_data, "text")
    assert result["format"] == "text"
    assert "word_count" in result

def test_analyzer_error_handling():
    """Test analyzer error handling"""
    analyzer = SentimentAnalyzer()
    
    # Test with very long text (should still work but might hit limits)
    long_text = "word " * 1000
    result = analyzer.analyze(long_text)
    assert "sentiment" in result or "error" in result
    
    # Test with empty text
    result = analyzer.analyze("")
    assert "sentiment" in result or "error" in result