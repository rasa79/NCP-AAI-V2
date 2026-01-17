"""
Configuration management for RAG service.

This module handles environment-based configuration using pydantic-settings.
"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables with
    the same name (case-insensitive).
    """
    
    # Service Configuration
    service_name: str = "rag-agent"
    version: str = "1.0.0"
    debug: bool = False
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["*"]
    
    # NVIDIA NIM Configuration
    nim_endpoint: str = "http://nim:8000"
    nim_timeout: int = 30
    nim_max_retries: int = 3
    
    # Vector Database Configuration
    vector_db_path: str = "/data/vector_db"
    vector_db_type: str = "faiss"  # faiss, milvus, chroma
    
    # Embedding Model Configuration
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # RAG Configuration
    chunk_size: int = 500
    chunk_overlap: int = 100
    top_k: int = 3
    similarity_threshold: float = 0.7
    
    # Performance Configuration
    max_concurrent_requests: int = 100
    request_timeout: int = 30
    
    # Circuit Breaker Configuration
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60
    
    # Monitoring Configuration
    metrics_enabled: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings instance
    """
    return Settings()
