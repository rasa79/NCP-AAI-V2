# NVIDIA NCP-AAI Exam Coverage Matrix

This document maps all learning materials to specific NCP-AAI exam objectives, ensuring 100% coverage of the certification requirements.

## Exam Domain Overview

| Domain | Weight | Modules | Notebooks | Questions | Labs |
|--------|--------|---------|-----------|-----------|------|
| 1. Agent Architecture and Design | 15% | 1 | 3 | 15 | 1, 2 |
| 2. Agent Development | 15% | 2 | 4 | 15 | 1, 2 |
| 3. Evaluation and Tuning | 13% | 3 | 3 | 13 | 4 |
| 4. Knowledge Integration | 10% | 4 | 4 | 10 | 1 |
| 5. Cognition, Planning, Memory | 10% | 5 | 3 | 10 | 2 |
| 6. NVIDIA Platform | 7% | 6 | 4 | 7 | 3 |
| 7. Monitoring and Maintenance | 7% | 7 | 3 | 7 | 3 |
| 8. Deployment and Scaling | 5% | 8 | 2 | 5 | 3 |
| 9. Safety, Ethics, Compliance | 5% | 9 | 2 | 5 | 5 |
| 10. Human-AI Interaction | 5% | 10 | 2 | 5 | 5 |
| Mixed Scenarios | 13% | - | - | 20 | - |
| **Total** | **100%** | **10** | **30** | **112** | **5** |

---

## Domain 1: Agent Architecture and Design (15%)

### Exam Objectives

**1.1** - Design intuitive human-agent interaction interfaces  
**1.2** - Implement reasoning and action frameworks (ReAct)  
**1.3** - Configure agent-to-agent communication protocols  
**1.4** - Manage short-term and long-term memory for context retention  
**1.5** - Orchestrate multi-agent workflows and coordination  
**1.6** - Apply logic trees, prompt chains, and stateful orchestration  
**1.7** - Integrate knowledge graphs for relational reasoning  
**1.8** - Ensure adaptability and scalability

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 1.1 | Module 01 §2.3, §6 | module-01/01, module-10/01 | domain-01 Q1-3 | Lab 01, 02 |
| 1.2 | Module 01 §3 | module-01/02 | domain-01 Q4-6 | Lab 01, 02 |
| 1.3 | Module 01 §4 | module-01/03 | domain-01 Q7-9 | Lab 02 |
| 1.4 | Module 01 §5, Module 05 §2 | module-05/01 | domain-01 Q10-11 | Lab 02 |
| 1.5 | Module 01 §4 | module-01/03 | domain-01 Q12-13 | Lab 02 |
| 1.6 | Module 01 §3, Module 05 §3 | module-01/02, module-05/03 | domain-01 Q14 | Lab 02 |
| 1.7 | Module 01 §7 | module-04/01 | domain-01 Q15 | Lab 01 |
| 1.8 | Module 01 §8, Module 08 | module-08/02 | mixed Q1-2 | Lab 03 |

---

## Domain 2: Agent Development (15%)

### Exam Objectives

**2.1** - Engineer prompts and dynamic prompt chains  
**2.2** - Integrate generative and multimodal models  
**2.3** - Build and connect custom tools, APIs, and functions  
**2.4** - Implement error handling (retry logic, graceful failure)  
**2.5** - Develop dynamic conversation flows with streaming  
**2.6** - Evaluate and refine agent decision-making strategies

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 2.1 | Module 02 §2 | module-02/01 | domain-02 Q1-3 | Lab 01, 02 |
| 2.2 | Module 02 §3 | module-02/02 | domain-02 Q4-5 | Lab 01 |
| 2.3 | Module 02 §4 | module-02/02 | domain-02 Q6-8 | Lab 01, 02 |
| 2.4 | Module 02 §5 | module-02/03 | domain-02 Q9-12 | Lab 01, 02, 03 |
| 2.5 | Module 02 §6 | module-02/04 | domain-02 Q13-14 | Lab 01 |
| 2.6 | Module 02 §7, Module 03 | module-03/01-03 | domain-02 Q15 | Lab 04 |

---

## Domain 3: Evaluation and Tuning (13%)

### Exam Objectives

**3.1** - Implement evaluation pipelines and task benchmarks  
**3.2** - Compare agent performance across tasks and datasets  
**3.3** - Collect and integrate structured user feedback  
**3.4** - Tune model parameters (accuracy vs latency trade-offs)  
**3.5** - Analyze evaluation results for targeted optimization

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 3.1 | Module 03 §2 | module-03/01, module-03/02 | domain-03 Q1-3 | Lab 04 |
| 3.2 | Module 03 §3 | module-03/03 | domain-03 Q4-6 | Lab 04 |
| 3.3 | Module 03 §4, Module 10 §4 | module-10/02 | domain-03 Q7-8 | Lab 04 |
| 3.4 | Module 03 §5 | module-03/02 | domain-03 Q9-11 | Lab 04 |
| 3.5 | Module 03 §6 | module-03/02, module-03/03 | domain-03 Q12-13 | Lab 04 |

---

## Domain 4: Knowledge Integration and Data Handling (10%)

### Exam Objectives

**4.1** - Implement retrieval pipelines (RAG, embedded search, hybrid)  
**4.2** - Configure and optimize vector databases  
**4.3** - Build ETL pipelines for enterprise data integration  
**4.4** - Conduct data quality checks and preprocessing  
**4.5** - Enable real-time access to structured/unstructured knowledge

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 4.1 | Module 04 §2 | module-04/01, module-04/04 | domain-04 Q1-3 | Lab 01 |
| 4.2 | Module 04 §4 | module-04/03 | domain-04 Q4-6 | Lab 01 |
| 4.3 | Module 04 §5 | module-04/01 | domain-04 Q7 | Lab 01 |
| 4.4 | Module 04 §3 | module-04/01, module-04/02 | domain-04 Q8-9 | Lab 01 |
| 4.5 | Module 04 §6 | module-04/04 | domain-04 Q10 | Lab 01 |

---

## Domain 5: Cognition, Planning, and Memory (10%)

### Exam Objectives

**5.1** - Implement memory mechanisms (short/long-term context)  
**5.2** - Apply reasoning frameworks (chain-of-thought, task decomposition)  
**5.3** - Engineer planning strategies for sequential decision-making  
**5.4** - Manage stateful orchestration for complex tasks  
**5.5** - Adapt reasoning strategies based on prior experiences

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 5.1 | Module 05 §2 | module-05/01 | domain-05 Q1-3 | Lab 02 |
| 5.2 | Module 05 §3 | module-05/02 | domain-05 Q4-6 | Lab 02 |
| 5.3 | Module 05 §4 | module-05/03 | domain-05 Q7-8 | Lab 02 |
| 5.4 | Module 05 §5 | module-05/03 | domain-05 Q9 | Lab 02 |
| 5.5 | Module 05 §6 | module-05/01, module-05/02 | domain-05 Q10 | Lab 02 |

---

## Domain 6: NVIDIA Platform Implementation (7%)

### Exam Objectives

**6.1** - Integrate NVIDIA NeMo Guardrails for compliance and safety  
**6.2** - Deploy NVIDIA NIM microservices for inference  
**6.3** - Optimize workflows with NVIDIA NeMo Agent Toolkit  
**6.4** - Leverage TensorRT-LLM and Triton Inference Server  
**6.5** - Manage multimodal input pipelines on NVIDIA hardware

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 6.1 | Module 06 §2, Module 09 §2 | module-06/02, module-09/01 | domain-06 Q1-2 | Lab 05 |
| 6.2 | Module 06 §3 | module-06/01 | domain-06 Q3-4 | Lab 03 |
| 6.3 | Module 06 §4 | module-06/01 | domain-06 Q5 | Lab 03 |
| 6.4 | Module 06 §5, §6 | module-06/03, module-06/04 | domain-06 Q6 | Lab 03 |
| 6.5 | Module 06 §7 | module-06/01 | domain-06 Q7 | Lab 03 |

---

## Domain 7: Run, Monitor, and Maintain (7%)

### Exam Objectives

**7.1** - Define monitoring dashboards and reliability metrics  
**7.2** - Track logs, errors, and anomalies for root cause diagnosis  
**7.3** - Continuously benchmark deployed agents  
**7.4** - Implement automated tuning, retraining, and versioning  
**7.5** - Ensure continuous uptime, transparency, and trust

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 7.1 | Module 07 §2 | module-07/01 | domain-07 Q1-2 | Lab 03 |
| 7.2 | Module 07 §3 | module-07/02 | domain-07 Q3-4 | Lab 03 |
| 7.3 | Module 07 §4 | module-07/03 | domain-07 Q5 | Lab 03, 04 |
| 7.4 | Module 07 §5 | module-07/01 | domain-07 Q6 | Lab 03 |
| 7.5 | Module 07 §6 | module-07/01, module-07/02 | domain-07 Q7 | Lab 03 |

---

## Domain 8: Deployment and Scaling (5%)

### Exam Objectives

**8.1** - Deploy and orchestrate multi-agent systems at production scale  
**8.2** - Apply MLOps practices (CI/CD workflows, monitoring, governance)  
**8.3** - Profile performance and reliability under distributed loads  
**8.4** - Scale deployments using containerization (Docker, Kubernetes)  
**8.5** - Optimize deployment costs while ensuring high availability

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 8.1 | Module 08 §2 | module-08/02 | domain-08 Q1 | Lab 03 |
| 8.2 | Module 08 §3 | module-08/01, module-08/02 | domain-08 Q2 | Lab 03 |
| 8.3 | Module 08 §4 | module-07/03 | domain-08 Q3 | Lab 03 |
| 8.4 | Module 08 §5 | module-08/01, module-08/02 | domain-08 Q4 | Lab 03 |
| 8.5 | Module 08 §6 | module-08/02 | domain-08 Q5 | Lab 03 |

---

## Domain 9: Safety, Ethics, and Compliance (5%)

### Exam Objectives

**9.1** - Design and enforce system security and audit trails  
**9.2** - Integrate compliance guardrails (privacy, enterprise policy)  
**9.3** - Mitigate bias and toxicity in outputs  
**9.4** - Deploy layered safety frameworks (filters, escalation protocols)  
**9.5** - Ensure compliance with licensing and regulatory standards

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 9.1 | Module 09 §2 | module-09/01 | domain-09 Q1 | Lab 05 |
| 9.2 | Module 09 §3 | module-09/01 | domain-09 Q2 | Lab 05 |
| 9.3 | Module 09 §4 | module-09/02 | domain-09 Q3-4 | Lab 05 |
| 9.4 | Module 09 §5 | module-09/01 | domain-09 Q5 | Lab 05 |
| 9.5 | Module 09 §6 | module-09/01 | mixed Q15-16 | Lab 05 |

---

## Domain 10: Human-AI Interaction and Oversight (5%)

### Exam Objectives

**10.1** - Build intuitive UIs with user-in-the-loop interaction  
**10.2** - Design structured feedback loops for iterative improvements  
**10.3** - Implement transparency mechanisms (explainable reasoning)  
**10.4** - Enable human oversight and intervention for accountability

### Coverage Mapping

| Objective | Course Notes | Notebooks | Questions | Labs |
|-----------|--------------|-----------|-----------|------|
| 10.1 | Module 10 §2 | module-10/01 | domain-10 Q1-2 | Lab 05 |
| 10.2 | Module 10 §3 | module-10/02 | domain-10 Q3 | Lab 05 |
| 10.3 | Module 10 §4 | module-10/01 | domain-10 Q4 | Lab 05 |
| 10.4 | Module 10 §5 | module-10/02 | domain-10 Q5 | Lab 05 |

---

## Mixed Scenarios (13%)

Mixed scenario questions integrate multiple domains and test holistic understanding of agentic AI systems.

### Coverage Mapping

| Question Range | Primary Domains | Secondary Domains | Labs |
|----------------|-----------------|-------------------|------|
| mixed Q1-4 | Architecture, Development | Deployment, Monitoring | Lab 01, 02, 03 |
| mixed Q5-8 | Evaluation, Knowledge Integration | Development, NVIDIA Platform | Lab 01, 04 |
| mixed Q9-12 | Cognition/Memory, Architecture | Development, Safety | Lab 02, 05 |
| mixed Q13-16 | NVIDIA Platform, Deployment | Monitoring, Safety | Lab 03, 05 |
| mixed Q17-20 | Safety/Ethics, Human Interaction | All domains | Lab 05 |

---

## Coverage Verification

### Module Coverage

✅ **Module 01** - Agent Architecture and Design  
✅ **Module 02** - Agent Development  
✅ **Module 03** - Evaluation and Tuning  
✅ **Module 04** - Knowledge Integration  
✅ **Module 05** - Cognition, Planning, and Memory  
✅ **Module 06** - NVIDIA Platform  
✅ **Module 07** - Monitoring and Maintenance  
✅ **Module 08** - Deployment and Scaling  
✅ **Module 09** - Safety, Ethics, and Compliance  
✅ **Module 10** - Human-AI Interaction

**Coverage:** 10/10 modules (100%)

### Notebook Coverage

✅ **Setup Notebooks** - 2 notebooks  
✅ **Module 01 Notebooks** - 3 notebooks  
✅ **Module 02 Notebooks** - 4 notebooks  
✅ **Module 03 Notebooks** - 3 notebooks  
✅ **Module 04 Notebooks** - 4 notebooks  
✅ **Module 05 Notebooks** - 3 notebooks  
✅ **Module 06 Notebooks** - 4 notebooks  
✅ **Module 07 Notebooks** - 3 notebooks  
✅ **Module 08 Notebooks** - 2 notebooks  
✅ **Module 09 Notebooks** - 2 notebooks  
✅ **Module 10 Notebooks** - 2 notebooks

**Coverage:** 32/32 notebooks (100%)

### Question Coverage

✅ **Domain 01** - 15 questions (15% weight)  
✅ **Domain 02** - 15 questions (15% weight)  
✅ **Domain 03** - 13 questions (13% weight)  
✅ **Domain 04** - 10 questions (10% weight)  
✅ **Domain 05** - 10 questions (10% weight)  
✅ **Domain 06** - 7 questions (7% weight)  
✅ **Domain 07** - 7 questions (7% weight)  
✅ **Domain 08** - 5 questions (5% weight)  
✅ **Domain 09** - 5 questions (5% weight)  
✅ **Domain 10** - 5 questions (5% weight)  
✅ **Mixed Scenarios** - 20 questions (13% weight)

**Coverage:** 112/112 questions (100%)

### Lab Coverage

✅ **Lab 01** - Basic RAG Agent (Domains 1, 2, 4)  
✅ **Lab 02** - Multi-Agent Research System (Domains 1, 2, 5)  
✅ **Lab 03** - Production Deployment (Domains 6, 7, 8)  
✅ **Lab 04** - Evaluation and Optimization (Domain 3)  
✅ **Lab 05** - Safe and Compliant Agent (Domains 9, 10)

**Coverage:** 5/5 labs (100%)

### Exam Objective Coverage

**Total Exam Objectives:** 48 (across 10 domains)  
**Covered Objectives:** 48  
**Coverage:** 100%

---

## Gap Analysis

### Strengths

- ✅ Complete coverage of all 10 exam domains
- ✅ Balanced question distribution matching exam weights
- ✅ Progressive lab complexity from beginner to advanced
- ✅ Multiple touchpoints per objective (notes + notebooks + questions + labs)
- ✅ Strong emphasis on high-weight domains (Architecture, Development, Evaluation)
- ✅ Comprehensive NVIDIA platform integration throughout

### Recommendations for Study

1. **High-Priority Domains (15% each):**
   - Focus extra time on Modules 01 and 02
   - Complete all notebooks in module-01 and module-02
   - Master Labs 01 and 02 thoroughly

2. **Medium-Priority Domains (10-13%):**
   - Allocate significant time to Modules 03, 04, 05
   - Practice evaluation metrics and RAG pipelines extensively
   - Complete Lab 04 multiple times for evaluation mastery

3. **NVIDIA Platform Mastery:**
   - Hands-on practice with all NVIDIA tools in Module 06
   - Complete Lab 03 to gain production deployment experience
   - Review NVIDIA-specific questions in all domains

4. **Integration Practice:**
   - Focus on mixed scenario questions
   - Practice explaining trade-offs across domains
   - Complete all labs to build end-to-end understanding

---

## Study Path Recommendations

### Path 1: Sequential (Recommended for Beginners)
Follow modules 1-10 in order, completing corresponding notebooks and questions after each module.

### Path 2: Weight-Based (Recommended for Time-Constrained)
1. Modules 01, 02 (30% of exam)
2. Module 03 (13% of exam)
3. Modules 04, 05 (20% of exam)
4. Modules 06-10 (37% of exam)

### Path 3: Hands-On First (Recommended for Experienced Practitioners)
1. Complete all labs first to identify knowledge gaps
2. Study relevant modules for weak areas
3. Practice questions to validate understanding
4. Review quick reference guide before exam

---

## Validation Checklist

Use this checklist to verify your exam readiness:

- [ ] Completed all 10 course note modules
- [ ] Executed all 32 Jupyter notebooks successfully
- [ ] Answered all 112 practice questions
- [ ] Achieved 80%+ accuracy on practice questions
- [ ] Completed all 5 practice labs
- [ ] Scored 70%+ on all lab rubrics
- [ ] Can explain trade-offs for architecture decisions
- [ ] Familiar with all NVIDIA platform tools
- [ ] Can troubleshoot common agent issues
- [ ] Understand evaluation metrics and optimization strategies
- [ ] Can design end-to-end agentic AI systems
- [ ] Reviewed quick reference guide thoroughly

**Exam Ready:** All items checked ✅

---

*Last Updated: January 2026*  
*Aligned with: NVIDIA NCP-AAI Certification Exam v1.0*
