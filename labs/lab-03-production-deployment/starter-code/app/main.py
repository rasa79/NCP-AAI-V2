"""
FastAPI application for production RAG agent deployment.

This module implements the REST API endpoints for the RAG agent service,
including health checks, query processing, and metrics exposure.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import time
import logging

from .rag_service import RAGService
from .monitoring import setup_logging, setup_metrics, track_request
from .config import get_settings

# Initialize settings and logging
settings = get_settings()
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="Production RAG agent service with NVIDIA NIM integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service: Optional[RAGService] = None


# Request/Response Models
class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    question: str = Field(..., min_length=1, max_length=1000, description="Question to ask")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of documents to retrieve")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are the key components of RAG systems?",
                "top_k": 3
            }
        }


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    answer: str = Field(..., description="Generated answer")
    sources: List[dict] = Field(default_factory=list, description="Source documents")
    latency_ms: float = Field(..., description="Query latency in milliseconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "RAG systems consist of...",
                "sources": [{"doc_id": "1", "score": 0.95}],
                "latency_ms": 1234.5
            }
        }


class IngestRequest(BaseModel):
    """Request model for document ingestion."""
    documents: List[str] = Field(..., min_items=1, description="Documents to ingest")
    
    class Config:
        json_schema_extra = {
            "example": {
                "documents": ["Document 1 content...", "Document 2 content..."]
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
    timestamp: float = Field(..., description="Current timestamp")


# Startup and Shutdown Events
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global rag_service
    
    logger.info("Starting RAG agent service...")
    
    # TODO: Initialize RAG service
    # Hints:
    # - Create RAGService instance with NIM endpoint from settings
    # - Load vector database if it exists
    # - Initialize monitoring
    # - Log successful startup
    
    try:
        # YOUR CODE HERE
        rag_service = RAGService(
            nim_endpoint=settings.nim_endpoint,
            vector_db_path=settings.vector_db_path
        )
        logger.info("RAG service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down RAG agent service...")
    
    # TODO: Cleanup resources
    # Hints:
    # - Close database connections
    # - Save any pending data
    # - Log shutdown
    
    # YOUR CODE HERE
    pass


# Health Check Endpoints
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint for liveness probe.
    
    Returns basic service status without checking dependencies.
    """
    # TODO: Implement health check
    # Hints:
    # - Return service status, version, and timestamp
    # - This should always return 200 if service is running
    # - Don't check external dependencies here
    
    # YOUR CODE HERE
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=time.time()
    )


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check endpoint for readiness probe.
    
    Checks if service is ready to handle requests by verifying dependencies.
    """
    # TODO: Implement readiness check
    # Hints:
    # - Check if RAG service is initialized
    # - Check if vector database is accessible
    # - Check if NIM endpoint is reachable
    # - Return 200 if ready, 503 if not ready
    
    # YOUR CODE HERE
    if rag_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    # Check dependencies
    try:
        # Add checks for vector DB, NIM, etc.
        pass
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service not ready: {e}")
    
    return {"status": "ready"}


# Main API Endpoints
@app.post("/query", response_model=QueryResponse, tags=["RAG"])
@track_request("query")
async def query(request: QueryRequest):
    """
    Query the RAG agent with a question.
    
    Args:
        request: Query request containing question and parameters
        
    Returns:
        QueryResponse with answer, sources, and latency
    """
    start_time = time.time()
    
    # TODO: Implement query endpoint
    # Hints:
    # - Validate RAG service is initialized
    # - Call rag_service.query() with question and top_k
    # - Handle errors gracefully
    # - Calculate latency
    # - Log request and response
    # - Return structured response
    
    try:
        # YOUR CODE HERE
        if rag_service is None:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        logger.info(f"Processing query: {request.question[:50]}...")
        
        # Call RAG service
        result = await rag_service.query(
            question=request.question,
            top_k=request.top_k
        )
        
        latency_ms = (time.time() - start_time) * 1000
        
        logger.info(f"Query completed in {latency_ms:.2f}ms")
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            latency_ms=latency_ms
        )
        
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest", tags=["RAG"])
@track_request("ingest")
async def ingest(request: IngestRequest):
    """
    Ingest documents into the vector database.
    
    Args:
        request: Ingest request containing documents
        
    Returns:
        Status message with number of documents ingested
    """
    # TODO: Implement ingest endpoint
    # Hints:
    # - Validate RAG service is initialized
    # - Call rag_service.ingest() with documents
    # - Handle errors gracefully
    # - Log ingestion
    # - Return success message
    
    try:
        # YOUR CODE HERE
        if rag_service is None:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        logger.info(f"Ingesting {len(request.documents)} documents...")
        
        # Call RAG service
        result = await rag_service.ingest(request.documents)
        
        logger.info(f"Ingested {result['count']} documents successfully")
        
        return {
            "status": "success",
            "documents_ingested": result["count"]
        }
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Metrics Endpoint
@app.get("/metrics", response_class=PlainTextResponse, tags=["Monitoring"])
async def metrics():
    """
    Prometheus metrics endpoint.
    
    Returns metrics in Prometheus text format.
    """
    # TODO: Implement metrics endpoint
    # Hints:
    # - Import prometheus_client
    # - Use generate_latest() to get metrics
    # - Return as plain text
    
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    
    # YOUR CODE HERE
    return PlainTextResponse(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


# Error Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
