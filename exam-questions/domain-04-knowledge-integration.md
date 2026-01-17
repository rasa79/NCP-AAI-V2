# Domain 4: Knowledge Integration and Data Handling

**Exam Weight**: 10%  
**Number of Questions**: 10

---

### Question 1: Vector Database Selection

**Scenario:**
A company is building a RAG system for 10M documents (50GB total). They need fast semantic search (< 100ms), support for metadata filtering, and ability to update documents frequently. They're evaluating FAISS, Milvus, and Chroma.

**Requirements:**
- Handle 10M vectors efficiently
- Sub-100ms search latency
- Metadata filtering (date, category, author)
- Frequent updates (1000 docs/day)
- Horizontal scalability

**Question:** Which vector database best meets these requirements?

**Options:**

A) Milvus: distributed architecture supports 10M+ vectors, sub-100ms search with GPU acceleration, metadata filtering, supports updates, horizontally scalable.

B) FAISS: in-memory, fast search, but limited metadata filtering and no built-in distribution.

C) Chroma: good for prototyping but not optimized for 10M scale.

D) Elasticsearch with vector search plugin.

**Correct Answer:** A

**Explanation:**
**Milvus** designed for large-scale production: distributed architecture (scales horizontally), GPU acceleration (fast search), metadata filtering (hybrid search), supports CRUD operations (updates), persistent storage. **FAISS** (B) excellent for speed but in-memory (50GB RAM required), limited metadata support, no distribution. **Chroma** (C) better for smaller datasets. **Elasticsearch** (D) general-purpose, not optimized for vector search.

**NVIDIA Tools:** NVIDIA NIM for embedding generation, Milvus with GPU acceleration

**Exam Mapping:** Domain 4, Objective 4.2 (Configure and optimize vector databases)

**Key Concepts:** Vector databases, scalability, metadata filtering, distributed systems, Milvus vs FAISS

---

### Question 2: Chunking Strategy for RAG

**Scenario:**
A legal RAG system processes contracts (10-50 pages). Current approach uses fixed 512-token chunks, but retrieval quality is poor. Some chunks split mid-sentence, others combine unrelated sections.

**Requirements:**
- Maintain semantic coherence in chunks
- Preserve document structure (sections, clauses)
- Optimize chunk size for retrieval
- Handle varying document lengths

**Question:** What chunking strategy improves retrieval quality?

**Options:**

A) Semantic chunking: split by document structure (sections, clauses), maintain semantic boundaries, use sliding window with overlap for context, optimize chunk size (256-512 tokens) based on evaluation.

B) Fixed 512-token chunks with no overlap.

C) Split by sentences, one sentence per chunk.

D) Use entire document as single chunk.

**Correct Answer:** A

**Explanation:**
**Semantic chunking** preserves meaning: (1) Respect document structure (split at section boundaries), (2) Keep related content together (entire clause in one chunk), (3) Sliding window with overlap (128-token overlap provides context), (4) Optimize size (evaluate 256, 512, 1024 tokens). Fixed chunks (B) split arbitrarily. Sentence-level (C) too granular, loses context. Whole document (D) too large, poor retrieval precision.

**NVIDIA Tools:** NIM for embedding generation, LangChain for chunking utilities

**Exam Mapping:** Domain 4, Objective 4.1 (Implement retrieval pipelines)

**Key Concepts:** Chunking strategies, semantic boundaries, sliding windows, chunk size optimization

---

### Question 3: Hybrid Search Implementation

**Scenario:**
A technical documentation RAG system struggles with queries containing specific terms (product names, error codes). Semantic search misses exact matches. Users want both semantic similarity and keyword matching.

**Requirements:**
- Find semantically similar content
- Match exact keywords and phrases
- Combine both approaches effectively
- Rank results by relevance

**Question:** What retrieval approach combines semantic and keyword search?

**Options:**

A) Hybrid search: perform semantic search (vector similarity) and keyword search (BM25) in parallel, combine results using weighted scoring (e.g., 0.7×semantic + 0.3×keyword), rerank combined results.

B) Use only semantic search with better embeddings.

C) Use only keyword search (BM25).

D) Perform semantic search, then filter by keywords.

**Correct Answer:** A

**Explanation:**
**Hybrid search** leverages both: (1) Semantic search finds conceptually similar docs, (2) Keyword search finds exact matches, (3) Weighted combination (tune weights based on evaluation), (4) Reranking improves final ordering. Example: Query "GPU memory error 0x0001" → Semantic finds memory error docs, Keyword finds exact error code. Better embeddings (B) still miss exact matches. Keyword-only (C) misses semantic similarity. Sequential filtering (D) may miss relevant docs.

**NVIDIA Tools:** Milvus for hybrid search, NIM for embeddings

**Exam Mapping:** Domain 4, Objective 4.1 (Implement retrieval pipelines including hybrid approaches)

**Key Concepts:** Hybrid search, semantic search, keyword search, BM25, result fusion, reranking

---

### Question 4: Embedding Model Selection

**Scenario:**
A multilingual customer support system needs embeddings for 20 languages. Current English-only model performs poorly on non-English queries. They need embeddings that work across languages.

**Requirements:**
- Support 20 languages
- Maintain quality across languages
- Enable cross-lingual search (query in English, find Spanish docs)
- Reasonable inference cost

**Question:** What embedding approach works for multilingual support?

**Options:**

A) Use multilingual embedding model (e.g., multilingual-e5, LaBSE) that maps all languages to shared embedding space, enabling cross-lingual search.

B) Train separate embedding model for each language.

C) Translate all content to English, use English embeddings.

D) Use language-specific models, search only within same language.

**Correct Answer:** A

**Explanation:**
**Multilingual embeddings** map all languages to shared space: query in English finds semantically similar Spanish docs. Models like multilingual-e5 trained on parallel corpora. Single model (simpler deployment), cross-lingual capability (key requirement). Separate models (B) can't do cross-lingual search. Translation (C) loses nuance, expensive. Language-specific (D) no cross-lingual search.

**NVIDIA Tools:** NIM for multilingual embedding models

**Exam Mapping:** Domain 4, Objective 4.1 (Implement retrieval pipelines)

**Key Concepts:** Multilingual embeddings, cross-lingual search, embedding spaces, multilingual models

---

### Question 5: Data Quality and Preprocessing

**Scenario:**
A RAG system ingests documents from multiple sources with inconsistent formatting, OCR errors, duplicate content, and missing metadata. Retrieval quality suffers from noisy data.

**Requirements:**
- Clean and normalize text
- Remove duplicates
- Fix OCR errors
- Enrich with metadata
- Validate data quality

**Question:** What data preprocessing pipeline ensures quality?

**Options:**

A) Multi-stage pipeline: (1) Text cleaning (remove special chars, normalize whitespace), (2) OCR correction (spell check, pattern matching), (3) Deduplication (content hashing), (4) Metadata extraction (NER for entities), (5) Quality validation (reject low-quality docs).

B) Use documents as-is to preserve original content.

C) Manually review and clean all documents.

D) Filter out documents with any errors.

**Correct Answer:** A

**Explanation:**
**Preprocessing pipeline** ensures quality: (1) **Cleaning**: normalize text, remove artifacts, (2) **OCR correction**: fix common errors (l→1, O→0), (3) **Deduplication**: hash-based detection (saves storage, improves retrieval), (4) **Metadata extraction**: NER for dates, names, locations, (5) **Validation**: reject docs with >20% errors. As-is (B) propagates errors. Manual review (C) doesn't scale. Filtering all errors (D) too strict.

**NVIDIA Tools:** NeMo for NER, NIM for text processing

**Exam Mapping:** Domain 4, Objective 4.4 (Conduct data quality checks, augmentation, preprocessing)

**Key Concepts:** Data preprocessing, OCR correction, deduplication, metadata extraction, quality validation

---

### Question 6: Real-Time Data Integration

**Scenario:**
A news aggregation RAG system must incorporate breaking news within minutes. Current batch update process runs hourly, causing stale results.

**Requirements:**
- Ingest new documents in real-time (< 5 min latency)
- Update vector database without downtime
- Handle high ingestion rate (100 docs/min during breaking news)
- Maintain search performance

**Question:** What architecture enables real-time updates?

**Options:**

A) Streaming pipeline: documents → message queue → embedding service → vector DB with incremental updates. Use vector DB that supports real-time inserts (Milvus, Pinecone).

B) Increase batch update frequency to every 5 minutes.

C) Rebuild entire vector database on each update.

D) Cache new documents, update database overnight.

**Correct Answer:** A

**Explanation:**
**Streaming architecture**: (1) Message queue (Kafka) buffers incoming docs, (2) Embedding service processes docs in parallel, (3) Vector DB incremental inserts (no rebuild), (4) Milvus supports real-time inserts without downtime. Handles bursts (queue buffers), maintains performance (incremental updates). Frequent batches (B) still have latency. Rebuild (C) too slow. Overnight updates (D) violate real-time requirement.

**NVIDIA Tools:** NIM for real-time embedding generation, Milvus for incremental updates

**Exam Mapping:** Domain 4, Objective 4.5 (Enable real-time access to structured and unstructured knowledge)

**Key Concepts:** Real-time ingestion, streaming pipelines, message queues, incremental updates

---

### Question 7: ETL Pipeline for Enterprise Data

**Scenario:**
A company needs RAG system accessing data from multiple sources: SQL databases (customer data), SharePoint (documents), Salesforce (CRM), Slack (conversations). Data must be synchronized daily.

**Requirements:**
- Extract from multiple sources
- Transform to common format
- Load into vector database
- Handle schema changes
- Schedule daily updates

**Question:** What ETL architecture handles multiple sources?

**Options:**

A) Build modular ETL pipeline: source-specific extractors → common transformation layer → vector database loader. Use orchestration tool (Airflow) for scheduling and error handling.

B) Write custom scripts for each source, run manually.

C) Use single connector that works with all sources.

D) Export all data to CSV, process manually.

**Correct Answer:** A

**Explanation:**
**Modular ETL**: (1) **Extractors**: SQL connector, SharePoint API, Salesforce API, Slack API, (2) **Transformation**: normalize to common schema, extract text, generate embeddings, (3) **Loader**: batch insert to vector DB, (4) **Orchestration**: Airflow schedules daily runs, handles failures, retries. Modular design (easy to add sources). Custom scripts (B) hard to maintain. Single connector (C) doesn't exist for all sources. Manual CSV (D) doesn't scale.

**NVIDIA Tools:** NIM for embedding generation in ETL pipeline

**Exam Mapping:** Domain 4, Objective 4.3 (Build ETL pipelines for enterprise data integration)

**Key Concepts:** ETL pipelines, data integration, orchestration, Airflow, modular architecture

---

### Question 8: Retrieval Optimization

**Scenario:**
A RAG system retrieves top-10 documents but only top-3 are relevant. Retrieval recall is good (relevant docs are in top-100) but precision is poor (many irrelevant in top-10).

**Requirements:**
- Improve top-K precision
- Maintain recall
- Reduce irrelevant retrievals
- Optimize for user experience

**Question:** What technique improves retrieval precision?

**Options:**

A) Implement reranking: retrieve top-100 with fast first-stage retrieval, rerank with cross-encoder model to get best top-10, use reranked results for generation.

B) Retrieve only top-3 documents.

C) Use better embedding model.

D) Increase chunk overlap.

**Correct Answer:** A

**Explanation:**
**Two-stage retrieval**: (1) **First stage**: Fast retrieval (bi-encoder) gets top-100 candidates (high recall), (2) **Reranking**: Cross-encoder scores query-document pairs (more accurate but slower), (3) **Final**: Top-10 after reranking (high precision). Reranking improves precision without sacrificing recall. Top-3 only (B) may miss relevant docs. Better embeddings (C) help but reranking more effective. Chunk overlap (D) doesn't address precision.

**NVIDIA Tools:** NIM for embedding and reranking models, TensorRT-LLM for fast reranking

**Exam Mapping:** Domain 4, Objective 4.1 (Implement retrieval pipelines), 4.6 (Optimize retrieval)

**Key Concepts:** Reranking, two-stage retrieval, cross-encoders, precision vs recall

---

### Question 9: Handling Structured and Unstructured Data

**Scenario:**
A product support RAG system needs both unstructured data (manuals, FAQs) and structured data (product specs, pricing tables). Current system only handles unstructured text.

**Requirements:**
- Query both unstructured and structured data
- Combine information from both sources
- Handle table data effectively
- Provide accurate structured information

**Question:** What approach integrates structured and unstructured data?

**Options:**

A) Hybrid approach: (1) Vector search for unstructured text, (2) SQL queries for structured data, (3) LLM decides which source(s) to query based on question, (4) Combine results in generation.

B) Convert all structured data to text, use vector search only.

C) Use only structured data in SQL database.

D) Maintain separate systems, let users choose which to query.

**Correct Answer:** A

**Explanation:**
**Hybrid data access**: (1) **Routing**: LLM analyzes query ("What's the price of Model X?" → structured, "How do I install Model X?" → unstructured), (2) **Retrieval**: Query appropriate source(s), (3) **Combination**: LLM synthesizes from both sources. Example: "Compare prices and features" → SQL for prices, vector search for feature descriptions. Text conversion (B) loses structure (tables). SQL-only (C) misses unstructured knowledge. Separate systems (D) poor UX.

**NVIDIA Tools:** NIM for LLM routing and generation, NeMo Agent Toolkit for tool orchestration

**Exam Mapping:** Domain 4, Objective 4.5 (Enable real-time access to structured and unstructured knowledge)

**Key Concepts:** Hybrid data access, structured vs unstructured data, query routing, data integration

---

### Question 10: Document Update and Versioning

**Scenario:**
A compliance RAG system references regulations that change over time. Users need current regulations but also historical versions for auditing. System must track document versions and retrieve correct version.

**Requirements:**
- Store multiple document versions
- Retrieve current version by default
- Support historical queries ("What was the regulation in 2022?")
- Track version metadata (date, changes)

**Question:** What versioning approach meets these requirements?

**Options:**

A) Version-aware storage: store each document version with metadata (version number, effective date, superseded date), index all versions in vector DB with version metadata, query filters by date to retrieve correct version.

B) Keep only current version, archive old versions separately.

C) Store all versions in single document with version markers.

D) Overwrite old versions with new versions.

**Correct Answer:** A

**Explanation:**
**Version-aware system**: (1) **Storage**: Each version as separate document with metadata (v1.0, effective: 2022-01-01, superseded: 2023-01-01), (2) **Indexing**: All versions in vector DB, (3) **Querying**: Default filter (superseded_date = null) gets current, historical query filters by effective_date, (4) **Metadata**: Track changes, reasons. Separate archive (B) complicates retrieval. Single document (C) confuses retrieval. Overwriting (D) loses history.

**NVIDIA Tools:** Milvus with metadata filtering for version queries

**Exam Mapping:** Domain 4, Objective 4.3 (Build ETL pipelines), 4.4 (Data quality checks)

**Key Concepts:** Document versioning, metadata filtering, historical queries, compliance requirements

---

**End of Domain 4 Questions**

**Summary:**
- Total Questions: 10
- Domain Weight: 10%
- Topics Covered: Vector database selection, chunking strategies, hybrid search, embedding models, data preprocessing, real-time integration, ETL pipelines, retrieval optimization, structured/unstructured data, document versioning


---

## Study Resources

To prepare for these questions, review:

**Course Notes:** [Module 04 Knowledge Integration](../../course-notes/module-04-knowledge-integration.md)

**Practice Notebooks:**
- [01 Rag Fundamentals](../../notebooks/module-04/01-rag-fundamentals.ipynb)
- [03 Vector Stores](../../notebooks/module-04/03-vector-stores.ipynb)
