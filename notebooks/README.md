# Interactive Jupyter Notebooks

Hands-on practice with executable code for all exam domains.

## Setup Notebooks

Start here to configure your environment:

1. `setup/00-environment-setup.ipynb` - Install dependencies and verify setup
2. `setup/01-nvidia-platform-setup.ipynb` - Configure NVIDIA tools

## Module Notebooks

### Module 01: Agent Architecture and Design (15%)
- `module-01/01-agent-architectures.ipynb` - Agent architecture patterns
- `module-01/02-react-pattern.ipynb` - ReAct pattern implementation
- `module-01/03-multi-agent-systems.ipynb` - Multi-agent orchestration

### Module 02: Agent Development (15%)
- `module-02/01-prompt-engineering.ipynb` - Dynamic prompt chains
- `module-02/02-tool-integration.ipynb` - API and tool integration
- `module-02/03-error-handling-patterns.ipynb` - Retry logic and circuit breakers
- `module-02/04-streaming-responses.ipynb` - Real-time interaction

### Module 03: Evaluation and Tuning (13%)
- `module-03/01-evaluation-metrics.ipynb` - RAG evaluation metrics
- `module-03/02-evaluation-pipelines.ipynb` - Automated evaluation
- `module-03/03-ab-testing.ipynb` - A/B testing frameworks

### Module 04: Knowledge Integration (10%)
- `module-04/01-rag-fundamentals.ipynb` - Basic RAG pipeline
- `module-04/02-embedding-models.ipynb` - Embedding models comparison
- `module-04/03-vector-stores.ipynb` - FAISS, Milvus, Chroma
- `module-04/04-retrieval-optimization.ipynb` - Hybrid search strategies

### Module 05: Cognition, Planning, and Memory (10%)
- `module-05/01-memory-mechanisms.ipynb` - Short/long-term memory
- `module-05/02-chain-of-thought.ipynb` - Reasoning patterns
- `module-05/03-task-decomposition.ipynb` - Planning strategies

### Module 06: NVIDIA Platform (7%)
- `module-06/01-nvidia-nim.ipynb` - NIM deployment
- `module-06/02-nemo-guardrails.ipynb` - Safety configuration
- `module-06/03-tensorrt-llm.ipynb` - Inference optimization
- `module-06/04-triton-inference.ipynb` - Model serving

### Module 07: Monitoring and Maintenance (7%)
- `module-07/01-monitoring-dashboards.ipynb` - Metrics tracking
- `module-07/02-logging-tracing.ipynb` - LangSmith integration
- `module-07/03-performance-profiling.ipynb` - Bottleneck analysis

### Module 08: Deployment and Scaling (5%)
- `module-08/01-containerization.ipynb` - Docker examples
- `module-08/02-kubernetes-deployment.ipynb` - K8s deployment

### Module 09: Safety, Ethics, and Compliance (5%)
- `module-09/01-guardrails-implementation.ipynb` - NeMo Guardrails
- `module-09/02-bias-detection.ipynb` - Fairness metrics

### Module 10: Human-AI Interaction (5%)
- `module-10/01-ui-development.ipynb` - Gradio interfaces
- `module-10/02-feedback-loops.ipynb` - User feedback integration

## How to Use

1. **Launch Jupyter Lab:** `jupyter lab`
2. **Start with Setup:** Complete setup notebooks first
3. **Follow Learning Path:** Work through modules sequentially
4. **Execute All Cells:** Run cells in order to avoid errors
5. **Complete Exercises:** Don't skip the hands-on exercises
6. **Experiment:** Modify code to deepen understanding

## Notebook Structure

Each notebook includes:
- Setup and imports
- Theory and concepts
- Step-by-step implementation
- Working demonstrations
- Hands-on exercises
- Troubleshooting tips
- Performance analysis
- Self-assessment checkpoints

## Tips

- Save your work frequently
- Create a copy before experimenting
- Read comments carefully
- Use Shift+Enter to run cells
- Restart kernel if you encounter errors
- Check GPU availability for NVIDIA-specific code
