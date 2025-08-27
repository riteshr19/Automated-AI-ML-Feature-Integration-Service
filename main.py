from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv
from loguru import logger

from app.api.routes import router as api_router
from app.core.config import settings

# Load environment variables
load_dotenv()

# Configure logging
logger.add("logs/app.log", rotation="10 MB", level=settings.LOG_LEVEL)

# Create FastAPI application
app = FastAPI(
    title="AI/ML Feature Integration Service",
    description="A microservice that uses AI/ML models to analyze unstructured data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint providing service information"""
    return {
        "service": "AI/ML Feature Integration Service",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "analyze_text": "/api/v1/analyze/text",
            "analyze_file": "/api/v1/analyze/file",
            "batch_analyze": "/api/v1/analyze/batch"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    logger.info("Starting AI/ML Feature Integration Service")
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_DEBUG
    )