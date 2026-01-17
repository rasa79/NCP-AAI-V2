# Module 8: Deployment and Scaling

**Exam Weight:** 5%  
**Estimated Study Time:** 4-5 hours  
**Prerequisites:** Module 6 (NVIDIA Platform), Docker, Kubernetes basics

## Learning Objectives

1. **Deploy and orchestrate** multi-agent systems at production scale
2. **Apply MLOps practices** (CI/CD workflows, monitoring, governance)
3. **Profile performance** and reliability under distributed loads
4. **Scale deployments** using containerization (Docker, Kubernetes)
5. **Optimize deployment costs** while ensuring high availability

## Exam Objective Mapping

- **8.1** - Deploy and orchestrate multi-agent systems at production scale
- **8.2** - Apply MLOps practices (CI/CD workflows, monitoring, governance)
- **8.3** - Profile performance and reliability under distributed loads
- **8.4** - Scale deployments using containerization
- **8.5** - Optimize deployment costs while ensuring high availability

---

## 1. Containerization with Docker

### 1.1 Dockerfile for Agent

```dockerfile
# Dockerfile
FROM nvcr.io/nvidia/pytorch:24.01-py3

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "agent_server.py"]
```

### 1.2 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NVIDIA_API_KEY=${NVIDIA_API_KEY}
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
  
  vectordb:
    image: milvusdb/milvus:latest
    ports:
      - "19530:19530"
  
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
```

> 📝 **EXAM TIP**
> 
> Containerization ensures consistency across environments. Use multi-stage builds to reduce image size.

---

## 2. Kubernetes Deployment

### 2.1 Deployment Manifest

```yaml
# agent-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent
  template:
    metadata:
      labels:
        app: agent
    spec:
      containers:
      - name: agent
        image: myregistry/agent:v1.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            nvidia.com/gpu: 1
            memory: "16Gi"
            cpu: "4"
          limits:
            nvidia.com/gpu: 1
            memory: "32Gi"
            cpu: "8"
        env:
        - name: NVIDIA_API_KEY
          valueFrom:
            secretKeyRef:
              name: nvidia-secrets
              key: api-key
```

### 2.2 Service and Ingress

```yaml
# agent-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: agent-service
spec:
  selector:
    app: agent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer

---
# agent-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: agent-ingress
spec:
  rules:
  - host: agent.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: agent-service
            port:
              number: 80
```

### 2.3 Horizontal Pod Autoscaling

```yaml
# agent-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

> 📝 **EXAM TIP**
> 
> HPA scales based on metrics. Set appropriate min/max replicas and target utilization (typically 70-80%).

---

## 3. CI/CD Pipeline

### 3.1 GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy Agent

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest tests/
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: |
          docker build -t myregistry/agent:${{ github.sha }} .
          docker push myregistry/agent:${{ github.sha }}
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/agent-deployment \
            agent=myregistry/agent:${{ github.sha }}
          kubectl rollout status deployment/agent-deployment
```

> 📝 **EXAM TIP**
> 
> CI/CD automates testing, building, and deployment. Always test before deploying to production.

---

## 4. Load Balancing and Scaling

### 4.1 Load Balancing Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Round Robin** | Distribute evenly | Uniform workload |
| **Least Connections** | Route to least busy | Variable request times |
| **IP Hash** | Same client → same server | Session affinity |
| **Weighted** | Distribute by capacity | Heterogeneous servers |

### 4.2 Scaling Strategies

```python
class AdaptiveScaler:
    """Adaptive scaling based on metrics"""
    
    def __init__(self, min_replicas: int = 2, max_replicas: int = 10):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
    
    def calculate_desired_replicas(
        self,
        current_replicas: int,
        current_load: float,
        target_load: float = 0.7
    ) -> int:
        """Calculate desired replicas"""
        
        # Scale up if load > target
        if current_load > target_load:
            desired = int(current_replicas * (current_load / target_load))
        # Scale down if load < target * 0.5
        elif current_load < target_load * 0.5:
            desired = int(current_replicas * (current_load / target_load))
        else:
            desired = current_replicas
        
        # Clamp to min/max
        return max(self.min_replicas, min(desired, self.max_replicas))
```

---

## 5. Cost Optimization

### 5.1 Cost Analysis

```python
class CostOptimizer:
    """Analyze and optimize deployment costs"""
    
    def __init__(self, gpu_cost_per_hour: float = 3.0):
        self.gpu_cost_per_hour = gpu_cost_per_hour
    
    def calculate_cost(
        self,
        num_gpus: int,
        hours: float,
        requests_per_hour: int,
        tokens_per_request: int
    ) -> dict:
        """Calculate deployment costs"""
        
        # Infrastructure cost
        infra_cost = num_gpus * self.gpu_cost_per_hour * hours
        
        # Per-request cost
        total_requests = requests_per_hour * hours
        cost_per_request = infra_cost / total_requests if total_requests > 0 else 0
        
        # Per-token cost
        total_tokens = total_requests * tokens_per_request
        cost_per_1k_tokens = (infra_cost / total_tokens * 1000) if total_tokens > 0 else 0
        
        return {
            "total_cost": infra_cost,
            "cost_per_request": cost_per_request,
            "cost_per_1k_tokens": cost_per_1k_tokens,
            "requests_per_dollar": 1 / cost_per_request if cost_per_request > 0 else 0
        }
    
    def optimize(self, target_cost_per_request: float, current_config: dict) -> dict:
        """Suggest optimizations"""
        
        suggestions = []
        
        # Use smaller model
        if current_config["model_size"] == "70b":
            suggestions.append({
                "action": "Use 8B model",
                "savings": "~75%",
                "trade_off": "Slight accuracy reduction"
            })
        
        # Batch requests
        if current_config["batch_size"] < 32:
            suggestions.append({
                "action": "Increase batch size to 32",
                "savings": "~30%",
                "trade_off": "Slightly higher latency"
            })
        
        # Use quantization
        if current_config["precision"] == "fp16":
            suggestions.append({
                "action": "Use INT8 quantization",
                "savings": "~50%",
                "trade_off": "Minimal accuracy impact"
            })
        
        return suggestions
```

> 📝 **EXAM TIP**
> 
> Cost optimization involves model selection, batching, quantization, and right-sizing infrastructure. Balance cost with performance requirements.

---

## 6. Exam Focus Areas

### Key Concepts

1. **Containerization**: Docker, multi-stage builds, GPU support
2. **Kubernetes**: Deployments, services, HPA, resource limits
3. **CI/CD**: Automated testing, building, deployment
4. **Scaling**: Load balancing, autoscaling, cost optimization
5. **MLOps**: Version control, monitoring, rollback

### Scenario Example

**Example: Scaling Decision**
> Your agent handles 100 req/s during business hours, 10 req/s at night. How to optimize costs?
>
> A) Keep 10 replicas always  
> B) Use HPA with min=1, max=10  
> C) Manual scaling twice daily  
> D) Single large instance  
>
> **Answer: B** - HPA automatically scales based on load, optimizing costs while maintaining performance.

---

## 7. Summary

**Key Takeaways:**
1. Containerization ensures consistency
2. Kubernetes enables scalable orchestration
3. CI/CD automates deployment pipeline
4. HPA scales based on metrics
5. Cost optimization balances performance and budget

**Related Modules:**
- Module 6: NVIDIA Platform (NIM deployment)
- Module 7: Monitoring (production metrics)

---

## References

1. **Documentation**
   - Docker: https://docs.docker.com
   - Kubernetes: https://kubernetes.io/docs
   - NVIDIA GPU Operator: https://docs.nvidia.com/datacenter/cloud-native/gpu-operator

2. **Related Materials**
   - Notebook: `module-08/01-containerization.ipynb`
   - Notebook: `module-08/02-kubernetes-deployment.ipynb`
   - Lab: `lab-03-production-deployment`


---

## Related Materials

### Hands-On Practice

**Interactive Notebooks:**
- [01-containerization.ipynb](../../notebooks/module-08/01-containerization.ipynb)
- [02-kubernetes-deployment.ipynb](../../notebooks/module-08/02-kubernetes-deployment.ipynb)

**Practice Labs:**
- [Lab: Lab 03 Production Deployment](../../labs/lab-03-production-deployment/README.md)

### Assessment

**Exam Questions:**
- [Domain 08 Deployment](../../exam-questions/domain-08-deployment.md)
