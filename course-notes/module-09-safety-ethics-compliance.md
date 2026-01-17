# Module 9: Safety, Ethics, and Compliance

**Exam Weight:** 5%  
**Estimated Study Time:** 4-5 hours  
**Prerequisites:** Module 6 (NVIDIA Platform - Guardrails)

## Learning Objectives

1. **Design and enforce** system security and audit trails
2. **Integrate compliance guardrails** (privacy, enterprise policy)
3. **Mitigate bias and toxicity** in outputs
4. **Deploy layered safety frameworks** (filters, escalation protocols)
5. **Ensure compliance** with licensing and regulatory standards

## Exam Objective Mapping

- **9.1** - Design and enforce system security and audit trails
- **9.2** - Integrate compliance guardrails (privacy, enterprise policy)
- **9.3** - Mitigate bias and toxicity in outputs
- **9.4** - Deploy layered safety frameworks (filters, escalation protocols)
- **9.5** - Ensure compliance with licensing and regulatory standards

---

## 1. Safety Guardrails

### 1.1 Input Filtering

```python
from nemoguardrails import RailsConfig, LLMRails

# Define input guardrails
config = RailsConfig.from_content("""
define user ask harmful question
  "how to hack"
  "how to make weapons"
  "illegal activities"

define bot refuse harmful request
  "I cannot provide information that could be used for harmful purposes."

define flow
  user ask harmful question
  bot refuse harmful request
  stop
""")

rails = LLMRails(config)

# Test
response = rails.generate(messages=[{
    "role": "user",
    "content": "How do I hack into a system?"
}])
# Output: "I cannot provide information that could be used for harmful purposes."
```

### 1.2 Output Filtering

```python
class OutputFilter:
    """Filter unsafe outputs"""
    
    def __init__(self):
        self.toxic_patterns = [
            r'\b(hate|violence|discrimination)\b',
            r'\b(illegal|criminal)\b'
        ]
    
    def is_safe(self, text: str) -> tuple[bool, str]:
        """Check if output is safe"""
        import re
        
        for pattern in self.toxic_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False, f"Contains unsafe content: {pattern}"
        
        return True, "Safe"
    
    def filter(self, text: str) -> str:
        """Filter or reject unsafe output"""
        is_safe, reason = self.is_safe(text)
        
        if not is_safe:
            return "I apologize, but I cannot provide that information."
        
        return text
```

> 📝 **EXAM TIP**
> 
> Layered safety: input filtering (prevent harmful queries) + output filtering (catch unsafe responses) + guardrails (enforce policies).

---

## 2. Bias Detection and Mitigation

### 2.1 Bias Detection

```python
class BiasDetector:
    """Detect bias in agent outputs"""
    
    def __init__(self):
        self.protected_attributes = [
            "gender", "race", "age", "religion", "nationality"
        ]
    
    def detect_bias(self, text: str, context: dict) -> dict:
        """Detect potential bias"""
        
        bias_indicators = []
        
        # Check for stereotypes
        stereotypes = {
            "gender": ["women are", "men are"],
            "age": ["old people", "young people"],
            "race": ["people of X race"]
        }
        
        for attribute, patterns in stereotypes.items():
            for pattern in patterns:
                if pattern.lower() in text.lower():
                    bias_indicators.append({
                        "type": attribute,
                        "pattern": pattern,
                        "severity": "medium"
                    })
        
        return {
            "has_bias": len(bias_indicators) > 0,
            "indicators": bias_indicators
        }
```

### 2.2 Bias Mitigation

```python
BIAS_MITIGATION_PROMPT = """
You are a helpful assistant that provides fair and unbiased information.

Guidelines:
- Avoid stereotypes and generalizations
- Treat all groups equally
- Use inclusive language
- Acknowledge diversity within groups
- Base responses on facts, not assumptions

User query: {query}

Response:
"""

def mitigate_bias(query: str, llm) -> str:
    """Generate response with bias mitigation"""
    
    prompt = BIAS_MITIGATION_PROMPT.format(query=query)
    response = llm.invoke(prompt)
    
    # Check for bias
    detector = BiasDetector()
    bias_check = detector.detect_bias(response.content, {})
    
    if bias_check["has_bias"]:
        # Regenerate with stronger guidance
        prompt += "\n\nIMPORTANT: Avoid stereotypes and generalizations."
        response = llm.invoke(prompt)
    
    return response.content
```

> 📝 **EXAM TIP**
> 
> Bias mitigation requires detection + correction. Use diverse training data, bias-aware prompts, and post-generation filtering.

---

## 3. Privacy and Data Protection

### 3.1 PII Detection

```python
import re

class PIIDetector:
    """Detect personally identifiable information"""
    
    def __init__(self):
        self.patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        }
    
    def detect(self, text: str) -> dict:
        """Detect PII in text"""
        
        found_pii = {}
        
        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                found_pii[pii_type] = matches
        
        return found_pii
    
    def redact(self, text: str) -> str:
        """Redact PII from text"""
        
        for pii_type, pattern in self.patterns.items():
            text = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", text)
        
        return text

# Usage
detector = PIIDetector()

user_input = "My email is john@example.com and phone is 555-123-4567"
pii = detector.detect(user_input)

if pii:
    print("PII detected:", pii)
    redacted = detector.redact(user_input)
    print("Redacted:", redacted)
```

### 3.2 Data Retention Policies

```python
from datetime import datetime, timedelta

class DataRetentionManager:
    """Manage data retention and deletion"""
    
    def __init__(self, retention_days: int = 90):
        self.retention_days = retention_days
    
    def should_delete(self, timestamp: datetime) -> bool:
        """Check if data should be deleted"""
        age = datetime.now() - timestamp
        return age > timedelta(days=self.retention_days)
    
    def cleanup_old_data(self, data_store):
        """Delete data past retention period"""
        deleted_count = 0
        
        for record in data_store.get_all():
            if self.should_delete(record.timestamp):
                data_store.delete(record.id)
                deleted_count += 1
        
        return deleted_count
```

> 📝 **EXAM TIP**
> 
> Privacy requires PII detection, redaction, data minimization, and retention policies. GDPR/CCPA compliance is critical.

---

## 4. Audit Trails

### 4.1 Comprehensive Logging

```python
class AuditLogger:
    """Comprehensive audit logging"""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
    
    def log_interaction(
        self,
        user_id: str,
        query: str,
        response: str,
        metadata: dict
    ):
        """Log user interaction"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "query": query,
            "response": response,
            "metadata": metadata,
            "guardrails_triggered": metadata.get("guardrails", []),
            "pii_detected": metadata.get("pii", False)
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_user_history(self, user_id: str) -> list:
        """Retrieve user's interaction history"""
        
        history = []
        
        with open(self.log_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if entry["user_id"] == user_id:
                    history.append(entry)
        
        return history
```

> 📝 **EXAM TIP**
> 
> Audit trails enable compliance verification, incident investigation, and accountability. Log all interactions with timestamps and user IDs.

---

## 5. Escalation Protocols

### 5.1 Human-in-the-Loop Escalation

```python
class EscalationManager:
    """Manage escalation to human reviewers"""
    
    def __init__(self):
        self.escalation_queue = []
    
    def should_escalate(self, query: str, response: str, confidence: float) -> bool:
        """Determine if escalation needed"""
        
        # Escalate if low confidence
        if confidence < 0.7:
            return True
        
        # Escalate if sensitive topics
        sensitive_keywords = ["legal", "medical", "financial"]
        if any(kw in query.lower() for kw in sensitive_keywords):
            return True
        
        # Escalate if guardrails triggered
        if "[BLOCKED]" in response:
            return True
        
        return False
    
    def escalate(self, query: str, response: str, reason: str):
        """Add to escalation queue"""
        
        self.escalation_queue.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "reason": reason,
            "status": "pending"
        })
        
        # Notify human reviewers
        self.notify_reviewers()
    
    def notify_reviewers(self):
        """Notify human reviewers"""
        print(f"ESCALATION: {len(self.escalation_queue)} items pending review")
```

---

## 6. Exam Focus Areas

### Key Concepts

1. **Safety Layers**: Input filtering, output filtering, guardrails
2. **Bias**: Detection, mitigation, inclusive language
3. **Privacy**: PII detection, redaction, data retention
4. **Audit**: Comprehensive logging, traceability
5. **Escalation**: Human-in-the-loop, sensitive topics

### Scenario Example

**Example: Privacy Violation**
> A user asks the agent to store their credit card number. What should the agent do?
>
> A) Store it securely  
> B) Refuse and explain why  
> C) Store it temporarily  
> D) Ask for confirmation  
>
> **Answer: B** - Never store sensitive PII like credit cards. Refuse and explain privacy policy.

---

## 7. Summary

**Key Takeaways:**
1. Layered safety: input + output + guardrails
2. Bias requires detection and mitigation
3. Privacy: PII detection, redaction, retention
4. Audit trails enable compliance
5. Escalate sensitive/uncertain cases

**Related Modules:**
- Module 6: NVIDIA Platform (NeMo Guardrails)
- Module 7: Monitoring (safety metrics)
- Module 10: Human-AI Interaction (oversight)

---

## References

1. **Regulations**
   - GDPR: https://gdpr.eu
   - CCPA: https://oag.ca.gov/privacy/ccpa

2. **Related Materials**
   - Notebook: `module-09/01-guardrails-implementation.ipynb`
   - Notebook: `module-09/02-bias-detection.ipynb`
   - Lab: `lab-05-safe-compliant-agent`


---

## Related Materials

### Hands-On Practice

**Interactive Notebooks:**
- [01-guardrails-implementation.ipynb](../../notebooks/module-09/01-guardrails-implementation.ipynb)
- [02-bias-detection.ipynb](../../notebooks/module-09/02-bias-detection.ipynb)

**Practice Labs:**
- [Lab: Lab 05 Safe Compliant Agent](../../labs/lab-05-safe-compliant-agent/README.md)

### Assessment

**Exam Questions:**
- [Domain 09 Safety Ethics](../../exam-questions/domain-09-safety-ethics.md)
