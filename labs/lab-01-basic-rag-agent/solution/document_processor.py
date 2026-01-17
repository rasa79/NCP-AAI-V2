"""
Document processing module for RAG agent - REFERENCE SOLUTION

This is a complete, working implementation demonstrating best practices.
"""

import os
from typing import List, Dict, Any
from pathlib import Path
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Import from starter code utils
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "starter-code"))
from utils import validate_input, measure_time

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processes documents for RAG pipeline."""
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
        separators: List[str] = None
    ):
        """Initialize document processor."""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if separators is None:
            separators = ["\n\n", "\n", ". ", " ", ""]
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            length_function=len
        )
        
        logger.info(
            f"DocumentProcessor initialized with chunk_size={chunk_size}, "
            f"chunk_overlap={chunk_overlap}"
        )
    
    @measure_time
    def load_documents(self, directory_path: str) -> List[Document]:
        """Load all text documents from a directory."""
        validate_input(directory_path, "directory_path", str)
        
        dir_path = Path(directory_path)
        if not dir_path.exists():
            raise ValueError(f"Directory does not exist: {directory_path}")
        
        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        documents = []
        
        # Find all .txt files
        txt_files = list(dir_path.glob("*.txt"))
        
        if not txt_files:
            raise ValueError(f"No .txt files found in directory: {directory_path}")
        
        # Load each file
        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Create Document with metadata
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": file_path.name,
                        "full_path": str(file_path),
                        "file_size": len(content)
                    }
                )
                documents.append(doc)
                
                logger.debug(f"Loaded document: {file_path.name} ({len(content)} chars)")
                
            except Exception as e:
                logger.error(f"Error loading file {file_path}: {e}")
                # Continue with other files
                continue
        
        if len(documents) == 0:
            raise ValueError(f"Failed to load any documents from {directory_path}")
        
        logger.info(f"Loaded {len(documents)} documents from {directory_path}")
        return documents
    
    @measure_time
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks for embedding."""
        validate_input(documents, "documents", list)
        
        if len(documents) == 0:
            raise ValueError("Documents list cannot be empty")
        
        all_chunks = []
        
        for doc_idx, doc in enumerate(documents):
            # Split document into chunks
            chunks = self.text_splitter.split_documents([doc])
            
            # Add chunk metadata
            for chunk_idx, chunk in enumerate(chunks):
                # Preserve original metadata and add chunk info
                chunk.metadata.update({
                    "chunk_id": chunk_idx,
                    "doc_id": doc_idx,
                    "total_chunks": len(chunks)
                })
                all_chunks.append(chunk)
        
        logger.info(
            f"Split {len(documents)} documents into {len(all_chunks)} chunks "
            f"(avg {len(all_chunks)/len(documents):.1f} chunks per document)"
        )
        
        return all_chunks
    
    @measure_time
    def process_documents(self, directory_path: str) -> List[Document]:
        """Complete document processing pipeline: load and chunk."""
        try:
            documents = self.load_documents(directory_path)
            chunks = self.chunk_documents(documents)
            
            logger.info(f"Document processing complete: {len(chunks)} chunks ready")
            return chunks
            
        except Exception as e:
            logger.error(f"Error in document processing: {e}")
            raise
    
    def get_chunk_statistics(self, chunks: List[Document]) -> Dict[str, Any]:
        """Calculate statistics about document chunks."""
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
