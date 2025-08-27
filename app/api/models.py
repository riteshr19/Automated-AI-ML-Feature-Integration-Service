from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from enum import Enum

class AnalysisType(str, Enum):
    """Supported analysis types"""
    SENTIMENT = "sentiment"
    TEXT = "text"
    DATA_FORMAT = "data_format"
    COMPREHENSIVE = "comprehensive"

class DataFormat(str, Enum):
    """Supported data formats"""
    TEXT = "text"
    JSON = "json"
    CSV = "csv"
    AUTO = "auto"

class TextAnalysisRequest(BaseModel):
    """Request model for text analysis"""
    text: str = Field(..., description="Text to analyze", min_length=1)
    analysis_type: AnalysisType = Field(default=AnalysisType.COMPREHENSIVE, description="Type of analysis to perform")

class FileAnalysisRequest(BaseModel):
    """Request model for file analysis"""
    format_type: DataFormat = Field(default=DataFormat.AUTO, description="Expected data format")
    analysis_type: AnalysisType = Field(default=AnalysisType.COMPREHENSIVE, description="Type of analysis to perform")

class BatchAnalysisRequest(BaseModel):
    """Request model for batch analysis"""
    texts: List[str] = Field(..., description="List of texts to analyze", min_items=1)
    analysis_type: AnalysisType = Field(default=AnalysisType.COMPREHENSIVE, description="Type of analysis to perform")

class AnalysisResponse(BaseModel):
    """Response model for analysis results"""
    success: bool = Field(description="Whether the analysis was successful")
    analysis_type: str = Field(description="Type of analysis performed")
    data: Dict[str, Any] = Field(description="Analysis results")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    error: Optional[str] = Field(default=None, description="Error message if analysis failed")

class BatchAnalysisResponse(BaseModel):
    """Response model for batch analysis results"""
    success: bool = Field(description="Whether the batch analysis was successful")
    total_items: int = Field(description="Total number of items analyzed")
    successful_items: int = Field(description="Number of successfully analyzed items")
    results: List[AnalysisResponse] = Field(description="Individual analysis results")
    summary: Optional[Dict[str, Any]] = Field(default=None, description="Summary statistics")

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(description="Service status")
    timestamp: str = Field(description="Current timestamp")
    version: str = Field(default="1.0.0", description="Service version")

class ServiceInfo(BaseModel):
    """Service information model"""
    service: str = Field(description="Service name")
    version: str = Field(description="Service version")
    status: str = Field(description="Service status")
    endpoints: Dict[str, str] = Field(description="Available endpoints")