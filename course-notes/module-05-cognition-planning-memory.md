# Module 5: Cognition, Planning, and Memory

**Exam Weight:** 10%  
**Estimated Study Time:** 6-8 hours  
**Prerequisites:** Module 1 (Agent Architecture), Module 2 (Agent Development)

## Learning Objectives

1. **Implement memory mechanisms** (short-term and long-term context)
2. **Apply reasoning frameworks** (chain-of-thought, task decomposition)
3. **Engineer planning strategies** for sequential decision-making
4. **Manage stateful orchestration** for complex tasks
5. **Adapt reasoning strategies** based on prior experiences

## Exam Objective Mapping

- **5.1** - Implement memory mechanisms (short- and long-term context)
- **5.2** - Apply reasoning frameworks (chain-of-thought, task decomposition)
- **5.3** - Engineer planning strategies for sequential decision-making
- **5.4** - Manage stateful orchestration for complex tasks
- **5.5** - Adapt reasoning strategies based on prior experiences

---

## 1. Memory Mechanisms

### 1.1 Short-Term Memory (Conversation Buffer)

```python
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory

# Full conversation history
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Last K messages only
window_memory = ConversationBufferWindowMemory(
    k=5,  # Keep last 5 exchanges
    memory_key="chat_history",
    return_messages=True
)

# Usage with agent
from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=window_memory,
    verbose=True
)
```

### 1.2 Long-Term Memory (Vector Store)

```python
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import NVIDIAEmbeddings

# Create vector store for memories
embeddings = NVIDIAEmbeddings(model="nvidia/nv-embed-v1")
vectorstore = FAISS.from_texts([], embeddings)

# Create memory with retrieval
long_term_memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    memory_key="history"
)

# Save context
long_term_memory.save_context(
    {"input": "My name is Alice"},
    {"output": "Nice to meet you, Alice!"}
)

# Retrieve relevant memories
relevant = long_term_memory.load_memory_variables(
    {"input": "What's my name?"}
)
```

### 1.3 Summary Memory

```python
from langchain.memory import ConversationSummaryMemory
from langchain_nvidia_ai_endpoints import ChatNVIDIA

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")

summary_memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history"
)

# Automatically summarizes old conversations
summary_memory.save_context(
    {"input": "Tell me about RAG"},
    {"output": "RAG combines retrieval with generation..."}
)

# Get summarized history
print(summary_memory.load_memory_variables({}))
```

> 📝 **EXAM TIP**
> 
> Buffer for short conversations, window for medium, summary for long, vector store for personalization across sessions.

---

## 2. Chain-of-Thought Reasoning

### 2.1 Basic Chain-of-Thought

```python
COT_PROMPT = """
Solve this problem step by step:

Problem: {problem}

Step 1: Understand what is being asked
Step 2: Identify the key information
Step 3: Plan the solution approach
Step 4: Execute the solution
Step 5: Verify the answer

Solution:
"""

from langchain_nvidia_ai_endpoints import ChatNVIDIA

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct", temperature=0.3)

response = llm.invoke(COT_PROMPT.format(
    problem="If a store has 15 apples and sells 40% of them, how many remain?"
))
```

### 2.2 Self-Consistency

```python
def self_consistency_cot(problem: str, num_samples: int = 5):
    """Generate multiple reasoning paths and vote"""
    
    responses = []
    for _ in range(num_samples):
        response = llm.invoke(COT_PROMPT.format(problem=problem))
        responses.append(response.content)
    
    # Extract final answers
    answers = [extract_answer(r) for r in responses]
    
    # Vote for most common answer
    from collections import Counter
    most_common = Counter(answers).most_common(1)[0][0]
    
    return most_common, responses
```

> 📝 **EXAM TIP**
> 
> CoT improves accuracy on complex reasoning. Self-consistency (multiple samples + voting) further improves reliability.

---

## 3. Task Decomposition

### 3.1 Hierarchical Task Planning

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class PlanState(TypedDict):
    task: str
    subtasks: List[str]
    completed: List[str]
    current_subtask: str
    result: str

def decompose_task(state: PlanState) -> PlanState:
    """Break task into subtasks"""
    prompt = f"Break this task into 3-5 subtasks: {state['task']}"
    response = llm.invoke(prompt)
    
    # Parse subtasks
    subtasks = [line.strip() for line in response.content.split('\n') if line.strip()]
    state["subtasks"] = subtasks
    state["current_subtask"] = subtasks[0] if subtasks else ""
    
    return state

def execute_subtask(state: PlanState) -> PlanState:
    """Execute current subtask"""
    result = agent_executor.invoke({"input": state["current_subtask"]})
    
    state["completed"].append(state["current_subtask"])
    state["result"] = result["output"]
    
    # Move to next subtask
    remaining = [t for t in state["subtasks"] if t not in state["completed"]]
    state["current_subtask"] = remaining[0] if remaining else ""
    
    return state

def should_continue(state: PlanState) -> str:
    """Check if more subtasks remain"""
    return "execute" if state["current_subtask"] else "end"

# Build workflow
workflow = StateGraph(PlanState)
workflow.add_node("decompose", decompose_task)
workflow.add_node("execute", execute_subtask)

workflow.set_entry_point("decompose")
workflow.add_edge("decompose", "execute")
workflow.add_conditional_edges("execute", should_continue, {
    "execute": "execute",
    "end": END
})

app = workflow.compile()
```

### 3.2 ReWOO (Reasoning WithOut Observation)

```python
class ReWOOPlanner:
    """Plan all steps before execution"""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def plan(self, task: str) -> List[Dict]:
        """Generate complete plan"""
        prompt = f"""
        Create a plan to solve: {task}
        
        Available tools: {[t.name for t in self.tools]}
        
        Format:
        #E1 = Tool[input]
        #E2 = Tool[input using #E1]
        ...
        """
        
        response = self.llm.invoke(prompt)
        return self._parse_plan(response.content)
    
    def execute_plan(self, plan: List[Dict]) -> str:
        """Execute all steps"""
        results = {}
        
        for step in plan:
            tool = self._get_tool(step["tool"])
            input_text = self._resolve_references(step["input"], results)
            
            result = tool.run(input_text)
            results[step["id"]] = result
        
        return results[plan[-1]["id"]]
```

> 📝 **EXAM TIP**
> 
> Task decomposition is essential for complex multi-step problems. ReWOO plans all steps upfront (faster), while ReAct plans iteratively (more adaptive).

---

## 4. Stateful Orchestration

### 4.1 LangGraph State Management

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

class AgentState(TypedDict):
    messages: List[str]
    user_info: Dict[str, Any]
    context: Dict[str, Any]
    next_action: str

# Define nodes
def process_input(state: AgentState) -> AgentState:
    """Process user input"""
    last_message = state["messages"][-1]
    
    # Update context based on input
    if "name" in last_message.lower():
        name = extract_name(last_message)
        state["user_info"]["name"] = name
    
    state["next_action"] = "respond"
    return state

def generate_response(state: AgentState) -> AgentState:
    """Generate personalized response"""
    context = f"User info: {state['user_info']}"
    prompt = f"{context}\n\nUser: {state['messages'][-1]}\nAssistant:"
    
    response = llm.invoke(prompt)
    state["messages"].append(response.content)
    state["next_action"] = "end"
    
    return state

# Build graph with persistence
memory = SqliteSaver.from_conn_string(":memory:")

workflow = StateGraph(AgentState)
workflow.add_node("process", process_input)
workflow.add_node("respond", generate_response)

workflow.set_entry_point("process")
workflow.add_edge("process", "respond")
workflow.add_edge("respond", END)

app = workflow.compile(checkpointer=memory)

# Use with persistent state
config = {"configurable": {"thread_id": "user_123"}}

# First interaction
result1 = app.invoke({
    "messages": ["My name is Alice"],
    "user_info": {},
    "context": {},
    "next_action": ""
}, config)

# Second interaction (remembers Alice)
result2 = app.invoke({
    "messages": ["What's my name?"],
    "user_info": result1["user_info"],
    "context": {},
    "next_action": ""
}, config)
```

> 📝 **EXAM TIP**
> 
> Stateful orchestration maintains context across interactions. LangGraph with checkpointers enables persistent state and conversation resumption.

---

## 5. Adaptive Reasoning

### 5.1 Learning from Feedback

```python
class AdaptiveAgent:
    """Agent that adapts based on feedback"""
    
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.success_patterns = []
        self.failure_patterns = []
    
    def invoke(self, query: str) -> str:
        """Invoke with adaptive strategy"""
        
        # Check if similar query succeeded before
        strategy = self._select_strategy(query)
        
        try:
            result = self._execute_with_strategy(query, strategy)
            self._record_success(query, strategy)
            return result
        except Exception as e:
            self._record_failure(query, strategy)
            # Try alternative strategy
            return self._execute_with_fallback(query)
    
    def _select_strategy(self, query: str) -> str:
        """Select strategy based on past performance"""
        # Check success patterns
        for pattern in self.success_patterns:
            if self._matches_pattern(query, pattern):
                return pattern["strategy"]
        
        return "default"
    
    def _record_success(self, query: str, strategy: str):
        """Record successful pattern"""
        self.success_patterns.append({
            "query_type": self._classify_query(query),
            "strategy": strategy
        })
    
    def _record_failure(self, query: str, strategy: str):
        """Record failed pattern"""
        self.failure_patterns.append({
            "query_type": self._classify_query(query),
            "strategy": strategy
        })
```

---

## 6. Exam Focus Areas

### Key Concepts

1. **Memory Types**: Buffer (short), Window (medium), Summary (long), Vector (persistent)
2. **Reasoning**: Chain-of-thought for complex problems, self-consistency for reliability
3. **Planning**: Task decomposition, ReWOO vs ReAct
4. **State Management**: LangGraph for stateful workflows
5. **Adaptation**: Learning from feedback, strategy selection

### Scenario Examples

**Example 1: Memory Selection**
> Your agent needs to remember user preferences across sessions. Which memory?
> 
> A) ConversationBufferMemory  
> B) ConversationBufferWindowMemory  
> C) VectorStoreRetrieverMemory  
> D) ConversationSummaryMemory  
>
> **Answer: C** - Vector store memory persists across sessions and retrieves relevant memories.

**Example 2: Reasoning Strategy**
> You need to solve a multi-step math problem with high accuracy. Which approach?
>
> A) Direct prompting  
> B) Chain-of-thought  
> C) Few-shot learning  
> D) Fine-tuning  
>
> **Answer: B** - Chain-of-thought breaks down complex reasoning into steps, improving accuracy.

---

## 7. Summary

**Key Takeaways:**
1. Memory mechanisms enable context retention
2. Chain-of-thought improves reasoning on complex tasks
3. Task decomposition handles multi-step problems
4. Stateful orchestration maintains context across interactions
5. Adaptive strategies improve over time

**Related Modules:**
- Module 1: Agent Architecture (memory in architecture)
- Module 2: Agent Development (implementing reasoning)
- Module 7: Monitoring (tracking reasoning quality)

---

## References

1. **Research Papers**
   - "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
   - "ReAct: Synergizing Reasoning and Acting in Language Models"
   - "ReWOO: Decoupling Reasoning from Observations"

2. **Related Materials**
   - Notebook: `module-05/01-memory-mechanisms.ipynb`
   - Notebook: `module-05/02-chain-of-thought.ipynb`
   - Notebook: `module-05/03-task-decomposition.ipynb`
   - Lab: `lab-02-multi-agent-research`


---

## Related Materials

### Hands-On Practice

**Interactive Notebooks:**
- [01-memory-mechanisms.ipynb](../../notebooks/module-05/01-memory-mechanisms.ipynb)
- [02-chain-of-thought.ipynb](../../notebooks/module-05/02-chain-of-thought.ipynb)
- [03-task-decomposition.ipynb](../../notebooks/module-05/03-task-decomposition.ipynb)

**Practice Labs:**
- [Lab: Lab 02 Multi Agent Research](../../labs/lab-02-multi-agent-research/README.md)

### Assessment

**Exam Questions:**
- [Domain 05 Cognition Memory](../../exam-questions/domain-05-cognition-memory.md)
