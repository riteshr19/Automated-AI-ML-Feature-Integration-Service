from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from typing import List
import json
from loguru import logger
from datetime import datetime

from app.api.models import (
    TextAnalysisRequest, 
    FileAnalysisRequest,
    BatchAnalysisRequest,
    AnalysisResponse, 
    BatchAnalysisResponse,
    AnalysisType
)
from app.ml.analyzers import TextAnalyzer, SentimentAnalyzer, DataFormatAnalyzer

router = APIRouter()

# Initialize analyzers
text_analyzer = TextAnalyzer()
sentiment_analyzer = SentimentAnalyzer()
data_format_analyzer = DataFormatAnalyzer()

@router.post("/analyze/text", response_model=AnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text data using specified analysis type
    
    This endpoint can perform various types of text analysis including:
    - Sentiment analysis
    - Comprehensive text analysis (statistics, readability, sentiment)
    - Data format detection and analysis
    """
    try:
        logger.info(f"Received text analysis request: {request.analysis_type}")
        
        if request.analysis_type == AnalysisType.SENTIMENT:
            result = sentiment_analyzer.analyze(request.text)
        elif request.analysis_type == AnalysisType.TEXT:
            result = text_analyzer.analyze(request.text)
        elif request.analysis_type == AnalysisType.DATA_FORMAT:
            result = data_format_analyzer.analyze(request.text)
        else:  # COMPREHENSIVE
            result = text_analyzer.analyze(request.text)
        
        return AnalysisResponse(
            success=True,
            analysis_type=request.analysis_type.value,
            data=result,
            metadata={
                "timestamp": datetime.now().isoformat(),
                "text_length": len(request.text)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in text analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/file", response_model=AnalysisResponse)
async def analyze_file(
    file: UploadFile = File(...),
    format_type: str = "auto",
    analysis_type: str = "comprehensive"
):
    """
    Analyze uploaded file content
    
    Supports various file formats:
    - Text files (.txt)
    - JSON files (.json)
    - CSV files (.csv)
    """
    try:
        logger.info(f"Received file analysis request: {file.filename}")
        
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Determine analysis type
        if analysis_type == "sentiment":
            result = sentiment_analyzer.analyze(text_content)
        elif analysis_type == "data_format":
            result = data_format_analyzer.analyze(text_content, format_type)
        else:  # comprehensive or text
            if format_type == "auto":
                result = data_format_analyzer.analyze(text_content)
            else:
                result = data_format_analyzer.analyze(text_content, format_type)
        
        return AnalysisResponse(
            success=True,
            analysis_type=analysis_type,
            data=result,
            metadata={
                "timestamp": datetime.now().isoformat(),
                "filename": file.filename,
                "file_size": len(content),
                "format_type": format_type
            }
        )
        
    except Exception as e:
        logger.error(f"Error in file analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/batch", response_model=BatchAnalysisResponse)
async def analyze_batch(request: BatchAnalysisRequest):
    """
    Perform batch analysis on multiple text items
    
    Useful for processing large amounts of data efficiently.
    Returns individual results plus summary statistics.
    """
    try:
        logger.info(f"Received batch analysis request for {len(request.texts)} items")
        
        results = []
        successful_count = 0
        
        for i, text in enumerate(request.texts):
            try:
                if request.analysis_type == AnalysisType.SENTIMENT:
                    analysis_result = sentiment_analyzer.analyze(text)
                elif request.analysis_type == AnalysisType.TEXT:
                    analysis_result = text_analyzer.analyze(text)
                elif request.analysis_type == AnalysisType.DATA_FORMAT:
                    analysis_result = data_format_analyzer.analyze(text)
                else:  # COMPREHENSIVE
                    analysis_result = text_analyzer.analyze(text)
                
                result = AnalysisResponse(
                    success=True,
                    analysis_type=request.analysis_type.value,
                    data=analysis_result,
                    metadata={"item_index": i, "text_length": len(text)}
                )
                results.append(result)
                successful_count += 1
                
            except Exception as e:
                logger.error(f"Error analyzing item {i}: {e}")
                result = AnalysisResponse(
                    success=False,
                    analysis_type=request.analysis_type.value,
                    data={},
                    metadata={"item_index": i},
                    error=str(e)
                )
                results.append(result)
        
        # Calculate summary statistics
        summary = _calculate_batch_summary(results, request.analysis_type)
        
        return BatchAnalysisResponse(
            success=True,
            total_items=len(request.texts),
            successful_items=successful_count,
            results=results,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def _calculate_batch_summary(results: List[AnalysisResponse], analysis_type: AnalysisType) -> dict:
    """Calculate summary statistics for batch analysis"""
    successful_results = [r for r in results if r.success]
    
    if not successful_results:
        return {"message": "No successful analyses"}
    
    summary = {
        "success_rate": len(successful_results) / len(results),
        "average_text_length": sum(r.metadata.get("text_length", 0) for r in successful_results) / len(successful_results)
    }
    
    # Add analysis-specific summaries
    if analysis_type == AnalysisType.SENTIMENT:
        sentiments = [r.data.get("sentiment") for r in successful_results if r.data.get("sentiment")]
        if sentiments:
            sentiment_counts = {}
            for sentiment in sentiments:
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            
            summary["sentiment_distribution"] = sentiment_counts
            summary["average_confidence"] = sum(
                r.data.get("confidence", 0) for r in successful_results
            ) / len(successful_results)
    
    elif analysis_type in [AnalysisType.TEXT, AnalysisType.COMPREHENSIVE]:
        word_counts = [r.data.get("word_count", 0) for r in successful_results]
        if word_counts:
            summary["average_word_count"] = sum(word_counts) / len(word_counts)
            summary["total_words"] = sum(word_counts)
    
    return summary

@router.get("/models/info")
async def get_model_info():
    """Get information about available models and their capabilities"""
    return {
        "available_models": {
            "sentiment_analysis": {
                "description": "Sentiment analysis using transformer models",
                "input_types": ["text"],
                "output": "sentiment classification with confidence scores"
            },
            "text_analysis": {
                "description": "Comprehensive text analysis including statistics and readability",
                "input_types": ["text"],
                "output": "text statistics, sentiment, and readability metrics"
            },
            "data_format_analysis": {
                "description": "Analysis of structured data formats",
                "input_types": ["text", "json", "csv"],
                "output": "format detection and structure analysis"
            }
        },
        "supported_formats": ["text", "json", "csv"],
        "analysis_types": ["sentiment", "text", "data_format", "comprehensive"]
    }