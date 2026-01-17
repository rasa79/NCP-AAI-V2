#!/usr/bin/env python3
import json
from pathlib import Path

def create_module6_notebooks():
    """Create Module 6 notebooks with proper structure."""
    
    notebooks = {
        "01-nvidia-nim.ipynb": {
            "title": "NVIDIA NIM: High-Performance Inference",
            "code": """# Import required libraries for NVIDIA NIM integration
import os
import requests
from typing import Dict, Any

# Function to check NIM health status
def check_nim_health(url: str = "http://localhost:8000") -> Dict[str, Any]:
    # Send health check request to NIM endpoint
    # Returns health status dictionary
    try:
        response = requests.get(f"{url}/health", timeout=5)
        return {"status": "healthy" if response.status_code == 200 else "unhealthy"}
    except Exception as e:
        # Handle connection errors gracefully
        return {"status": "error", "message": str(e)}

print("NIM health check function created")"""
        },
        "02-nemo-guardrails.ipynb": {
            "title": "NeMo Guardrails: Safety Controls",
            "code": """# Import NeMo Guardrails for safety implementation
import os
from typing import List, Dict

# Function to create safety guardrail
def create_guardrail(blocked_topics: List[str]) -> callable:
    # Create guardrail function that blocks specific topics
    # Returns callable that checks input safety
    def check_input(text: str) -> Dict[str, bool]:
        # Check if input contains blocked topics
        # Return blocking decision
        for topic in blocked_topics:
            if topic.lower() in text.lower():
                return {"blocked": True, "reason": f"Topic '{topic}' not allowed"}
        return {"blocked": False}
    return check_input

print("Guardrail function created")"""
        },
        "03-tensorrt-llm.ipynb": {
            "title": "TensorRT-LLM: Optimized Inference",
            "code": """# Import TensorRT-LLM for model optimization
import os
from pathlib import Path

# Function to build TensorRT engine
def build_tensorrt_engine(model_path: str, output_path: str) -> bool:
    # Build optimized TensorRT engine from model
    # Applies kernel fusion and quantization
    # Returns success status
    try:
        # Engine building process (placeholder)
        # Actual implementation requires TensorRT-LLM
        print(f"Building engine from {model_path}")
        return True
    except Exception as e:
        # Handle build errors
        print(f"Build failed: {e}")
        return False

print("TensorRT engine builder created")"""
        },
        "04-triton-inference.ipynb": {
            "title": "Triton Inference Server: Model Serving",
            "code": """# Import Triton client for inference
import numpy as np
from typing import Optional

# Function to perform Triton inference
def triton_inference(model_name: str, input_data: np.ndarray) -> Optional[np.ndarray]:
    # Send inference request to Triton server
    # Handles batching and model execution
    # Returns model output or None on error
    try:
        # Inference logic (placeholder)
        # Actual implementation requires Triton client
        print(f"Running inference on {model_name}")
        return input_data  # Placeholder
    except Exception as e:
        # Handle inference errors
        print(f"Inference failed: {e}")
        return None

print("Triton inference function created")"""
        }
    }
    
    module_path = Path("notebooks/module-06")
    module_path.mkdir(parents=True, exist_ok=True)
    
    for filename, content in notebooks.items():
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"# {content['title']}\n\n## Learning Objectives\n\n- Understand the technology\n- Implement practical examples\n- Apply best practices"]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": content['code'].split('\n')
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["## Exercise\n\nPractice the concepts covered above."]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["## Checkpoint\n\nReview key concepts before proceeding."]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        output_file = module_path / filename
        with open(output_file, 'w') as f:
            json.dump(notebook, f, indent=1)
        print(f"Created: {output_file}")

if __name__ == "__main__":
    create_module6_notebooks()
