from typing import Dict, Any, List
import json
import csv
import io
from loguru import logger

def format_response(success: bool, data: Any = None, error: str = None, metadata: Dict = None) -> Dict[str, Any]:
    """Format API response consistently"""
    response = {
        "success": success,
        "timestamp": "2024-01-01T00:00:00Z"  # Would use datetime.now().isoformat() in production
    }
    
    if data is not None:
        response["data"] = data
    
    if error:
        response["error"] = error
    
    if metadata:
        response["metadata"] = metadata
    
    return response

def validate_text_input(text: str, min_length: int = 1, max_length: int = 10000) -> bool:
    """Validate text input"""
    if not isinstance(text, str):
        return False
    
    if len(text) < min_length or len(text) > max_length:
        return False
    
    return True

def parse_csv_content(content: str) -> List[Dict[str, Any]]:
    """Parse CSV content and return as list of dictionaries"""
    try:
        reader = csv.DictReader(io.StringIO(content))
        return list(reader)
    except Exception as e:
        logger.error(f"Error parsing CSV: {e}")
        return []

def parse_json_content(content: str) -> Any:
    """Parse JSON content"""
    try:
        return json.loads(content)
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")
        return None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    import re
    # Remove any non-alphanumeric characters except dots, hyphens, and underscores
    sanitized = re.sub(r'[^\w\.-]', '_', filename)
    return sanitized[:100]  # Limit length

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return filename.split('.')[-1].lower() if '.' in filename else ''

def estimate_processing_time(text_length: int, analysis_type: str) -> float:
    """Estimate processing time based on text length and analysis type"""
    base_time = 0.1  # Base processing time in seconds
    
    # Different analysis types have different complexity
    complexity_multipliers = {
        "sentiment": 1.0,
        "text": 1.5,
        "data_format": 0.8,
        "comprehensive": 2.0
    }
    
    multiplier = complexity_multipliers.get(analysis_type, 1.0)
    
    # Estimate based on text length (rough approximation)
    time_per_char = 0.0001
    estimated_time = base_time + (text_length * time_per_char * multiplier)
    
    return round(estimated_time, 2)