"""
Vector retrieval module for RAG agent.

This module handles vector database operations including indexing,
searching, and retrieving relevant documents.
"""

import logging
from typing import List, Tuple, Dict, Any
import numpy as np
import faiss
from langchain.docstore.document import Document

from utils import validate_input, measure_time

logger = logging.getLogger(__name__)


class VectorRetriever:
    """
    Vector database retriever using FAISS.
    
    Handles document indexing, similarity search, and retrieval
    with metadata management.
    """
    
    def __init__(self, embedding_dimension: int = 384):
        """
        Initialize vector retriever.
        
        Args:
            embedding_dimension: Dimension of embedding vectors
        """
        self.embedding_dimension = embedding_dimension
        
        # TODO: Initialize FAISS index
        # Hints:
        # 1. Use faiss.IndexFlatL2 for exact L2 distance search
        # 2. Initialize empty index with embedding_dimension
        
        self.index = None  # REPLACE THIS LINE
        
        # Store document metadata (FAISS only stores vectors)
        self.documents: List[Document] = []
        self.document_embeddings: List[np.ndarray] = []
        
        logger.info(f"VectorRetriever initialized with dimension={embedding_dimension}")
    
    @measure_time
    def add_documents(
        self,
        documents: List[Document],
        embeddings: np.ndarray
    ) -> None:
        """
        Add documents and their embeddings to the index.
        
        Args:
            documents: List of Document objects with content and metadata
            embeddings: Numpy array of embeddings (shape: [n_docs, embedding_dim])
            
        Raises:
            ValueError: If documents and embeddings don't match in length
            ValueError: If embedding dimension doesn't match index
        """
        # TODO: Implement document indexing
        # Hints:
        # 1. Validate inputs (length match, dimension match)
        # 2. Add embeddings to FAISS index using index.add()
        # 3. Store documents and embeddings for metadata retrieval
        # 4. Handle errors gracefully
        
        validate_input(documents, "documents", list)
        validate_input(embeddings, "embeddings", np.ndarray)
        
        # YOUR CODE HERE
        # Validate and add documents to index
        
        logger.info(f"Added {len(documents)} documents to index")
        logger.info(f"Total documents in index: {self.index.ntotal}")
    
    @measure_time
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        score_threshold: float = None
    ) -> List[Tuple[Document, float]]:
        """
        Search for most similar documents to query.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            score_threshold: Optional minimum similarity score (filters results)
            
        Returns:
            List of (Document, similarity_score) tuples, sorted by relevance
            
        Raises:
            ValueError: If index is empty
            ValueError: If k is invalid
        """
        # TODO: Implement vector search
        # Hints:
        # 1. Validate inputs (index not empty, k > 0)
        # 2. Reshape query_embedding for FAISS (needs 2D array)
        # 3. Use index.search() to get distances and indices
        # 4. Convert L2 distances to similarity scores
        # 5. Filter by score_threshold if provided
        # 6. Return documents with scores
        
        if self.index.ntotal == 0:
            raise ValueError("Index is empty. Add documents before searching.")
        
        if k <= 0:
            raise ValueError(f"k must be positive, got {k}")
        
        # Limit k to available documents
        k = min(k, self.index.ntotal)
        
        try:
            # YOUR CODE HERE
            # Perform FAISS search and return results
            
            results = []  # REPLACE THIS LINE
            
            logger.info(f"Search returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Error during search: {e}")
            raise
    
    def _l2_distance_to_similarity(self, distance: float) -> float:
        """
        Convert L2 distance to similarity score.
        
        FAISS IndexFlatL2 returns L2 distances (lower = more similar).
        Convert to similarity score (higher = more similar) for consistency.
        
        Args:
            distance: L2 distance from FAISS
            
        Returns:
            Similarity score (0 to 1, higher = more similar)
        """
        # TODO: Implement distance to similarity conversion
        # Hints:
        # 1. L2 distance ranges from 0 (identical) to infinity
        # 2. Convert to similarity: 1 / (1 + distance)
        # 3. This gives scores from 0 to 1, with 1 being most similar
        
        return 0.0  # REPLACE THIS LINE
    
    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector index.
        
        Returns:
            Dictionary with index statistics
        """
        return {
            "total_documents": self.index.ntotal if self.index else 0,
            "embedding_dimension": self.embedding_dimension,
            "index_type": type(self.index).__name__ if self.index else None,
            "documents_stored": len(self.documents)
        }
    
    def clear_index(self) -> None:
        """
        Clear all documents from the index.
        """
        # TODO: Implement index clearing
        # Hints:
        # 1. Reset FAISS index
        # 2. Clear document and embedding lists
        
        # YOUR CODE HERE
        
        logger.info("Index cleared")
    
    def save_index(self, filepath: str) -> None:
        """
        Save FAISS index to disk.
        
        Args:
            filepath: Path to save index file
        """
        try:
            faiss.write_index(self.index, filepath)
            logger.info(f"Index saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            raise
    
    def load_index(self, filepath: str) -> None:
        """
        Load FAISS index from disk.
        
        Args:
            filepath: Path to index file
            
        Note: This only loads the index, not the document metadata.
              You'll need to separately manage document storage.
        """
        try:
            self.index = faiss.read_index(filepath)
            logger.info(f"Index loaded from {filepath}")
            logger.info(f"Loaded {self.index.ntotal} vectors")
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            raise
