# Command Cheatsheet

## NVIDIA NIM (Inference Microservices)

### Basic Deployment

```bash
# Pull NIM container
docker pull nvcr.io/nim/meta/llama3-8b-instruct:latest

# Run NIM with GPU
docker run --gpus all \
  -p 8000:8000 \
  -e NGC_API_KEY=$NGC_API_KEY \
  nvcr.io/nim/meta/llama3-8b-instruct:latest

# Run with custom configuration
docker run --gpus all \
  -p 8000:8000 \
  -v $(pwd)/models:/models \
  -e MODEL_NAME=llama3-8b \
  -e MAX_BATCH_SIZE=32 \
  nvcr.io/nim/meta/llama3-8b-instruct:latest
```

### Configuration Options

```bash
# Set environment variables
-e NGC_API_KEY=<your_key>           # NVIDIA NGC API key
-e MODEL_NAME=<model_name>          # Model identifier
-e MAX_BATCH_SIZE=32                # Maximum batch size
-e MAX_SEQUENCE_LENGTH=2048         # Maximum sequence length
-e TENSOR_PARALLEL_SIZE=1           # Tensor parallelism degree
-e PIPELINE_PARALLEL_SIZE=1         # Pipeline parallelism degree
```

### Health Check

```bash
# Check NIM health
curl http://localhost:8000/health

# Check model info
curl http://localhost:8000/v1/models

# Test inference
curl -X POST http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3-8b",
    "prompt": "What is RAG?",
    "max_tokens": 100
  }'
```

---

## TensorRT-LLM

### Model Conversion

```bash
# Convert HuggingFace model to TensorRT-LLM
python convert_checkpoint.py \
  --model_dir /path/to/hf_model \
  --output_dir /path/to/trt_checkpoint \
  --dtype float16

# Build TensorRT engine
trtllm-build \
  --checkpoint_dir /path/to/trt_checkpoint \
  --output_dir /path/to/engine \
  --gemm_plugin float16 \
  --max_batch_size 32 \
  --max_input_len 1024 \
  --max_output_len 512
```

### Optimization Options

```bash
# Build with tensor parallelism
trtllm-build \
  --checkpoint_dir /path/to/checkpoint \
  --output_dir /path/to/engine \
  --tp_size 2 \
  --pp_size 1 \
  --max_batch_size 64

# Build with INT8 quantization
trtllm-build \
  --checkpoint_dir /path/to/checkpoint \
  --output_dir /path/to/engine \
  --use_weight_only \
  --weight_only_precision int8

# Build with FP8 quantization (H100+)
trtllm-build \
  --checkpoint_dir /path/to/checkpoint \
  --output_dir /path/to/engine \
  --use_fp8 \
  --fp8_kv_cache
```

### Inference

```bash
# Run inference with TensorRT-LLM
python run.py \
  --engine_dir /path/to/engine \
  --tokenizer_dir /path/to/tokenizer \
  --input_text "What is agentic AI?" \
  --max_output_len 256

# Benchmark performance
python benchmark.py \
  --engine_dir /path/to/engine \
  --batch_size 32 \
  --input_len 128 \
  --output_len 128
```

---

## Triton Inference Server

### Server Management

```bash
# Start Triton server
tritonserver \
  --model-repository=/models \
  --http-port=8000 \
  --grpc-port=8001 \
  --metrics-port=8002

# Start with GPU specification
tritonserver \
  --model-repository=/models \
  --gpus=0,1 \
  --log-verbose=1

# Start with dynamic batching
tritonserver \
  --model-repository=/models \
  --backend-config=tensorflow,version=2
```

### Model Management

```bash
# Load model
curl -X POST http://localhost:8000/v2/repository/models/my_model/load

# Unload model
curl -X POST http://localhost:8000/v2/repository/models/my_model/unload

# Check model status
curl http://localhost:8000/v2/models/my_model

# List all models
curl http://localhost:8000/v2/models
```

### Inference Requests

```bash
# HTTP inference request
curl -X POST http://localhost:8000/v2/models/my_model/infer \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [{
      "name": "input_text",
      "shape": [1],
      "datatype": "BYTES",
      "data": ["What is RAG?"]
    }]
  }'

# Check server metrics
curl http://localhost:8002/metrics
```

### Configuration Files

```bash
# Model config.pbtxt example
name: "llama3_trt"
platform: "tensorrt_llm"
max_batch_size: 32

dynamic_batching {
  preferred_batch_size: [8, 16, 32]
  max_queue_delay_microseconds: 1000
}

instance_group [
  {
    count: 1
    kind: KIND_GPU
    gpus: [0]
  }
]
```

---

## LangChain

### Installation

```bash
# Install LangChain
pip install langchain langchain-community langchain-core

# Install with specific integrations
pip install langchain-openai langchain-nvidia-ai-endpoints

# Install LangServe for deployment
pip install langserve[all]
```

### Basic Usage

```python
# Create a simple chain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

llm = ChatNVIDIA(model="llama3-8b")
prompt = PromptTemplate.from_template("What is {topic}?")
chain = LLMChain(llm=llm, prompt=prompt)

result = chain.run(topic="RAG")
```

### RAG Pipeline

```python
# Build RAG pipeline
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# Create vector store
embeddings = HuggingFaceEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

answer = qa_chain.run("What is agentic AI?")
```

### LangServe Deployment

```bash
# Create LangServe app
langchain serve

# Run LangServe server
python app.py

# Deploy with custom port
uvicorn app:app --host 0.0.0.0 --port 8080
```

```python
# app.py example
from fastapi import FastAPI
from langserve import add_routes
from langchain.chains import LLMChain

app = FastAPI(title="RAG API")

add_routes(
    app,
    chain,
    path="/rag"
)
```

---

## Gradio

### Installation

```bash
# Install Gradio
pip install gradio

# Install with specific version
pip install gradio==4.0.0
```

### Basic Interface

```python
# Create simple interface
import gradio as gr

def chat(message, history):
    return f"You said: {message}"

demo = gr.ChatInterface(
    fn=chat,
    title="RAG Agent",
    description="Ask questions about your documents"
)

demo.launch()
```

### Advanced Interface

```python
# Create custom interface
import gradio as gr

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your question")
    clear = gr.Button("Clear")
    
    msg.submit(chat_fn, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch(server_name="0.0.0.0", server_port=7860)
```

### Deployment

```bash
# Launch with sharing
python app.py --share

# Launch on specific port
python app.py --server-port 8080

# Launch with authentication
python app.py --auth username:password

# Deploy to Hugging Face Spaces
git push hf main
```

---

## NVIDIA NeMo Guardrails

### Installation

```bash
# Install NeMo Guardrails
pip install nemoguardrails

# Verify installation
nemoguardrails --version
```

### Configuration

```bash
# Create guardrails config directory
mkdir -p config
cd config

# Create config.yml
cat > config.yml << EOF
models:
  - type: main
    engine: nvidia_ai_endpoints
    model: llama3-8b

rails:
  input:
    flows:
      - check jailbreak
      - check toxicity
  output:
    flows:
      - check hallucination
      - check factuality
EOF
```

### Running Guardrails

```bash
# Start guardrails server
nemoguardrails server --config=./config

# Test guardrails
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Python API

```python
# Use guardrails in Python
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("./config")
rails = LLMRails(config)

response = rails.generate(
    messages=[{"role": "user", "content": "What is RAG?"}]
)
print(response["content"])
```

---

## Vector Databases

### FAISS

```python
# Install FAISS
pip install faiss-cpu  # CPU version
pip install faiss-gpu  # GPU version

# Create and save index
import faiss
import numpy as np

# Create index
dimension = 768
index = faiss.IndexFlatL2(dimension)

# Add vectors
vectors = np.random.random((1000, dimension)).astype('float32')
index.add(vectors)

# Save index
faiss.write_index(index, "my_index.faiss")

# Load and search
index = faiss.read_index("my_index.faiss")
distances, indices = index.search(query_vector, k=5)
```

### Milvus

```bash
# Start Milvus with Docker
docker-compose up -d

# Install Python client
pip install pymilvus

# Check Milvus status
curl http://localhost:9091/healthz
```

```python
# Connect and create collection
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

connections.connect("default", host="localhost", port="19530")

# Define schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)
]
schema = CollectionSchema(fields, description="RAG documents")
collection = Collection("rag_docs", schema)

# Create index
collection.create_index("embedding", {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}})
```

### Chroma

```bash
# Install Chroma
pip install chromadb

# Start Chroma server
chroma run --path ./chroma_data
```

```python
# Use Chroma
import chromadb

client = chromadb.Client()
collection = client.create_collection("rag_docs")

# Add documents
collection.add(
    documents=["Document 1", "Document 2"],
    metadatas=[{"source": "doc1"}, {"source": "doc2"}],
    ids=["id1", "id2"]
)

# Query
results = collection.query(
    query_texts=["What is RAG?"],
    n_results=5
)
```

---

## Monitoring and Logging

### LangSmith

```bash
# Set environment variables
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your_key>
export LANGCHAIN_PROJECT=<project_name>

# Run with tracing
python your_agent.py
```

### Prometheus

```bash
# Start Prometheus
prometheus --config.file=prometheus.yml

# Query metrics
curl http://localhost:9090/api/v1/query?query=up
```

### Grafana

```bash
# Start Grafana
docker run -d -p 3000:3000 grafana/grafana

# Access dashboard
# Navigate to http://localhost:3000
# Default credentials: admin/admin
```

---

## Docker and Kubernetes

### Docker

```bash
# Build image
docker build -t rag-agent:latest .

# Run container
docker run -d -p 8000:8000 rag-agent:latest

# View logs
docker logs <container_id>

# Execute command in container
docker exec -it <container_id> bash

# Stop and remove
docker stop <container_id>
docker rm <container_id>
```

### Kubernetes

```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Check pods
kubectl get pods

# View logs
kubectl logs <pod_name>

# Port forward
kubectl port-forward <pod_name> 8000:8000

# Scale deployment
kubectl scale deployment rag-agent --replicas=3

# Delete deployment
kubectl delete deployment rag-agent
```

---

## Quick Command Reference

| Tool | Start Command | Port | Health Check |
|------|--------------|------|--------------|
| NIM | `docker run --gpus all -p 8000:8000 nvcr.io/nim/...` | 8000 | `curl localhost:8000/health` |
| Triton | `tritonserver --model-repository=/models` | 8000 | `curl localhost:8000/v2/health/ready` |
| LangServe | `uvicorn app:app --port 8080` | 8080 | `curl localhost:8080/docs` |
| Gradio | `python app.py` | 7860 | `curl localhost:7860` |
| Guardrails | `nemoguardrails server --config=./config` | 8000 | `curl localhost:8000/health` |
| Milvus | `docker-compose up -d` | 19530 | `curl localhost:9091/healthz` |
| Chroma | `chroma run --path ./data` | 8000 | `curl localhost:8000/api/v1/heartbeat` |

## Exam Tips

**Memorize These Commands**:
- NIM deployment: `docker run --gpus all -p 8000:8000 nvcr.io/nim/...`
- TensorRT build: `trtllm-build --checkpoint_dir ... --output_dir ...`
- Triton start: `tritonserver --model-repository=/models`
- Guardrails server: `nemoguardrails server --config=./config`

**Common Scenarios**:
- **Deploy model**: Use NIM for quick deployment, TensorRT-LLM for optimization
- **Serve multiple models**: Use Triton Inference Server
- **Add safety**: Use NeMo Guardrails
- **Build UI**: Use Gradio for rapid prototyping
- **Production API**: Use LangServe with FastAPI

**Troubleshooting**:
- Port conflicts: Change `-p` flag in Docker
- GPU not detected: Add `--gpus all` flag
- Out of memory: Reduce batch size or use quantization
- Model not loading: Check model repository path and config
