"""
Utility functions for multi-agent research system.
"""

import logging
from typing import Any, Dict, List
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_timestamp() -> str:
    """Return current timestamp as string."""
    return datetime.now().isoformat()


def create_message(sender: str, recipient: str, content: Any, msg_type: str = "info") -> Dict[str, Any]:
    """
    Create standardized message for inter-agent communication.
    
    Args:
        sender: Agent sending the message
        recipient: Agent receiving the message
        content: Message content
        msg_type: Type of message (info, task, result, error)
    
    Returns:
        Formatted message dictionary
    """
    return {
        "sender": sender,
        "recipient": recipient,
        "content": content,
        "type": msg_type,
        "timestamp": format_timestamp()
    }


def validate_agent_response(response: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    Validate that agent response contains required fields.
    
    Args:
        response: Agent response dictionary
        required_fields: List of required field names
    
    Returns:
        True if valid, False otherwise
    """
    return all(field in response for field in required_fields)


def truncate_context(text: str, max_length: int = 2000) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "... [truncated]"


def log_agent_action(agent_name: str, action: str, details: str = ""):
    """Log agent action with consistent formatting."""
    logger.info(f"[{agent_name}] {action} {details}")
