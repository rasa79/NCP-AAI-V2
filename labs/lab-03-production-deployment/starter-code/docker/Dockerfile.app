# Multi-stage Dockerfile for RAG Agent Application

# Stage 1: Builder
# TODO: Create builder stage
# Hints:
# - Use Python 3.10-slim as base
# - Install build dependencies
# - Copy requirements.txt
# - Install Python dependencies
# - Create virtual environment (optional)

FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt


# Stage 2: Runtime
# TODO: Create runtime stage
# Hints:
# - Use Python 3.10-slim as base
# - Copy installed packages from builder
# - Copy application code
# - Create non-root user
# - Set appropriate permissions
# - Expose port 8000
# - Set health check
# - Define entrypoint

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY starter-code/app ./app

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
