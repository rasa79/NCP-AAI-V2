# Module 10: Human-AI Interaction and Oversight

**Exam Weight:** 5%  
**Estimated Study Time:** 4-5 hours  
**Prerequisites:** Module 2 (Agent Development), Gradio basics

## Learning Objectives

1. **Build intuitive UIs** with user-in-the-loop interaction
2. **Design structured feedback loops** for iterative improvements
3. **Implement transparency mechanisms** (explainable reasoning)
4. **Enable human oversight** and intervention for accountability

## Exam Objective Mapping

- **10.1** - Build intuitive UIs with user-in-the-loop interaction
- **10.2** - Design structured feedback loops for iterative improvements
- **10.3** - Implement transparency mechanisms (explainable reasoning)
- **10.4** - Enable human oversight and intervention for accountability

---

## 1. Building Intuitive UIs with Gradio

### 1.1 Basic Chat Interface

```python
import gradio as gr
from langchain.agents import AgentExecutor

def chat_interface(message, history):
    """Chat interface for agent"""
    
    # Invoke agent
    response = agent_executor.invoke({"input": message})
    
    return response["output"]

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat_interface,
    title="RAG Agent Assistant",
    description="Ask me anything about our documentation",
    examples=[
        "What is RAG?",
        "How do I deploy with Kubernetes?",
        "Explain NVIDIA NIM"
    ]
)

demo.launch()
```

### 1.2 Advanced Interface with Feedback

```python
import gradio as gr

def chat_with_feedback(message, history):
    """Chat with feedback collection"""
    
    response = agent_executor.invoke({"input": message})
    
    return response["output"], response.get("sources", [])

def collect_feedback(message, response, rating, comment):
    """Collect user feedback"""
    
    feedback_collector.collect_feedback(
        session_id="gradio_session",
        question=message,
        answer=response,
        feedback_type=FeedbackType.RATING,
        rating=rating,
        comment=comment
    )
    
    return "Thank you for your feedback!"

with gr.Blocks() as demo:
    gr.Markdown("# RAG Agent with Feedback")
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your question")
    sources = gr.Textbox(label="Sources", interactive=False)
    
    # Feedback section
    with gr.Row():
        rating = gr.Slider(1, 5, step=1, label="Rating")
        comment = gr.Textbox(label="Comments (optional)")
        submit_feedback = gr.Button("Submit Feedback")
    
    feedback_status = gr.Textbox(label="Status")
    
    # Event handlers
    msg.submit(chat_with_feedback, [msg, chatbot], [chatbot, sources])
    submit_feedback.click(
        collect_feedback,
        [msg, chatbot, rating, comment],
        feedback_status
    )

demo.launch()
```

> 📝 **EXAM TIP**
> 
> Gradio enables rapid UI development. Include examples, feedback mechanisms, and source attribution for transparency.

---

## 2. User-in-the-Loop Workflows

### 2.1 Confirmation Before Action

```python
class UserInTheLoopAgent:
    """Agent that requests user confirmation for critical actions"""
    
    def __init__(self, agent, critical_actions: list):
        self.agent = agent
        self.critical_actions = critical_actions
        self.pending_actions = []
    
    def invoke(self, query: str, auto_approve: bool = False):
        """Invoke with user confirmation"""
        
        # Get agent's planned actions
        plan = self.agent.plan(query)
        
        # Check for critical actions
        for action in plan:
            if action["tool"] in self.critical_actions:
                if not auto_approve:
                    # Request user confirmation
                    approved = self.request_confirmation(action)
                    if not approved:
                        return "Action cancelled by user"
        
        # Execute approved actions
        return self.agent.execute(plan)
    
    def request_confirmation(self, action: dict) -> bool:
        """Request user confirmation"""
        print(f"\nConfirmation required:")
        print(f"Action: {action['tool']}")
        print(f"Parameters: {action['params']}")
        
        response = input("Approve? (yes/no): ")
        return response.lower() == "yes"
```

### 2.2 Gradio Interface with Confirmation

```python
import gradio as gr

def agent_with_confirmation(message, history, auto_approve):
    """Agent that requests confirmation"""
    
    if auto_approve:
        response = agent_executor.invoke({"input": message})
        return response["output"], "Auto-approved"
    else:
        # Show planned actions
        plan = agent.plan(message)
        
        actions_text = "\n".join([
            f"- {action['tool']}: {action['params']}"
            for action in plan
        ])
        
        return "", f"Planned actions:\n{actions_text}\n\nClick 'Execute' to proceed"

def execute_plan():
    """Execute approved plan"""
    result = agent.execute_pending_plan()
    return result, "Executed"

with gr.Blocks() as demo:
    gr.Markdown("# Agent with User Confirmation")
    
    msg = gr.Textbox(label="Your request")
    auto_approve = gr.Checkbox(label="Auto-approve actions")
    
    response = gr.Textbox(label="Response")
    status = gr.Textbox(label="Status")
    
    submit = gr.Button("Submit")
    execute = gr.Button("Execute Plan")
    
    submit.click(agent_with_confirmation, [msg, None, auto_approve], [response, status])
    execute.click(execute_plan, [], [response, status])

demo.launch()
```

> 📝 **EXAM TIP**
> 
> User-in-the-loop is critical for high-stakes actions (financial transactions, data deletion). Always confirm before executing.

---

## 3. Feedback Loops

### 3.1 Structured Feedback Collection

```python
class FeedbackLoop:
    """Continuous feedback collection and integration"""
    
    def __init__(self, agent, feedback_collector):
        self.agent = agent
        self.feedback_collector = feedback_collector
        self.improvement_threshold = 10  # Retrain after N negative feedbacks
    
    def collect_and_improve(self, query: str, response: str, rating: int):
        """Collect feedback and trigger improvements"""
        
        # Collect feedback
        self.feedback_collector.collect_feedback(
            session_id="production",
            question=query,
            answer=response,
            feedback_type=FeedbackType.RATING,
            rating=rating
        )
        
        # Check if improvement needed
        negative_count = sum(
            1 for f in self.feedback_collector.feedback_data
            if f.rating <= 2
        )
        
        if negative_count >= self.improvement_threshold:
            self.trigger_improvement()
    
    def trigger_improvement(self):
        """Trigger improvement process"""
        
        # Analyze negative feedback
        negative_examples = self.feedback_collector.get_negative_feedback_examples()
        
        # Extract common issues
        issues = self.analyze_issues(negative_examples)
        
        # Generate improvement suggestions
        suggestions = self.generate_suggestions(issues)
        
        # Notify team
        self.notify_team(suggestions)
    
    def analyze_issues(self, examples: list) -> dict:
        """Analyze common issues in negative feedback"""
        
        issues = {
            "incorrect": 0,
            "incomplete": 0,
            "irrelevant": 0,
            "slow": 0
        }
        
        for example in examples:
            if example.issue_category:
                category = example.issue_category.value
                issues[category] = issues.get(category, 0) + 1
        
        return issues
```

### 3.2 Active Learning

```python
class ActiveLearner:
    """Select most informative examples for human review"""
    
    def __init__(self, agent):
        self.agent = agent
        self.uncertain_examples = []
    
    def identify_uncertain(self, query: str, response: str, confidence: float):
        """Identify uncertain predictions"""
        
        if confidence < 0.7:
            self.uncertain_examples.append({
                "query": query,
                "response": response,
                "confidence": confidence
            })
    
    def get_examples_for_review(self, n: int = 10) -> list:
        """Get most uncertain examples for human review"""
        
        # Sort by confidence (lowest first)
        sorted_examples = sorted(
            self.uncertain_examples,
            key=lambda x: x["confidence"]
        )
        
        return sorted_examples[:n]
```

> 📝 **EXAM TIP**
> 
> Feedback loops enable continuous improvement. Collect structured feedback, analyze patterns, and trigger improvements automatically.

---

## 4. Explainability and Transparency

### 4.1 Explaining Agent Reasoning

```python
class ExplainableAgent:
    """Agent that explains its reasoning"""
    
    def __init__(self, agent):
        self.agent = agent
    
    def invoke_with_explanation(self, query: str) -> dict:
        """Invoke and provide explanation"""
        
        # Get response with intermediate steps
        response = self.agent.invoke(
            {"input": query},
            return_intermediate_steps=True
        )
        
        # Generate explanation
        explanation = self.generate_explanation(
            response["intermediate_steps"]
        )
        
        return {
            "answer": response["output"],
            "explanation": explanation,
            "sources": self.extract_sources(response["intermediate_steps"])
        }
    
    def generate_explanation(self, steps: list) -> str:
        """Generate human-readable explanation"""
        
        explanation_parts = ["Here's how I arrived at this answer:\n"]
        
        for i, (action, observation) in enumerate(steps, 1):
            explanation_parts.append(
                f"{i}. I used {action.tool} to {action.tool_input}"
            )
            explanation_parts.append(
                f"   Result: {observation[:100]}..."
            )
        
        return "\n".join(explanation_parts)
    
    def extract_sources(self, steps: list) -> list:
        """Extract source documents"""
        
        sources = []
        for action, observation in steps:
            if hasattr(observation, 'metadata'):
                sources.append(observation.metadata.get('source', 'Unknown'))
        
        return list(set(sources))
```

### 4.2 Gradio Interface with Explanations

```python
import gradio as gr

def chat_with_explanation(message, history):
    """Chat with explanations"""
    
    explainable_agent = ExplainableAgent(agent_executor)
    result = explainable_agent.invoke_with_explanation(message)
    
    return (
        result["answer"],
        result["explanation"],
        "\n".join(result["sources"])
    )

with gr.Blocks() as demo:
    gr.Markdown("# Explainable RAG Agent")
    
    with gr.Row():
        with gr.Column():
            msg = gr.Textbox(label="Your question")
            submit = gr.Button("Ask")
        
        with gr.Column():
            answer = gr.Textbox(label="Answer")
            explanation = gr.Textbox(label="Reasoning", lines=5)
            sources = gr.Textbox(label="Sources")
    
    submit.click(chat_with_explanation, [msg, None], [answer, explanation, sources])

demo.launch()
```

> 📝 **EXAM TIP**
> 
> Explainability builds trust. Show reasoning steps, source documents, and confidence scores. Critical for high-stakes decisions.

---

## 5. Human Oversight

### 5.1 Monitoring Dashboard

```python
class OversightDashboard:
    """Dashboard for human oversight"""
    
    def __init__(self, agent):
        self.agent = agent
        self.interactions = []
        self.flagged_interactions = []
    
    def log_interaction(self, query: str, response: str, metadata: dict):
        """Log interaction for oversight"""
        
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "metadata": metadata
        }
        
        self.interactions.append(interaction)
        
        # Flag if needed
        if self.should_flag(interaction):
            self.flagged_interactions.append(interaction)
    
    def should_flag(self, interaction: dict) -> bool:
        """Determine if interaction should be flagged"""
        
        # Flag low confidence
        if interaction["metadata"].get("confidence", 1.0) < 0.7:
            return True
        
        # Flag guardrail triggers
        if interaction["metadata"].get("guardrails_triggered"):
            return True
        
        # Flag sensitive topics
        sensitive_keywords = ["legal", "medical", "financial"]
        if any(kw in interaction["query"].lower() for kw in sensitive_keywords):
            return True
        
        return False
    
    def get_flagged_for_review(self) -> list:
        """Get flagged interactions for human review"""
        return self.flagged_interactions
```

### 5.2 Intervention Mechanisms

```python
class InterventionManager:
    """Enable human intervention"""
    
    def __init__(self, agent):
        self.agent = agent
        self.intervention_log = []
    
    def intervene(self, interaction_id: str, corrected_response: str, reason: str):
        """Human intervenes to correct response"""
        
        self.intervention_log.append({
            "timestamp": datetime.now().isoformat(),
            "interaction_id": interaction_id,
            "corrected_response": corrected_response,
            "reason": reason
        })
        
        # Update agent's knowledge
        self.agent.learn_from_correction(corrected_response, reason)
    
    def get_intervention_stats(self) -> dict:
        """Get intervention statistics"""
        
        return {
            "total_interventions": len(self.intervention_log),
            "intervention_rate": len(self.intervention_log) / total_interactions,
            "common_reasons": self.analyze_reasons()
        }
```

> 📝 **EXAM TIP**
> 
> Human oversight is essential for accountability. Flag uncertain/sensitive cases, enable intervention, and learn from corrections.

---

## 6. Exam Focus Areas

### Key Concepts

1. **UI Design**: Gradio, chat interfaces, feedback collection
2. **User-in-the-Loop**: Confirmation workflows, approval gates
3. **Feedback Loops**: Structured collection, active learning
4. **Explainability**: Reasoning traces, source attribution
5. **Oversight**: Monitoring, flagging, intervention

### Scenario Example

**Example: High-Stakes Decision**
> Your agent recommends a medical treatment. What should you implement?
>
> A) Auto-execute recommendation  
> B) Require human confirmation + show reasoning  
> C) Block medical queries entirely  
> D) Show disclaimer only  
>
> **Answer: B** - High-stakes decisions require human confirmation and explainability. Never auto-execute medical/legal/financial advice.

---

## 7. Summary

**Key Takeaways:**
1. Intuitive UIs improve user experience
2. User-in-the-loop for critical actions
3. Feedback loops enable continuous improvement
4. Explainability builds trust
5. Human oversight ensures accountability

**Related Modules:**
- Module 2: Agent Development (UI integration)
- Module 9: Safety and Ethics (oversight)

---

## References

1. **Tools**
   - Gradio: https://gradio.app
   - Streamlit: https://streamlit.io

2. **Related Materials**
   - Notebook: `module-10/01-ui-development.ipynb`
   - Notebook: `module-10/02-feedback-loops.ipynb`
   - Lab: `lab-05-safe-compliant-agent`


---

## Related Materials

### Hands-On Practice

**Interactive Notebooks:**
- [01-ui-development.ipynb](../../notebooks/module-10/01-ui-development.ipynb)
- [02-feedback-loops.ipynb](../../notebooks/module-10/02-feedback-loops.ipynb)

**Practice Labs:**
- [Lab: Lab 05 Safe Compliant Agent](../../labs/lab-05-safe-compliant-agent/README.md)

### Assessment

**Exam Questions:**
- [Domain 10 Human Interaction](../../exam-questions/domain-10-human-interaction.md)
