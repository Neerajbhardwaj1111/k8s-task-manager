# Kubernetes Task Manager

A small full-stack task management application deployed on Kubernetes using Minikube.

This project was built as a hands-on Kubernetes environment to work with application deployments, service discovery, configuration management, persistent storage, health checks, scaling, and containerized workloads.

## Architecture

```text
                    ┌─────────────────────┐
                    │      Browser        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Frontend Service    │
                    │      NodePort       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Frontend Deployment │
                    │     Nginx / HTML    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Backend Service     │
                    │      ClusterIP      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ FastAPI Backend     │
                    │   2 Replicas        │
                    └──────┬────────┬─────┘
                           │        │
                 ┌─────────┘        └─────────┐
                 ▼                            ▼
        ┌─────────────────┐          ┌─────────────────┐
        │   PostgreSQL    │          │      Redis      │
        │ Persistent Data │          │      Cache      │
        └────────┬────────┘          └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   PostgreSQL    │
        │      PVC        │
        └─────────────────┘
```

## Tech Stack

### Application

- Python
- FastAPI
- PostgreSQL
- Redis
- HTML
- CSS
- JavaScript

### Containerization

- Docker
- Docker Compose

### Kubernetes

- Kubernetes
- Minikube
- Deployments
- Services
- ConfigMaps
- Secrets
- PersistentVolumeClaims
- Health probes
- Replica management
- Kubernetes service discovery

## Project Structure

```text
k8s-task-manager/
├── backend/
│   ├── app/
│   │   ├── cache.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   ├── nginx.conf
│   ├── style.css
│   └── Dockerfile
│
├── k8s/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── configmap.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── namespace.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-pvc.yaml
│   ├── postgres-service.yaml
│   ├── redis-deployment.yaml
│   ├── redis-service.yaml
│   └── secret.yaml
│
├── docker-compose.yml
├── .gitignore
└── readme.md
```

> `k8s/secret.yaml` is intentionally excluded from Git. Create it locally before deploying if needed.

## Running Locally with Docker Compose

Clone the repository:

```bash
git clone git@github.com:Neerajbhardwaj1111/k8s-task-manager.git
cd k8s-task-manager
```

Start the application:

```bash
docker compose up --build
```

The application services include:

- FastAPI backend
- PostgreSQL
- Redis
- Frontend

## Running on Kubernetes with Minikube

Start Minikube:

```bash
minikube start
```

Check the cluster:

```bash
minikube status
```

Create the namespace:

```bash
kubectl apply -f k8s/namespace.yaml
```

Create configuration and secrets:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
```

Deploy PostgreSQL:

```bash
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
```

Deploy Redis:

```bash
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/redis-service.yaml
```

Deploy the backend:

```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
```

Deploy the frontend:

```bash
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

Check the workloads:

```bash
kubectl get pods -n task-app
```

Check services:

```bash
kubectl get svc -n task-app
```

## Access the Application

Get the frontend URL:

```bash
minikube service frontend-service -n task-app --url
```

Open the returned URL in your browser.

## Backend Health Check

The backend exposes a health endpoint:

```text
GET /health
```

Example:

```bash
curl http://<backend-url>/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "backend"
}
```

## Kubernetes Features Practiced

### Deployments

The frontend and backend run as Kubernetes Deployments.

The backend is configured with multiple replicas to demonstrate workload distribution and recovery.

### Services

Services provide stable networking between components:

```text
frontend-service
backend-service
postgres-service
redis-service
```

The frontend is exposed externally using a NodePort service, while internal services use ClusterIP.

### ConfigMaps

Application configuration that doesn't contain sensitive data is managed through a Kubernetes ConfigMap.

### Secrets

Database credentials are managed through a Kubernetes Secret.

The Secret manifest is intentionally excluded from version control.

### Persistent Storage

PostgreSQL uses a PersistentVolumeClaim so database data isn't tied directly to the lifecycle of a Pod.

### Health Checks

Health probes are used to allow Kubernetes to determine whether application containers are ready to receive traffic and remain healthy.

### Service Discovery

The backend communicates with PostgreSQL and Redis using Kubernetes service names rather than hardcoded Pod IP addresses.

For example:

```text
postgres-service:5432
redis-service:6379
```

### Scaling and Self-Healing

The backend can be scaled using:

```bash
kubectl scale deployment backend -n task-app --replicas=3
```

Kubernetes also recreates Pods automatically if a running Pod is deleted.

For example:

```bash
kubectl delete pod <pod-name> -n task-app
```

Then watch the Pods:

```bash
kubectl get pods -n task-app -w
```

## Useful Kubernetes Commands

View all resources:

```bash
kubectl get all -n task-app
```

View deployments:

```bash
kubectl get deployments -n task-app
```

View services:

```bash
kubectl get svc -n task-app
```

View persistent volumes:

```bash
kubectl get pvc -n task-app
```

View Pod logs:

```bash
kubectl logs -n task-app <pod-name>
```

Describe a Pod:

```bash
kubectl describe pod -n task-app <pod-name>
```

Restart a deployment:

```bash
kubectl rollout restart deployment backend -n task-app
```

Check rollout status:

```bash
kubectl rollout status deployment backend -n task-app
```

## What I Practiced

This project was mainly about getting comfortable with the complete application-to-cluster flow:

```text
Code
  ↓
Docker Image
  ↓
Kubernetes Deployment
  ↓
Pod
  ↓
Service
  ↓
Application Communication
  ↓
Database / Cache
```

Along the way, I also worked through common local Kubernetes issues such as Docker permissions, local image availability in Minikube, service discovery, Pod recovery, and `ImagePullBackOff` troubleshooting.

## Future Improvements

Some areas I'd like to explore next:

- Kubernetes Ingress
- Horizontal Pod Autoscaler (HPA)
- Helm
- Prometheus and Grafana
- More advanced health checks
- Resource requests and limits
- Rolling updates and rollback strategies
- CI/CD pipeline
- Production-style secret management
- Deploying to a cloud Kubernetes platform

## Author

**Neeraj Bhardwaj**

Hands-on Kubernetes, Docker, backend, and cloud-native experimentation.
