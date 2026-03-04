Todo App — Full DevOps Pipeline
A simple Todo web application built with Flask and PostgreSQL, deployed on Kubernetes with a full CI/CD pipeline using GitHub Actions.

🚀 What This Project Does
Add todo items
View all todos
Delete todo items
Data saved to PostgreSQL database
Auto builds and deploys on every code push
🏗️ Tech Stack
Tool	Purpose
Flask (Python)	Web application
PostgreSQL	Database
Docker	Containerization
Kubernetes (Minikube)	Container orchestration
GitHub Actions	CI/CD pipeline
Docker Hub	Image registry
🔄 Full DevOps Pipeline
Developer pushes code to GitHub
        ↓
GitHub Actions triggers automatically
        ↓
Builds new Docker image
        ↓
Pushes to Docker Hub
        ↓
kubectl set image → deploys to Kubernetes
        ↓
New version live in browser ✅
📁 Project Structure
todo-app/
├── app.py                      → Flask application
├── requirements.txt            → Python dependencies
├── Dockerfile                  → Docker image instructions
└── kubernetes/
    ├── postgres-deployment.yml → PostgreSQL Pod
    ├── postgres-service.yml    → PostgreSQL Service
    ├── todo-deployment.yml     → Todo App Pod
    └── todo-service.yml        → Todo App Service (NodePort)
⚙️ Prerequisites
Docker installed
Minikube installed
kubectl installed
Docker Hub account
🚀 How to Run Locally
Step 1 — Start Minikube
bash
minikube start
Step 2 — Deploy to Kubernetes
bash
kubectl apply -f todo-app/kubernetes/
Step 3 — Watch Pods start
bash
kubectl get pods --watch
Step 4 — Get app URL
bash
minikube service todo-service --url
Step 5 — Open URL in browser ✅
🛑 How to Stop
bash
minikube stop
🗑️ How to Delete Everything
bash
kubectl delete -f todo-app/kubernetes/
🔄 CI/CD Pipeline
Pipeline file: .github/workflows/todo-app.yml

Triggers automatically when:

Code is pushed to main branch
Changes are inside todo-app/ folder
Pipeline steps:

Checkout code
Login to Docker Hub
Build Docker image
Push to Docker Hub as saqib321/todo-app:latest
Required GitHub Secrets
Secret	Value
DOCKER_USERNAME	Your Docker Hub username
DOCKER_PASSWORD	Your Docker Hub password
🔁 Deploy New Version
After pipeline runs successfully:

bash
# Pull and deploy latest image
kubectl set image deployment/todo-app todo-app=saqib321/todo-app:latest

# Check deployment status
kubectl rollout status deployment/todo-app

# Get URL
minikube service todo-service --url
🏗️ Kubernetes Architecture
Browser
    ↓
todo-service (NodePort :30001)
    ↓
todo-app Pod (Flask :5000)
    ↓
postgres-db Service (ClusterIP :5432)
    ↓
postgres-db Pod (PostgreSQL)
📋 YAML Files Explained
File	Purpose
postgres-deployment.yml	Runs PostgreSQL with credentials
postgres-service.yml	Creates hostname "postgres-db" inside cluster
todo-deployment.yml	Runs Flask app with database env vars
todo-service.yml	Exposes app to browser on port 30001
🔑 Environment Variables
Variable	Value	Used By
POSTGRES_USER	admin	postgres-db Pod
POSTGRES_PASSWORD	secret	postgres-db Pod
POSTGRES_DB	tododb	postgres-db Pod
DB_HOST	postgres-db	todo-app Pod
DB_USER	admin	todo-app Pod
DB_PASSWORD	secret	todo-app Pod
DB_NAME	tododb	todo-app Pod
🐛 Debugging Commands
bash
# Check pod status
kubectl get pods

# Check pod logs
kubectl logs <pod-name>

# Check pod details
kubectl describe pod <pod-name>

# Rollback if something goes wrong
kubectl rollout undo deployment/todo-app

# Connect to database
kubectl exec -it <postgres-pod-name> -- psql -U admin -d tododb
⚠️ Important Notes
URL changes every Minikube restart — always run minikube service todo-service --url
Data is lost when Pods are deleted — PersistentVolumes needed for production
Always apply postgres files before todo-app files
