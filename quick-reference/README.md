# Quick Reference Guide

This quick reference guide provides rapid access to key concepts, formulas, commands, and decision frameworks for the NVIDIA NCP-AAI certification exam and RAG agent development.

## Contents

1. **[Formulas and Metrics](formulas-metrics.md)** - Evaluation and performance metrics with formulas
2. **[Command Cheatsheet](command-cheatsheet.md)** - Essential commands for NVIDIA tools and frameworks
3. **[Patterns and Anti-Patterns](patterns-antipatterns.md)** - When to use specific architectures and what to avoid
4. **[Decision Trees](decision-trees.md)** - Visual guides for architecture and technology selection
5. **[Troubleshooting Flowcharts](troubleshooting-flowcharts.md)** - Systematic diagnosis of common issues
6. **[Exam Tips](exam-tips.md)** - Strategies for certification exam success

## How to Use This Guide

- **Before the Exam**: Review all sections to refresh key concepts
- **During Development**: Reference commands and decision trees for implementation guidance
- **When Troubleshooting**: Use flowcharts to systematically diagnose issues
- **For Architecture Decisions**: Consult patterns and decision trees

## Quick Navigation

### Most Important Metrics
- **Retrieval**: Precision, Recall, F1, MRR, NDCG
- **Generation**: BLEU, ROUGE, Faithfulness, Answer Relevance
- **Performance**: Latency (p50, p95, p99), Throughput, Tokens/sec

### Most Used Commands
- NVIDIA NIM: `docker run nvcr.io/nim/...`
- TensorRT-LLM: `trtllm-build --checkpoint_dir ...`
- Triton: `tritonserver --model-repository ...`

### Key Decision Points
- RAG vs Fine-tuning: Use RAG for dynamic knowledge, fine-tuning for style/format
- Vector Store: FAISS (local), Milvus (scale), Chroma (simplicity)
- Retrieval: Semantic (meaning), Keyword (exact), Hybrid (both)

### Common Issues
- High Latency → Check batch size, model optimization, network
- Low Accuracy → Improve retrieval, tune prompts, add context
- Hallucinations → Add guardrails, improve grounding, validate outputs
- Memory Issues → Optimize context window, implement summarization

## Exam Preparation Checklist

- [ ] Memorize key evaluation metrics and formulas
- [ ] Practice NVIDIA platform commands
- [ ] Understand when to use each architecture pattern
- [ ] Review decision trees for common scenarios
- [ ] Study troubleshooting flowcharts
- [ ] Practice time management strategies

## Related Materials

- **Course Notes**: Detailed explanations in `course-notes/`
- **Notebooks**: Hands-on practice in `notebooks/`
- **Exam Questions**: Scenario practice in `exam-questions/`
- **Labs**: End-to-end projects in `labs/`
