"""
Monitoring and observability utilities.

This module implements Prometheus metrics collection and structured logging
for production observability.
"""

import logging
import time
import json
from functools import wraps
from typing import Callable
from prometheus_client import Counter, Histogram, Gauge, Info
from pythonjsonlogger import jsonlogger


# Prometheus Metrics
# TODO: Define Prometheus metrics
# Hints:
# - Counter for request counts
# - Histogram for latencies
# - Gauge for active connections
# - Counter for errors

# Request metrics
REQUEST_COUNT = Counter(
    'rag_requests_total',
    'Total number of requests',
    ['endpoint', 'method', 'status']
)

REQUEST_LATENCY = Histogram(
    'rag_request_duration_seconds',
    'Request latency in seconds',
    ['endpoint', 'method']
)

# NIM metrics
NIM_LATENCY = Histogram(
    'nim_request_duration_seconds',
    'NIM request latency in seconds',
    ['operation']
)

NIM_ERRORS = Counter(
    'nim_errors_total',
    'Total number of NIM errors',
    ['error_type']
)

# Vector DB metrics
VECTOR_DB_LATENCY = Histogram(
    'vector_db_query_duration_seconds',
    'Vector DB query latency in seconds',
    ['operation']
)

# Active connections
ACTIVE_CONNECTIONS = Gauge(
    'rag_active_connections',
    'Number of active connections'
)

# Service info
SERVICE_INFO = Info('rag_service', 'RAG service information')


def setup_logging():
    """
    Configure structured JSON logging.
    
    Sets up logging with JSON formatter for better log aggregation
    and analysis in production environments.
    """
    # TODO: Configure logging
    # Hints:
    # - Use JSON formatter
    # - Set appropriate log level
    # - Configure handlers
    # - Add correlation ID support
    
    # YOUR CODE HERE
    logger = logging.getLogger()
    
    # Create JSON formatter
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    
    # Configure handler
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    logging.info("Structured logging configured")


def setup_metrics():
    """
    Initialize Prometheus metrics.
    
    Sets up service information and initial metric values.
    """
    # TODO: Initialize metrics
    # Hints:
    # - Set service info
    # - Initialize gauges
    # - Log metrics setup
    
    # YOUR CODE HERE
    SERVICE_INFO.info({
        'version': '1.0.0',
        'service': 'rag-agent'
    })
    
    ACTIVE_CONNECTIONS.set(0)
    
    logging.info("Prometheus metrics initialized")


def track_request(endpoint: str) -> Callable:
    """
    Decorator to track request metrics.
    
    Args:
        endpoint: Endpoint name for labeling
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # TODO: Implement request tracking
            # Hints:
            # - Increment active connections
            # - Track request latency
            # - Count requests by status
            # - Decrement active connections
            # - Handle errors
            
            # YOUR CODE HERE
            ACTIVE_CONNECTIONS.inc()
            start_time = time.time()
            status = "success"
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                raise
            finally:
                # Record metrics
                duration = time.time() - start_time
                REQUEST_LATENCY.labels(
                    endpoint=endpoint,
                    method="POST"
                ).observe(duration)
                
                REQUEST_COUNT.labels(
                    endpoint=endpoint,
                    method="POST",
                    status=status
                ).inc()
                
                ACTIVE_CONNECTIONS.dec()
        
        return wrapper
    return decorator


def track_nim_call(operation: str) -> Callable:
    """
    Decorator to track NIM API call metrics.
    
    Args:
        operation: Operation name for labeling
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # TODO: Implement NIM call tracking
            # Hints:
            # - Track NIM latency
            # - Count NIM errors by type
            # - Log NIM interactions
            
            # YOUR CODE HERE
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                NIM_ERRORS.labels(error_type=type(e).__name__).inc()
                raise
            finally:
                duration = time.time() - start_time
                NIM_LATENCY.labels(operation=operation).observe(duration)
        
        return wrapper
    return decorator


def track_vector_db_query(operation: str) -> Callable:
    """
    Decorator to track vector database query metrics.
    
    Args:
        operation: Operation name for labeling
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # TODO: Implement vector DB query tracking
            # Hints:
            # - Track query latency
            # - Log query details
            
            # YOUR CODE HERE
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                VECTOR_DB_LATENCY.labels(operation=operation).observe(duration)
        
        return wrapper
    return decorator


class StructuredLogger:
    """
    Structured logger with correlation ID support.
    
    Provides consistent structured logging with request correlation.
    """
    
    def __init__(self, name: str):
        """
        Initialize structured logger.
        
        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self.correlation_id = None
    
    def set_correlation_id(self, correlation_id: str):
        """Set correlation ID for request tracking."""
        self.correlation_id = correlation_id
    
    def _log(self, level: str, message: str, **kwargs):
        """
        Log message with structured data.
        
        Args:
            level: Log level
            message: Log message
            **kwargs: Additional structured data
        """
        # TODO: Implement structured logging
        # Hints:
        # - Add correlation ID
        # - Add timestamp
        # - Add structured fields
        # - Use appropriate log level
        
        # YOUR CODE HERE
        extra = {
            'correlation_id': self.correlation_id,
            **kwargs
        }
        
        log_func = getattr(self.logger, level.lower())
        log_func(message, extra=extra)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log('INFO', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log('ERROR', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log('WARNING', message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log('DEBUG', message, **kwargs)
