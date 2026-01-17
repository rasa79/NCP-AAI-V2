# Domain 3: Evaluation and Tuning

**Exam Weight**: 13%  
**Number of Questions**: 13

---

### Question 1: RAG Evaluation Metrics Selection

**Scenario:**
A legal research RAG system retrieves case law and generates summaries. The team needs to evaluate system quality before production. They must measure both retrieval quality (are relevant cases found?) and generation quality (are summaries accurate and complete?).

**Requirements:**
- Measure retrieval relevance
- Measure generation accuracy and faithfulness
- Detect hallucinations
- Quantify answer completeness

**Question:** What evaluation metrics best assess this RAG system?

**Options:**

A) Use retrieval metrics (Precision@K, Recall@K, MRR) for retrieval quality, and generation metrics (Faithfulness, Answer Relevance, Context Precision) for generation quality.

B) Use only BLEU and ROUGE scores to evaluate output quality.

C) Manually review 100 random outputs.

D) Measure user satisfaction scores only.

**Correct Answer:** A

**Explanation:**
Comprehensive RAG evaluation requires both retrieval and generation metrics. **Retrieval**: Precision@K (% of retrieved cases that are relevant), Recall@K (% of relevant cases retrieved), MRR (Mean Reciprocal Rank). **Generation**: Faithfulness (is answer grounded in retrieved context?), Answer Relevance (does answer address question?), Context Precision (is retrieved context relevant?). BLEU/ROUGE (B) only measure n-gram overlap, miss semantic quality. Manual review (C) not scalable. User satisfaction (D) important but insufficient for technical evaluation.

**NVIDIA Tools:** NVIDIA Agent Intelligence Toolkit for evaluation pipelines

**Exam Mapping:** Domain 3, Objectives 3.1 (Implement evaluation pipelines), 3.2 (Compare agent performance)

**Key Concepts:** RAG evaluation, retrieval metrics, generation metrics, faithfulness, hallucination detection

---

### Question 2: A/B Testing Framework Design

**Scenario:**
A customer service agent team wants to test two prompt variations: Prompt A (formal tone) vs Prompt B (friendly tone). They need to determine which produces better customer satisfaction while maintaining accuracy. They serve 10,000 customers daily.

**Requirements:**
- Statistically significant results
- Fair traffic distribution
- Track multiple metrics (satisfaction, accuracy, resolution time)
- Minimize risk of poor customer experience

**Question:** What A/B testing approach is most appropriate?

**Options:**

A) Implement randomized A/B test with 50/50 traffic split, track satisfaction scores, accuracy, and resolution time, run for 2 weeks to achieve statistical significance, use t-test to compare results.

B) Run Prompt A for 1 week, then Prompt B for 1 week, compare results.

C) Let customer service reps choose which prompt to use.

D) Deploy Prompt B to 10% of traffic for 1 day, then decide.

**Correct Answer:** A

**Explanation:**
Proper A/B testing requires: (1) Randomization (eliminates selection bias), (2) Concurrent running (controls for time-based factors), (3) Sufficient sample size (10K customers/day × 14 days = 140K total, 70K per variant = statistically significant), (4) Multiple metrics (holistic evaluation), (5) Statistical testing (t-test determines if difference is significant). Sequential testing (B) confounded by time. Manual selection (C) introduces bias. Short test (D) insufficient for significance.

**NVIDIA Tools:** Agent Intelligence Toolkit for A/B testing infrastructure

**Exam Mapping:** Domain 3, Objective 3.2 (Compare agent performance across tasks)

**Key Concepts:** A/B testing, randomization, statistical significance, sample size, concurrent testing

---

### Question 3: Cost-Performance Trade-off Optimization

**Scenario:**
A document summarization service uses GPT-4 (high quality, $0.03/1K tokens) and processes 1M documents/month (avg 5K tokens each), costing $150K/month. The company wants to reduce costs while maintaining acceptable quality (user satisfaction > 80%).

**Requirements:**
- Reduce costs significantly
- Maintain quality above 80% satisfaction
- Measure quality-cost trade-offs
- Support different quality tiers for different use cases

**Question:** What optimization strategy balances cost and quality?

**Options:**

A) Implement tiered approach: use smaller/cheaper model (GPT-3.5) for simple documents, GPT-4 for complex documents, with classifier routing documents based on complexity. Measure quality per tier and adjust thresholds.

B) Switch entirely to cheapest model available.

C) Reduce document length by truncating to 2K tokens.

D) Use GPT-4 but reduce output length to save tokens.

**Correct Answer:** A

**Explanation:**
Tiered approach optimizes cost-quality: (1) Train classifier to predict document complexity, (2) Route simple docs (70%) to GPT-3.5 ($0.002/1K tokens), complex docs (30%) to GPT-4, (3) Cost: 700K docs × 5K tokens × $0.002 + 300K docs × 5K tokens × $0.03 = $7K + $45K = $52K (65% reduction), (4) Measure satisfaction per tier, adjust routing if quality drops. Complete switch (B) may reduce quality below 80%. Truncation (C) loses information. Shorter output (D) may be incomplete.

**NVIDIA Tools:** TensorRT-LLM for cost-effective inference, NIM for model deployment

**Exam Mapping:** Domain 3, Objective 3.4 (Tune model parameters for accuracy vs latency trade-offs)

**Key Concepts:** Cost optimization, tiered models, routing strategies, quality-cost trade-offs

---

### Question 4: Evaluation Pipeline Automation

**Scenario:**
A development team releases agent updates weekly. They need automated evaluation to catch regressions before production. Manual testing takes 2 days and delays releases.

**Requirements:**
- Automated evaluation on every release
- Test multiple scenarios and edge cases
- Detect regressions quickly
- Integrate with CI/CD pipeline
- Generate evaluation reports

**Question:** What automated evaluation approach works best?

**Options:**

A) Build evaluation pipeline with test dataset, automated metrics computation, regression detection (compare to baseline), integration with CI/CD, and automated reports. Block deployment if metrics drop below thresholds.

B) Deploy to staging and manually test for 1 day.

C) Use LLM to evaluate LLM outputs automatically.

D) Deploy to production and monitor user complaints.

**Correct Answer:** A

**Explanation:**
Automated pipeline: (1) Curated test dataset (100+ scenarios), (2) Run agent on test set, (3) Compute metrics (accuracy, latency, cost), (4) Compare to baseline (previous version), (5) Flag regressions (>5% accuracy drop), (6) Generate report, (7) Block deployment if critical regression. Runs in CI/CD in <1 hour. Manual testing (B) slow. LLM-as-judge (C) useful but needs validation. Production monitoring (D) too late.

**NVIDIA Tools:** Agent Intelligence Toolkit for evaluation automation

**Exam Mapping:** Domain 3, Objective 3.1 (Implement evaluation pipelines and task benchmarks)

**Key Concepts:** Automated evaluation, CI/CD integration, regression detection, test datasets

---

### Question 5: Feedback Collection and Integration

**Scenario:**
A chatbot receives 1000 user interactions daily. The team wants to collect feedback to improve the agent but users rarely provide explicit feedback. They need scalable feedback collection.

**Requirements:**
- Collect feedback at scale
- Minimize user friction
- Capture both explicit and implicit feedback
- Use feedback for improvement

**Question:** What feedback strategy is most effective?

**Options:**

A) Implement multi-channel feedback: thumbs up/down buttons (explicit), track conversation abandonment and retry rates (implicit), periodic surveys (detailed), and use feedback to identify improvement areas and update training data.

B) Ask users to rate every response on 1-5 scale.

C) Manually call users to ask about their experience.

D) Only collect feedback when users complain.

**Correct Answer:** A

**Explanation:**
Multi-channel approach: (1) **Explicit**: Thumbs up/down (low friction, high volume), (2) **Implicit**: Abandonment (user leaves mid-conversation = poor experience), retry (user rephrases = agent didn't understand), (3) **Detailed**: Monthly survey (10% sample, detailed insights), (4) **Analysis**: Identify patterns (agent struggles with refund requests), (5) **Improvement**: Add refund examples to training data. Rating every response (B) creates friction. Manual calls (C) don't scale. Complaint-only (D) misses most issues.

**NVIDIA Tools:** Agent Intelligence Toolkit for feedback analysis

**Exam Mapping:** Domain 3, Objective 3.3 (Collect and integrate structured user feedback)

**Key Concepts:** Feedback collection, explicit vs implicit feedback, feedback analysis, continuous improvement

---

### Questions 6-13: Additional Evaluation Scenarios

### Question 6: Latency vs Accuracy Trade-offs

**Scenario:**
A real-time translation agent must balance translation quality with response time. Users tolerate max 2-second latency. Current model (99% accuracy, 5 seconds) too slow.

**Question:** What optimization approach balances latency and accuracy?

**Options:**

A) Use smaller model (95% accuracy, 1 second) for real-time, larger model for batch translation. Measure user satisfaction at different accuracy levels to find acceptable threshold.

B) Use largest model but optimize with TensorRT-LLM to reduce latency.

C) Reduce input length to speed up processing.

D) Use caching for common phrases.

**Correct Answer:** B (with A as alternative)

**Explanation:**
TensorRT-LLM can reduce latency 2-5x through optimization (quantization, kernel fusion). May achieve 99% accuracy in 1-2 seconds. If still too slow, tiered approach (A): real-time uses fast model, batch uses accurate model. Measure if 95% accuracy acceptable. Input reduction (C) loses context. Caching (D) helps but limited coverage.

**Key Concepts:** Latency optimization, accuracy trade-offs, model optimization, TensorRT-LLM

---

### Question 7: Benchmark Dataset Creation

**Scenario:**
A medical diagnosis agent needs evaluation dataset. Team must create representative test cases covering common and rare conditions.

**Question:** What dataset creation approach ensures comprehensive evaluation?

**Options:**

A) Create stratified dataset: common conditions (70%), uncommon (20%), rare (10%), edge cases (5%). Include ground truth diagnoses from medical experts. Ensure diversity in patient demographics and symptoms.

B) Use random sample of 100 patient cases.

C) Use only common conditions for testing.

D) Generate synthetic cases with LLM.

**Correct Answer:** A

**Explanation:**
Stratified sampling ensures coverage: common conditions (most volume), rare conditions (critical to catch), edge cases (test robustness). Expert-labeled ground truth ensures accuracy. Demographic diversity prevents bias. Random sample (B) may miss rare cases. Common-only (C) incomplete. Synthetic (D) may not reflect real complexity.

**Key Concepts:** Benchmark datasets, stratified sampling, ground truth, evaluation coverage

---

### Question 8: Detecting Model Degradation

**Scenario:**
A deployed agent's performance gradually declines over 3 months. Team needs to detect and diagnose degradation.

**Question:** What monitoring approach detects degradation?

**Options:**

A) Continuous monitoring: track key metrics (accuracy, latency, user satisfaction) over time, set up alerts for degradation trends, maintain holdout test set for periodic evaluation, investigate when metrics drop.

B) Re-evaluate monthly with full test suite.

C) Wait for user complaints.

D) Compare to competitor agents.

**Correct Answer:** A

**Explanation:**
Continuous monitoring detects degradation early: track metrics daily, use statistical process control to detect trends, alert when metrics drop >5%, investigate causes (data drift, API changes, model issues). Monthly evaluation (B) too infrequent. User complaints (C) too late. Competitor comparison (D) doesn't detect own degradation.

**Key Concepts:** Continuous monitoring, model degradation, drift detection, alerting

---

### Question 9: Multi-Metric Evaluation

**Scenario:**
An agent must be evaluated on accuracy, latency, cost, and user satisfaction. Metrics sometimes conflict (higher accuracy = higher latency).

**Question:** How should team balance multiple metrics?

**Options:**

A) Define weighted scoring function combining all metrics based on business priorities, set minimum thresholds for critical metrics, optimize for overall score while respecting constraints.

B) Optimize for accuracy only.

C) Optimize each metric separately.

D) Let users choose which metric to prioritize.

**Correct Answer:** A

**Explanation:**
Weighted scoring: Score = 0.4×Accuracy + 0.3×Satisfaction + 0.2×(1/Latency) + 0.1×(1/Cost). Weights reflect business priorities. Constraints: Accuracy > 90%, Latency < 3s. Optimize score within constraints. Single-metric (B) ignores trade-offs. Separate optimization (C) creates conflicts. User choice (D) impractical.

**Key Concepts:** Multi-objective optimization, weighted scoring, constraint satisfaction, trade-off analysis

---

### Question 10: Evaluation Metric Selection for Specific Tasks

**Scenario:**
Team must choose evaluation metrics for three different agents: (1) Summarization, (2) Question answering, (3) Creative writing.

**Question:** What metrics are appropriate for each task?

**Options:**

A) Summarization: ROUGE, faithfulness, compression ratio. QA: Exact match, F1, answer relevance. Creative writing: Diversity, coherence, user preference.

B) Use accuracy for all tasks.

C) Use BLEU for all tasks.

D) Use user satisfaction for all tasks.

**Correct Answer:** A

**Explanation:**
Task-specific metrics: **Summarization** needs ROUGE (content overlap), faithfulness (no hallucinations), compression (conciseness). **QA** needs exact match (correct answer), F1 (partial credit), relevance (addresses question). **Creative writing** needs diversity (not repetitive), coherence (makes sense), preference (subjective quality). Generic metrics (B, C) miss task-specific requirements. Satisfaction (D) important but insufficient.

**Key Concepts:** Task-specific metrics, evaluation metric selection, ROUGE, F1, diversity

---

### Question 11: Handling Evaluation Bias

**Scenario:**
An agent's evaluation dataset contains mostly simple cases. Agent performs well in evaluation but poorly in production with complex cases.

**Question:** How should team address evaluation bias?

**Options:**

A) Analyze production data to identify difficult cases, add them to evaluation dataset, stratify dataset by difficulty, ensure evaluation reflects production distribution.

B) Make production cases simpler to match evaluation.

C) Increase evaluation dataset size with more simple cases.

D) Use different model for complex cases.

**Correct Answer:** A

**Explanation:**
Fix evaluation bias: (1) Analyze production failures, (2) Add difficult cases to evaluation, (3) Stratify by difficulty (easy 40%, medium 40%, hard 20%), (4) Ensure distribution matches production. Evaluation should reflect reality. Simplifying production (B) impractical. More simple cases (C) worsens bias. Different model (D) doesn't fix evaluation.

**Key Concepts:** Evaluation bias, dataset stratification, production-evaluation alignment, difficulty distribution

---

### Question 12: Parameter Tuning Strategy

**Scenario:**
An agent has multiple tunable parameters: temperature (creativity), top_p (diversity), max_tokens (length), frequency_penalty (repetition). Team needs systematic tuning approach.

**Question:** What parameter tuning strategy is most effective?

**Options:**

A) Grid search over parameter ranges, evaluate each combination on validation set, select parameters maximizing target metric, validate on holdout test set.

B) Manually try different parameters until results look good.

C) Use default parameters.

D) Tune one parameter at a time.

**Correct Answer:** A

**Explanation:**
Systematic tuning: (1) Define ranges (temperature: 0.0-1.0, top_p: 0.8-1.0), (2) Grid search (test all combinations), (3) Evaluate on validation set, (4) Select best parameters, (5) Validate on test set (ensure no overfitting). Manual tuning (B) unsystematic. Defaults (C) may be suboptimal. One-at-a-time (D) misses parameter interactions.

**Key Concepts:** Hyperparameter tuning, grid search, validation sets, parameter optimization

---

### Question 13: Evaluation Result Analysis and Action

**Scenario:**
Evaluation shows agent has 95% accuracy on common queries but 60% on edge cases. Latency is 2 seconds (target: 1 second). Cost is $0.05/query (target: $0.02).

**Question:** What actions should team prioritize?

**Options:**

A) Prioritize based on impact: (1) Improve edge case accuracy (biggest quality gap), (2) Optimize latency with TensorRT-LLM (achievable), (3) Reduce cost through model optimization or tiering (requires trade-off analysis).

B) Focus only on cost reduction.

C) Improve common query accuracy to 99%.

D) Accept current performance.

**Correct Answer:** A

**Explanation:**
Prioritize by impact: **Edge cases** (60% → 80% = major quality improvement), **Latency** (2s → 1s = better UX, achievable with optimization), **Cost** (requires careful trade-off analysis to maintain quality). Cost-only focus (B) may hurt quality. Common query improvement (C) marginal benefit (95% → 99%). Accepting (D) ignores significant gaps.

**Key Concepts:** Evaluation analysis, prioritization, impact assessment, optimization strategies

---

**End of Domain 3 Questions**

**Summary:**
- Total Questions: 13
- Domain Weight: 13%
- Topics Covered: RAG evaluation metrics, A/B testing, cost-performance trade-offs, evaluation automation, feedback collection, latency-accuracy trade-offs, benchmark datasets, degradation detection, multi-metric evaluation, task-specific metrics, evaluation bias, parameter tuning, result analysis


---

## Study Resources

To prepare for these questions, review:

**Course Notes:** [Module 03 Evaluation Tuning](../../course-notes/module-03-evaluation-tuning.md)

**Practice Notebooks:**
- [01 Evaluation Metrics](../../notebooks/module-03/01-evaluation-metrics.ipynb)
