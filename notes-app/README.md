Pipeline

A simple Notes web application built with Flask and PostgreSQL,
deployed on Kubernetes with Namespaces, ConfigMaps, Secrets and CI/CD.

---

## 🏗️ Tech Stack

- Flask (Python) — Web application
- PostgreSQL — Database
- Docker — Containerization
- Kubernetes (Minikube) — Container orchestration
- GitHub Actions — CI/CD pipeline
- ArgoCD — Continuous Deployment
- Docker Hub — Image registry

---

## 📁 Project Structure

```
notes-app/
├── app.py
├── Dockerfile
├── requirements.txt
└── k8s/
    ├── configmap.yml                ← DB_HOST, DB_USER, DB_NAME
    ├── secret.yml                   ← DB_PASSWORD
    ├── postgres-init-configmap.yml  ← auto-creates notesdb on startup
    ├── postgres-deployment.yml      ← runs postgres pod
    ├── postgres-service.yml         ← internal access to postgres
    ├── notes-deployment.yml         ← runs notes-app (2 pods)
    └── notes-service.yml            ← external access port 30005
```

---

## 🗂️ Day 50 — ConfigMaps & Secrets

### What is a ConfigMap?
Stores non-sensitive configuration — DB_HOST, DB_USER, DB_NAME.
Injected into pods as environment variables automatically.

```bash
# List all ConfigMaps
kubectl get configmaps

# See values inside ConfigMap
kubectl describe configmap notes-app-config

# See ConfigMaps in specific namespace
kubectl get configmaps -n development
```

### What is a Secret?
Stores sensitive data — DB_PASSWORD, API_KEY.
Base64 encoded, never stored in GitHub.

```bash
# List all Secrets
kubectl get secrets

# See secret keys (values hidden)
kubectl describe secret notes-app-secret

# Decode a secret value
kubectl get secret notes-app-secret -o jsonpath='{.data.DB_PASSWORD}' | base64 --decode && echo

# Verify env vars inside running pod
kubectl exec -it <pod-name> -- env | grep DB
```

### ConfigMap vs Secret

| | ConfigMap | Secret |
|---|---|---|
| Use for | Non-sensitive config | Passwords, tokens, keys |
| Storage | Plain text | Base64 encoded |
| Example | DB_HOST, DB_NAME | DB_PASSWORD, API_KEY |
| Visible in describe | Yes | Hidden |

> ⚠️ Base64 is NOT encryption — it is just encoding. Use Vault or Sealed Secrets for real production security.

---

## 🗂️ Day 51 — Namespaces

### What is a Namespace?
Divides one Kubernetes cluster into separate isolated areas.
Like floors in an office building — each floor is completely separate.

```
One Kubernetes Cluster
├── default      ← existing apps (todo, book, student)
├── development  ← notes-app testing version
├── production   ← notes-app live version
└── kube-system  ← Kubernetes internals (never touch!)
```

### Why Namespaces?
```
Without Namespaces:
Developer tests new feature → breaks live app → customers see errors ❌

With Namespaces:
Developer tests in development namespace
Live app runs in production namespace
Changes in development NEVER affect production ✅
```

### Namespace Commands

```bash
# List all namespaces
kubectl get namespaces

# Create namespace
kubectl create namespace development
kubectl create namespace production

# See pods in specific namespace
kubectl get pods -n development

# See everything in namespace
kubectl get all -n development

# See ALL pods across ALL namespaces
kubectl get pods --all-namespaces

# Delete namespace and ALL contents inside it ⚠️
kubectl delete namespace development
```

### Key Rule
```
kubectl get pods              → default namespace only
kubectl get pods -n dev       → development namespace only
kubectl get pods --all-namespaces → everything everywhere
```

---

## 🚀 How to Run

### Step 1 — Start Minikube
```bash
minikube start
```

### Step 2 — Create Namespace
```bash
kubectl create namespace development
kubectl get namespaces
```

### Step 3 — Deploy Postgres First ⚠️
Always deploy postgres before notes-app!
```bash
kubectl apply -f k8s/postgres-init-configmap.yml -n development
kubectl apply -f k8s/postgres-deployment.yml -n development
kubectl apply -f k8s/postgres-service.yml -n development
```

### Step 4 — Wait for Postgres
```bash
kubectl get pods -n development -w
# Wait until postgres shows 1/1 Running
```

### Step 5 — Deploy Notes App
```bash
kubectl apply -f k8s/configmap.yml -n development
kubectl apply -f k8s/secret.yml -n development
kubectl apply -f k8s/notes-deployment.yml -n development
kubectl apply -f k8s/notes-service.yml -n development
```

### Step 6 — Verify Everything
```bash
kubectl get all -n development
```

### Step 7 — Get URL and Test
```bash
minikube service notes-service -n development --url
curl http://127.0.0.1:<port>
```

---

## 🏗️ Kubernetes Architecture

```
User visits browser
↓
notes-service (NodePort 30005)    ← external access
↓
notes-app pods (2 replicas)       ← Flask app
reads DB_HOST, DB_USER, DB_NAME   ← from ConfigMap
reads DB_PASSWORD                 ← from Secret
↓
postgres-service (ClusterIP)      ← internal access only
↓
postgres-db pod                   ← PostgreSQL database
auto-creates notesdb              ← from init ConfigMap
```

---

## 🐛 Debugging Commands

```bash
# Check pod status
kubectl get pods -n development

# See app logs
kubectl logs deployment/notes-app -n development

# Follow logs live
kubectl logs deployment/notes-app -n development -f

# Describe pod for events
kubectl describe pod <pod-name> -n development

# Go inside postgres pod
kubectl exec -it <postgres-pod> -n development -- psql -U admin -d mydb

# Check databases exist
\l

# Check tables exist
\dt

# Exit psql
\q
```

---

## ⚠️ Important Notes

- Always deploy postgres **before** notes-app
- Namespaces are completely isolated — notes-service in `development` is NOT visible in `default`
- Use `--all-namespaces` to see everything across all namespaces
- Init script only runs on a **fresh** postgres container
- `kubectl delete namespace` removes EVERYTHING inside — be careful in production!
- URL changes every Minikube restart — always run `minikube service notes-service -n development --url`

---

## 🔄 CI/CD Pipeline

```
You push code to GitHub (notes-app/ folder)
↓
GitHub Actions triggers automatically
↓
Builds Docker image
↓
Pushes to Docker Hub (saqib321/notes-app:latest)
↓
ArgoCD detects change
↓
Deploys to Kubernetes automatically ✅
```


