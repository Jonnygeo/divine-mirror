import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any, Optional
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_environment_variables():
    """
    Load environment variables from .env file
    """
    try:
        load_dotenv()
        logger.info("Environment variables loaded from .env file")
        
        # Check for required environment variables
        required_vars = ["OPENAI_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.warning(f"Missing required environment variables: {', '.join(missing_vars)}")
            logger.warning("Some functionality may be limited or unavailable")
    except Exception as e:
        logger.error(f"Error loading environment variables: {str(e)}")

def safe_json_load(json_str: str) -> Optional[Dict[str, Any]]:
    """
    Safely load JSON string
    
    Args:
        json_str: JSON string to load
        
    Returns:
        Dict if successful, None if failed
    """
    try:
        return json.loads(json_str)
    except Exception as e:
        logger.error(f"Error parsing JSON: {str(e)}")
        return None

def format_error_response(error_message: str) -> Dict[str, Any]:
    """
    Format standard error response
    
    Args:
        error_message: Error message to include
        
    Returns:
        Dictionary with error details
    """
    return {
        "error": True,
        "message": error_message,
        "data": None
    }

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent prompt injection
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove potential prompt injection attempts
    dangerous_patterns = [
        "ignore previous instructions",
        "ignore above instructions",
        "disregard previous",
        "forget your instructions",
        "you are now",
        "as an AI",
        "system:",
        "system prompt:"
    ]
    
    sanitized = text
    for pattern in dangerous_patterns:
        sanitized = sanitized.lower().replace(pattern.lower(), "[filtered]")
    
    return sanitized

def validate_tradition(tradition: str, valid_traditions: list) -> bool:
    """
    Validate that a tradition is in the list of valid traditions
    
    Args:
        tradition: Tradition to validate
        valid_traditions: List of valid traditions
        
    Returns:
        True if valid, False otherwise
    """
    return tradition in valid_traditions

def validate_time_period(time_period: str, valid_periods: list) -> bool:
    """
    Validate that a time period is in the list of valid time periods
    
    Args:
        time_period: Time period to validate
        valid_periods: List of valid time periods
        
    Returns:
        True if valid, False otherwise
    """
    return time_period in valid_periods
