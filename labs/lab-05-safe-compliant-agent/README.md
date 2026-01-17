# Lab 5: Safe and Compliant Agent

## Overview

In this lab, you'll implement comprehensive safety and compliance mechanisms for RAG agents. This advanced lab introduces NVIDIA NeMo Guardrails, bias detection, privacy preservation, audit trails, and escalation protocols. You'll transform a basic RAG agent into a production-ready system that meets enterprise safety, ethical, and regulatory requirements.

## Learning Objectives

- Integrate NVIDIA NeMo Guardrails for safety enforcement (maps to exam objective 9.1: Guardrails Implementation)
- Implement input validation and output filtering (maps to exam objective 9.2: Content Filtering)
- Detect and mitigate bias in responses (maps to exam objective 9.3: Bias Detection)
- Apply privacy preservation techniques (maps to exam objective 9.4: Privacy Preservation)
- Implement compliance audit trails (maps to exam objective 9.5: Compliance)
- Design escalation protocols for unsafe outputs (maps to exam objective 9.6: Escalation)

## Prerequisites

- Completed modules: Module 9 (Safety, Ethics, and Compliance), Module 10 (Human-AI Interaction)
- Completed Lab 1: Basic RAG Agent
- Required knowledge: Safety concepts, compliance requirements, NVIDIA NeMo Guardrails
- Estimated time: 5-6 hours

## Scenario

**Company:** SecureAI Corp., a healthcare AI solutions provider

**Challenge:** Your company is deploying a RAG agent to assist healthcare professionals with medical information. Due to the sensitive nature of healthcare, the system must meet strict requirements:
- HIPAA compliance for patient data
- FDA guidelines for medical AI systems
- Prevent harmful medical advice
- Detect and mitigate bias (racial, gender, age)
- Maintain comprehensive audit trails
- Escalate uncertain or risky queries to humans

**Your Task:** Implement a comprehensive safety and compliance framework that:
- Blocks harmful, biased, or inappropriate content
- Validates inputs and filters outputs
- Detects and mitigates various forms of bias
- Preserves privacy (PII redaction, data anonymization)
- Maintains detailed audit logs for compliance
- Escalates high-risk queries to human reviewers
- Provides transparency and explainability

**Business Requirements:**
- Block 100% of explicitly harmful content
- Detect bias with > 90% accuracy
- Redact all PII automatically
- Maintain audit trail for 7 years
- Escalate high-risk queries within 1 second
- Meet HIPAA and FDA compliance standards

**Technical Constraints:**
- Use NVIDIA NeMo Guardrails for safety enforcement
- Implement multi-layer defense (input, output, retrieval)
- Support real-time bias detection
- Maintain performance (< 500ms overhead)
- Provide explainable decisions

## Requirements

### Functional Requirements

1. **Input Guardrails**
   - Block jailbreak attempts
   - Detect prompt injection
   - Validate input format and length
   - Check for malicious patterns
   - Rate limiting per user

2. **Output Guardrails**
   - Filter harmful content
   - Detect hallucinations
   - Check factual accuracy
   - Prevent data leakage
   - Ensure appropriate tone

3. **Bias Detection and Mitigation**
   - Detect racial bias
   - Detect gender bias
   - Detect age bias
   - Detect socioeconomic bias
   - Mitigate detected biases

4. **Privacy Preservation**
   - Detect and redact PII (names, SSN, addresses, etc.)
   - Anonymize sensitive data
   - Implement differential privacy (optional)
   - Secure data handling
   - Comply with GDPR/HIPAA

5. **Audit and Compliance**
   - Log all interactions
   - Track guardrail triggers
   - Maintain decision provenance
   - Generate compliance reports
   - Support audit queries

6. **Escalation Protocol**
   - Identify high-risk queries
   - Route to human reviewers
   - Provide context for review
   - Track escalation outcomes
   - Learn from escalations

### Performance Requirements

- Guardrail latency: < 500ms overhead
- Bias detection: < 200ms
- PII redaction: < 100ms
- Audit logging: < 50ms
- Escalation routing: < 1 second

### Quality Requirements

- Harmful content blocking: 100% recall
- Bias detection: > 90% accuracy
- PII detection: > 95% recall
- False positive rate: < 5%
- Audit completeness: 100%

## Success Criteria

- [ ] NeMo Guardrails integrated successfully
- [ ] Input validation blocks malicious inputs
- [ ] Output filtering prevents harmful content
- [ ] Bias detection identifies biased responses
- [ ] PII redaction works correctly
- [ ] Audit trail captures all interactions
- [ ] Escalation protocol routes high-risk queries
- [ ] Performance overhead < 500ms
- [ ] All compliance tests pass

## Setup Instructions

### 1. Environment Setup

```bash
# Navigate to lab directory
cd labs/lab-05-safe-compliant-agent

# Install dependencies
pip install -r requirements.txt

# Verify NeMo Guardrails installation
nemoguardrails --version
```

### 2. Project Structure

```
lab-05-safe-compliant-agent/
├── README.md (this file)
├── requirements.txt
├── starter-code/
│   ├── guardrails/
│   │   ├── config.yml (NeMo Guardrails config)
│   │   ├── input_rails.py (input validation)
│   │   ├── output_rails.py (output filtering)
│   │   └── retrieval_rails.py (retrieval filtering)
│   ├── bias/
│   │   ├── detector.py (bias detection)
│   │   ├── mitigator.py (bias mitigation)
│   │   └── metrics.py (bias metrics)
│   ├── privacy/
│   │   ├── pii_detector.py (PII detection)
│   │   ├── redactor.py (PII redaction)
│   │   └── anonymizer.py (data anonymization)
│   ├── compliance/
│   │   ├── audit_logger.py (audit logging)
│   │   ├── compliance_checker.py (compliance validation)
│   │   └── report_generator.py (compliance reports)
│   ├── escalation/
│   │   ├── risk_assessor.py (risk assessment)
│   │   ├── escalation_router.py (routing logic)
│   │   └── human_review.py (review interface)
│   └── safe_rag_agent.py (integrated agent)
├── test-data/
│   ├── harmful_inputs.json (test cases)
│   ├── biased_responses.json (bias test cases)
│   ├── pii_examples.json (PII test cases)
│   └── compliance_scenarios.json (compliance tests)
├── solution/
│   └── [reference implementation]
└── rubric.md (evaluation criteria)
```

## Implementation Tasks

### Task 1: Configure NeMo Guardrails (60 minutes)

Configure guardrails in `guardrails/config.yml`:

**Guardrail Types:**
1. **Input Rails**
   - Jailbreak detection
   - Prompt injection prevention
   - Topic restrictions
   - Length limits

2. **Output Rails**
   - Harmful content filtering
   - Hallucination detection
   - Factuality checking
   - Tone enforcement

3. **Retrieval Rails**
   - Source validation
   - Content filtering
   - Relevance checking

**Hints:**
- Use NeMo Guardrails YAML configuration
- Define custom rails for domain-specific needs
- Set appropriate thresholds
- Test with adversarial inputs

**Validation:**
```bash
# Test guardrails configuration
nemoguardrails test --config guardrails/config.yml
```

### Task 2: Implement Bias Detection (60 minutes)

Implement bias detection in `bias/detector.py`:

**Bias Types to Detect:**
- Racial/ethnic bias
- Gender bias
- Age bias
- Socioeconomic bias
- Disability bias

**Detection Methods:**
- Keyword-based detection
- Sentiment analysis by demographic
- Counterfactual testing
- LLM-based bias scoring

**Hints:**
- Use pre-trained bias detection models
- Implement counterfactual generation
- Test with known biased examples
- Provide bias scores and explanations

**Validation:**
```python
from bias.detector import BiasDetector

detector = BiasDetector()
result = detector.detect(
    text="The doctor said he would...",
    context="medical advice"
)
print(f"Gender bias score: {result['gender_bias']}")
```

### Task 3: Implement PII Detection and Redaction (45 minutes)

Implement privacy protection in `privacy/`:

**PII Types:**
- Names (person, organization)
- Addresses
- Phone numbers
- Email addresses
- SSN, credit cards
- Medical record numbers
- Dates of birth

**Redaction Strategies:**
- Replace with placeholders ([NAME], [ADDRESS])
- Replace with synthetic data
- Hash sensitive values
- Complete removal

**Hints:**
- Use spaCy or transformers for NER
- Implement regex patterns for structured PII
- Support multiple redaction strategies
- Preserve context where possible

**Validation:**
```python
from privacy.pii_detector import PIIDetector
from privacy.redactor import PIIRedactor

detector = PIIDetector()
redactor = PIIRedactor()

text = "John Smith lives at 123 Main St, SSN: 123-45-6789"
pii_entities = detector.detect(text)
redacted = redactor.redact(text, pii_entities)
print(redacted)  # "[NAME] lives at [ADDRESS], SSN: [SSN]"
```

### Task 4: Implement Audit Logging (45 minutes)

Implement compliance logging in `compliance/audit_logger.py`:

**Audit Information:**
- Timestamp
- User ID (anonymized)
- Query and response
- Guardrail triggers
- Bias detection results
- PII redactions
- Escalation decisions
- System version

**Storage:**
- Structured logging (JSON)
- Secure storage
- Retention policies
- Query capabilities

**Hints:**
- Use structured logging library
- Encrypt sensitive audit data
- Implement log rotation
- Support compliance queries

**Validation:**
```python
from compliance.audit_logger import AuditLogger

logger = AuditLogger()
logger.log_interaction(
    user_id="user_123",
    query="What is the treatment for...",
    response="The treatment involves...",
    guardrails_triggered=["output_filter"],
    bias_detected=False,
    pii_redacted=["patient_name"]
)
```

### Task 5: Implement Escalation Protocol (60 minutes)

Implement escalation in `escalation/`:

**Risk Assessment Criteria:**
- Uncertainty score (model confidence)
- Sensitivity of topic
- Potential harm level
- Compliance risk
- Bias detection
- Guardrail triggers

**Escalation Routing:**
- Immediate escalation (high risk)
- Deferred review (medium risk)
- Automated handling (low risk)
- Human-in-the-loop for edge cases

**Hints:**
- Define risk scoring function
- Implement routing logic
- Create review queue
- Track escalation outcomes
- Learn from human feedback

**Validation:**
```python
from escalation.risk_assessor import RiskAssessor
from escalation.escalation_router import EscalationRouter

assessor = RiskAssessor()
router = EscalationRouter()

risk_score = assessor.assess(
    query="Should I stop taking my medication?",
    response="You should...",
    confidence=0.6
)

if risk_score > 0.8:
    router.escalate(query, response, risk_score)
```

### Task 6: Integration and Testing (60 minutes)

Integrate all components in `safe_rag_agent.py`:

**Integration Points:**
1. Input validation (before RAG)
2. Retrieval filtering (during RAG)
3. Output filtering (after generation)
4. Bias detection (on response)
5. PII redaction (on response)
6. Audit logging (all stages)
7. Risk assessment and escalation

**Hints:**
- Create SafeRAGAgent wrapper
- Apply guardrails at each stage
- Handle guardrail failures gracefully
- Maintain performance
- Provide transparency

**Validation:**
```bash
# Run comprehensive safety tests
python tests/test_safe_agent.py

# Expected output:
# ✓ Input validation test passed
# ✓ Output filtering test passed
# ✓ Bias detection test passed
# ✓ PII redaction test passed
# ✓ Audit logging test passed
# ✓ Escalation test passed
```

## Testing

### Safety Test Cases

Test with adversarial inputs:
1. Jailbreak attempts
2. Prompt injection
3. Harmful queries
4. Biased prompts
5. PII in queries
6. High-risk medical questions

### Compliance Test Cases

Verify compliance requirements:
1. HIPAA compliance
2. GDPR compliance
3. FDA guidelines
4. Audit trail completeness
5. Data retention policies

## Evaluation Rubric

See `rubric.md` for detailed evaluation criteria.

**Summary:**
- Functionality (40%): Do all safety mechanisms work?
- Code Quality (20%): Is it well-structured and documented?
- Performance (15%): Does it meet latency requirements?
- Compliance (10%): Does it meet regulatory requirements?
- Best Practices (15%): Does it follow safety best practices?

## Common Issues and Troubleshooting

### Issue: High false positive rate
**Solution:**
- Adjust guardrail thresholds
- Improve context understanding
- Add domain-specific rules
- Collect feedback and retrain

### Issue: PII detection misses entities
**Solution:**
- Improve NER model
- Add regex patterns
- Use ensemble methods
- Test with diverse examples

### Issue: Performance overhead too high
**Solution:**
- Optimize guardrail execution
- Use caching
- Parallelize checks
- Prioritize critical checks

### Issue: Bias detection inconsistent
**Solution:**
- Use multiple detection methods
- Improve counterfactual generation
- Calibrate thresholds
- Validate with diverse test cases

## Resources

### Relevant Course Notes
- Module 9: Safety, Ethics, and Compliance
- Module 10: Human-AI Interaction

### Relevant Notebooks
- `notebooks/module-09/01-guardrails-implementation.ipynb`
- `notebooks/module-09/02-bias-detection.ipynb`

### External Documentation
- [NVIDIA NeMo Guardrails Documentation](https://docs.nvidia.com/nemo/guardrails/)
- [HIPAA Compliance Guide](https://www.hhs.gov/hipaa/)
- [FDA AI/ML Guidelines](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices)

## Submission

When complete, ensure:
1. All guardrails configured and tested
2. Bias detection works accurately
3. PII redaction is comprehensive
4. Audit logging captures all interactions
5. Escalation protocol routes correctly
6. Performance meets requirements
7. All compliance tests pass

## Next Steps

After completing this lab:
- Review the reference solution
- Experiment with different guardrail configurations
- Test with real-world scenarios
- Consider additional safety mechanisms

