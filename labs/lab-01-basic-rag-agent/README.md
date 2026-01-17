# Lab 1: Basic RAG Agent

## Overview

In this lab, you'll build a document question-answering agent for research papers using Retrieval-Augmented Generation (RAG). This foundational lab introduces core RAG concepts including document processing, embedding generation, vector storage, semantic retrieval, and LLM-based answer generation. You'll implement a production-ready RAG pipeline with proper error handling and evaluation.

## Learning Objectives

- Implement a complete RAG pipeline from document ingestion to answer generation (maps to exam objective 4.1: Knowledge Integration)
- Configure and optimize vector databases for semantic search (maps to exam objective 4.2: Vector Store Configuration)
- Apply chunking strategies for document processing (maps to exam objective 4.3: Data Preprocessing)
- Integrate embedding models for semantic representation (maps to exam objective 4.4: Embedding Models)
- Implement error handling patterns for production systems (maps to exam objective 2.3: Error Handling)
- Evaluate RAG system performance using standard metrics (maps to exam objective 3.1: Evaluation Pipelines)

## Prerequisites

- Completed modules: Module 1 (Agent Architecture), Module 2 (Agent Development), Module 4 (Knowledge Integration)
- Required knowledge: Python programming, basic understanding of embeddings and vector similarity
- Estimated time: 3-4 hours

## Scenario

**Company:** TechResearch Inc., a technology research firm

**Challenge:** Your team receives hundreds of research papers monthly across AI, cloud computing, and cybersecurity domains. Researchers spend significant time manually searching through papers to find relevant information for their projects. The current keyword-based search system produces too many irrelevant results and misses papers with relevant concepts expressed differently.

**Your Task:** Build an intelligent document Q&A agent that can:
- Understand natural language questions about research topics
- Retrieve relevant information from a corpus of research papers
- Generate accurate, contextual answers grounded in the source documents
- Cite sources and provide confidence indicators
- Handle edge cases gracefully (no relevant documents, ambiguous questions, etc.)

**Business Requirements:**
- Response time: < 5 seconds per query
- Accuracy: Answers must be grounded in source documents (no hallucinations)
- Scalability: Support corpus of 100+ research papers
- Usability: Simple API interface for integration with existing tools

**Technical Constraints:**
- Use open-source embedding models (sentence-transformers)
- Use FAISS for vector storage (lightweight, no external dependencies)
- Use LangChain for RAG orchestration
- Include comprehensive error handling and logging

## Requirements

### Functional Requirements

1. **Document Ingestion**
   - Load research papers from text files
   - Split documents into semantically meaningful chunks (500-1000 tokens)
   - Generate embeddings for each chunk
   - Store embeddings in FAISS vector database

2. **Query Processing**
   - Accept natural language questions
   - Generate query embeddings
   - Retrieve top-k most relevant document chunks (k=3-5)
   - Rerank results if needed for improved relevance

3. **Answer Generation**
   - Generate answers using retrieved context
   - Ground answers in source documents (no hallucination)
   - Include source citations with document names and chunk IDs
   - Provide confidence scores or indicators

4. **Error Handling**
   - Handle missing or corrupted documents gracefully
   - Handle queries with no relevant results
   - Handle embedding generation failures
   - Handle LLM API failures with retry logic

### Performance Requirements

- Query latency: < 5 seconds (end-to-end)
- Retrieval precision: > 0.7 for relevant documents
- Answer faithfulness: > 0.8 (answers grounded in context)

### Quality Requirements

- Code must include comprehensive error handling (try-except blocks)
- Code must include logging for debugging
- Code must include type hints for function signatures
- Code must include docstrings for all functions
- Code must follow PEP 8 style guidelines

## Success Criteria

- [ ] Document ingestion pipeline successfully processes all test papers
- [ ] Vector database is created and populated with embeddings
- [ ] Query processing retrieves relevant document chunks
- [ ] Answer generation produces accurate, grounded responses
- [ ] All error handling paths are tested and functional
- [ ] Evaluation metrics meet minimum thresholds (precision > 0.7, faithfulness > 0.8)
- [ ] Code includes comprehensive comments and documentation
- [ ] All test queries produce valid responses within latency requirements

## Setup Instructions

### 1. Environment Setup

```bash
# Navigate to lab directory
cd labs/lab-01-basic-rag-agent

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import langchain, sentence_transformers, faiss; print('Setup successful!')"
```

### 2. Test Data Setup

The `test-data/` directory contains sample research papers:
- `paper_01_transformers.txt` - Attention mechanisms and transformers
- `paper_02_rag_systems.txt` - RAG architectures and best practices
- `paper_03_vector_databases.txt` - Vector database comparison
- `paper_04_llm_evaluation.txt` - LLM evaluation methodologies
- `paper_05_prompt_engineering.txt` - Prompt engineering techniques

### 3. Project Structure

```
lab-01-basic-rag-agent/
├── README.md (this file)
├── requirements.txt
├── starter-code/
│   ├── rag_agent.py (main implementation - YOUR WORK HERE)
│   ├── document_processor.py (document loading and chunking)
│   ├── embeddings.py (embedding generation)
│   ├── retriever.py (vector search)
│   ├── generator.py (answer generation)
│   └── utils.py (helper functions)
├── solution/
│   └── [reference implementation - DO NOT LOOK UNTIL COMPLETE]
├── test-data/
│   └── [research papers]
├── tests/
│   └── test_rag_agent.py (validation tests)
└── rubric.md (evaluation criteria)
```

## Starter Code

The starter code provides scaffolding for the main components:

- **`rag_agent.py`**: Main RAG agent class with method stubs
- **`document_processor.py`**: Document loading and chunking utilities
- **`embeddings.py`**: Embedding model wrapper
- **`retriever.py`**: Vector database and retrieval logic
- **`generator.py`**: LLM integration for answer generation
- **`utils.py`**: Logging, error handling, and helper functions

Your task is to implement the core logic in each module following the TODO comments.

## Implementation Tasks

### Task 1: Document Processing (30 minutes)

Implement document loading and chunking in `document_processor.py`:

**Hints:**
- Use LangChain's `TextLoader` for file loading
- Use `RecursiveCharacterTextSplitter` for chunking
- Chunk size: 500-1000 characters with 100-200 character overlap
- Preserve document metadata (filename, chunk_id)

**Validation:**
```python
from document_processor import DocumentProcessor
processor = DocumentProcessor()
chunks = processor.process_documents("test-data/")
print(f"Processed {len(chunks)} chunks")
```

### Task 2: Embedding Generation (30 minutes)

Implement embedding generation in `embeddings.py`:

**Hints:**
- Use `sentence-transformers` library
- Model: `all-MiniLM-L6-v2` (fast, good quality)
- Batch processing for efficiency
- Error handling for encoding failures

**Validation:**
```python
from embeddings import EmbeddingModel
model = EmbeddingModel()
embedding = model.encode("What are transformers?")
print(f"Embedding shape: {embedding.shape}")
```

### Task 3: Vector Database Setup (30 minutes)

Implement vector storage and retrieval in `retriever.py`:

**Hints:**
- Use FAISS IndexFlatL2 for exact search
- Store document metadata alongside vectors
- Implement top-k retrieval with configurable k
- Add similarity score thresholding

**Validation:**
```python
from retriever import VectorRetriever
retriever = VectorRetriever()
retriever.add_documents(chunks, embeddings)
results = retriever.search("What are transformers?", k=3)
print(f"Retrieved {len(results)} documents")
```

### Task 4: Answer Generation (45 minutes)

Implement answer generation in `generator.py`:

**Hints:**
- Use LangChain's prompt templates
- Include retrieved context in prompt
- Add source citations to answers
- Implement retry logic for API failures
- Use temperature=0 for deterministic outputs

**Validation:**
```python
from generator import AnswerGenerator
generator = AnswerGenerator()
answer = generator.generate(query="What are transformers?", context=retrieved_docs)
print(f"Answer: {answer}")
```

### Task 5: Integration and Error Handling (45 minutes)

Integrate all components in `rag_agent.py`:

**Hints:**
- Create RAGAgent class with `ingest()` and `query()` methods
- Add comprehensive error handling at each stage
- Implement logging for debugging
- Add input validation
- Handle edge cases (empty results, API failures, etc.)

**Validation:**
```python
from rag_agent import RAGAgent
agent = RAGAgent()
agent.ingest("test-data/")
answer = agent.query("What are the key components of RAG systems?")
print(answer)
```

### Task 6: Evaluation (30 minutes)

Run evaluation tests in `tests/test_rag_agent.py`:

**Hints:**
- Test with provided test queries
- Measure retrieval precision
- Measure answer faithfulness
- Measure query latency
- Verify error handling paths

**Validation:**
```bash
python tests/test_rag_agent.py
```

## Testing

### Manual Testing

Test your implementation with these queries:

1. "What are transformers and how do they work?"
2. "Compare different vector database options"
3. "What metrics should I use to evaluate RAG systems?"
4. "Explain prompt engineering best practices"
5. "How do I handle hallucinations in LLM outputs?"

Expected behavior:
- Each query returns a relevant answer
- Answers include source citations
- Queries complete within 5 seconds
- No crashes or unhandled exceptions

### Automated Testing

```bash
# Run validation tests
python tests/test_rag_agent.py

# Expected output:
# ✓ Document ingestion test passed
# ✓ Embedding generation test passed
# ✓ Retrieval test passed
# ✓ Answer generation test passed
# ✓ Error handling test passed
# ✓ Performance test passed
```

## Evaluation Rubric

See `rubric.md` for detailed evaluation criteria.

**Summary:**
- Functionality (40%): Does it work correctly?
- Code Quality (20%): Is it well-structured and documented?
- Performance (15%): Does it meet latency requirements?
- Error Handling (10%): Does it handle errors gracefully?
- Best Practices (15%): Does it follow RAG best practices?

## Common Issues and Troubleshooting

### Issue: "Module not found" errors
**Solution:** Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: Slow query performance
**Solution:** 
- Reduce chunk size or number of retrieved documents
- Use smaller embedding model
- Implement caching for repeated queries

### Issue: Low retrieval precision
**Solution:**
- Adjust chunk size and overlap
- Try different embedding models
- Implement hybrid search (semantic + keyword)
- Add reranking step

### Issue: Hallucinated answers
**Solution:**
- Lower LLM temperature (use 0 for deterministic)
- Improve prompt to emphasize grounding in context
- Add explicit instruction: "Only answer based on provided context"
- Implement faithfulness checking

### Issue: Out of memory errors
**Solution:**
- Process documents in batches
- Use smaller embedding model
- Reduce number of documents in corpus

## Resources

### Relevant Course Notes
- Module 4: Knowledge Integration (RAG fundamentals, vector stores, retrieval optimization)
- Module 2: Agent Development (error handling patterns, tool integration)
- Module 3: Evaluation and Tuning (evaluation metrics, performance optimization)

### Relevant Notebooks
- `notebooks/module-04/01-rag-fundamentals.ipynb`
- `notebooks/module-04/02-embedding-models.ipynb`
- `notebooks/module-04/03-vector-stores.ipynb`
- `notebooks/module-02/03-error-handling-patterns.ipynb`

### External Documentation
- [LangChain RAG Documentation](https://python.langchain.com/docs/use_cases/question_answering/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)
- [Sentence Transformers Documentation](https://www.sbert.net/)

## Submission

When complete, ensure:
1. All code is committed and documented
2. All tests pass
3. README includes any setup notes or known issues
4. Evaluation results are documented

## Next Steps

After completing this lab:
- Review the reference solution to compare approaches
- Experiment with different embedding models and chunk sizes
- Try implementing hybrid search (semantic + keyword)
- Move on to Lab 2: Multi-Agent Research System
