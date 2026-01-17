# Module 6: NVIDIA Platform Implementation

**Exam Weight:** 7%  
**Estimated Study Time:** 5-6 hours  
**Prerequisites:** Modules 1-5, Docker basics, API concepts

## Learning Objectives

1. **Integrate NVIDIA NeMo Guardrails** for compliance and safety
2. **Deploy NVIDIA NIM microservices** for high-performance inference
3. **Optimize workflows** with NVIDIA NeMo Agent Toolkit
4. **Leverage TensorRT-LLM and Triton Inference Server** for production
5. **Manage multimodal input pipelines** on NVIDIA hardware

## Exam Objective Mapping

- **6.1** - Integrate NVIDIA NeMo Guardrails for compliance and safety
- **6.2** - Deploy NVIDIA NIM microservices for high-performance inference
- **6.3** - Optimize workflows with NVIDIA NeMo Agent Toolkit
- **6.4** - Leverage TensorRT-LLM and Triton Inference Server
- **6.5** - Manage multimodal input pipelines on NVIDIA hardware

---

## 1. NVIDIA NIM (NVIDIA Inference Microservices)

### 1.1 Overview

**NVIDIA NIM** provides optimized, production-ready microservices for LLM inference.

**Key Benefits:**
- Pre-optimized for NVIDIA GPUs
- Containerized deployment
- High throughput and low latency
- Support for multiple models
- Enterprise-grade reliability

### 1.2 Deploying NIM

```bash
# Pull NIM container
docker pull nvcr.io/nim/meta/llama-3.1-70b-instruct:latest

# Run NIM microservice
docker run -d \
  --gpus all \
  --name llama-nim \
  -p 8000:8000 \
  -e NGC_API_KEY=$NGC_API_KEY \
  nvcr.io/nim/meta/llama-3.1-70b-instruct:latest

# Check status
curl http://localhost:8000/v1/health
```

### 1.3 Using NIM with LangChain

```python
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Connect to local NIM instance
llm = ChatNVIDIA(
    base_url="http://localhost:8000/v1",
    model="meta/llama-3.1-70b-instruct"
)

# Use like any LangChain LLM
response = llm.invoke("What is NVIDIA NIM?")
print(response.content)

# Streaming
for chunk in llm.stream("Explain RAG"):
    print(chunk.content, end="", flush=True)
```

### 1.4 NIM Configuration Best Practices

```yaml
# nim-config.yaml
model:
  name: "meta/llama-3.1-70b-instruct"
  max_batch_size: 128
  max_sequence_length: 4096

inference:
  tensor_parallel_size: 4  # Multi-GPU
  pipeline_parallel_size: 1
  max_num_seqs: 256

optimization:
  enable_chunked_prefill: true
  enable_prefix_caching: true
  gpu_memory_utilization: 0.9
```

> 📝 **EXAM TIP**
> 
> NIM provides production-ready inference with minimal setup. Understand deployment options (Docker, Kubernetes) and configuration parameters (batch size, parallelism).

---

## 2. NVIDIA NeMo Guardrails

### 2.1 Overview

**NeMo Guardrails** provides programmable safety and compliance controls for LLM applications.

**Key Features:**
- Input/output filtering
- Topic restrictions
- Fact-checking
- Jailbreak prevention
- Custom guardrails

### 2.2 Basic Guardrails Configuration

```yaml
# config.yml
models:
  - type: main
    engine: nvidia_ai_endpoints
    model: meta/llama-3.1-70b-instruct

rails:
  input:
    flows:
      - check toxic language
      - check jailbreak attempts
  
  output:
    flows:
      - check hallucination
      - check sensitive information

  retrieval:
    flows:
      - check source reliability
```

```colang
# guardrails.co
define user ask about illegal activity
  "how to hack"
  "how to make explosives"

define bot refuse illegal request
  "I cannot provide information on illegal activities."

define flow
  user ask about illegal activity
  bot refuse illegal request
  stop
```

### 2.3 Implementing Guardrails

```python
from nemoguardrails import RailsConfig, LLMRails
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Load configuration
config = RailsConfig.from_path("./config")

# Create rails
rails = LLMRails(config)

# Use with guardrails
response = rails.generate(
    messages=[{
        "role": "user",
        "content": "How do I hack into a system?"
    }]
)

print(response["content"])
# Output: "I cannot provide information on illegal activities."
```

### 2.4 Custom Guardrails

```python
from nemoguardrails.actions import action

@action(name="check_pii")
async def check_pii(context: dict):
    """Check for personally identifiable information"""
    text = context.get("user_message", "")
    
    # Simple PII detection
    import re
    
    patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b'
    }
    
    for pii_type, pattern in patterns.items():
        if re.search(pattern, text):
            return {
                "allowed": False,
                "reason": f"Contains {pii_type}"
            }
    
    return {"allowed": True}

# Register action
config.actions.register_action(check_pii)
```

> 📝 **EXAM TIP**
> 
> Guardrails are critical for production safety. Understand input/output filtering, topic restrictions, and custom guardrail implementation.

---

## 3. TensorRT-LLM

### 3.1 Overview

**TensorRT-LLM** optimizes LLM inference for NVIDIA GPUs, reducing latency and increasing throughput.

**Optimizations:**
- Kernel fusion
- Quantization (INT8, FP8)
- In-flight batching
- Paged attention (PagedKV)

### 3.2 Building TensorRT-LLM Engine

```bash
# Convert model to TensorRT-LLM
python convert_checkpoint.py \
  --model_dir ./llama-3.1-70b \
  --output_dir ./trt_engines/llama-70b \
  --dtype float16 \
  --tp_size 4  # Tensor parallelism

# Build engine
trtllm-build \
  --checkpoint_dir ./trt_engines/llama-70b \
  --output_dir ./engines/llama-70b \
  --gemm_plugin float16 \
  --max_batch_size 128 \
  --max_input_len 2048 \
  --max_output_len 1024
```

### 3.3 Performance Comparison

| Configuration | Latency (ms) | Throughput (tok/s) | Memory (GB) |
|---------------|--------------|---------------------|-------------|
| **PyTorch FP16** | 45 | 2,200 | 140 |
| **TensorRT-LLM FP16** | 18 | 5,500 | 140 |
| **TensorRT-LLM INT8** | 12 | 8,300 | 70 |
| **TensorRT-LLM FP8** | 10 | 10,000 | 70 |

> 📝 **EXAM TIP**
> 
> TensorRT-LLM provides 2-4x speedup over PyTorch. Quantization (INT8/FP8) further improves performance with minimal accuracy loss.

---

## 4. Triton Inference Server

### 4.1 Overview

**Triton Inference Server** provides production-grade model serving with advanced features.

**Key Features:**
- Multi-model serving
- Dynamic batching
- Model ensembles
- HTTP/gRPC APIs
- Metrics and monitoring

### 4.2 Deploying with Triton

```bash
# Model repository structure
model_repository/
├── llama-70b/
│   ├── config.pbtxt
│   └── 1/
│       └── model.plan  # TensorRT engine

# config.pbtxt
name: "llama-70b"
platform: "tensorrt_llm"
max_batch_size: 128

input [
  {
    name: "input_ids"
    data_type: TYPE_INT32
    dims: [-1]
  }
]

output [
  {
    name: "output_ids"
    data_type: TYPE_INT32
    dims: [-1]
  }
]

dynamic_batching {
  max_queue_delay_microseconds: 100
}

# Run Triton
docker run --gpus all --rm \
  -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  -v $(pwd)/model_repository:/models \
  nvcr.io/nvidia/tritonserver:24.01-trtllm-python-py3 \
  tritonserver --model-repository=/models
```

### 4.3 Client Usage

```python
import tritonclient.http as httpclient
from tritonclient.utils import np_to_triton_dtype
import numpy as np

# Create client
client = httpclient.InferenceServerClient(url="localhost:8000")

# Prepare input
input_ids = np.array([[1, 2, 3, 4, 5]], dtype=np.int32)

inputs = [
    httpclient.InferInput("input_ids", input_ids.shape, 
                          np_to_triton_dtype(input_ids.dtype))
]
inputs[0].set_data_from_numpy(input_ids)

# Inference
response = client.infer(model_name="llama-70b", inputs=inputs)

# Get output
output_ids = response.as_numpy("output_ids")
```

> 📝 **EXAM TIP**
> 
> Triton enables production deployment with dynamic batching, multi-model serving, and monitoring. Understand configuration options and performance tuning.

---

## 5. NVIDIA NeMo Agent Toolkit

### 5.1 Overview

**NeMo Agent Toolkit** provides tools for building, evaluating, and optimizing agentic AI systems.

**Components:**
- Agent templates
- Evaluation frameworks
- Optimization tools
- Deployment utilities

### 5.2 Using NeMo Agent Toolkit

```python
from nemo_agent_toolkit import AgentBuilder, AgentEvaluator

# Build agent with template
builder = AgentBuilder(
    model="meta/llama-3.1-70b-instruct",
    tools=["search", "calculator", "database"],
    memory_type="vector_store"
)

agent = builder.build()

# Evaluate agent
evaluator = AgentEvaluator(
    agent=agent,
    metrics=["accuracy", "latency", "cost"]
)

results = evaluator.evaluate(test_dataset)

# Optimize
from nemo_agent_toolkit import AgentOptimizer

optimizer = AgentOptimizer(agent)
optimized_agent = optimizer.optimize(
    target_latency_ms=1000,
    min_accuracy=0.85
)
```

> 📝 **EXAM TIP**
> 
> NeMo Agent Toolkit streamlines agent development with templates, evaluation, and optimization. Know the key components and use cases.

---

## 6. Multimodal Pipelines

### 6.1 Vision-Language Models

```python
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import base64

# Initialize vision model
vlm = ChatNVIDIA(model="microsoft/phi-3-vision-128k-instruct")

# Load image
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# Create multimodal message
messages = [{
    "role": "user",
    "content": [
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
    ]
}]

response = vlm.invoke(messages)
print(response.content)
```

### 6.2 Audio Processing

```python
from nvidia_audio_toolkit import AudioProcessor

# Initialize audio processor
processor = AudioProcessor(
    model="nvidia/parakeet-tdt-1.1b",
    device="cuda"
)

# Transcribe audio
transcription = processor.transcribe("audio.wav")

# Use in agent
agent_input = f"User said: {transcription}"
response = agent.invoke(agent_input)
```

---

## 7. Exam Focus Areas

### Key Concepts

1. **NIM**: Containerized inference, deployment, configuration
2. **Guardrails**: Input/output filtering, custom guardrails, safety
3. **TensorRT-LLM**: Optimization, quantization, performance gains
4. **Triton**: Model serving, dynamic batching, production deployment
5. **NeMo Agent Toolkit**: Agent building, evaluation, optimization

### Scenario Examples

**Example 1: Optimization Choice**
> You need to reduce inference latency by 50%. Which NVIDIA tool?
> 
> A) NeMo Guardrails  
> B) TensorRT-LLM  
> C) NIM  
> D) Triton  
>
> **Answer: B** - TensorRT-LLM provides 2-4x speedup through optimization.

**Example 2: Safety Implementation**
> Your agent must block requests for illegal information. Which tool?
>
> A) TensorRT-LLM  
> B) Triton  
> C) NeMo Guardrails  
> D) NIM  
>
> **Answer: C** - NeMo Guardrails provides programmable safety controls.

---

## 8. Summary

**Key Takeaways:**
1. NIM simplifies production deployment
2. Guardrails ensure safety and compliance
3. TensorRT-LLM optimizes inference performance
4. Triton enables scalable model serving
5. NeMo Agent Toolkit streamlines development

**Command Reference:**
```bash
# NIM
docker run --gpus all nvcr.io/nim/meta/llama-3.1-70b-instruct

# TensorRT-LLM
trtllm-build --checkpoint_dir ./model --output_dir ./engine

# Triton
tritonserver --model-repository=/models

# Guardrails
nemoguardrails server --config ./config
```

**Related Modules:**
- Module 2: Agent Development (tool integration)
- Module 3: Evaluation (performance metrics)
- Module 8: Deployment (production patterns)

---

## References

1. **NVIDIA Documentation**
   - [NIM Documentation](https://docs.nvidia.com/nim)
   - [NeMo Guardrails Guide](https://docs.nvidia.com/nemo/guardrails)
   - [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)
   - [Triton Inference Server](https://docs.nvidia.com/deeplearning/triton-inference-server)

2. **Related Materials**
   - Notebook: `module-06/01-nvidia-nim.ipynb`
   - Notebook: `module-06/02-nemo-guardrails.ipynb`
   - Notebook: `module-06/03-tensorrt-llm.ipynb`
   - Lab: `lab-03-production-deployment`


---

## Related Materials

### Hands-On Practice

**Interactive Notebooks:**
- [01-nvidia-nim.ipynb](../../notebooks/module-06/01-nvidia-nim.ipynb)
- [02-nemo-guardrails.ipynb](../../notebooks/module-06/02-nemo-guardrails.ipynb)
- [03-tensorrt-llm.ipynb](../../notebooks/module-06/03-tensorrt-llm.ipynb)
- [04-triton-inference.ipynb](../../notebooks/module-06/04-triton-inference.ipynb)

**Practice Labs:**
- [Lab: Lab 03 Production Deployment](../../labs/lab-03-production-deployment/README.md)
- [Lab: Lab 05 Safe Compliant Agent](../../labs/lab-05-safe-compliant-agent/README.md)

### Assessment

**Exam Questions:**
- [Domain 06 Nvidia Platform](../../exam-questions/domain-06-nvidia-platform.md)
