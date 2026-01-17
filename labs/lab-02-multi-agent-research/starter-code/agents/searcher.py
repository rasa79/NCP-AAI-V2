"""
Searcher Agent - Finds and retrieves relevant information.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class SearcherAgent:
    """
    Searcher agent responsible for:
    - Searching for relevant information
    - Retrieving documents from knowledge base
    - Extracting key findings
    - Ranking results by relevance
    """
    
    def __init__(self):
        """Initialize searcher agent."""
        self.name = "Searcher"
        # TODO: Initialize RAG components from Lab 1
        logger.info(f"{self.name} agent initialized")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for information on given topic.
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of findings with content and metadata
        
        TODO: Implement search functionality
        Hints:
        - Reuse RAG components from Lab 1
        - Generate query embedding
        - Retrieve relevant documents
        - Format results with citations
        """
        logger.info(f"Searching for: {query}")
        
        # YOUR CODE HERE
        
        findings = []  # REPLACE THIS
        return findings
