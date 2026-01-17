"""
Document processing module for RAG agent.

This module handles document loading, chunking, and preprocessing
for the RAG pipeline.
"""

import os
from typing import List, Dict, Any
from pathlib import Path
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from utils import validate_input, measure_time

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Processes documents for RAG pipeline.
    
    Handles loading documents from files, splitting them into chunks,
    and maintaining metadata for retrieval.
    """
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
        separators: List[str] = None
    ):
        """
        Initialize document processor.
        
        Args:
            chunk_size: Target size for each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
            separators: List of separators for splitting (default: paragraph, sentence)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Default separators: paragraph, sentence, word
        if separators is None:
            separators = ["\n\n", "\n", ". ", " ", ""]
        
        # TODO: Initialize RecursiveCharacterTextSplitter with the parameters
        # Hint: Use langchain's RecursiveCharacterTextSplitter
        self.text_splitter = None  # REPLACE THIS LINE
        
        logger.info(
            f"DocumentProcessor initialized with chunk_size={chunk_size}, "
            f"chunk_overlap={chunk_overlap}"
        )
    
    @measure_time
    def load_documents(self, directory_path: str) -> List[Document]:
        """
        Load all text documents from a directory.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of Document objects with content and metadata
            
        Raises:
            ValueError: If directory doesn't exist or is empty
            IOError: If file reading fails
        """
        # TODO: Implement document loading
        # Hints:
        # 1. Validate that directory exists
        # 2. Find all .txt files in directory
        # 3. Read each file and create Document objects
        # 4. Include metadata: filename, source path
        # 5. Handle file reading errors gracefully
        
        validate_input(directory_path, "directory_path", str)
        
        # Check if directory exists
        dir_path = Path(directory_path)
        if not dir_path.exists():
            raise ValueError(f"Directory does not exist: {directory_path}")
        
        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        documents = []
        
        # YOUR CODE HERE
        # Load all .txt files from directory
        # Create Document objects with metadata
        
        if len(documents) == 0:
            raise ValueError(f"No documents found in directory: {directory_path}")
        
        logger.info(f"Loaded {len(documents)} documents from {directory_path}")
        return documents
    
    @measure_time
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for embedding.
        
        Args:
            documents: List of Document objects to chunk
            
        Returns:
            List of chunked Document objects with updated metadata
            
        Raises:
            ValueError: If documents list is empty
        """
        # TODO: Implement document chunking
        # Hints:
        # 1. Validate input documents
        # 2. Use self.text_splitter to split documents
        # 3. Add chunk_id to metadata for each chunk
        # 4. Preserve original document metadata
        
        validate_input(documents, "documents", list)
        
        if len(documents) == 0:
            raise ValueError("Documents list cannot be empty")
        
        # YOUR CODE HERE
        # Split documents into chunks
        # Add chunk metadata (chunk_id, original_doc_id, etc.)
        
        chunks = []  # REPLACE THIS LINE
        
        logger.info(
            f"Split {len(documents)} documents into {len(chunks)} chunks "
            f"(avg {len(chunks)/len(documents):.1f} chunks per document)"
        )
        
        return chunks
    
    @measure_time
    def process_documents(self, directory_path: str) -> List[Document]:
        """
        Complete document processing pipeline: load and chunk.
        
        Args:
            directory_path: Path to directory containing documents
            
        Returns:
            List of chunked Document objects ready for embedding
            
        Raises:
            ValueError: If directory is invalid or empty
            IOError: If file operations fail
        """
        try:
            # Load documents
            documents = self.load_documents(directory_path)
            
            # Chunk documents
            chunks = self.chunk_documents(documents)
            
            logger.info(f"Document processing complete: {len(chunks)} chunks ready")
            return chunks
            
        except Exception as e:
            logger.error(f"Error in document processing: {e}")
            raise
    
    def get_chunk_statistics(self, chunks: List[Document]) -> Dict[str, Any]:
        """
        Calculate statistics about document chunks.
        
        Args:
            chunks: List of chunked documents
            
        Returns:
            Dictionary with statistics (count, avg_length, etc.)
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "avg_chunk_length": 0,
                "min_chunk_length": 0,
                "max_chunk_length": 0
            }
        
        chunk_lengths = [len(chunk.page_content) for chunk in chunks]
        
        return {
            "total_chunks": len(chunks),
            "avg_chunk_length": sum(chunk_lengths) / len(chunk_lengths),
            "min_chunk_length": min(chunk_lengths),
            "max_chunk_length": max(chunk_lengths),
            "unique_sources": len(set(chunk.metadata.get("source", "") for chunk in chunks))
        }
