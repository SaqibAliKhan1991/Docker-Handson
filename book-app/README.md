![Build and Push Docker Image](https://github.com/SaqibAliKhan1991/Docker-Handson/actions/workflows/docker-build.yml/badge.svg)
![Flask App CI/CD](https://github.com/SaqibAliKhan1991/Docker-Handson/actions/workflows/flask-app.yml/badge.svg)
![DevOps Scripts CI/CD](https://github.com/SaqibAliKhan1991/Docker-Handson/actions/workflows/devops-scripts.yml/badge.svg)
# 📚 Book Library App — Kubernetes Deployment

A simple Book Library web application built with Flask and PostgreSQL, deployed on Kubernetes. Built as a practice project to learn Kubernetes YAML files from scratch.

---

## 📌 What This App Does

- Add a book with title and author
- View all books
- Delete a book
- Data saved to PostgreSQL database

---

## 🏗️ Tech Stack

| Tool | Purpose |
|---|---|
| Flask (Python) | Web application |
| PostgreSQL | Database |
| Docker | Containerization |
| Kubernetes (Minikube) | Container orchestration |
| GitHub Actions | CI/CD pipeline |
| Docker Hub | Image registry |

---

## 🏗️ Architecture

```
Browser
    ↓
book-service (NodePort :30004)
    ↓
book-app Pod (Flask :5000)
    ↓
postgres-db Service (ClusterIP :5432)
    ↓
postgres-db Pod (PostgreSQL)
```

---

## 🔄 CI/CD Pipeline

Pipeline file: `.github/workflows/book-app.yml`

Triggers automatically when:
- Code is pushed to `main` branch
- Changes are inside `book-app/` folder

```
You push code to GitHub
        ↓
GitHub Actions triggers automatically
        ↓
Builds new Docker image
        ↓
Pushes to Docker Hub as saqib321/book-app:latest ✅
```

### Pipeline Steps
1. Checkout code
2. Login to Docker Hub
3. Build Docker image
4. Push to Docker Hub

### Required GitHub Secrets
| Secret | Value |
|---|---|
| DOCKER_USERNAME | Your Docker Hub username |
| DOCKER_PASSWORD | Your Docker Hub password |

### Deploy New Version After Pipeline Runs
```bash
kubectl rollout restart deployment/book-app
minikube service book-service --url
```

---

## 📁 Project Structure

```
book-app/
├── app.py                       → Flask application
├── requirements.txt             → Python dependencies
├── Dockerfile                   → Docker image instructions
└── kubernetes/
    ├── postgres-deployment.yml  → runs PostgreSQL Pod
    ├── postgres-service.yml     → internal database service
    ├── book-deployment.yml      → runs Flask app Pod
    └── book-service.yml         → exposes app to browser
```

---

## ⚙️ Prerequisites

- Docker installed
- Minikube installed
- kubectl installed

---

## 🚀 How to Run

### Step 1 — Start Minikube
```bash
minikube start
```

### Step 2 — Deploy everything
```bash
kubectl apply -f book-app/kubernetes/
```

### Step 3 — Watch Pods start
```bash
kubectl get pods --watch
```

### Step 4 — Get app URL
```bash
minikube service book-service --url
```

### Step 5 — Open URL in Windows browser ✅

---

## 🛑 How to Stop

```bash
minikube stop
```

---

## 🗑️ How to Delete Everything

```bash
kubectl delete -f book-app/kubernetes/
```

---

## 📋 YAML Files Explained

| File | Purpose |
|---|---|
| postgres-deployment.yml | Runs PostgreSQL Pod with credentials |
| postgres-service.yml | Creates hostname "postgres-db" inside cluster |
| book-deployment.yml | Runs Flask app with database env vars |
| book-service.yml | Exposes app to browser on port 30004 |

---

## 🔑 Environment Variables

| Variable | Value | Used By |
|---|---|---|
| POSTGRES_USER | admin | postgres-db Pod |
| POSTGRES_PASSWORD | secret | postgres-db Pod |
| POSTGRES_DB | bookdb | postgres-db Pod |
| DB_HOST | postgres-db | book-app Pod |
| DB_USER | admin | book-app Pod |
| DB_PASSWORD | secret | book-app Pod |
| DB_NAME | bookdb | book-app Pod |

---

## 🔑 3 Golden Rules Applied in This Project

```
Rule 1: deployment labels = service selector
book-deployment labels: app: book-app
book-service selector:  app: book-app ✅

Rule 2: containerPort = targetPort
book-deployment containerPort: 5000
book-service targetPort:        5000 ✅

Rule 3: DB_HOST = postgres service name
book-deployment DB_HOST:    postgres-db
postgres-service name:      postgres-db ✅
```

---

## 🔍 Useful Commands

```bash
# Check everything running
kubectl get all

# Check pod logs
kubectl logs <pod-name>

# Follow logs in real time
kubectl logs <pod-name> -f

# Check pod details
kubectl describe pod <pod-name>

# Connect to database
kubectl exec -it <postgres-pod-name> -- psql -U admin -d bookdb

# Scale app
kubectl scale deployment book-app --replicas=3

# Rollback
kubectl rollout undo deployment/book-app
```

---

## 🐛 Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| CrashLoopBackOff | Database not ready | Check `kubectl logs` |
| ImagePullBackOff | Wrong image name | Check image in YAML |
| Connection refused | Minikube not running | Run `minikube start` |

---

## ⚠️ Important Notes

- URL changes every Minikube restart — always run `minikube service book-service --url`
- Data is lost when Pods deleted — PersistentVolumes fix this (Week 8)
- Always apply postgres files before book-app files

---

## 🐛 Real Debugging Experience

While running this project a real production error was encountered and fixed:

**Problem:**
```
FATAL: database "bookdb" does not exist
Internal Server Error in browser
```

**Root Cause:**
```
Two projects sharing same postgres-db Pod
Student-app's postgres replaced book-app's postgres
bookdb database was gone
book-app could not connect
```

**Fix:**
```bash
# Connected to postgres directly
kubectl exec -it <postgres-pod> -- psql -U admin -d mydb

# Created missing database
CREATE DATABASE bookdb;

# Created books table
\c bookdb
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(200) NOT NULL
);

# Restarted deployment
kubectl rollout restart deployment/book-app
```

**Lesson Learned:**
```
Always deploy projects in separate namespaces
to avoid conflicts between projects
→ Namespaces covered in Week 8
```

---

## 🗺️ What I Learned Building This

```
✅ How to count YAML files needed for a project
✅ Writing deployment.yml from scratch
✅ Writing service.yml from scratch
✅ Connecting app to database via Service hostname
✅ 3 golden rules for YAML files
✅ Debugging with kubectl logs and describe
✅ Scaling deployments
✅ Debugging real production errors
✅ Fixing database connection issues
✅ Using kubectl exec to fix database directly
