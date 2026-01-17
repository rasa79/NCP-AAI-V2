# Lab 3: Production Deployment

## Overview

In this lab, you'll deploy a RAG agent to production using containerization, orchestration, and monitoring best practices. This intermediate-advanced lab introduces Docker containerization, Kubernetes deployment, NVIDIA NIM integration, monitoring dashboards, and production-grade error handling. You'll transform a development RAG system into a production-ready service with observability and reliability.

## Learning Objectives

- Containerize RAG applications with Docker (maps to exam objective 8.1: Containerization)
- Deploy agents to Kubernetes clusters (maps to exam objective 8.2: Kubernetes Deployment)
- Integrate NVIDIA NIM for high-performance inference (maps to exam objective 6.2: NVIDIA NIM)
- Implement monitoring and logging (maps to exam objective 7.1: Monitoring Dashboards)
- Configure load balancing and scaling (maps to exam objective 8.3: Scaling Strategies)
- Apply MLOps practices for agent deployment (maps to exam objective 8.4: MLOps Practices)

## Prerequisites

- Completed modules: Module 6 (NVIDIA Platform), Module 7 (Monitoring), Module 8 (Deployment)
- Completed Lab 1: Basic RAG Agent
- Required knowledge: Docker, Kubernetes basics, REST APIs, monitoring concepts
- Estimated time: 5-6 hours

## Scenario

**Company:** ProductionAI Inc., an enterprise AI solutions provider

**Challenge:** Your team has developed a successful RAG agent prototype that's being used by 50 internal users. The company wants to scale this to 10,000+ external customers with enterprise SLAs: 99.9% uptime, < 2 second response time, and comprehensive monitoring. The current development setup cannot meet these requirements.

**Your Task:** Deploy the RAG agent to production with:
- Containerized microservices architecture
- Kubernetes orchestration for scalability
- NVIDIA NIM for optimized inference
- Comprehensive monitoring and alerting
- Load balancing and auto-scaling
- Production-grade error handling and logging
- CI/CD pipeline for updates

**Business Requirements:**
- Availability: 99.9% uptime (< 9 hours downtime/year)
- Performance: < 2 second response time at p95
- Scalability: Handle 1000+ concurrent users
- Observability: Real-time monitoring and alerting
- Cost: Optimize infrastructure costs

**Technical Constraints:**
- Use Docker for containerization
- Use Kubernetes for orchestration
- Use NVIDIA NIM for LLM inference
- Use Prometheus + Grafana for monitoring
- Implement health checks and readiness probes
- Include comprehensive logging

## Requirements

### Functional Requirements

1. **Containerization**
   - Create Dockerfile for RAG agent service
   - Create Dockerfile for vector database
   - Optimize container images for size and security
   - Implement multi-stage builds
   - Configure environment variables

2. **Kubernetes Deployment**
   - Create Kubernetes deployment manifests
   - Configure services and ingress
   - Implement ConfigMaps and Secrets
   - Set up persistent volumes for vector store
   - Configure resource limits and requests

3. **NVIDIA NIM Integration**
   - Deploy NVIDIA NIM microservice
   - Configure LLM inference endpoints
   - Implement connection pooling
   - Add retry logic and circuit breakers
   - Monitor NIM performance metrics

4. **Monitoring and Observability**
   - Implement Prometheus metrics collection
   - Create Grafana dashboards
   - Configure alerting rules
   - Implement distributed tracing
   - Add structured logging

5. **Load Balancing and Scaling**
   - Configure horizontal pod autoscaling
   - Implement load balancing
   - Set up health checks
   - Configure readiness and liveness probes
   - Test scaling behavior

6. **CI/CD Pipeline**
   - Create deployment pipeline
   - Implement automated testing
   - Configure rolling updates
   - Add rollback capabilities
   - Document deployment process

### Performance Requirements

- Response time: < 2 seconds at p95
- Throughput: 100+ requests/second
- Availability: 99.9% uptime
- Resource efficiency: < 4GB memory per pod
- Startup time: < 30 seconds

### Quality Requirements

- All containers must pass security scans
- All deployments must include health checks
- All services must emit metrics
- All errors must be logged with context
- All configurations must be externalized

## Success Criteria

- [ ] Docker containers build successfully
- [ ] Kubernetes deployment succeeds
- [ ] NVIDIA NIM integration works correctly
- [ ] Monitoring dashboards display metrics
- [ ] Load balancing distributes traffic
- [ ] Auto-scaling responds to load
- [ ] Health checks detect failures
- [ ] Logs are structured and searchable
- [ ] Performance meets SLA requirements
- [ ] All tests pass

## Setup Instructions

### 1. Environment Setup

```bash
# Navigate to lab directory
cd labs/lab-03-production-deployment

# Install dependencies
pip install -r requirements.txt

# Install Docker (if not already installed)
# Follow: https://docs.docker.com/get-docker/

# Install kubectl (if not already installed)
# Follow: https://kubernetes.io/docs/tasks/tools/

# Install minikube for local Kubernetes (optional)
# Follow: https://minikube.sigs.k8s.io/docs/start/

# Verify installations
docker --version
kubectl version --client
```

### 2. Project Structure

```
lab-03-production-deployment/
├── README.md (this file)
├── requirements.txt
├── starter-code/
│   ├── app/
│   │   ├── main.py (FastAPI application)
│   │   ├── rag_service.py (RAG service)
│   │   ├── monitoring.py (metrics and logging)
│   │   └── config.py (configuration)
│   ├── docker/
│   │   ├── Dockerfile.app (application container)
│   │   ├── Dockerfile.vectordb (vector DB container)
│   │   └── docker-compose.yml (local testing)
│   ├── kubernetes/
│   │   ├── deployment.yaml (K8s deployment)
│   │   ├── service.yaml (K8s service)
│   │   ├── ingress.yaml (K8s ingress)
│   │   ├── configmap.yaml (configuration)
│   │   ├── secret.yaml (secrets)
│   │   ├── hpa.yaml (autoscaling)
│   │   └── monitoring.yaml (Prometheus/Grafana)
│   ├── monitoring/
│   │   ├── prometheus.yml (Prometheus config)
│   │   └── grafana-dashboard.json (Grafana dashboard)
│   └── tests/
│       ├── test_deployment.py (deployment tests)
│       └── load_test.py (load testing)
├── solution/
│   └── [reference implementation]
└── rubric.md (evaluation criteria)
```

## Starter Code

The starter code provides scaffolding for:

- **`app/main.py`**: FastAPI application with REST endpoints
- **`app/rag_service.py`**: RAG service wrapper
- **`app/monitoring.py`**: Prometheus metrics and logging
- **`docker/`**: Dockerfile templates
- **`kubernetes/`**: Kubernetes manifest templates
- **`monitoring/`**: Monitoring configuration templates

## Implementation Tasks

### Task 1: Containerize Application (60 minutes)

Create Docker containers in `docker/`:

**Dockerfile.app:**
- Base image: Python 3.10-slim
- Install dependencies
- Copy application code
- Expose port 8000
- Set entrypoint

**Dockerfile.vectordb:**
- Base image: appropriate for FAISS/Milvus
- Configure vector database
- Expose database port
- Set up persistent storage

**docker-compose.yml:**
- Define services (app, vectordb, nim)
- Configure networking
- Set up volumes
- Add environment variables

**Hints:**
- Use multi-stage builds to reduce image size
- Run as non-root user for security
- Use .dockerignore to exclude unnecessary files
- Pin dependency versions
- Add health check commands

**Validation:**
```bash
# Build containers
docker build -f docker/Dockerfile.app -t rag-agent:latest .
docker build -f docker/Dockerfile.vectordb -t vectordb:latest .

# Test locally
docker-compose -f docker/docker-compose.yml up

# Test endpoint
curl http://localhost:8000/health
```

### Task 2: Create FastAPI Application (45 minutes)

Implement REST API in `app/main.py`:

**Endpoints:**
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `POST /query` - Query endpoint
- `POST /ingest` - Document ingestion
- `GET /metrics` - Prometheus metrics

**Hints:**
- Use FastAPI for async support
- Add request validation with Pydantic
- Implement rate limiting
- Add CORS middleware
- Include request/response logging

**Validation:**
```python
# Test locally
uvicorn app.main:app --reload

# Test endpoints
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

### Task 3: Integrate NVIDIA NIM (60 minutes)

Configure NIM integration in `app/rag_service.py`:

**Requirements:**
- Connect to NIM inference endpoint
- Implement connection pooling
- Add retry logic with exponential backoff
- Implement circuit breaker pattern
- Monitor NIM latency and errors

**Hints:**
- Use environment variables for NIM endpoint
- Set appropriate timeouts
- Implement fallback to alternative models
- Cache frequent queries
- Log all NIM interactions

**Validation:**
```python
from app.rag_service import RAGService
service = RAGService(nim_endpoint="http://nim:8000")
response = service.query("What is RAG?")
print(response)
```

### Task 4: Implement Monitoring (60 minutes)

Add monitoring in `app/monitoring.py`:

**Prometheus Metrics:**
- Request count by endpoint
- Request duration histogram
- Error rate by type
- Active connections gauge
- NIM latency histogram
- Vector DB query time

**Logging:**
- Structured JSON logging
- Request/response logging
- Error logging with stack traces
- Performance logging
- Audit logging

**Hints:**
- Use prometheus_client library
- Add custom metrics for business logic
- Use correlation IDs for tracing
- Configure log levels via environment
- Implement log rotation

**Validation:**
```bash
# Check metrics endpoint
curl http://localhost:8000/metrics

# Check logs
docker logs <container-id>
```

### Task 5: Create Kubernetes Manifests (90 minutes)

Implement K8s resources in `kubernetes/`:

**deployment.yaml:**
- Define RAG agent deployment
- Set replicas (3 for HA)
- Configure resource limits
- Add health/readiness probes
- Set environment variables

**service.yaml:**
- Create ClusterIP service
- Expose port 8000
- Configure load balancing

**ingress.yaml:**
- Configure ingress rules
- Set up TLS (optional)
- Add rate limiting

**configmap.yaml:**
- Store non-sensitive configuration
- Model parameters
- Feature flags

**secret.yaml:**
- Store sensitive data (API keys)
- NIM credentials
- Database passwords

**hpa.yaml:**
- Configure horizontal pod autoscaler
- Set CPU/memory thresholds
- Define min/max replicas

**Hints:**
- Use labels for organization
- Add annotations for documentation
- Use namespaces for isolation
- Implement pod disruption budgets
- Add network policies

**Validation:**
```bash
# Apply manifests
kubectl apply -f kubernetes/

# Check deployment
kubectl get deployments
kubectl get pods
kubectl get services

# Test service
kubectl port-forward service/rag-agent 8000:8000
curl http://localhost:8000/health
```

### Task 6: Configure Monitoring Stack (45 minutes)

Set up Prometheus and Grafana in `monitoring/`:

**prometheus.yml:**
- Configure scrape targets
- Set scrape intervals
- Define alerting rules

**grafana-dashboard.json:**
- Create dashboard for RAG metrics
- Add panels for:
  - Request rate
  - Response time (p50, p95, p99)
  - Error rate
  - NIM latency
  - Resource usage

**Hints:**
- Use Prometheus Operator for K8s
- Configure service monitors
- Set up alert manager
- Create meaningful alerts
- Test alert firing

**Validation:**
```bash
# Deploy monitoring stack
kubectl apply -f kubernetes/monitoring.yaml

# Access Grafana
kubectl port-forward service/grafana 3000:3000
# Open http://localhost:3000
```

### Task 7: Implement Load Testing (30 minutes)

Create load tests in `tests/load_test.py`:

**Test Scenarios:**
- Baseline load (10 req/s)
- Peak load (100 req/s)
- Spike test (sudden 10x increase)
- Sustained load (1 hour)

**Metrics to Collect:**
- Response time distribution
- Error rate
- Throughput
- Resource usage

**Hints:**
- Use locust or k6 for load testing
- Ramp up gradually
- Monitor during tests
- Verify auto-scaling triggers
- Document results

**Validation:**
```bash
# Run load test
python tests/load_test.py

# Monitor metrics
kubectl top pods
```

## Testing

### Local Testing

```bash
# Build and run locally
docker-compose up

# Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'

# Check metrics
curl http://localhost:8000/metrics
```

### Kubernetes Testing

```bash
# Deploy to K8s
kubectl apply -f kubernetes/

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=rag-agent

# Test service
kubectl port-forward service/rag-agent 8000:8000
curl http://localhost:8000/health

# Check logs
kubectl logs -l app=rag-agent --tail=100

# Test auto-scaling
kubectl get hpa
```

### Load Testing

```bash
# Run load test
python tests/load_test.py --users 100 --duration 300

# Monitor during test
watch kubectl get hpa
watch kubectl top pods
```

## Evaluation Rubric

See `rubric.md` for detailed evaluation criteria.

**Summary:**
- Functionality (40%): Does deployment work correctly?
- Code Quality (20%): Is it well-structured and documented?
- Performance (15%): Does it meet SLA requirements?
- Error Handling (10%): Does it handle failures gracefully?
- Best Practices (15%): Does it follow production patterns?

## Common Issues and Troubleshooting

### Issue: Container fails to start
**Solution:**
- Check container logs: `docker logs <container-id>`
- Verify environment variables
- Check file permissions
- Review Dockerfile syntax

### Issue: Pods in CrashLoopBackOff
**Solution:**
- Check pod logs: `kubectl logs <pod-name>`
- Verify resource limits
- Check health probe configuration
- Review dependencies

### Issue: Service not accessible
**Solution:**
- Verify service configuration
- Check ingress rules
- Test with port-forward first
- Review network policies

### Issue: High latency
**Solution:**
- Check NIM connection
- Review resource limits
- Optimize vector search
- Add caching layer
- Scale horizontally

### Issue: Auto-scaling not working
**Solution:**
- Verify metrics-server is running
- Check HPA configuration
- Review resource requests
- Monitor metrics

## Resources

### Relevant Course Notes
- Module 6: NVIDIA Platform (NIM deployment)
- Module 7: Monitoring and Maintenance
- Module 8: Deployment and Scaling

### Relevant Notebooks
- `notebooks/module-06/01-nvidia-nim.ipynb`
- `notebooks/module-07/01-monitoring-dashboards.ipynb`
- `notebooks/module-08/01-containerization.ipynb`
- `notebooks/module-08/02-kubernetes-deployment.ipynb`

### External Documentation
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

## Submission

When complete, ensure:
1. All containers build successfully
2. Kubernetes deployment works
3. Monitoring is functional
4. Load tests pass
5. Documentation is complete
6. All tests pass

## Next Steps

After completing this lab:
- Review the reference solution
- Experiment with different scaling strategies
- Try implementing blue-green deployment
- Move on to Lab 4: Evaluation and Optimization

