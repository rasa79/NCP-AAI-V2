# Practice Lab Exercises

5 comprehensive hands-on projects simulating NCP-AAI certification scenarios.

## Lab Overview

| Lab | Title | Complexity | Time | Modules | Skills |
|-----|-------|------------|------|---------|--------|
| 01 | Basic RAG Agent | Beginner | 3-4h | 1-2, 4 | RAG pipeline, embeddings, vector store |
| 02 | Multi-Agent Research System | Intermediate | 4-5h | 1-2, 5 | Multi-agent orchestration, memory |
| 03 | Production Deployment | Intermediate-Advanced | 5-6h | 6-8 | Docker, K8s, monitoring, NVIDIA NIM |
| 04 | Evaluation and Optimization | Intermediate | 4-5h | 3 | Metrics, A/B testing, tuning |
| 05 | Safe and Compliant Agent | Advanced | 5-6h | 9-10 | Guardrails, bias detection, compliance |

**Total Time:** 21-26 hours

## Lab Structure

Each lab includes:
- `README.md` - Scenario, requirements, instructions
- `requirements.txt` - Lab-specific dependencies
- `starter-code/` - Scaffolding to get you started
- `solution/` - Complete reference implementation
- `test-data/` - Sample data for testing
- `rubric.md` - Evaluation criteria

## How to Use

### Setup
1. Navigate to lab directory: `cd labs/lab-XX-name`
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

### Implementation
1. Read `README.md` thoroughly
2. Understand the scenario and requirements
3. Review starter code structure
4. Implement required functionality
5. Test your implementation
6. Compare with reference solution

### Evaluation
1. Check against success criteria
2. Review rubric for scoring
3. Test edge cases
4. Verify error handling
5. Assess code quality

## Lab Descriptions

### Lab 01: Basic RAG Agent
Build a document Q&A agent for research papers using RAG pipeline.

**Key Skills:**
- Implement document loading and chunking
- Create embeddings and vector store
- Build retrieval pipeline
- Integrate LLM for answer generation
- Evaluate retrieval quality

**Deliverables:**
- Working RAG agent
- Evaluation results
- Performance metrics

### Lab 02: Multi-Agent Research System
Build a research assistant with specialized agents for different tasks.

**Key Skills:**
- Design multi-agent architecture
- Implement agent coordination
- Manage shared memory
- Handle task decomposition
- Orchestrate agent workflows

**Deliverables:**
- Multi-agent system
- Coordination logic
- Demonstration results

### Lab 03: Production Deployment
Deploy a RAG agent to production with monitoring and scaling.

**Key Skills:**
- Containerize application with Docker
- Deploy to Kubernetes
- Configure NVIDIA NIM
- Set up monitoring dashboards
- Implement logging and tracing

**Deliverables:**
- Deployed system
- Monitoring dashboard
- Deployment documentation

### Lab 04: Evaluation and Optimization
Evaluate and optimize a RAG system for performance and accuracy.

**Key Skills:**
- Implement evaluation metrics
- Build A/B testing framework
- Tune parameters
- Optimize cost-performance
- Analyze results

**Deliverables:**
- Evaluation report
- Optimized system
- Recommendations

### Lab 05: Safe and Compliant Agent
Add safety guardrails and compliance to an existing agent.

**Key Skills:**
- Implement NeMo Guardrails
- Detect and mitigate bias
- Create audit trails
- Build escalation protocols
- Test safety mechanisms

**Deliverables:**
- Hardened agent
- Compliance documentation
- Safety test results

## Tips for Success

1. **Read Everything First:** Understand the full scope before coding
2. **Start with Starter Code:** Don't start from scratch
3. **Test Incrementally:** Verify each component works
4. **Handle Errors:** Production code needs error handling
5. **Document Your Work:** Add comments and documentation
6. **Compare Solutions:** Learn from reference implementations
7. **Time Yourself:** Practice under time constraints
8. **Ask Questions:** If stuck, review related modules

## Common Pitfalls

- Skipping error handling
- Not testing edge cases
- Ignoring performance requirements
- Over-complicating solutions
- Not reading requirements carefully
- Skipping validation steps
- Not documenting code
- Rushing through labs

## Evaluation Rubric

Each lab is scored on:
- **Functionality (40%):** Does it work correctly?
- **Code Quality (20%):** Is it well-structured and documented?
- **Performance (15%):** Does it meet performance requirements?
- **Error Handling (10%):** Does it handle errors gracefully?
- **Best Practices (15%):** Does it follow NVIDIA best practices?

**Passing Score:** 70%+

## After Completing Labs

1. Review your implementations
2. Compare with reference solutions
3. Identify areas for improvement
4. Practice explaining your design choices
5. Be ready to discuss trade-offs in interviews
