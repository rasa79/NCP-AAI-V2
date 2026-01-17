# Lab 4: Evaluation and Optimization

## Overview

In this lab, you'll implement comprehensive evaluation and optimization strategies for RAG systems. This intermediate-advanced lab introduces evaluation metrics, A/B testing frameworks, parameter tuning, and cost-performance optimization. You'll learn to measure RAG system quality, compare different configurations, and optimize for accuracy, latency, and cost trade-offs.

## Learning Objectives

- Implement evaluation pipelines for RAG systems (maps to exam objective 3.1: Evaluation Pipelines)
- Apply RAG-specific metrics (faithfulness, relevance, answer quality) (maps to exam objective 3.2: Evaluation Metrics)
- Design and execute A/B testing frameworks (maps to exam objective 3.3: A/B Testing)
- Tune parameters for accuracy-latency trade-offs (maps to exam objective 3.4: Parameter Tuning)
- Optimize costs while maintaining quality (maps to exam objective 3.5: Cost Optimization)
- Collect and integrate user feedback (maps to exam objective 3.6: Feedback Integration)

## Prerequisites

- Completed modules: Module 3 (Evaluation and Tuning), Module 4 (Knowledge Integration)
- Completed Lab 1: Basic RAG Agent
- Required knowledge: RAG systems, evaluation metrics, statistical testing
- Estimated time: 4-5 hours

## Scenario

**Company:** OptimizeAI Labs, an AI performance consulting firm

**Challenge:** Your client has deployed a RAG system that works but has inconsistent quality and high operational costs. Users complain about slow responses and occasional irrelevant answers. The client needs to:
- Measure current system performance objectively
- Identify bottlenecks and quality issues
- Test different configurations systematically
- Optimize for 80% cost reduction while maintaining quality
- Establish continuous evaluation processes

**Your Task:** Build an evaluation and optimization framework that:
- Measures RAG system quality across multiple dimensions
- Implements automated evaluation pipelines
- Compares different system configurations via A/B testing
- Tunes parameters for optimal accuracy-latency-cost balance
- Provides actionable optimization recommendations
- Enables continuous monitoring and improvement

**Business Requirements:**
- Reduce operational costs by 80%
- Maintain answer quality (faithfulness > 0.8, relevance > 0.75)
- Reduce p95 latency to < 2 seconds
- Establish automated evaluation pipeline
- Provide data-driven optimization recommendations

**Technical Constraints:**
- Use standard RAG evaluation metrics (faithfulness, relevance, answer quality)
- Implement statistical significance testing for A/B tests
- Support multiple evaluation datasets
- Generate comprehensive evaluation reports
- Track cost metrics (inference cost, storage cost)

## Requirements

### Functional Requirements

1. **Evaluation Metrics Implementation**
   - Implement faithfulness scoring (answer grounded in context)
   - Implement relevance scoring (retrieved docs relevant to query)
   - Implement answer quality scoring (completeness, correctness)
   - Implement latency measurement
   - Implement cost tracking

2. **Evaluation Pipeline**
   - Load evaluation datasets
   - Run RAG system on test queries
   - Compute all metrics automatically
   - Generate evaluation reports
   - Support batch evaluation

3. **A/B Testing Framework**
   - Define system configurations (variants)
   - Run experiments with statistical rigor
   - Compute significance tests
   - Compare variants across metrics
   - Generate comparison reports

4. **Parameter Tuning**
   - Tune chunk size and overlap
   - Tune retrieval parameters (top-k, similarity threshold)
   - Tune generation parameters (temperature, max_tokens)
   - Tune embedding model selection
   - Find optimal parameter combinations

5. **Cost Optimization**
   - Track inference costs
   - Track storage costs
   - Identify cost drivers
   - Test cost-reduction strategies
   - Measure cost-quality trade-offs

6. **Reporting and Visualization**
   - Generate evaluation reports
   - Create performance visualizations
   - Show metric distributions
   - Display A/B test results
   - Provide optimization recommendations

### Performance Requirements

- Evaluation pipeline: < 5 minutes for 100 queries
- Metrics computation: < 100ms per query
- A/B test: Statistical significance with 95% confidence
- Cost tracking: Real-time cost accumulation

### Quality Requirements

- Metrics must be reproducible
- Statistical tests must be valid
- Reports must be comprehensive
- Visualizations must be clear
- Recommendations must be actionable

## Success Criteria

- [ ] All evaluation metrics implemented correctly
- [ ] Evaluation pipeline runs successfully
- [ ] A/B testing framework produces valid results
- [ ] Parameter tuning identifies optimal configurations
- [ ] Cost optimization achieves 80% reduction
- [ ] Reports are comprehensive and actionable
- [ ] All tests pass
- [ ] Optimization recommendations are data-driven

## Setup Instructions

### 1. Environment Setup

```bash
# Navigate to lab directory
cd labs/lab-04-evaluation-optimization

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import ragas, pandas, matplotlib; print('Setup successful!')"
```

### 2. Project Structure

```
lab-04-evaluation-optimization/
├── README.md (this file)
├── requirements.txt
├── starter-code/
│   ├── evaluation/
│   │   ├── metrics.py (evaluation metrics)
│   │   ├── pipeline.py (evaluation pipeline)
│   │   └── datasets.py (dataset loading)
│   ├── optimization/
│   │   ├── ab_testing.py (A/B testing framework)
│   │   ├── parameter_tuning.py (parameter optimization)
│   │   └── cost_optimizer.py (cost optimization)
│   ├── reporting/
│   │   ├── report_generator.py (report generation)
│   │   └── visualizations.py (charts and plots)
│   └── utils.py (helper functions)
├── test-data/
│   ├── eval_dataset_100.json (100 test queries)
│   ├── eval_dataset_500.json (500 test queries)
│   └── ground_truth.json (reference answers)
├── solution/
│   └── [reference implementation]
└── rubric.md (evaluation criteria)
```

## Starter Code

The starter code provides scaffolding for:

- **`evaluation/metrics.py`**: Metric implementations
- **`evaluation/pipeline.py`**: Automated evaluation pipeline
- **`optimization/ab_testing.py`**: A/B testing framework
- **`optimization/parameter_tuning.py`**: Parameter tuning utilities
- **`optimization/cost_optimizer.py`**: Cost optimization strategies
- **`reporting/`**: Report generation and visualization

## Implementation Tasks

### Task 1: Implement Evaluation Metrics (60 minutes)

Implement metrics in `evaluation/metrics.py`:

**Metrics to Implement:**

1. **Faithfulness Score**
   - Measures if answer is grounded in retrieved context
   - Use LLM to verify claims against context
   - Score: 0.0 (not faithful) to 1.0 (fully faithful)

2. **Relevance Score**
   - Measures if retrieved documents are relevant to query
   - Use semantic similarity or LLM judgment
   - Score: 0.0 (irrelevant) to 1.0 (highly relevant)

3. **Answer Quality Score**
   - Measures completeness and correctness
   - Compare against ground truth (if available)
   - Use BLEU, ROUGE, or LLM-based scoring
   - Score: 0.0 (poor) to 1.0 (excellent)

4. **Latency Metrics**
   - Measure end-to-end latency
   - Break down by component (retrieval, generation)
   - Track p50, p95, p99 percentiles

5. **Cost Metrics**
   - Track inference API costs
   - Track storage costs
   - Calculate cost per query

**Hints:**
- Use Ragas library for RAG-specific metrics
- Implement custom metrics where needed
- Cache LLM calls for efficiency
- Handle edge cases (empty results, errors)

**Validation:**
```python
from evaluation.metrics import evaluate_response

result = evaluate_response(
    query="What is RAG?",
    answer="RAG combines retrieval and generation...",
    context=["RAG is a technique that..."],
    ground_truth="RAG stands for..."
)
print(f"Faithfulness: {result['faithfulness']}")
print(f"Relevance: {result['relevance']}")
print(f"Quality: {result['quality']}")
```

### Task 2: Build Evaluation Pipeline (45 minutes)

Implement pipeline in `evaluation/pipeline.py`:

**Pipeline Steps:**
1. Load evaluation dataset
2. For each query:
   - Run RAG system
   - Collect response and metadata
   - Compute all metrics
3. Aggregate results
4. Generate summary statistics
5. Save detailed results

**Hints:**
- Support batch processing
- Add progress tracking
- Handle errors gracefully
- Save intermediate results
- Support resume from checkpoint

**Validation:**
```python
from evaluation.pipeline import EvaluationPipeline

pipeline = EvaluationPipeline(rag_system)
results = pipeline.run("test-data/eval_dataset_100.json")
print(f"Average faithfulness: {results['avg_faithfulness']}")
print(f"Average latency: {results['avg_latency_ms']}ms")
```

### Task 3: Implement A/B Testing Framework (60 minutes)

Implement A/B testing in `optimization/ab_testing.py`:

**Framework Features:**
- Define system variants (A, B, C, ...)
- Run experiments with random assignment
- Collect metrics for each variant
- Compute statistical significance
- Generate comparison reports

**Statistical Tests:**
- T-test for continuous metrics (latency, scores)
- Chi-square for categorical metrics
- Confidence intervals (95%)
- Effect size calculation

**Hints:**
- Use scipy.stats for statistical tests
- Ensure sufficient sample size
- Control for confounding variables
- Validate assumptions (normality, etc.)

**Validation:**
```python
from optimization.ab_testing import ABTest

# Define variants
variant_a = {"chunk_size": 500, "top_k": 3}
variant_b = {"chunk_size": 1000, "top_k": 5}

# Run A/B test
test = ABTest(rag_system, variants=[variant_a, variant_b])
results = test.run("test-data/eval_dataset_100.json")
print(f"Winner: {results['winner']}")
print(f"P-value: {results['p_value']}")
```

### Task 4: Parameter Tuning (60 minutes)

Implement tuning in `optimization/parameter_tuning.py`:

**Parameters to Tune:**
- Chunk size: [250, 500, 750, 1000]
- Chunk overlap: [50, 100, 150, 200]
- Top-k: [1, 3, 5, 7, 10]
- Similarity threshold: [0.5, 0.6, 0.7, 0.8]
- Temperature: [0.0, 0.3, 0.5, 0.7]
- Max tokens: [256, 512, 1024]

**Tuning Strategies:**
- Grid search (exhaustive)
- Random search (sampling)
- Bayesian optimization (efficient)

**Hints:**
- Start with grid search on key parameters
- Use random search for large spaces
- Track all experiments
- Visualize parameter impact
- Find Pareto-optimal configurations

**Validation:**
```python
from optimization.parameter_tuning import ParameterTuner

tuner = ParameterTuner(rag_system)
best_params = tuner.tune(
    param_grid={
        "chunk_size": [500, 1000],
        "top_k": [3, 5]
    },
    eval_dataset="test-data/eval_dataset_100.json",
    metric="faithfulness"
)
print(f"Best parameters: {best_params}")
```

### Task 5: Cost Optimization (45 minutes)

Implement cost optimization in `optimization/cost_optimizer.py`:

**Cost Reduction Strategies:**
1. Reduce chunk size (less storage, faster retrieval)
2. Reduce top-k (fewer documents, faster generation)
3. Use smaller embedding model
4. Cache frequent queries
5. Batch processing
6. Use cheaper LLM for simple queries

**Cost Tracking:**
- Inference API costs (per token)
- Storage costs (per GB)
- Compute costs (per hour)

**Hints:**
- Model costs accurately
- Test each strategy independently
- Measure quality impact
- Find optimal cost-quality balance
- Generate cost-benefit analysis

**Validation:**
```python
from optimization.cost_optimizer import CostOptimizer

optimizer = CostOptimizer(rag_system)
recommendations = optimizer.optimize(
    current_cost=1000,  # $1000/month
    target_cost=200,    # $200/month
    min_quality=0.8     # Maintain 0.8 faithfulness
)
print(f"Recommendations: {recommendations}")
```

### Task 6: Reporting and Visualization (30 minutes)

Implement reporting in `reporting/`:

**Reports to Generate:**
1. Evaluation summary report
2. A/B test comparison report
3. Parameter tuning results
4. Cost optimization recommendations
5. Performance visualizations

**Visualizations:**
- Metric distributions (histograms)
- Latency percentiles (line charts)
- A/B test comparisons (bar charts)
- Parameter impact (heatmaps)
- Cost-quality trade-offs (scatter plots)

**Hints:**
- Use matplotlib/seaborn for plots
- Generate PDF reports
- Include executive summary
- Make recommendations actionable
- Add confidence intervals

**Validation:**
```python
from reporting.report_generator import ReportGenerator

generator = ReportGenerator()
generator.generate_evaluation_report(
    results=eval_results,
    output_path="evaluation_report.pdf"
)
```

## Testing

### Manual Testing

Test your evaluation framework:

1. Run evaluation on small dataset (10 queries)
2. Verify metrics are reasonable
3. Run A/B test with two variants
4. Check statistical significance
5. Run parameter tuning
6. Generate reports

### Automated Testing

```bash
# Run validation tests
python tests/test_evaluation.py

# Expected output:
# ✓ Metrics computation test passed
# ✓ Evaluation pipeline test passed
# ✓ A/B testing test passed
# ✓ Parameter tuning test passed
# ✓ Cost optimization test passed
# ✓ Reporting test passed
```

## Evaluation Rubric

See `rubric.md` for detailed evaluation criteria.

**Summary:**
- Functionality (40%): Do all components work correctly?
- Code Quality (20%): Is it well-structured and documented?
- Performance (15%): Does it meet efficiency requirements?
- Statistical Rigor (10%): Are tests valid?
- Best Practices (15%): Does it follow evaluation best practices?

## Common Issues and Troubleshooting

### Issue: Metrics are inconsistent
**Solution:**
- Check for randomness in LLM calls
- Use temperature=0 for deterministic scoring
- Cache metric computations
- Verify ground truth quality

### Issue: A/B test shows no significance
**Solution:**
- Increase sample size
- Check if variants are actually different
- Verify metric sensitivity
- Review statistical assumptions

### Issue: Parameter tuning is slow
**Solution:**
- Use smaller evaluation dataset
- Implement parallel evaluation
- Use random search instead of grid search
- Cache intermediate results

### Issue: Cost optimization degrades quality
**Solution:**
- Relax quality constraints
- Try different optimization strategies
- Focus on high-impact changes
- Test incrementally

## Resources

### Relevant Course Notes
- Module 3: Evaluation and Tuning
- Module 4: Knowledge Integration (RAG optimization)

### Relevant Notebooks
- `notebooks/module-03/01-evaluation-metrics.ipynb`
- `notebooks/module-03/02-evaluation-pipelines.ipynb`
- `notebooks/module-03/03-ab-testing.ipynb`

### External Documentation
- [Ragas Documentation](https://docs.ragas.io/)
- [Statistical Testing in Python](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [RAG Evaluation Best Practices](https://www.anthropic.com/index/evaluating-rag-systems)

## Submission

When complete, ensure:
1. All metrics implemented and tested
2. Evaluation pipeline runs successfully
3. A/B testing produces valid results
4. Parameter tuning finds optimal configs
5. Cost optimization achieves targets
6. Reports are comprehensive
7. All tests pass

## Next Steps

After completing this lab:
- Review the reference solution
- Experiment with different metrics
- Try advanced optimization techniques
- Move on to Lab 5: Safe and Compliant Agent

