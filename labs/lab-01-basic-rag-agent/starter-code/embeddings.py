"""
Embedding generation module for RAG agent.

This module handles text embedding generation using sentence-transformers
for semantic search and retrieval.
"""

import logging
from typing import List, Union
import numpy as np

from sentence_transformers import SentenceTransformer

from utils import validate_input, measure_time, retry_with_backoff

logger = logging.getLogger(__name__)


class EmbeddingModel:
    """
    Wrapper for sentence-transformers embedding model.
    
    Provides text encoding functionality with error handling and
    batch processing support.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model.
        
        Args:
            model_name: Name of sentence-transformers model to use
                       Default: all-MiniLM-L6-v2 (fast, good quality, 384 dimensions)
        """
        # TODO: Initialize the sentence-transformers model
        # Hints:
        # 1. Load the model using SentenceTransformer
        # 2. Handle model loading errors
        # 3. Log model information (name, dimensions)
        
        self.model_name = model_name
        self.model = None  # REPLACE THIS LINE
        
        try:
            # YOUR CODE HERE
            # Load the sentence-transformers model
            
            logger.info(f"Loaded embedding model: {model_name}")
            logger.info(f"Embedding dimension: {self.get_embedding_dimension()}")
            
        except Exception as e:
            logger.error(f"Failed to load embedding model {model_name}: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this model.
        
        Returns:
            Embedding dimension size
        """
        # TODO: Return the embedding dimension
        # Hint: Use model.get_sentence_embedding_dimension()
        return 384  # REPLACE THIS LINE
    
    @measure_time
    @retry_with_backoff(max_retries=3)
    def encode(
        self,
        texts: Union[str, List[str]],
        batch_size: int = 32,
        show_progress: bool = False
    ) -> np.ndarray:
        """
        Encode text(s) into embeddings.
        
        Args:
            texts: Single text string or list of text strings
            batch_size: Batch size for encoding (larger = faster but more memory)
            show_progress: Whether to show progress bar
            
        Returns:
            Numpy array of embeddings (shape: [n_texts, embedding_dim])
            
        Raises:
            ValueError: If texts is empty
            RuntimeError: If encoding fails
        """
        # TODO: Implement text encoding
        # Hints:
        # 1. Validate input (handle both string and list)
        # 2. Convert single string to list if needed
        # 3. Use model.encode() with batch_size parameter
        # 4. Handle encoding errors
        # 5. Return numpy array of embeddings
        
        # Handle single string input
        if isinstance(texts, str):
            texts = [texts]
        
        validate_input(texts, "texts", list)
        
        if len(texts) == 0:
            raise ValueError("Cannot encode empty text list")
        
        try:
            # YOUR CODE HERE
            # Encode texts using the model
            
            embeddings = None  # REPLACE THIS LINE
            
            logger.info(f"Encoded {len(texts)} texts into embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error encoding texts: {e}")
            raise RuntimeError(f"Failed to encode texts: {e}")
    
    def encode_query(self, query: str) -> np.ndarray:
        """
        Encode a single query string.
        
        Convenience method for encoding queries with appropriate settings.
        
        Args:
            query: Query text to encode
            
        Returns:
            Numpy array of query embedding (shape: [embedding_dim])
        """
        validate_input(query, "query", str)
        
        # Encode and return first (and only) embedding
        embeddings = self.encode(query, batch_size=1)
        return embeddings[0]
    
    def encode_documents(
        self,
        documents: List[str],
        batch_size: int = 32,
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Encode a list of documents with progress tracking.
        
        Args:
            documents: List of document texts to encode
            batch_size: Batch size for encoding
            show_progress: Whether to show progress bar
            
        Returns:
            Numpy array of document embeddings
        """
        validate_input(documents, "documents", list)
        
        logger.info(f"Encoding {len(documents)} documents...")
        
        return self.encode(
            documents,
            batch_size=batch_size,
            show_progress=show_progress
        )
    
    def compute_similarity(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray
    ) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0 to 1, higher = more similar)
        """
        # TODO: Implement cosine similarity calculation
        # Hints:
        # 1. Normalize embeddings
        # 2. Compute dot product
        # 3. Handle edge cases (zero vectors)
        
        try:
            # YOUR CODE HERE
            # Calculate cosine similarity
            
            similarity = 0.0  # REPLACE THIS LINE
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0
