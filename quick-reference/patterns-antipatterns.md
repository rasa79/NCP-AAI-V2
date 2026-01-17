# Patterns and Anti-Patterns Guide

## Architecture Patterns

### ReAct (Reasoning + Acting)

**When to Use**:
- ✓ Tasks require iterative reasoning and action
- ✓ Need to use external tools based on reasoning
- ✓ Multi-step problem solving with decision points
- ✓ Debugging or exploratory tasks
- ✓ Tasks where intermediate steps need validation

**When NOT to Use**:
- ✗ Simple retrieval or generation tasks
- ✗ Latency is critical (< 100ms requirements)
- ✗ Tasks with fixed, predictable workflows
- ✗ High-volume, low-complexity queries

**Example Use Cases**:
- Research assistant that searches, analyzes, and synthesizes
- Code debugging agent that tests hypotheses
- Customer support agent that investigates issues
- Data analysis agent that explores datasets

**Implementation Pattern**:
```python
# ReAct loop
while not task_complete:
    # Reasoning step
    thought = llm.generate(f"Thought: {context}")
    
    # Action step
    action = parse_action(thought)
    observation = execute_tool(action)
    
    # Update context
    context += f"\nObservation: {observation}"
```

**Trade-offs**:
- **Pros**: Flexible, interpretable, handles complex tasks
- **Cons**: Higher latency, more token usage, can get stuck in loops

---

### RAG (Retrieval-Augmented Generation)

**When to Use**:
- ✓ Need to ground responses in external knowledge
- ✓ Knowledge base changes frequently
- ✓ Domain-specific information not in model training
- ✓ Need to cite sources for answers
- ✓ Reduce hallucinations with factual grounding

**When NOT to Use**:
- ✗ Knowledge is already in model (common facts)
- ✗ Real-time data not available in knowledge base
- ✗ Retrieval adds unacceptable latency
- ✗ Creative tasks where grounding limits output

**Example Use Cases**:
- Document Q&A systems
- Enterprise knowledge bases
- Technical support with documentation
- Legal/medical information systems
- Product recommendation with catalog

**Implementation Pattern**:
```python
# RAG pipeline
def rag_query(question):
    # Retrieve relevant documents
    docs = vector_store.similarity_search(question, k=5)
    
    # Generate with context
    context = "\n".join([doc.content for doc in docs])
    prompt = f"Context: {context}\n\nQuestion: {question}"
    answer = llm.generate(prompt)
    
    return answer, docs
```

**Trade-offs**:
- **Pros**: Factual accuracy, updatable knowledge, source attribution
- **Cons**: Retrieval latency, context window limits, retrieval quality dependency

---

### Multi-Agent Systems

**When to Use**:
- ✓ Complex tasks requiring specialized expertise
- ✓ Parallel processing of independent subtasks
- ✓ Need for role-based reasoning (e.g., critic, executor)
- ✓ Collaborative problem solving
- ✓ Fault tolerance through redundancy

**When NOT to Use**:
- ✗ Simple, single-domain tasks
- ✗ Tight latency requirements
- ✗ Limited computational resources
- ✗ Coordination overhead exceeds benefits

**Example Use Cases**:
- Research team (searcher, analyzer, writer)
- Software development (architect, coder, tester)
- Content creation (researcher, writer, editor)
- Customer service (router, specialist, escalation)

**Implementation Pattern**:
```python
# Multi-agent orchestration
class AgentTeam:
    def __init__(self):
        self.researcher = ResearchAgent()
        self.analyzer = AnalysisAgent()
        self.writer = WriterAgent()
    
    def solve(self, task):
        # Parallel research
        research = self.researcher.execute(task)
        
        # Sequential analysis and writing
        analysis = self.analyzer.execute(research)
        report = self.writer.execute(analysis)
        
        return report
```

**Trade-offs**:
- **Pros**: Specialization, parallelization, modularity
- **Cons**: Coordination complexity, higher cost, potential conflicts

---

### Streaming Responses

**When to Use**:
- ✓ Interactive user interfaces (chat, assistants)
- ✓ Long-form content generation
- ✓ Need to show progress to users
- ✓ Time to first token matters more than total time
- ✓ User can interrupt generation

**When NOT to Use**:
- ✗ Batch processing workflows
- ✗ Need complete response for downstream processing
- ✗ API consumers can't handle streaming
- ✗ Response requires post-processing before display

**Example Use Cases**:
- Chatbots and conversational AI
- Content generation tools
- Code generation assistants
- Real-time translation

**Implementation Pattern**:
```python
# Streaming generation
def stream_response(prompt):
    for chunk in llm.stream(prompt):
        yield chunk
        # Can add processing, filtering, etc.

# Usage
for token in stream_response("Write an essay"):
    print(token, end="", flush=True)
```

**Trade-offs**:
- **Pros**: Better UX, lower perceived latency, interruptible
- **Cons**: More complex error handling, harder to cache, limited post-processing

---

### Chain-of-Thought (CoT)

**When to Use**:
- ✓ Complex reasoning tasks
- ✓ Mathematical or logical problems
- ✓ Need interpretable reasoning steps
- ✓ Multi-step problem decomposition
- ✓ Debugging or verification needed

**When NOT to Use**:
- ✗ Simple factual queries
- ✗ Latency-critical applications
- ✗ Token budget is limited
- ✗ Reasoning steps not valuable to user

**Example Use Cases**:
- Math word problems
- Logical reasoning tasks
- Code debugging and analysis
- Strategic planning
- Complex decision making

**Implementation Pattern**:
```python
# Chain-of-thought prompting
prompt = """
Let's solve this step by step:

Question: {question}

Step 1: Identify what we know
Step 2: Determine what we need to find
Step 3: Apply relevant formulas or logic
Step 4: Calculate the result
Step 5: Verify the answer

Let's begin:
"""

response = llm.generate(prompt.format(question=question))
```

**Trade-offs**:
- **Pros**: Better accuracy on complex tasks, interpretable, debuggable
- **Cons**: Higher token usage, increased latency, verbose output

---

### Memory-Augmented Agents

**When to Use**:
- ✓ Multi-turn conversations requiring context
- ✓ Personalization based on history
- ✓ Learning from past interactions
- ✓ Long-running sessions
- ✓ Need to reference previous information

**When NOT to Use**:
- ✗ Stateless, single-turn queries
- ✗ Privacy concerns with data retention
- ✗ Memory management overhead too high
- ✗ Context window sufficient for task

**Example Use Cases**:
- Personal assistants
- Customer support with history
- Educational tutors
- Project management assistants
- Collaborative tools

**Implementation Pattern**:
```python
# Memory management
class MemoryAgent:
    def __init__(self):
        self.short_term = []  # Recent conversation
        self.long_term = {}   # Persistent facts
    
    def respond(self, message):
        # Add to short-term memory
        self.short_term.append(message)
        
        # Retrieve relevant long-term memory
        context = self.retrieve_relevant(message)
        
        # Generate with full context
        response = llm.generate(
            context=context,
            history=self.short_term[-10:],  # Last 10 turns
            message=message
        )
        
        # Update memories
        self.update_long_term(message, response)
        
        return response
```

**Trade-offs**:
- **Pros**: Contextual awareness, personalization, continuity
- **Cons**: Storage costs, privacy concerns, memory retrieval complexity

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Over-Engineering Simple Tasks

**Problem**: Using complex multi-agent systems or ReAct loops for simple queries

**Example**:
```python
# ❌ BAD: Over-engineered
class SimpleQAAgent:
    def __init__(self):
        self.planner = PlanningAgent()
        self.executor = ExecutionAgent()
        self.critic = CriticAgent()
    
    def answer(self, question):
        plan = self.planner.create_plan(question)
        answer = self.executor.execute(plan)
        critique = self.critic.evaluate(answer)
        return self.refine(answer, critique)

# ✓ GOOD: Simple and direct
def answer_question(question):
    return llm.generate(f"Answer: {question}")
```

**Solution**: Start simple, add complexity only when needed

---

### Anti-Pattern 2: Ignoring Error Handling

**Problem**: No retry logic, circuit breakers, or graceful degradation

**Example**:
```python
# ❌ BAD: No error handling
def call_api(prompt):
    response = api.generate(prompt)
    return response

# ✓ GOOD: Robust error handling
def call_api(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = api.generate(prompt)
            return response
        except APIError as e:
            if attempt == max_retries - 1:
                return fallback_response(prompt)
            time.sleep(2 ** attempt)  # Exponential backoff
```

**Solution**: Always implement retry logic, timeouts, and fallbacks

---

### Anti-Pattern 3: Unbounded Context Windows

**Problem**: Adding unlimited history to context without management

**Example**:
```python
# ❌ BAD: Unbounded context
class ChatAgent:
    def __init__(self):
        self.history = []
    
    def chat(self, message):
        self.history.append(message)
        # Eventually exceeds context window
        return llm.generate(context=self.history)

# ✓ GOOD: Managed context
class ChatAgent:
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
    
    def chat(self, message):
        self.history.append(message)
        # Keep only recent history
        context = self.history[-self.max_history:]
        # Or use summarization for older context
        return llm.generate(context=context)
```

**Solution**: Implement context window management with truncation or summarization

---

### Anti-Pattern 4: No Retrieval Optimization

**Problem**: Retrieving too many or too few documents without tuning

**Example**:
```python
# ❌ BAD: Fixed retrieval without optimization
def rag_query(question):
    docs = vector_store.search(question, k=50)  # Too many!
    context = "\n".join([d.content for d in docs])
    return llm.generate(f"Context: {context}\nQ: {question}")

# ✓ GOOD: Optimized retrieval
def rag_query(question):
    # Retrieve with relevance threshold
    docs = vector_store.search(
        question,
        k=5,
        score_threshold=0.7
    )
    
    # Rerank for quality
    docs = reranker.rerank(question, docs)[:3]
    
    # Use only top results
    context = "\n".join([d.content for d in docs])
    return llm.generate(f"Context: {context}\nQ: {question}")
```

**Solution**: Tune retrieval parameters, use reranking, filter by relevance

---

### Anti-Pattern 5: Ignoring Latency Budgets

**Problem**: Not considering latency requirements in architecture decisions

**Example**:
```python
# ❌ BAD: Multiple sequential LLM calls
def process_query(query):
    classification = llm.generate(f"Classify: {query}")
    entities = llm.generate(f"Extract entities: {query}")
    intent = llm.generate(f"Determine intent: {query}")
    response = llm.generate(f"Respond to: {query}")
    return response  # 4x latency!

# ✓ GOOD: Parallel or combined processing
def process_query(query):
    # Single call with structured output
    result = llm.generate(f"""
    Analyze this query and provide:
    1. Classification
    2. Entities
    3. Intent
    4. Response
    
    Query: {query}
    """)
    return parse_structured_output(result)
```

**Solution**: Minimize sequential LLM calls, use batching, consider latency in design

---

### Anti-Pattern 6: No Monitoring or Observability

**Problem**: Deploying without logging, metrics, or tracing

**Example**:
```python
# ❌ BAD: No observability
def agent_endpoint(request):
    response = agent.process(request)
    return response

# ✓ GOOD: Full observability
def agent_endpoint(request):
    start_time = time.time()
    
    try:
        # Log request
        logger.info(f"Request: {request.id}")
        
        # Trace execution
        with tracer.span("agent_process"):
            response = agent.process(request)
        
        # Record metrics
        latency = time.time() - start_time
        metrics.record("latency", latency)
        metrics.record("success", 1)
        
        return response
    
    except Exception as e:
        logger.error(f"Error: {e}")
        metrics.record("error", 1)
        raise
```

**Solution**: Implement comprehensive logging, metrics, and tracing from day one

---

### Anti-Pattern 7: Hardcoded Prompts

**Problem**: Prompts embedded in code without version control or A/B testing

**Example**:
```python
# ❌ BAD: Hardcoded prompts
def generate_summary(text):
    prompt = "Summarize this text: " + text
    return llm.generate(prompt)

# ✓ GOOD: Managed prompts
class PromptManager:
    def __init__(self):
        self.prompts = self.load_prompts("prompts.yaml")
    
    def get_prompt(self, name, version="latest"):
        return self.prompts[name][version]

def generate_summary(text):
    prompt_template = prompt_manager.get_prompt("summarize")
    prompt = prompt_template.format(text=text)
    return llm.generate(prompt)
```

**Solution**: Externalize prompts, version them, enable A/B testing

---

### Anti-Pattern 8: No Guardrails or Safety Checks

**Problem**: Deploying without input validation or output filtering

**Example**:
```python
# ❌ BAD: No safety checks
def chat(user_input):
    return llm.generate(user_input)

# ✓ GOOD: Comprehensive safety
def chat(user_input):
    # Input validation
    if is_jailbreak_attempt(user_input):
        return "I cannot process that request."
    
    if contains_pii(user_input):
        user_input = redact_pii(user_input)
    
    # Generate with guardrails
    response = guardrails.generate(user_input)
    
    # Output filtering
    if is_toxic(response) or is_hallucination(response):
        return fallback_response()
    
    return response
```

**Solution**: Implement input validation, output filtering, and guardrails

---

### Anti-Pattern 9: Ignoring Cost Optimization

**Problem**: Not considering token usage, caching, or model selection

**Example**:
```python
# ❌ BAD: Expensive, uncached
def answer_faq(question):
    # Always uses largest model
    return gpt4.generate(f"Answer: {question}")

# ✓ GOOD: Cost-optimized
def answer_faq(question):
    # Check cache first
    cached = cache.get(question)
    if cached:
        return cached
    
    # Use smaller model for simple queries
    if is_simple_query(question):
        response = gpt3_5.generate(f"Answer: {question}")
    else:
        response = gpt4.generate(f"Answer: {question}")
    
    # Cache result
    cache.set(question, response)
    return response
```

**Solution**: Implement caching, use appropriate model sizes, optimize token usage

---

### Anti-Pattern 10: No Evaluation Pipeline

**Problem**: Deploying without systematic evaluation or testing

**Example**:
```python
# ❌ BAD: No evaluation
def deploy_agent():
    agent = build_agent()
    deploy(agent)  # Hope it works!

# ✓ GOOD: Systematic evaluation
def deploy_agent():
    agent = build_agent()
    
    # Run evaluation suite
    results = evaluate(
        agent,
        test_cases=load_test_cases(),
        metrics=["accuracy", "latency", "cost"]
    )
    
    # Check thresholds
    if results["accuracy"] < 0.8:
        raise ValueError("Accuracy below threshold")
    
    # A/B test before full rollout
    deploy_canary(agent, traffic_percent=10)
    
    # Monitor and gradually increase
    if monitor_metrics_ok():
        deploy_full(agent)
```

**Solution**: Build evaluation pipelines, set quality thresholds, use canary deployments

---

## Pattern Selection Guide

| Requirement | Recommended Pattern | Alternative |
|-------------|-------------------|-------------|
| External knowledge needed | RAG | Fine-tuning |
| Complex multi-step reasoning | ReAct | Chain-of-Thought |
| Specialized expertise needed | Multi-Agent | Single agent with tools |
| Interactive UI | Streaming | Batch generation |
| Long conversations | Memory-Augmented | Stateless with summarization |
| Real-time data access | Tool-augmented agent | RAG with live updates |
| High accuracy critical | Ensemble/Multi-agent | Single model with validation |
| Low latency critical | Cached + Small model | Large model optimization |

## Exam Tips

**Pattern Recognition**:
- Identify requirements in scenario (latency, accuracy, cost, complexity)
- Match requirements to appropriate patterns
- Consider trade-offs explicitly

**Common Traps**:
- Don't over-engineer simple problems
- Don't ignore error handling and monitoring
- Don't forget about cost and latency constraints
- Don't skip evaluation and testing

**Decision Framework**:
1. What is the core requirement?
2. What are the constraints (latency, cost, accuracy)?
3. What patterns fit these requirements?
4. What are the trade-offs?
5. How will we monitor and improve?
