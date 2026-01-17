# Lab 2: Multi-Agent Research System

## Overview

In this lab, you'll build a multi-agent research system that coordinates specialized agents to conduct comprehensive research on technical topics. This intermediate lab introduces agent orchestration, task decomposition, inter-agent communication, and memory management. You'll implement a system where multiple agents collaborate to gather, analyze, and synthesize information.

## Learning Objectives

- Design and implement multi-agent architectures (maps to exam objective 1.5: Multi-Agent Orchestration)
- Implement agent-to-agent communication protocols (maps to exam objective 1.3: Agent Communication)
- Apply task decomposition strategies (maps to exam objective 5.3: Planning Strategies)
- Manage agent memory and state (maps to exam objective 5.1: Memory Mechanisms)
- Coordinate agent workflows (maps to exam objective 1.6: Stateful Orchestration)
- Implement error handling in distributed systems (maps to exam objective 2.3: Error Handling)

## Prerequisites

- Completed modules: Module 1 (Agent Architecture), Module 2 (Agent Development), Module 5 (Cognition and Memory)
- Completed Lab 1: Basic RAG Agent
- Required knowledge: Agent architectures, ReAct pattern, LangChain, multi-agent systems
- Estimated time: 4-5 hours

## Scenario

**Company:** ResearchAI Corp., an AI research consultancy

**Challenge:** Your team needs to conduct rapid, comprehensive research on emerging AI technologies for client reports. Currently, researchers manually search multiple sources, synthesize findings, and write reports - a process taking days. Clients need faster turnaround with consistent quality.

**Your Task:** Build an intelligent multi-agent research system that can:
- Decompose research questions into sub-tasks
- Coordinate specialized agents (searcher, analyzer, synthesizer)
- Gather information from multiple sources
- Analyze and validate findings
- Synthesize comprehensive research reports
- Maintain context and memory across the research process

**Business Requirements:**
- Research time: < 10 minutes for comprehensive report
- Quality: Reports must be well-structured, factual, and cited
- Scalability: Handle multiple concurrent research requests
- Flexibility: Adapt to different research topics and depths

**Technical Constraints:**
- Use LangChain for agent orchestration
- Implement at least 3 specialized agents
- Use LangGraph for workflow management
- Include comprehensive error handling and logging
- Maintain conversation history and agent memory

## Requirements

### Functional Requirements

1. **Agent Architecture**
   - Implement Coordinator Agent (orchestrates workflow)
   - Implement Searcher Agent (finds relevant information)
   - Implement Analyzer Agent (evaluates and validates findings)
   - Implement Synthesizer Agent (creates final report)
   - Define clear roles and responsibilities for each agent

2. **Task Decomposition**
   - Break research questions into sub-questions
   - Assign sub-tasks to appropriate agents
   - Track task dependencies and completion
   - Handle dynamic task generation based on findings

3. **Inter-Agent Communication**
   - Implement message passing between agents
   - Define communication protocols and message formats
   - Handle asynchronous agent interactions
   - Maintain conversation context

4. **Memory Management**
   - Implement short-term memory (current research session)
   - Implement long-term memory (persistent findings)
   - Share relevant context between agents
   - Prevent memory overflow with context window management

5. **Workflow Orchestration**
   - Define research workflow (plan → search → analyze → synthesize)
   - Implement state transitions
   - Handle workflow branching and loops
   - Support workflow visualization

6. **Error Handling**
   - Handle agent failures gracefully
   - Implement retry logic for failed tasks
   - Provide fallback strategies
   - Log all agent interactions for debugging

### Performance Requirements

- Research completion time: < 10 minutes
- Agent response time: < 30 seconds per task
- Memory efficiency: Handle 50+ research findings
- Concurrent requests: Support 5+ simultaneous research sessions

### Quality Requirements

- Code must include comprehensive error handling
- Code must include detailed logging of agent interactions
- Code must include type hints and docstrings
- Code must follow multi-agent best practices
- Reports must be well-structured and cited

## Success Criteria

- [ ] All agents are implemented and functional
- [ ] Task decomposition works correctly
- [ ] Agents communicate effectively
- [ ] Memory management prevents context loss
- [ ] Workflow orchestration completes successfully
- [ ] Error handling covers all failure modes
- [ ] Research reports are comprehensive and well-cited
- [ ] Performance meets requirements
- [ ] All tests pass

## Setup Instructions

### 1. Environment Setup

```bash
# Navigate to lab directory
cd labs/lab-02-multi-agent-research

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import langchain, langgraph; print('Setup successful!')"
```

### 2. Test Data Setup

The `test-data/` directory contains sample research topics:
- `topic_01_rag_systems.txt` - RAG architecture research
- `topic_02_vector_databases.txt` - Vector database comparison
- `topic_03_llm_evaluation.txt` - LLM evaluation methods

### 3. Project Structure

```
lab-02-multi-agent-research/
├── README.md (this file)
├── requirements.txt
├── starter-code/
│   ├── multi_agent_system.py (main orchestrator - YOUR WORK HERE)
│   ├── agents/
│   │   ├── coordinator.py (coordinator agent)
│   │   ├── searcher.py (search agent)
│   │   ├── analyzer.py (analysis agent)
│   │   └── synthesizer.py (synthesis agent)
│   ├── memory/
│   │   ├── short_term_memory.py (session memory)
│   │   └── long_term_memory.py (persistent memory)
│   ├── workflow/
│   │   └── research_workflow.py (LangGraph workflow)
│   └── utils.py (helper functions)
├── solution/
│   └── [reference implementation - DO NOT LOOK UNTIL COMPLETE]
├── test-data/
│   └── [research topics]
├── tests/
│   └── test_multi_agent.py (validation tests)
└── rubric.md (evaluation criteria)
```

## Starter Code

The starter code provides scaffolding for:

- **`multi_agent_system.py`**: Main system class coordinating all agents
- **`agents/coordinator.py`**: Coordinator agent for task decomposition
- **`agents/searcher.py`**: Searcher agent for information retrieval
- **`agents/analyzer.py`**: Analyzer agent for validation
- **`agents/synthesizer.py`**: Synthesizer agent for report generation
- **`memory/`**: Memory management modules
- **`workflow/`**: LangGraph workflow definition
- **`utils.py`**: Shared utilities

## Implementation Tasks

### Task 1: Coordinator Agent (45 minutes)

Implement the coordinator agent in `agents/coordinator.py`:

**Responsibilities:**
- Receive research question
- Decompose into sub-questions
- Assign tasks to specialized agents
- Monitor progress and coordinate workflow

**Hints:**
- Use LLM to decompose questions
- Create task queue for sub-questions
- Track task status (pending, in-progress, completed)
- Implement ReAct pattern for decision-making

**Validation:**
```python
from agents.coordinator import CoordinatorAgent
coordinator = CoordinatorAgent()
tasks = coordinator.decompose_question("What are the best practices for RAG systems?")
print(f"Generated {len(tasks)} sub-tasks")
```

### Task 2: Searcher Agent (45 minutes)

Implement the searcher agent in `agents/searcher.py`:

**Responsibilities:**
- Search for information on given topics
- Retrieve relevant documents
- Extract key information
- Return structured findings

**Hints:**
- Reuse RAG components from Lab 1
- Implement multiple search strategies
- Rank results by relevance
- Format findings with citations

**Validation:**
```python
from agents.searcher import SearcherAgent
searcher = SearcherAgent()
findings = searcher.search("RAG architecture patterns")
print(f"Found {len(findings)} relevant documents")
```

### Task 3: Analyzer Agent (45 minutes)

Implement the analyzer agent in `agents/analyzer.py`:

**Responsibilities:**
- Evaluate quality of findings
- Validate factual accuracy
- Identify contradictions
- Assess completeness

**Hints:**
- Use LLM for quality assessment
- Check for source credibility
- Identify gaps in information
- Provide confidence scores

**Validation:**
```python
from agents.analyzer import AnalyzerAgent
analyzer = AnalyzerAgent()
analysis = analyzer.analyze(findings)
print(f"Analysis confidence: {analysis['confidence']}")
```

### Task 4: Synthesizer Agent (45 minutes)

Implement the synthesizer agent in `agents/synthesizer.py`:

**Responsibilities:**
- Combine findings from multiple sources
- Generate coherent research report
- Include citations and references
- Structure report logically

**Hints:**
- Use LLM for synthesis
- Create report template
- Organize by themes/topics
- Include executive summary

**Validation:**
```python
from agents.synthesizer import SynthesizerAgent
synthesizer = SynthesizerAgent()
report = synthesizer.synthesize(analyzed_findings)
print(f"Generated report: {len(report)} characters")
```

### Task 5: Memory Management (30 minutes)

Implement memory modules in `memory/`:

**Short-term Memory:**
- Store current research session data
- Maintain conversation history
- Track agent interactions
- Clear after session completion

**Long-term Memory:**
- Store validated findings
- Maintain research history
- Enable knowledge reuse
- Implement retrieval mechanisms

**Hints:**
- Use dictionaries for short-term storage
- Consider SQLite for long-term storage
- Implement memory pruning for context limits
- Add memory search functionality

**Validation:**
```python
from memory.short_term_memory import ShortTermMemory
memory = ShortTermMemory()
memory.add("finding", {"topic": "RAG", "content": "..."})
findings = memory.get_all("finding")
```

### Task 6: Workflow Orchestration (60 minutes)

Implement workflow in `workflow/research_workflow.py`:

**Workflow Steps:**
1. Receive research question
2. Coordinator decomposes question
3. Searcher finds information for each sub-question
4. Analyzer validates findings
5. Synthesizer creates final report
6. Return report to user

**Hints:**
- Use LangGraph for workflow definition
- Define states and transitions
- Implement conditional branching
- Add error recovery paths

**Validation:**
```python
from workflow.research_workflow import ResearchWorkflow
workflow = ResearchWorkflow()
result = workflow.run("What are RAG best practices?")
print(result['report'])
```

### Task 7: Integration and Testing (30 minutes)

Integrate all components in `multi_agent_system.py`:

**Hints:**
- Initialize all agents
- Set up memory systems
- Configure workflow
- Add comprehensive logging
- Implement error handling

**Validation:**
```bash
python tests/test_multi_agent.py
```

## Testing

### Manual Testing

Test your system with these research questions:

1. "What are the key components of RAG systems and how do they work together?"
2. "Compare different vector database options for production RAG systems"
3. "What are the best practices for evaluating LLM-based applications?"

Expected behavior:
- System decomposes question into sub-tasks
- Agents execute tasks in coordination
- Final report is comprehensive and well-structured
- All sources are cited
- Process completes within 10 minutes

### Automated Testing

```bash
# Run validation tests
python tests/test_multi_agent.py

# Expected output:
# ✓ Coordinator agent test passed
# ✓ Searcher agent test passed
# ✓ Analyzer agent test passed
# ✓ Synthesizer agent test passed
# ✓ Memory management test passed
# ✓ Workflow orchestration test passed
# ✓ Integration test passed
```

## Evaluation Rubric

See `rubric.md` for detailed evaluation criteria.

**Summary:**
- Functionality (40%): Do all agents work correctly?
- Code Quality (20%): Is it well-structured and documented?
- Performance (15%): Does it meet timing requirements?
- Error Handling (10%): Does it handle failures gracefully?
- Best Practices (15%): Does it follow multi-agent patterns?

## Common Issues and Troubleshooting

### Issue: Agents not communicating
**Solution:**
- Check message format consistency
- Verify agent initialization
- Review communication protocol
- Add debug logging

### Issue: Memory overflow
**Solution:**
- Implement memory pruning
- Limit context window size
- Summarize old findings
- Clear completed tasks

### Issue: Workflow stuck
**Solution:**
- Check state transitions
- Verify task completion signals
- Add timeout handling
- Review workflow logic

### Issue: Poor report quality
**Solution:**
- Improve synthesis prompts
- Ensure sufficient findings
- Add quality validation
- Include more context

## Resources

### Relevant Course Notes
- Module 1: Agent Architecture (multi-agent systems, coordination)
- Module 2: Agent Development (tool integration, error handling)
- Module 5: Cognition and Memory (memory mechanisms, planning)

### Relevant Notebooks
- `notebooks/module-01/03-multi-agent-systems.ipynb`
- `notebooks/module-05/01-memory-mechanisms.ipynb`
- `notebooks/module-05/03-task-decomposition.ipynb`

### External Documentation
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Multi-Agent Systems](https://python.langchain.com/docs/use_cases/agent_simulations/)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)

## Submission

When complete, ensure:
1. All agents are implemented and tested
2. Workflow executes successfully
3. Memory management works correctly
4. All tests pass
5. Code is well-documented
6. Research reports are high quality

## Next Steps

After completing this lab:
- Review the reference solution
- Experiment with different agent architectures
- Try adding more specialized agents
- Move on to Lab 3: Production Deployment
