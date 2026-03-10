# 🚀 Todo App — Full DevOps Pipeline

A simple **Todo web application** built with **Flask** and **PostgreSQL**, deployed on **Kubernetes**, with a complete **CI/CD pipeline using GitHub Actions**.

---

## 📌 What This Project Does

- ✅ Add todo items
- ✅ View all todos
- ✅ Delete todo items
- ✅ Data saved to PostgreSQL database
- ✅ Auto builds and deploys on every code push

---

## 🏗️ Tech Stack

- Flask (Python) — Web application
- PostgreSQL — Database
- Docker — Containerization
- Kubernetes (Minikube) — Container orchestration
- GitHub Actions — CI/CD pipeline
- Docker Hub — Image registry

---

## 🔄 Full DevOps Pipeline

```
Developer pushes code to GitHub
↓
GitHub Actions triggers automatically
↓
Builds new Docker image
↓
Pushes image to Docker Hub
↓
kubectl set image → deploys to Kubernetes
↓
New version live in browser ✅
```

---

## 📁 Project Structure

```
todo-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── k8s/
    ├── postgres-init-configmap.yml   ← auto-creates databases on startup
    ├── postgres-deployment.yml
    ├── postgres-service.yml
    ├── configmap.yml                 ← app env vars (DB_HOST, DB_NAME, etc.)
    ├── secret.yml                    ← DB_PASSWORD
    ├── todo-deployment.yml
    └── todo-service.yml
```

---

## ⚙️ Prerequisites

- Docker installed
- Minikube installed
- kubectl installed
- Docker Hub account

---

## 🚀 How to Run Locally

### Step 1 — Start Minikube

```bash
minikube start
```

### Step 2 — Apply postgres init ConfigMap first

```bash
kubectl apply -f todo-app/k8s/postgres-init-configmap.yml
kubectl apply -f todo-app/k8s/postgres-deployment.yml
kubectl apply -f todo-app/k8s/postgres-service.yml
```

> ⚠️ Always deploy postgres **before** the app so databases are ready.

### Step 3 — Deploy the app

```bash
kubectl apply -f todo-app/k8s/configmap.yml
kubectl apply -f todo-app/k8s/secret.yml
kubectl apply -f todo-app/k8s/todo-deployment.yml
kubectl apply -f todo-app/k8s/todo-service.yml
```

### Step 4 — Watch Pods Start

```bash
kubectl get pods --watch
```

All pods should show `1/1 Running` with 0 restarts.

### Step 5 — Get Application URL

```bash
minikube service todo-service --url
```

### Step 6 — Open URL in Browser ✅

---

## 🗄️ Database Architecture

This project uses a **single shared PostgreSQL pod** that hosts multiple databases, each owned by a separate app:

| Database | Used By  |
|----------|----------|
| tododb   | todo-app |
| bookdb   | book-app |
| mydb     | default  |

All databases are **auto-created on postgres startup** via the init ConfigMap mounted at `/docker-entrypoint-initdb.d/`.

> ⚠️ The init script only runs on a **fresh** postgres container. If the pod already has data, it will not re-run.

---

## 🔐 Environment Variables

| Variable          | Value       | Source     |
|-------------------|-------------|------------|
| POSTGRES_USER     | admin       | Deployment |
| POSTGRES_PASSWORD | secret      | Secret     |
| POSTGRES_DB       | mydb        | Deployment |
| DB_HOST           | postgres-db | ConfigMap  |
| DB_USER           | admin       | ConfigMap  |
| DB_PASSWORD       | secret      | Secret     |
| DB_NAME           | tododb      | ConfigMap  |

---

## 🔄 CI/CD Pipeline

**Pipeline file:** `.github/workflows/todo-app.yml`

### Triggers Automatically When:

- Code is pushed to `main` branch
- Changes are inside `todo-app/` folder

### Pipeline Steps:

1. Checkout code
2. Login to Docker Hub
3. Build Docker image
4. Push image to Docker Hub as `saqib321/todo-app:latest`

---

## 🔐 Required GitHub Secrets

- `DOCKER_USERNAME` — Your Docker Hub username
- `DOCKER_PASSWORD` — Your Docker Hub password

---

## 🔁 Deploy New Version Manually

```bash
kubectl set image deployment/todo-app todo-app=saqib321/todo-app:latest
kubectl rollout status deployment/todo-app
minikube service todo-service --url
```

---

## 🏗️ Kubernetes Architecture

```
Browser
↓
todo-service (NodePort :30001)
↓
todo-app Pod (Flask :5000)
↓
postgres-db Service (ClusterIP :5432)
↓
postgres-db Pod (PostgreSQL)
```

---

## 🛑 How to Stop

```bash
minikube stop
```

---

## 🗑️ How to Delete Everything

```bash
kubectl delete -f todo-app/k8s/
```

---

## 🐛 Debugging Commands

```bash
# Check pod status
kubectl get pods

# View app logs
kubectl logs deployment/todo-app

# Follow logs in real time
kubectl logs deployment/todo-app -f

# Describe a pod for events and errors
kubectl describe pod <pod-name>

# Roll back to previous version
kubectl rollout undo deployment/todo-app

# Connect to postgres and inspect databases
kubectl exec -it <postgres-pod-name> -- psql -U admin -d mydb

# List all databases
\l

# List tables in tododb
kubectl exec -it <postgres-pod-name> -- psql -U admin -d tododb -c "\dt"

# Manually create a missing table
kubectl exec -it <postgres-pod-name> -- psql -U admin -d tododb
```

---

## 🗂️ ConfigMap & Secret Commands

### ConfigMap

ConfigMaps store **non-sensitive** config like hostnames, usernames, and database names. They are injected into pods as environment variables.

```bash
# List all ConfigMaps
kubectl get configmaps

# See what's inside a ConfigMap
kubectl describe configmap todo-app-config

# See the postgres init script
kubectl describe configmap postgres-init-script
```

### Secret

Secrets store **sensitive data** like passwords. Kubernetes hides the value and stores it base64 encoded.

```bash
# List all Secrets
kubectl get secrets

# Describe a secret (value is hidden, shows size only)
kubectl describe secret todo-app-secret

# Decode a single secret value
kubectl get secret todo-app-secret -o jsonpath='{.data.DB_PASSWORD}' | base64 --decode && echo

# Decode all fields in a secret (returns raw base64 JSON)
kubectl get secret todo-app-secret -o jsonpath='{.data}' && echo

# Verify what env vars a running pod actually receives
kubectl exec -it <pod-name> -- env | grep DB
```

### ConfigMap vs Secret

| | ConfigMap | Secret |
|---|---|---|
| Use for | Non-sensitive config | Passwords, tokens, keys |
| Storage | Plain text | Base64 encoded |
| Example | DB_HOST, DB_NAME, DB_USER | DB_PASSWORD, API_KEY |
| Visible in describe | ✅ Yes | ❌ Hidden |

> ⚠️ Base64 is **not encryption** — it is just encoding. For production, use tools like **Vault** or **Sealed Secrets** for real security.

---

## ⚠️ Important Notes

- URL changes every Minikube restart — always run: `minikube service todo-service --url`
- Data is lost when pods are deleted — PersistentVolumes required for production
- Always apply postgres files **before** app files
- The init script only runs on a **fresh** postgres container — existing data directories are not re-initialized
- If a new app needs a new database, add it to `postgres-init-configmap.yml` and restart the postgres deployment

---

Made with ❤️ using DevOps best practices.

