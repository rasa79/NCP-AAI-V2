"""
Main RAG Agent implementation.

This module integrates all components (document processing, embeddings,
retrieval, generation) into a complete RAG system.
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from document_processor import DocumentProcessor
from embeddings import EmbeddingModel
from retriever import VectorRetriever
from generator import AnswerGenerator
from utils import validate_input, measure_time

logger = logging.getLogger(__name__)


class RAGAgent:
    """
    Complete RAG (Retrieval-Augmented Generation) agent.
    
    Integrates document processing, embedding generation, vector retrieval,
    and answer generation into a unified system.
    """
    
    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        chunk_size: int = 800,
        chunk_overlap: int = 150,
        top_k: int = 3
    ):
        """
        Initialize RAG agent with all components.
        
        Args:
            embedding_model: Name of sentence-transformers model
            chunk_size: Size of document chunks in characters
            chunk_overlap: Overlap between chunks in characters
            top_k: Number of documents to retrieve for each query
        """
        self.top_k = top_k
        
        logger.info("Initializing RAG Agent...")
        
        # TODO: Initialize all components
        # Hints:
        # 1. Initialize DocumentProcessor with chunk parameters
        # 2. Initialize EmbeddingModel with model name
        # 3. Initialize VectorRetriever with embedding dimension
        # 4. Initialize AnswerGenerator
        # 5. Handle initialization errors
        
        try:
            # YOUR CODE HERE
            # Initialize all components
            
            self.document_processor = None  # REPLACE
            self.embedding_model = None  # REPLACE
            self.retriever = None  # REPLACE
            self.generator = None  # REPLACE
            
            logger.info("RAG Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG Agent: {e}")
            raise
    
    @measure_time
    def ingest(self, documents_path: str) -> Dict[str, Any]:
        """
        Ingest documents into the RAG system.
        
        This method:
        1. Loads and chunks documents
        2. Generates embeddings
        3. Indexes documents in vector database
        
        Args:
            documents_path: Path to directory containing documents
            
        Returns:
            Dictionary with ingestion statistics
            
        Raises:
            ValueError: If documents_path is invalid
            RuntimeError: If ingestion fails
        """
        # TODO: Implement document ingestion pipeline
        # Hints:
        # 1. Validate input path
        # 2. Process documents (load and chunk)
        # 3. Generate embeddings for all chunks
        # 4. Add documents and embeddings to retriever
        # 5. Return statistics (num docs, num chunks, etc.)
        # 6. Handle errors at each stage
        
        validate_input(documents_path, "documents_path", str)
        
        try:
            logger.info(f"Starting document ingestion from {documents_path}")
            
            # YOUR CODE HERE
            # Implement the complete ingestion pipeline
            
            # Step 1: Process documents
            # Step 2: Generate embeddings
            # Step 3: Index in vector database
            
            stats = {
                "documents_processed": 0,  # REPLACE
                "chunks_created": 0,  # REPLACE
                "embeddings_generated": 0,  # REPLACE
                "ingestion_successful": False  # REPLACE
            }
            
            logger.info(f"Ingestion complete: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error during ingestion: {e}")
            raise RuntimeError(f"Document ingestion failed: {e}")
    
    @measure_time
    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        include_sources: bool = True
    ) -> Dict[str, Any]:
        """
        Query the RAG system with a question.
        
        This method:
        1. Generates query embedding
        2. Retrieves relevant documents
        3. Generates answer using LLM
        
        Args:
            question: User question
            top_k: Number of documents to retrieve (uses default if None)
            include_sources: Whether to include source citations
            
        Returns:
            Dictionary with answer, sources, and metadata
            
        Raises:
            ValueError: If question is empty
            RuntimeError: If query processing fails
        """
        # TODO: Implement query processing pipeline
        # Hints:
        # 1. Validate input question
        # 2. Generate query embedding
        # 3. Retrieve relevant documents
        # 4. Generate answer using retrieved context
        # 5. Format and return response
        # 6. Handle errors (no results, API failures, etc.)
        
        validate_input(question, "question", str)
        
        if top_k is None:
            top_k = self.top_k
        
        try:
            logger.info(f"Processing query: {question[:50]}...")
            
            # YOUR CODE HERE
            # Implement the complete query pipeline
            
            # Step 1: Generate query embedding
            # Step 2: Retrieve relevant documents
            # Step 3: Generate answer
            
            response = {
                "question": question,
                "answer": "",  # REPLACE
                "sources": [],  # REPLACE
                "num_sources_retrieved": 0,  # REPLACE
                "query_successful": False  # REPLACE
            }
            
            logger.info("Query processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise RuntimeError(f"Query processing failed: {e}")
    
    def batch_query(
        self,
        questions: List[str],
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Process multiple queries in batch.
        
        Args:
            questions: List of questions to process
            top_k: Number of documents to retrieve per query
            
        Returns:
            List of response dictionaries
        """
        validate_input(questions, "questions", list)
        
        logger.info(f"Processing batch of {len(questions)} queries")
        
        responses = []
        for i, question in enumerate(questions, 1):
            try:
                logger.info(f"Processing query {i}/{len(questions)}")
                response = self.query(question, top_k=top_k)
                responses.append(response)
            except Exception as e:
                logger.error(f"Error processing query {i}: {e}")
                responses.append({
                    "question": question,
                    "answer": f"Error: {str(e)}",
                    "error": True
                })
        
        return responses
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the RAG system.
        
        Returns:
            Dictionary with system statistics
        """
        # TODO: Implement system statistics collection
        # Hints:
        # 1. Get stats from retriever (index size, etc.)
        # 2. Get stats from document processor
        # 3. Get embedding model info
        # 4. Combine into comprehensive stats dict
        
        stats = {
            "retriever_stats": {},  # REPLACE
            "embedding_model": "",  # REPLACE
            "embedding_dimension": 0,  # REPLACE
            "top_k": self.top_k
        }
        
        return stats
    
    def clear_index(self) -> None:
        """
        Clear all documents from the system.
        """
        try:
            self.retriever.clear_index()
            logger.info("System index cleared")
        except Exception as e:
            logger.error(f"Error clearing index: {e}")
            raise


def main():
    """
    Example usage of RAG Agent.
    """
    # Initialize agent
    agent = RAGAgent()
    
    # Ingest documents
    print("Ingesting documents...")
    stats = agent.ingest("../test-data/")
    print(f"Ingestion stats: {stats}")
    
    # Query the system
    print("\nQuerying system...")
    questions = [
        "What are transformers and how do they work?",
        "What are the key components of RAG systems?",
        "How do I evaluate RAG system performance?"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        response = agent.query(question)
        print(f"A: {response['answer']}")
        print(f"Sources: {len(response['sources'])}")


if __name__ == "__main__":
    main()
