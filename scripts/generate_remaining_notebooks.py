#!/usr/bin/env python3
"""
Script to generate remaining notebooks for Modules 7-10.
This ensures consistent structure and comprehensive content.
"""

import json
import os
from pathlib import Path

# Notebook templates for each module
NOTEBOOK_TEMPLATES = {
    "module-07": [
        {
            "filename": "01-monitoring-dashboards.ipynb",
            "title": "Monitoring Dashboards and Metrics Tracking",
            "objectives": ["Implement monitoring dashboards", "Track key performance metrics", "Set up alerts and notifications", "Visualize agent performance"],
            "exam_objectives": "7.1, 7.2, 7.3",
            "time": "60-75 minutes",
            "theory": """### Monitoring in Production

**Key Metrics to Track**:
- **Latency**: Response time (P50, P95, P99)
- **Throughput**: Requests per second
- **Error Rate**: Failed requests percentage
- **Resource Usage**: CPU, GPU, memory utilization
- **Cost**: Inference cost per request

**Monitoring Stack**:
- Prometheus: Metrics collection
- Grafana: Visualization dashboards
- AlertManager: Alert routing
- LangSmith: LLM-specific observability""",
            "implementation": """# Function to collect and export metrics
def collect_agent_metrics(agent_id: str) -> Dict[str, float]:
    \"\"\"
    Collect performance metrics for an agent.
    
    Args:
        agent_id: Unique identifier for the agent
    
    Returns:
        Dictionary of metric names to values
    \"\"\"\n    metrics = {
        \"requests_total\": 0,
        \"requests_failed\": 0,
        \"latency_p50_ms\": 0.0,
        \"latency_p95_ms\": 0.0,
        \"latency_p99_ms\": 0.0,
        \"tokens_generated\": 0,
        \"cost_usd\": 0.0
    }
    
    try:
        # Collect metrics from monitoring system
        # This is a placeholder - actual implementation depends on monitoring stack
        print(f\"Collecting metrics for agent: {agent_id}\")
        
        # Example: Query Prometheus for metrics
        # metrics = query_prometheus(agent_id)
        
        return metrics
    except Exception as e:
        # Handle errors gracefully
        print(f\"Error collecting metrics: {e}\")
        return metrics"""
        },
        {
            "filename": "02-logging-tracing.ipynb",
            "title": "Logging and Tracing with LangSmith",
            "objectives": ["Implement structured logging", "Set up distributed tracing", "Integrate LangSmith for LLM observability", "Debug agent workflows"],
            "exam_objectives": "7.2, 7.4",
            "time": "60-75 minutes",
            "theory": """### Logging and Tracing

**Structured Logging**:
- Use JSON format for machine-readable logs
- Include context (request_id, user_id, timestamp)
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)

**Distributed Tracing**:
- Track requests across multiple services
- Identify bottlenecks in agent workflows
- Measure end-to-end latency

**LangSmith Integration**:
- Automatic LLM call tracking
- Prompt and response logging
- Chain visualization
- Performance analytics""",
            "implementation": """# Function to set up structured logging
import logging
import json
from datetime import datetime

def setup_structured_logging(log_file: str = \"agent.log\") -> logging.Logger:
    \"\"\"
    Configure structured logging for agent application.
    
    Args:
        log_file: Path to log file
    
    Returns:
        Configured logger instance
    \"\"\"\n    # Create logger
    logger = logging.getLogger(\"agent_logger\")
    logger.setLevel(logging.INFO)
    
    # Create file handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    
    # Create JSON formatter
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_data = {
                \"timestamp\": datetime.utcnow().isoformat(),
                \"level\": record.levelname,
                \"message\": record.getMessage(),
                \"module\": record.module,
                \"function\": record.funcName
            }
            return json.dumps(log_data)
    
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    
    return logger"""
        },
        {
            "filename": "03-performance-profiling.ipynb",
            "title": "Performance Profiling and Bottleneck Analysis",
            "objectives": ["Profile agent performance", "Identify bottlenecks", "Optimize critical paths", "Measure optimization impact"],
            "exam_objectives": "7.3, 7.5",
            "time": "60-75 minutes",
            "theory": """### Performance Profiling

**Profiling Techniques**:
- **Time Profiling**: Measure function execution time
- **Memory Profiling**: Track memory allocation
- **GPU Profiling**: Monitor GPU utilization
- **I/O Profiling**: Identify slow I/O operations

**Common Bottlenecks**:
- Slow LLM inference
- Inefficient retrieval
- Network latency
- Memory constraints
- Suboptimal batching""",
            "implementation": """# Function to profile agent performance
import time
from functools import wraps

def profile_function(func):
    \"\"\"
    Decorator to profile function execution time.
    
    Args:
        func: Function to profile
    
    Returns:
        Wrapped function with profiling
    \"\"\"\n    @wraps(func)
    def wrapper(*args, **kwargs):
        # Measure execution time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Log profiling data
        execution_time = end_time - start_time
        print(f\"Function '{func.__name__}' took {execution_time:.3f}s\")
        
        return result
    
    return wrapper

# Example usage
@profile_function
def slow_retrieval(query: str) -> List[str]:
    \"\"\"Simulate slow retrieval operation.\"\"\"\n    time.sleep(0.5)  # Simulate slow operation
    return [\"doc1\", \"doc2\", \"doc3\"]"""
        }
    ],
    "module-08": [
        {
            "filename": "01-containerization.ipynb",
            "title": "Containerization with Docker",
            "objectives": ["Containerize agent applications", "Create optimized Docker images", "Manage dependencies", "Deploy containers"],
            "exam_objectives": "8.1, 8.2",
            "time": "60-75 minutes",
            "theory": """### Containerization Benefits

**Why Docker?**:
- Consistent environments across dev/prod
- Isolated dependencies
- Easy deployment and scaling
- Version control for infrastructure

**Best Practices**:
- Use multi-stage builds
- Minimize image size
- Cache dependencies
- Use .dockerignore
- Run as non-root user""",
            "implementation": """# Example Dockerfile for agent application
dockerfile_content = '''
# Multi-stage build for optimized image
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.10-slim

# Create non-root user
RUN useradd -m -u 1000 agent

# Copy dependencies from builder
COPY --from=builder /root/.local /home/agent/.local

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=agent:agent . .

# Switch to non-root user
USER agent

# Set environment variables
ENV PATH=/home/agent/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run application
CMD [\"python\", \"agent_server.py\"]
'''

print(\"Dockerfile for Agent Application:\")
print(dockerfile_content)"""
        },
        {
            "filename": "02-kubernetes-deployment.ipynb",
            "title": "Kubernetes Deployment and Scaling",
            "objectives": ["Deploy agents on Kubernetes", "Configure auto-scaling", "Manage resources", "Implement health checks"],
            "exam_objectives": "8.3, 8.4, 8.5",
            "time": "75-90 minutes",
            "theory": """### Kubernetes for Agent Deployment

**Key Concepts**:
- **Pods**: Smallest deployable units
- **Deployments**: Manage pod replicas
- **Services**: Expose pods to network
- **HPA**: Horizontal Pod Autoscaler
- **ConfigMaps/Secrets**: Configuration management

**Scaling Strategies**:
- Horizontal scaling: Add more pods
- Vertical scaling: Increase pod resources
- Auto-scaling based on metrics (CPU, custom)""",
            "implementation": """# Kubernetes deployment manifest
k8s_deployment = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent
  template:
    metadata:
      labels:
        app: agent
    spec:
      containers:
      - name: agent
        image: agent:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: \"2Gi\"
            cpu: \"1000m\"
            nvidia.com/gpu: \"1\"
          limits:
            memory: \"4Gi\"
            cpu: \"2000m\"
            nvidia.com/gpu: \"1\"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: agent-service
spec:
  selector:
    app: agent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
'''

print(\"Kubernetes Deployment Manifest:\")
print(k8s_deployment)"""
        }
    ],
    "module-09": [
        {
            "filename": "01-guardrails-implementation.ipynb",
            "title": "Implementing Guardrails with NeMo",
            "objectives": ["Configure NeMo Guardrails", "Implement safety controls", "Test guardrail effectiveness", "Monitor blocked content"],
            "exam_objectives": "9.1, 9.2, 9.3",
            "time": "75-90 minutes",
            "theory": """### Safety Guardrails

**Types of Guardrails**:
- **Input Guardrails**: Filter harmful user inputs
- **Output Guardrails**: Filter unsafe model outputs
- **Dialog Guardrails**: Control conversation flow
- **Retrieval Guardrails**: Control information access

**Implementation Strategies**:
- Layered defense (multiple guardrails)
- Fail-safe defaults (block when uncertain)
- Audit logging for compliance
- Regular testing and updates""",
            "implementation": """# Function to implement custom guardrail
def create_safety_guardrail(blocked_topics: List[str]) -> Callable:
    \"\"\"
    Create custom safety guardrail for specific topics.
    
    Args:
        blocked_topics: List of topics to block
    
    Returns:
        Guardrail function
    \"\"\"\n    def guardrail(user_input: str) -> Dict[str, Any]:
        \"\"\"Check if input contains blocked topics.\"\"\"\n        # Convert to lowercase for case-insensitive matching
        input_lower = user_input.lower()
        
        # Check for blocked topics
        for topic in blocked_topics:
            if topic.lower() in input_lower:
                return {
                    \"blocked\": True,
                    \"reason\": f\"Content related to '{topic}' is not allowed\",
                    \"topic\": topic
                }
        
        # Input is safe
        return {\"blocked\": False}
    
    return guardrail

# Example usage
safety_guardrail = create_safety_guardrail([
    \"medical advice\",
    \"legal advice\",
    \"financial advice\"
])

# Test guardrail
test_input = \"Should I invest in cryptocurrency?\"
result = safety_guardrail(test_input)
print(f\"Input: {test_input}\")
print(f\"Blocked: {result['blocked']}\")
if result['blocked']:
    print(f\"Reason: {result['reason']}\")"""
        },
        {
            "filename": "02-bias-detection.ipynb",
            "title": "Bias Detection and Fairness Metrics",
            "objectives": ["Detect bias in agent outputs", "Measure fairness metrics", "Implement bias mitigation", "Monitor for drift"],
            "exam_objectives": "9.4, 9.5",
            "time": "60-75 minutes",
            "theory": """### Bias and Fairness

**Types of Bias**:
- **Selection Bias**: Biased training data
- **Confirmation Bias**: Reinforcing existing beliefs
- **Representation Bias**: Underrepresented groups
- **Measurement Bias**: Biased evaluation metrics

**Fairness Metrics**:
- Demographic parity
- Equal opportunity
- Equalized odds
- Individual fairness

**Mitigation Strategies**:
- Diverse training data
- Bias detection in outputs
- Regular audits
- Human oversight""",
            "implementation": """# Function to detect potential bias in text
def detect_bias(text: str, sensitive_terms: List[str]) -> Dict[str, Any]:
    \"\"\"
    Detect potential bias in generated text.
    
    Args:
        text: Text to analyze
        sensitive_terms: List of potentially biased terms
    
    Returns:
        Bias detection results
    \"\"\"\n    # Convert to lowercase for matching
    text_lower = text.lower()
    
    # Check for sensitive terms
    found_terms = []
    for term in sensitive_terms:
        if term.lower() in text_lower:
            found_terms.append(term)
    
    # Calculate bias score (simple heuristic)
    bias_score = len(found_terms) / max(len(text.split()), 1)
    
    return {
        \"has_bias\": len(found_terms) > 0,
        \"bias_score\": bias_score,
        \"found_terms\": found_terms,
        \"recommendation\": \"Review and revise\" if found_terms else \"OK\"
    }

# Example usage
sensitive_terms = [\"always\", \"never\", \"all\", \"none\", \"everyone\", \"nobody\"]
test_text = \"All engineers are good at math and everyone knows that.\"
result = detect_bias(test_text, sensitive_terms)
print(f\"Text: {test_text}\")
print(f\"Has Bias: {result['has_bias']}\")
print(f\"Bias Score: {result['bias_score']:.3f}\")
print(f\"Found Terms: {result['found_terms']}\")"""
        }
    ],
    "module-10": [
        {
            "filename": "01-ui-development.ipynb",
            "title": "UI Development with Gradio",
            "objectives": ["Build interactive UIs with Gradio", "Design user-friendly interfaces", "Implement feedback collection", "Deploy web applications"],
            "exam_objectives": "10.1, 10.2, 10.3",
            "time": "60-75 minutes",
            "theory": """### User Interface Design

**Gradio Benefits**:
- Rapid prototyping
- No frontend coding required
- Built-in sharing capabilities
- Easy integration with Python

**UI Best Practices**:
- Clear input/output areas
- Helpful examples
- Error messages
- Loading indicators
- Feedback mechanisms""",
            "implementation": """# Function to create Gradio interface for agent
try:
    import gradio as gr
except ImportError:
    print(\"Install Gradio: pip install gradio\")

def create_agent_ui(agent_function: Callable) -> gr.Interface:
    \"\"\"
    Create Gradio interface for agent.
    
    Args:
        agent_function: Function that processes user input
    
    Returns:
        Gradio Interface object
    \"\"\"\n    # Define interface
    interface = gr.Interface(
        fn=agent_function,
        inputs=gr.Textbox(
            lines=3,
            placeholder=\"Ask me anything...\",
            label=\"Your Question\"
        ),
        outputs=gr.Textbox(
            lines=5,
            label=\"Agent Response\"
        ),
        title=\"AI Agent Assistant\",
        description=\"Ask questions and get intelligent responses\",
        examples=[
            [\"What is machine learning?\"],
            [\"Explain neural networks\"],
            [\"How do I deploy an AI model?\"]
        ],
        theme=\"default\",
        allow_flagging=\"manual\",
        flagging_options=[\"Helpful\", \"Not Helpful\", \"Incorrect\"]
    )
    
    return interface

# Example agent function
def simple_agent(user_input: str) -> str:
    \"\"\"Simple agent that echoes input.\"\"\"\n    return f\"You asked: {user_input}\\n\\nThis is a placeholder response.\"

# Create and launch interface
# interface = create_agent_ui(simple_agent)
# interface.launch()
print(\"Gradio interface created. Uncomment to launch.\")"""
        },
        {
            "filename": "02-feedback-loops.ipynb",
            "title": "Feedback Loops and Continuous Improvement",
            "objectives": ["Implement feedback collection", "Analyze user feedback", "Improve agent based on feedback", "Track improvement metrics"],
            "exam_objectives": "10.4, 10.5",
            "time": "60-75 minutes",
            "theory": """### Feedback Loops

**Types of Feedback**:
- **Explicit**: Thumbs up/down, ratings, comments
- **Implicit**: Click-through rates, time spent, task completion
- **Behavioral**: Usage patterns, feature adoption

**Feedback Pipeline**:
1. Collect feedback from users
2. Store in database
3. Analyze patterns
4. Identify improvement areas
5. Update agent
6. Measure impact

**Continuous Improvement**:
- A/B testing for changes
- Gradual rollout
- Monitor metrics
- Iterate based on data""",
            "implementation": """# Function to collect and process feedback
class FeedbackCollector:
    \"\"\"Collect and analyze user feedback.\"\"\"\n    
    def __init__(self):
        \"\"\"Initialize feedback collector.\"\"\"\n        self.feedback_data = []
    
    def collect_feedback(self, interaction_id: str, rating: int, 
                        comment: str = \"\") -> None:
        \"\"\"
        Collect feedback for an interaction.
        
        Args:
            interaction_id: Unique ID for the interaction
            rating: Rating (1-5)
            comment: Optional text comment
        \"\"\"\n        feedback = {
            \"interaction_id\": interaction_id,
            \"rating\": rating,
            \"comment\": comment,
            \"timestamp\": datetime.now().isoformat()
        }
        
        self.feedback_data.append(feedback)
        print(f\"Feedback collected: {rating}/5 stars\")
    
    def analyze_feedback(self) -> Dict[str, Any]:
        \"\"\"
        Analyze collected feedback.
        
        Returns:
            Analysis results
        \"\"\"\n        if not self.feedback_data:
            return {\"message\": \"No feedback data available\"}
        
        # Calculate average rating
        ratings = [f[\"rating\"] for f in self.feedback_data]
        avg_rating = sum(ratings) / len(ratings)
        
        # Count ratings by value
        rating_counts = {}
        for rating in ratings:
            rating_counts[rating] = rating_counts.get(rating, 0) + 1
        
        return {
            \"total_feedback\": len(self.feedback_data),
            \"average_rating\": avg_rating,
            \"rating_distribution\": rating_counts,
            \"satisfaction_rate\": sum(1 for r in ratings if r >= 4) / len(ratings)
        }

# Example usage
collector = FeedbackCollector()
collector.collect_feedback(\"int_001\", 5, \"Very helpful!\")
collector.collect_feedback(\"int_002\", 4, \"Good response\")
collector.collect_feedback(\"int_003\", 3, \"Could be better\")

analysis = collector.analyze_feedback()
print(f\"\\nFeedback Analysis:\")
print(f\"  Total Feedback: {analysis['total_feedback']}\")
print(f\"  Average Rating: {analysis['average_rating']:.2f}/5\")
print(f\"  Satisfaction Rate: {analysis['satisfaction_rate']:.1%}\")"""
        }
    ]
}


def create_notebook_cell(cell_type: str, content: str) -> dict:
    """Create a notebook cell."""
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": content.split("\n")
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def generate_notebook(module: str, template: dict) -> dict:
    """Generate complete notebook from template."""
    cells = []
    
    # Title and overview
    cells.append(create_notebook_cell("markdown", f"""# {template['title']}

## Overview

This notebook explores {template['title'].lower()}.

## Learning Objectives

{chr(10).join(f"- {obj}" for obj in template['objectives'])}

## Exam Objectives: {template['exam_objectives']}
## Estimated Time: {template['time']}"""))
    
    # Setup cell
    cells.append(create_notebook_cell("markdown", "## Setup: Import Dependencies"))
    cells.append(create_notebook_cell("code", """# Import core libraries
import os
import sys
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

print("\\n🎯 Setup complete!")"""))
    
    # Theory section
    cells.append(create_notebook_cell("markdown", f"## Theory\n\n{template['theory']}"))
    
    # Implementation section
    cells.append(create_notebook_cell("markdown", "## Implementation"))
    cells.append(create_notebook_cell("code", template['implementation']))
    
    # Exercise section
    cells.append(create_notebook_cell("markdown", """## Exercise

**Objective**: Practice implementing the concepts covered in this notebook.

Complete the exercise below based on the implementation examples."""))
    
    cells.append(create_notebook_cell("code", """# Exercise: Implement your solution here

# Your code here
pass"""))
    
    # Checkpoint
    cells.append(create_notebook_cell("markdown", """## Checkpoint: Self-Assessment

Before proceeding, ensure you understand the key concepts covered in this notebook.

Review the learning objectives and verify you can explain each concept."""))
    
    # Next steps
    cells.append(create_notebook_cell("markdown", """## Next Steps

Continue to the next notebook in this module or proceed to the next module.

## References

- Course Notes: Refer to the corresponding module documentation
- Official Documentation: Check vendor-specific documentation"""))
    
    # Create notebook structure
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return notebook


def main():
    """Generate all remaining notebooks."""
    base_path = Path("notebooks")
    
    for module, templates in NOTEBOOK_TEMPLATES.items():
        module_path = base_path / module
        module_path.mkdir(parents=True, exist_ok=True)
        
        for template in templates:
            notebook = generate_notebook(module, template)
            output_path = module_path / template['filename']
            
            with open(output_path, 'w') as f:
                json.dump(notebook, f, indent=1)
            
            print(f"✅ Created: {output_path}")
    
    print("\n🎉 All notebooks generated successfully!")


if __name__ == "__main__":
    main()
