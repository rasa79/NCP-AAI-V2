# Domain 8: Deployment and Scaling

**Exam Weight**: 5%  
**Number of Questions**: 5

---

### Question 1: Containerization Strategy for AI Agent Deployment

**Scenario:**
A healthcare AI agent assists doctors with diagnosis support, requiring deployment across 50 hospitals with varying infrastructure. Each hospital has different: GPU availability (some A100, some V100, some CPU-only), network configurations, and security requirements. The current deployment process involves manual installation and configuration at each site, taking 2 days per hospital and prone to configuration errors. The team wants to containerize the agent for consistent, rapid deployment.

**Requirements:**
- Consistent deployment across diverse infrastructure
- Support GPU and CPU-only environments
- Include all dependencies and configurations
- Enable rapid deployment (under 1 hour per site)
- Simplify updates and rollbacks
- Meet healthcare security requirements

**Question:** What containerization approach would best meet these deployment requirements?

**Options:**

A) Create a single Docker container with the agent and all dependencies, using runtime detection to utilize GPU if available or fall back to CPU.

B) Create separate Docker containers for each hospital's specific configuration, manually customizing each one.

C) Deploy the agent directly on hospital servers without containerization, using configuration management tools.

D) Use virtual machines instead of containers for better isolation.

**Correct Answer:** A

**Explanation:**

**Why A is correct:**
Single container with runtime detection provides flexibility and consistency:

```dockerfile
# Dockerfile for healthcare AI agent
FROM nvcr.io/nvidia/pytorch:23.10-py3

# Install agent dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy agent code
COPY agent/ /app/agent/
COPY models/ /app/models/

# Runtime GPU detection script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Entrypoint detects GPU and configures accordingly
ENTRYPOINT ["/app/entrypoint.sh"]
```

```bash
# entrypoint.sh - Runtime detection
#!/bin/bash

if nvidia-smi &> /dev/null; then
    echo "GPU detected, using GPU inference"
    export DEVICE="cuda"
    export BATCH_SIZE=32
    # Use TensorRT-optimized models
    export MODEL_PATH="/app/models/tensorrt/"
else
    echo "No GPU detected, using CPU inference"
    export DEVICE="cpu"
    export BATCH_SIZE=4
    # Use standard models
    export MODEL_PATH="/app/models/cpu/"
fi

# Start agent
python /app/agent/main.py
```

Benefits:
- Single container works everywhere (GPU or CPU)
- Automatic adaptation to available hardware
- Consistent deployment process
- All dependencies included
- Easy updates (push new container)
- Rapid deployment (pull and run)

```bash
# Deployment at any hospital (under 1 hour)
# 1. Pull container (10 minutes)
docker pull hospital-registry/diagnosis-agent:v1.2

# 2. Run with GPU support (if available)
docker run -d \
  --gpus all \
  --name diagnosis-agent \
  -v /hospital/data:/data \
  -v /hospital/config:/config \
  -p 8080:8080 \
  hospital-registry/diagnosis-agent:v1.2

# 3. Verify health
curl http://localhost:8080/health

# Total time: 15-30 minutes
```

**Why other options are suboptimal:**

**Option B** (separate containers per hospital): Maintenance nightmare, 50 different containers to maintain, difficult to update, violates DRY principle.

**Option C** (no containerization): Configuration drift, dependency conflicts, difficult to replicate, slow deployment, error-prone.

**Option D** (virtual machines): Heavier than containers, slower startup, more resource overhead, harder to update, unnecessary isolation.

**Trade-offs and Considerations:**
- Container adds small overhead (negligible for AI workloads)
- Benefits (consistency, portability, rapid deployment) far outweigh overhead
- Healthcare security: Container isolation + network policies
- NVIDIA base images include optimized libraries

**NVIDIA Tools:**
- **NVIDIA Container Toolkit**: GPU support in containers
- **NVIDIA NGC**: Pre-built base images with optimizations
- **NVIDIA NIM**: Production-ready containerized inference

**Exam Mapping:**
🎯 **Exam Objective:** 8.4 (Scale deployments using containerization)
📊 **Domain:** Deployment and Scaling
⚖️ **Weight:** 5%
🔑 **Difficulty:** Scenario-based analysis required

**Key Concepts:**
- Docker containerization
- Runtime hardware detection
- GPU vs CPU deployment
- Dependency management
- Consistent deployment
- Container portability

---

### Question 2: Kubernetes Orchestration for Multi-Agent System

**Scenario:**
A financial services company deploys a multi-agent system with 5 specialized agents (market analysis, risk assessment, portfolio optimization, compliance, coordinator). Each agent has different resource requirements: market analysis needs 2 GPUs, risk assessment needs 1 GPU, others are CPU-only. Traffic varies: 100 requests/second during market hours, 10 requests/second off-hours. The company wants to use Kubernetes for orchestration, auto-scaling, and efficient resource utilization.

**Requirements:**
- Deploy multi-agent system on Kubernetes
- Auto-scale based on traffic (100 req/s peak, 10 req/s off-peak)
- Allocate GPUs efficiently to agents that need them
- Ensure high availability (no single point of failure)
- Enable rolling updates without downtime
- Optimize costs by scaling down during off-hours

**Question:** What Kubernetes deployment strategy would best meet these requirements?

**Options:**

A) Deploy all agents in a single pod with all resources allocated statically.

B) Deploy each agent as a separate Kubernetes Deployment with appropriate resource requests/limits, use Horizontal Pod Autoscaler (HPA) for CPU-based agents, use node selectors for GPU allocation, and implement rolling update strategy.

C) Deploy all agents on a single large node with all GPUs.

D) Manually scale agents by changing replica counts based on time of day.

**Correct Answer:** B

**Explanation:**

**Why B is correct:**
Separate deployments with autoscaling provide optimal resource utilization:

```yaml
# Market Analysis Agent (GPU-intensive)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: market-analysis-agent
spec:
  replicas: 2  # High availability
  selector:
    matchLabels:
      app: market-analysis
  template:
    metadata:
      labels:
        app: market-analysis
    spec:
      nodeSelector:
        nvidia.com/gpu: "true"  # Schedule on GPU nodes
      containers:
      - name: agent
        image: financial-agents/market-analysis:v1.0
        resources:
          requests:
            nvidia.com/gpu: 2  # Request 2 GPUs
            memory: "16Gi"
            cpu: "4"
          limits:
            nvidia.com/gpu: 2
            memory: "16Gi"
            cpu: "4"
---
# Risk Assessment Agent (GPU-intensive)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: risk-assessment-agent
spec:
  replicas: 2
  template:
    spec:
      nodeSelector:
        nvidia.com/gpu: "true"
      containers:
      - name: agent
        resources:
          requests:
            nvidia.com/gpu: 1  # Request 1 GPU
            memory: "8Gi"
---
# Portfolio Optimization Agent (CPU-only with autoscaling)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio-agent
spec:
  replicas: 2  # Minimum replicas
  template:
    spec:
      containers:
      - name: agent
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "4Gi"
            cpu: "2"
---
# Horizontal Pod Autoscaler for CPU agents
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: portfolio-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: portfolio-agent
  minReplicas: 2   # Off-hours minimum
  maxReplicas: 10  # Peak hours maximum
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Scales up when CPU > 70%
  # Scales down when CPU < 70%
  # Handles 100 req/s peak, 10 req/s off-peak automatically
---
# Rolling Update Strategy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: coordinator-agent
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Add 1 new pod before removing old
      maxUnavailable: 0  # Keep all pods available during update
  # Zero-downtime updates
```

Benefits:
- Each agent scales independently
- GPU agents get GPU resources
- CPU agents autoscale based on load
- High availability (multiple replicas)
- Rolling updates (zero downtime)
- Cost optimization (scale down off-hours)

**Why other options are suboptimal:**

**Option A** (single pod): No scaling, no high availability, single point of failure, inefficient resource use, violates multiple requirements.

**Option C** (single node): No high availability, node failure = complete outage, cannot scale beyond one node, expensive to keep large node running 24/7.

**Option D** (manual scaling): Requires human intervention, slow to respond to traffic changes, cannot handle unexpected spikes, inefficient.

**Trade-offs and Considerations:**
- Kubernetes adds complexity but essential for production
- HPA reacts to load automatically (no manual intervention)
- GPU scheduling requires NVIDIA device plugin
- Cost savings: Scale down 80% during off-hours

**NVIDIA Tools:**
- **NVIDIA GPU Operator**: Kubernetes GPU support
- **NVIDIA Device Plugin**: GPU resource management in K8s
- **NVIDIA NIM**: Kubernetes-ready containers

**Exam Mapping:**
🎯 **Exam Objective:** 8.1 (Deploy and orchestrate multi-agent systems), 8.4 (Scale deployments)
📊 **Domain:** Deployment and Scaling
⚖️ **Weight:** 5%
🔑 **Difficulty:** Scenario-based analysis required

**Key Concepts:**
- Kubernetes deployments
- Horizontal Pod Autoscaler
- GPU scheduling
- Rolling updates
- High availability
- Resource requests/limits
- Auto-scaling strategies

---

### Question 3: CI/CD Pipeline for Agent Deployment

**Scenario:**
A development team releases agent updates weekly, including model improvements, bug fixes, and new features. The current manual deployment process involves: building containers, running tests, deploying to staging, manual testing, deploying to production. This takes 2 days and is error-prone. The team wants to implement CI/CD to automate testing and deployment, reducing time to 2 hours while improving reliability.

**Requirements:**
- Automate build, test, and deployment pipeline
- Run automated tests before deployment
- Deploy to staging for validation before production
- Enable rapid rollback if issues detected
- Maintain deployment history and audit trail
- Reduce deployment time from 2 days to 2 hours

**Question:** What CI/CD pipeline design would best meet these requirements?

**Options:**

A) Manually build and deploy, but document the process better.

B) Implement automated CI/CD pipeline with: code commit triggers build, automated unit and integration tests, automated deployment to staging, automated smoke tests in staging, manual approval gate, automated production deployment with canary testing, and automated rollback on failure.

C) Automate only the build step, keep testing and deployment manual.

D) Deploy directly to production after automated tests, skipping staging environment.

**Correct Answer:** B

**Explanation:**

**Why B is correct:**
Full CI/CD pipeline with safety gates provides speed and reliability:

```yaml
# CI/CD Pipeline (GitHub Actions example)
name: Agent Deployment Pipeline

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # 1. Build container (10 minutes)
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t agent:${{ github.sha }} .
      
      # 2. Run unit tests (15 minutes)
      - name: Unit tests
        run: docker run agent:${{ github.sha }} pytest tests/unit/
      
      # 3. Run integration tests (20 minutes)
      - name: Integration tests
        run: docker run agent:${{ github.sha }} pytest tests/integration/
      
      # 4. Push to registry
      - name: Push image
        run: docker push registry/agent:${{ github.sha }}
  
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    steps:
      # 5. Deploy to staging (5 minutes)
      - name: Deploy to staging
        run: |
          kubectl set image deployment/agent \
            agent=registry/agent:${{ github.sha }} \
            --namespace=staging
      
      # 6. Smoke tests in staging (10 minutes)
      - name: Smoke tests
        run: |
          python tests/smoke_tests.py \
            --endpoint=https://staging.agent.com
      
      # 7. Performance tests (15 minutes)
      - name: Performance tests
        run: |
          python tests/performance_tests.py \
            --endpoint=https://staging.agent.com \
            --target-latency=500ms
  
  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      # 8. Manual approval gate
      - name: Wait for approval
        uses: trstringer/manual-approval@v1
        with:
          approvers: ops-team
      
      # 9. Canary deployment (10% traffic) (10 minutes)
      - name: Canary deployment
        run: |
          kubectl set image deployment/agent-canary \
            agent=registry/agent:${{ github.sha }}
          # Route 10% traffic to canary
      
      # 10. Monitor canary (20 minutes)
      - name: Monitor canary metrics
        run: |
          python scripts/monitor_canary.py \
            --duration=20m \
            --error-threshold=0.01
      
      # 11. Full production deployment (10 minutes)
      - name: Full deployment
        run: |
          kubectl set image deployment/agent \
            agent=registry/agent:${{ github.sha }} \
            --namespace=production
      
      # 12. Automated rollback on failure
      - name: Rollback on failure
        if: failure()
        run: |
          kubectl rollout undo deployment/agent \
            --namespace=production

# Total time: ~2 hours (vs 2 days manual)
```

Benefits:
- Fully automated (no manual steps except approval)
- Multiple test layers catch issues early
- Staging validation before production
- Canary testing catches production issues
- Automated rollback on failure
- Complete audit trail
- 2-hour deployment time achieved

**Why other options are suboptimal:**

**Option A** (better documentation): Still manual, still slow, still error-prone, doesn't meet 2-hour requirement.

**Option C** (partial automation): Tests and deployment still manual (slow), doesn't achieve time reduction goal.

**Option D** (skip staging): Dangerous, production issues not caught, no validation before customer impact, violates best practices.

**NVIDIA Tools:**
- **NVIDIA NIM**: Container images for CI/CD
- **NVIDIA NGC**: Container registry
- **Kubernetes**: Deployment target

**Exam Mapping:**
🎯 **Exam Objective:** 8.2 (Apply MLOps practices including CI/CD workflows)
📊 **Domain:** Deployment and Scaling
⚖️ **Weight:** 5%
🔑 **Difficulty:** Scenario-based analysis required

**Key Concepts:**
- CI/CD pipelines
- Automated testing
- Staging environments
- Canary deployments
- Automated rollback
- Manual approval gates
- MLOps practices

---

### Question 4: Load Balancing and Scaling Strategy

**Scenario:**
A news summarization AI agent experiences highly variable traffic: 50 requests/second baseline, 500 requests/second during breaking news events (unpredictable timing). The agent uses a 70B parameter model requiring GPU inference. Current single-instance deployment cannot handle traffic spikes, causing 30-second queuing delays and user abandonment. The company needs a scaling strategy that handles spikes efficiently while minimizing costs during baseline traffic.

**Requirements:**
- Handle 10x traffic spikes (50 to 500 req/s)
- Maintain sub-2-second response time during spikes
- Minimize costs during baseline traffic
- Scale up quickly when spikes occur (under 2 minutes)
- Load balance across multiple instances
- Optimize GPU utilization

**Question:** What load balancing and scaling strategy would best handle these traffic patterns?

**Options:**

A) Deploy 10 instances permanently to handle peak load, using round-robin load balancing.

B) Implement auto-scaling with: Kubernetes HPA based on request queue depth, load balancer with least-connections algorithm, scale from 2 instances (baseline) to 10 instances (peak), and use NVIDIA Triton's dynamic batching to maximize GPU utilization per instance.

C) Use a single large instance with more GPUs to handle all traffic.

D) Implement request queuing with no scaling, making users wait during spikes.

**Correct Answer:** B

**Explanation:**

**Why B is correct:**
Auto-scaling with intelligent load balancing provides cost-effective spike handling:

```yaml
# Kubernetes HPA based on queue depth
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: summarization-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: summarization-agent
  minReplicas: 2   # Baseline: 2 instances (50 req/s)
  maxReplicas: 10  # Peak: 10 instances (500 req/s)
  metrics:
  - type: Pods
    pods:
      metric:
        name: request_queue_depth
      target:
        type: AverageValue
        averageValue: "10"  # Scale when queue > 10 per pod
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0  # Scale up immediately
      policies:
      - type: Percent
        value: 100  # Double instances quickly
        periodSeconds: 30
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
      - type: Pods
        value: 1  # Remove 1 instance at a time
        periodSeconds: 60
```

```yaml
# Load Balancer Configuration
apiVersion: v1
kind: Service
metadata:
  name: summarization-agent-lb
spec:
  type: LoadBalancer
  sessionAffinity: None  # No sticky sessions
  selector:
    app: summarization-agent
  ports:
  - port: 80
    targetPort: 8000
  # Least-connections algorithm (configured in ingress)
```

```python
# Triton dynamic batching per instance
# Maximizes GPU utilization
dynamic_batching {
  preferred_batch_size: [8, 16, 32]
  max_queue_delay_microseconds: 100000  # 100ms max wait
  max_batch_size: 32
}

# Each instance can handle 50 req/s with batching
# 2 instances: 100 req/s (covers baseline + buffer)
# 10 instances: 500 req/s (covers peak)
```

Scaling behavior:
```
Baseline (50 req/s):
- 2 instances running
- Cost: 2 GPU instances
- Response time: <1s

Breaking news spike (500 req/s):
- t=0s: Spike begins, queue depth increases
- t=30s: HPA detects queue depth > 10, scales to 4 instances
- t=60s: Still high queue, scales to 8 instances
- t=90s: Scales to 10 instances
- t=120s: All instances running, queue clears
- Response time: <2s maintained

After spike (back to 50 req/s):
- t=0s: Spike ends
- t=300s: Stabilization window passes
- t=360s: Scales down to 8 instances
- t=420s: Scales down to 6 instances
- ... gradually back to 2 instances
```

Benefits:
- Cost-efficient: 2 instances baseline (vs 10 permanent)
- Handles spikes: Scales to 10 in ~2 minutes
- Maintains latency: Dynamic batching + load balancing
- Intelligent load distribution: Least-connections algorithm
- GPU optimization: Triton batching maximizes utilization

**Why other options are suboptimal:**

**Option A** (10 permanent instances): Wastes 80% of resources during baseline, 8 idle instances most of the time, 5x higher cost than needed.

**Option C** (single large instance): Cannot scale beyond one instance, single point of failure, expensive, may not handle 500 req/s alone.

**Option D** (queuing without scaling): Poor user experience, 30-second delays unacceptable, users abandon, violates latency requirement.

**Trade-offs and Considerations:**
- Auto-scaling has 2-minute ramp-up time (acceptable for news spikes)
- Cost savings: 80% reduction during baseline
- Triton batching essential for GPU efficiency
- Queue-based scaling more responsive than CPU-based

**NVIDIA Tools:**
- **NVIDIA Triton**: Dynamic batching for GPU efficiency
- **NVIDIA NIM**: Scalable inference containers
- **Kubernetes HPA**: Auto-scaling orchestration

**Exam Mapping:**
🎯 **Exam Objective:** 8.3 (Profile performance and reliability under distributed loads), 8.4 (Scale deployments)
📊 **Domain:** Deployment and Scaling
⚖️ **Weight:** 5%
🔑 **Difficulty:** Scenario-based analysis required

**Key Concepts:**
- Auto-scaling strategies
- Load balancing algorithms
- Queue-based scaling
- Dynamic batching
- Cost optimization
- GPU utilization
- Traffic spike handling

---

### Question 5: Cost Optimization for Production Deployment

**Scenario:**
A startup deploys a customer support AI agent serving 1,000 customers. Current deployment costs $10,000/month: 4 NVIDIA A100 instances running 24/7, processing 100,000 requests/month. Analysis shows: 70% of requests during business hours (8am-6pm), 30% off-hours; average GPU utilization 40%; p95 latency 800ms (target: 1000ms). The startup needs to reduce costs by 50% while maintaining performance.

**Requirements:**
- Reduce costs from $10,000/month to $5,000/month
- Maintain p95 latency under 1000ms
- Serve all 100,000 requests/month
- No degradation in response quality
- Maintain high availability

**Question:** What cost optimization strategy would best achieve 50% cost reduction while maintaining performance?

**Options:**

A) Reduce to 2 A100 instances permanently, accepting higher latency during peak hours.

B) Implement multi-faceted optimization: time-based auto-scaling (4 instances business hours, 1 instance off-hours), use spot instances for non-critical workloads, optimize models with TensorRT-LLM to increase throughput per instance, and implement request caching for common queries.

C) Switch to smaller GPU instances (T4 instead of A100) to reduce costs.

D) Reduce model size to decrease inference costs, accepting quality degradation.

**Correct Answer:** B

**Explanation:**

**Why B is correct:**
Multi-faceted optimization achieves cost reduction without performance loss:

```python
# 1. Time-based auto-scaling
# Current: 4 A100 instances × 24 hours × 30 days = 2,880 instance-hours
# Optimized:
business_hours = 10 hours/day × 30 days = 300 hours × 4 instances = 1,200 hours
off_hours = 14 hours/day × 30 days = 420 hours × 1 instance = 420 hours
total_hours = 1,620 instance-hours  # 44% reduction

# Cost savings: $10,000 × 0.44 = $4,400 saved
```

```yaml
# Kubernetes CronJob for time-based scaling
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-up-business-hours
spec:
  schedule: "0 8 * * 1-5"  # 8am weekdays
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: scaler
            command:
            - kubectl
            - scale
            - deployment/support-agent
            - --replicas=4
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scale-down-off-hours
spec:
  schedule: "0 18 * * 1-5"  # 6pm weekdays
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: scaler
            command:
            - kubectl
            - scale
            - deployment/support-agent
            - --replicas=1
```

```python
# 2. Spot instances for batch processing
# Use spot instances (70% cheaper) for non-real-time tasks
# - Training data collection
# - Model evaluation
# - Analytics processing
# Cost savings: $500/month
```

```python
# 3. TensorRT-LLM optimization
# Current: 40% GPU utilization, 800ms p95 latency
# Optimized: 70% GPU utilization, 600ms p95 latency
# Result: Can handle same load with fewer instances

# Before: 100,000 requests / 4 instances = 25,000 req/instance
# After: 100,000 requests / 3 instances = 33,333 req/instance
# (during business hours, can reduce from 4 to 3 instances)

# Additional cost savings: $1,000/month
```

```python
# 4. Request caching
# Analysis shows 20% of requests are common queries
# Cache responses for 1 hour

cache_hit_rate = 0.20
cached_requests = 100,000 × 0.20 = 20,000 requests
compute_savings = 20,000 requests × $0.01/request = $200/month

# Also reduces latency for cached requests to <50ms
```

```python
# Total cost reduction:
time_based_scaling = $4,400
spot_instances = $500
tensorrt_optimization = $1,000
caching = $200
total_savings = $6,100  # 61% reduction (exceeds 50% target!)

# Final cost: $10,000 - $6,100 = $3,900/month
# Performance maintained: p95 latency 600ms (better than 1000ms target)
```

Benefits:
- Exceeds cost reduction target (61% vs 50%)
- Improves performance (600ms vs 800ms)
- No quality degradation
- High availability maintained
- Multiple optimization layers

**Why other options are suboptimal:**

**Option A** (reduce to 2 instances): Cannot handle business hours peak load, latency would exceed 1000ms, violates performance requirement.

**Option C** (switch to T4): T4 much slower than A100 for LLMs, would need more T4 instances to match performance, may not save costs, latency would increase.

**Option D** (smaller model): Quality degradation unacceptable for customer support, violates requirement to maintain quality.

**Trade-offs and Considerations:**
- Time-based scaling requires predictable traffic patterns
- Spot instances can be interrupted (use for non-critical only)
- TensorRT optimization requires one-time engineering effort
- Caching requires cache invalidation strategy
- Benefits justify implementation complexity

**NVIDIA Tools:**
- **TensorRT-LLM**: Optimize inference for higher throughput
- **NVIDIA NIM**: Efficient inference deployment
- **NVIDIA Triton**: Batching and caching support

**Exam Mapping:**
🎯 **Exam Objective:** 8.5 (Optimize deployment costs while ensuring high availability)
📊 **Domain:** Deployment and Scaling
⚖️ **Weight:** 5%
🔑 **Difficulty:** Scenario-based analysis required

**Key Concepts:**
- Cost optimization strategies
- Time-based auto-scaling
- Spot instances
- TensorRT-LLM optimization
- Request caching
- GPU utilization optimization
- Multi-faceted optimization

---

**End of Domain 8 Questions**



---

## Study Resources

To prepare for these questions, review:

**Course Notes:** [Module 08 Deployment Scaling](../../course-notes/module-08-deployment-scaling.md)

**Practice Notebooks:**
- [01 Containerization](../../notebooks/module-08/01-containerization.ipynb)
