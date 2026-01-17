"""
Answer generation module for RAG agent.

This module handles LLM-based answer generation using retrieved context
with proper prompt engineering and error handling.
"""

import logging
from typing import List, Dict, Any, Optional
import os

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.docstore.document import Document

from utils import validate_input, measure_time, retry_with_backoff

logger = logging.getLogger(__name__)


class AnswerGenerator:
    """
    Generates answers using LLM with retrieved context.
    
    Handles prompt construction, LLM interaction, and answer formatting
    with source citations.
    """
    
    def __init__(
        self,
        model_name: str = "gpt-3.5-turbo-instruct",
        temperature: float = 0.0,
        max_tokens: int = 500
    ):
        """
        Initialize answer generator.
        
        Args:
            model_name: Name of LLM model to use
            temperature: Sampling temperature (0 = deterministic)
            max_tokens: Maximum tokens in generated answer
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # TODO: Initialize LLM
        # Hints:
        # 1. Check for OPENAI_API_KEY environment variable
        # 2. Initialize OpenAI LLM with parameters
        # 3. Handle initialization errors
        
        # Check for API key
        if not os.getenv("OPENAI_API_KEY"):
            logger.warning("OPENAI_API_KEY not found in environment")
        
        try:
            # YOUR CODE HERE
            # Initialize the LLM
            
            self.llm = None  # REPLACE THIS LINE
            
            logger.info(f"AnswerGenerator initialized with model={model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
        
        # TODO: Create prompt template
        # Hints:
        # 1. Use PromptTemplate from langchain
        # 2. Include placeholders for context and question
        # 3. Add instructions to ground answer in context
        # 4. Add instruction to cite sources
        
        self.prompt_template = None  # REPLACE THIS LINE
    
    def _create_prompt_template(self) -> PromptTemplate:
        """
        Create prompt template for answer generation.
        
        Returns:
            PromptTemplate with context and question variables
        """
        # TODO: Implement prompt template creation
        # Hints:
        # 1. Template should include context and question
        # 2. Instruct model to only use provided context
        # 3. Instruct model to cite sources
        # 4. Instruct model to say "I don't know" if context insufficient
        
        template = """
        YOUR PROMPT TEMPLATE HERE
        
        Context: {context}
        
        Question: {question}
        
        Answer:
        """
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def _format_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into context string.
        
        Args:
            documents: List of retrieved Document objects
            
        Returns:
            Formatted context string with source citations
        """
        # TODO: Implement context formatting
        # Hints:
        # 1. Combine document contents
        # 2. Add source information (filename, chunk_id)
        # 3. Number each document for citation
        # 4. Keep formatting clean and readable
        
        if not documents:
            return "No relevant context found."
        
        # YOUR CODE HERE
        # Format documents into context string
        
        context = ""  # REPLACE THIS LINE
        
        return context
    
    @measure_time
    @retry_with_backoff(max_retries=3)
    def generate(
        self,
        query: str,
        context_documents: List[Document],
        include_sources: bool = True
    ) -> Dict[str, Any]:
        """
        Generate answer to query using retrieved context.
        
        Args:
            query: User question
            context_documents: Retrieved documents providing context
            include_sources: Whether to include source citations in response
            
        Returns:
            Dictionary with answer, sources, and metadata
            
        Raises:
            ValueError: If query is empty
            RuntimeError: If generation fails
        """
        # TODO: Implement answer generation
        # Hints:
        # 1. Validate inputs
        # 2. Format context from documents
        # 3. Create prompt using template
        # 4. Call LLM to generate answer
        # 5. Format response with sources
        # 6. Handle errors (API failures, empty responses)
        
        validate_input(query, "query", str)
        
        try:
            # YOUR CODE HERE
            # Generate answer using LLM
            
            # Format context
            context = self._format_context(context_documents)
            
            # Create prompt
            # Generate answer
            # Format response
            
            response = {
                "answer": "",  # REPLACE
                "sources": [],  # REPLACE
                "num_sources": 0,  # REPLACE
                "query": query
            }
            
            logger.info(f"Generated answer for query: {query[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise RuntimeError(f"Failed to generate answer: {e}")
    
    def _extract_sources(self, documents: List[Document]) -> List[Dict[str, str]]:
        """
        Extract source information from documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of source dictionaries with filename and metadata
        """
        sources = []
        
        for i, doc in enumerate(documents, 1):
            source_info = {
                "id": i,
                "filename": doc.metadata.get("source", "Unknown"),
                "chunk_id": doc.metadata.get("chunk_id", "N/A"),
                "content_preview": doc.page_content[:100] + "..."
            }
            sources.append(source_info)
        
        return sources
    
    def generate_with_confidence(
        self,
        query: str,
        context_documents: List[Document]
    ) -> Dict[str, Any]:
        """
        Generate answer with confidence score.
        
        Confidence is estimated based on:
        - Number of relevant documents found
        - Similarity scores of retrieved documents
        - Answer length and completeness
        
        Args:
            query: User question
            context_documents: Retrieved documents with similarity scores
            
        Returns:
            Dictionary with answer, sources, and confidence score
        """
        # TODO: Implement confidence scoring
        # Hints:
        # 1. Generate answer normally
        # 2. Calculate confidence based on retrieval quality
        # 3. Consider: number of docs, similarity scores, answer length
        # 4. Return confidence score (0 to 1)
        
        response = self.generate(query, context_documents)
        
        # YOUR CODE HERE
        # Calculate confidence score
        
        confidence = 0.5  # REPLACE THIS LINE
        
        response["confidence"] = confidence
        return response
