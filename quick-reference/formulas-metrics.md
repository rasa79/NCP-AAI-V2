# Formulas and Metrics Reference

## Evaluation Metrics

### Retrieval Metrics

#### Precision
**Formula**: `Precision = TP / (TP + FP)`

**Definition**: Proportion of retrieved documents that are relevant

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: When false positives are costly (e.g., legal document retrieval)

**Example**: Retrieved 10 docs, 7 relevant → Precision = 7/10 = 0.70

---

#### Recall
**Formula**: `Recall = TP / (TP + FN)`

**Definition**: Proportion of relevant documents that were retrieved

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: When missing relevant docs is costly (e.g., medical research)

**Example**: 7 retrieved, 10 total relevant → Recall = 7/10 = 0.70

---

#### F1 Score
**Formula**: `F1 = 2 × (Precision × Recall) / (Precision + Recall)`

**Definition**: Harmonic mean of precision and recall

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: Balanced evaluation when both precision and recall matter

**Example**: Precision=0.70, Recall=0.70 → F1 = 2×(0.70×0.70)/(0.70+0.70) = 0.70

---

#### Mean Reciprocal Rank (MRR)
**Formula**: `MRR = (1/|Q|) × Σ(1/rank_i)`

**Definition**: Average of reciprocal ranks of first relevant document

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: When position of first relevant result matters (e.g., search engines)

**Example**: First relevant at positions [1, 3, 2] → MRR = (1/1 + 1/3 + 1/2)/3 = 0.61

---

#### Normalized Discounted Cumulative Gain (NDCG)
**Formula**: `NDCG@k = DCG@k / IDCG@k`

Where: `DCG@k = Σ(rel_i / log₂(i+1))` for i=1 to k

**Definition**: Measures ranking quality with position-based discounting

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: When ranking order matters with graded relevance

**Example**: Relevance scores [3,2,3,0,1] → Calculate DCG and normalize by ideal DCG

---

### Generation Metrics

#### BLEU (Bilingual Evaluation Understudy)
**Formula**: `BLEU = BP × exp(Σ w_n × log(p_n))`

Where:
- `BP` = Brevity penalty
- `p_n` = n-gram precision
- `w_n` = weights (typically 1/4 for 1-4 grams)

**Definition**: Measures n-gram overlap between generated and reference text

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: Machine translation, text generation quality

**Note**: Sensitive to exact word matches, may miss semantic similarity

---

#### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
**Variants**:
- **ROUGE-N**: N-gram overlap (typically ROUGE-1, ROUGE-2)
- **ROUGE-L**: Longest common subsequence
- **ROUGE-S**: Skip-bigram overlap

**Formula (ROUGE-N)**: `ROUGE-N = Σ Count_match(n-gram) / Σ Count(n-gram)`

**Definition**: Measures recall of n-grams from reference in generated text

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: Summarization, content generation evaluation

---

#### Faithfulness
**Formula**: `Faithfulness = (# supported claims) / (# total claims)`

**Definition**: Proportion of generated claims supported by source documents

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: RAG systems, fact-checking, hallucination detection

**Measurement**: Typically requires LLM-based evaluation or human annotation

---

#### Answer Relevance
**Formula**: `Answer Relevance = cosine_similarity(question_embedding, answer_embedding)`

**Definition**: Semantic similarity between question and generated answer

**Range**: -1.0 to 1.0 (higher is better, typically 0.0 to 1.0 for normalized)

**Use Case**: Question answering systems, conversational agents

**Measurement**: Uses embedding models (e.g., sentence-transformers)

---

#### Context Precision
**Formula**: `Context Precision@k = (# relevant chunks in top-k) / k`

**Definition**: Proportion of retrieved context that is relevant to the query

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: RAG retrieval quality assessment

---

#### Context Recall
**Formula**: `Context Recall = (# ground truth facts in context) / (# total ground truth facts)`

**Definition**: Proportion of required information present in retrieved context

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: Ensuring sufficient information retrieval for answer generation

---

## Performance Metrics

### Latency Metrics

#### Mean Latency
**Formula**: `Mean Latency = Σ(latency_i) / n`

**Definition**: Average response time across all requests

**Unit**: milliseconds (ms) or seconds (s)

**Use Case**: Overall system performance assessment

---

#### Percentile Latency
**Formulas**:
- **p50 (Median)**: 50% of requests complete faster
- **p95**: 95% of requests complete faster
- **p99**: 99% of requests complete faster

**Definition**: Latency threshold for given percentage of requests

**Unit**: milliseconds (ms) or seconds (s)

**Use Case**: SLA definition, tail latency analysis

**Example**: p95 = 500ms means 95% of requests complete within 500ms

---

#### Time to First Token (TTFT)
**Formula**: `TTFT = time_first_token - time_request_received`

**Definition**: Time from request to first generated token

**Unit**: milliseconds (ms)

**Use Case**: Streaming response quality, user experience

**Target**: < 200ms for interactive applications

---

#### Time Per Output Token (TPOT)
**Formula**: `TPOT = (total_generation_time - TTFT) / (num_tokens - 1)`

**Definition**: Average time to generate each subsequent token

**Unit**: milliseconds per token (ms/token)

**Use Case**: Generation speed optimization

---

### Throughput Metrics

#### Requests Per Second (RPS)
**Formula**: `RPS = total_requests / time_period`

**Definition**: Number of requests processed per second

**Unit**: requests/second

**Use Case**: System capacity planning, load testing

---

#### Tokens Per Second (TPS)
**Formula**: `TPS = total_tokens_generated / total_time`

**Definition**: Token generation rate

**Unit**: tokens/second

**Use Case**: Model inference optimization, hardware utilization

**Typical Values**:
- CPU: 10-50 tokens/sec
- GPU (T4): 50-200 tokens/sec
- GPU (A100): 200-1000+ tokens/sec

---

#### Queries Per Second (QPS)
**Formula**: `QPS = total_queries / time_period`

**Definition**: Query processing rate for retrieval systems

**Unit**: queries/second

**Use Case**: Vector database performance, retrieval optimization

---

### Resource Utilization

#### GPU Utilization
**Formula**: `GPU Util = (active_time / total_time) × 100%`

**Definition**: Percentage of time GPU is actively computing

**Range**: 0% to 100%

**Target**: > 80% for efficient resource usage

---

#### Memory Utilization
**Formula**: `Memory Util = (used_memory / total_memory) × 100%`

**Definition**: Percentage of available memory in use

**Range**: 0% to 100%

**Warning**: > 90% may cause OOM errors

---

#### Batch Efficiency
**Formula**: `Batch Efficiency = actual_throughput / (max_throughput × batch_size)`

**Definition**: How efficiently batching improves throughput

**Range**: 0.0 to 1.0 (higher is better)

**Use Case**: Optimizing batch size for inference

---

## Cost Metrics

### Inference Cost Per Request
**Formula**: `Cost Per Request = (compute_cost_per_hour / requests_per_hour)`

**Definition**: Average cost to process one request

**Unit**: USD per request

**Components**:
- Compute cost (GPU/CPU hours)
- Storage cost (vector database)
- Network cost (data transfer)

---

### Cost Per Token
**Formula**: `Cost Per Token = total_cost / total_tokens_generated`

**Definition**: Cost to generate one token

**Unit**: USD per token (often expressed as USD per 1M tokens)

**Use Case**: Model selection, cost optimization

**Typical Values**:
- GPT-4: $0.03-0.06 per 1K tokens
- GPT-3.5: $0.001-0.002 per 1K tokens
- Open source (self-hosted): Variable based on infrastructure

---

### Total Cost of Ownership (TCO)
**Formula**: `TCO = Infrastructure + Operations + Development + Maintenance`

**Components**:
- **Infrastructure**: Hardware, cloud services, storage
- **Operations**: Monitoring, support, incident response
- **Development**: Engineering time, model training
- **Maintenance**: Updates, retraining, optimization

**Unit**: USD per month/year

**Use Case**: Budget planning, ROI analysis

---

## Scaling Formulas

### Amdahl's Law
**Formula**: `Speedup = 1 / ((1 - P) + P/N)`

Where:
- `P` = Proportion of parallelizable work
- `N` = Number of processors

**Definition**: Maximum speedup from parallelization

**Use Case**: Estimating benefits of distributed processing

**Example**: 90% parallelizable, 10 processors → Speedup = 1/(0.1 + 0.9/10) = 5.26×

---

### Little's Law
**Formula**: `L = λ × W`

Where:
- `L` = Average number of items in system
- `λ` = Average arrival rate
- `W` = Average time in system

**Definition**: Relationship between throughput, latency, and concurrency

**Use Case**: Capacity planning, queue sizing

**Example**: 100 req/sec, 0.5 sec latency → Need 50 concurrent workers

---

### Scaling Efficiency
**Formula**: `Efficiency = (Speedup / N) × 100%`

Where:
- `Speedup` = Performance improvement
- `N` = Number of resources added

**Definition**: How efficiently additional resources improve performance

**Range**: 0% to 100%

**Target**: > 70% for good scaling

---

## Quick Reference Table

| Metric | Formula | Range | Higher is Better? |
|--------|---------|-------|-------------------|
| Precision | TP/(TP+FP) | 0-1 | ✓ |
| Recall | TP/(TP+FN) | 0-1 | ✓ |
| F1 Score | 2PR/(P+R) | 0-1 | ✓ |
| MRR | Avg(1/rank) | 0-1 | ✓ |
| NDCG | DCG/IDCG | 0-1 | ✓ |
| BLEU | n-gram overlap | 0-1 | ✓ |
| ROUGE | recall overlap | 0-1 | ✓ |
| Faithfulness | supported/total | 0-1 | ✓ |
| Latency (p95) | Time threshold | ms | ✗ |
| Throughput | Requests/sec | req/s | ✓ |
| GPU Util | Active/total | 0-100% | ✓ |
| Cost/Request | Total cost/requests | USD | ✗ |

## Exam Tips

**Memorize These**:
- F1 = harmonic mean of precision and recall
- BLEU = n-gram precision with brevity penalty
- ROUGE = n-gram recall
- Faithfulness = claims supported by sources
- p95 latency = 95% of requests complete within this time

**Common Traps**:
- Precision vs Recall: Precision = "of retrieved, how many relevant?" Recall = "of relevant, how many retrieved?"
- BLEU vs ROUGE: BLEU = precision-focused, ROUGE = recall-focused
- Mean vs Percentile: Mean can hide tail latency issues, use p95/p99 for SLAs

**Calculation Practice**:
- Practice calculating F1 from precision/recall
- Understand when to use each metric
- Know typical values for production systems
