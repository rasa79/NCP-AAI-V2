"""
Short-term memory for current research session.
"""

import logging
from typing import Dict, List, Any
from collections import defaultdict

logger = logging.getLogger(__name__)


class ShortTermMemory:
    """
    Manages short-term memory for current research session.
    Stores conversation history, agent interactions, and findings.
    """
    
    def __init__(self, max_items: int = 100):
        """
        Initialize short-term memory.
        
        Args:
            max_items: Maximum items to store before pruning
        """
        self.max_items = max_items
        self.memory: Dict[str, List[Any]] = defaultdict(list)
        logger.info("Short-term memory initialized")
    
    def add(self, category: str, item: Any):
        """
        Add item to memory.
        
        Args:
            category: Memory category (e.g., 'finding', 'message', 'task')
            item: Item to store
        
        TODO: Implement memory addition with pruning
        """
        # YOUR CODE HERE
        pass
    
    def get_all(self, category: str) -> List[Any]:
        """Get all items in category."""
        return self.memory.get(category, [])
    
    def get_recent(self, category: str, n: int = 10) -> List[Any]:
        """Get n most recent items in category."""
        items = self.memory.get(category, [])
        return items[-n:]
    
    def clear(self, category: str = None):
        """Clear memory (all or specific category)."""
        if category:
            self.memory[category] = []
        else:
            self.memory.clear()
        logger.info(f"Memory cleared: {category or 'all'}")
    
    def get_stats(self) -> Dict[str, int]:
        """Get memory statistics."""
        return {
            category: len(items)
            for category, items in self.memory.items()
        }
