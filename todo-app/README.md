# 🚀 Todo App --- Full DevOps Pipeline

A simple **Todo web application** built with **Flask** and
**PostgreSQL**, deployed on **Kubernetes**, with a complete **CI/CD
pipeline using GitHub Actions**.

------------------------------------------------------------------------

## 📌 What This Project Does

-   ✅ Add todo items
-   ✅ View all todos
-   ✅ Delete todo items
-   ✅ Data saved to PostgreSQL database
-   ✅ Auto builds and deploys on every code push

------------------------------------------------------------------------

## 🏗️ Tech Stack

-   Flask (Python) --- Web application\
-   PostgreSQL --- Database\
-   Docker --- Containerization\
-   Kubernetes (Minikube) --- Container orchestration\
-   GitHub Actions --- CI/CD pipeline\
-   Docker Hub --- Image registry

------------------------------------------------------------------------

## 🔄 Full DevOps Pipeline

Developer pushes code to GitHub\
↓\
GitHub Actions triggers automatically\
↓\
Builds new Docker image\
↓\
Pushes image to Docker Hub\
↓\
kubectl set image → deploys to Kubernetes\
↓\
New version live in browser ✅

------------------------------------------------------------------------

## 📁 Project Structure

    todo-app/
    ├── app.py
    ├── requirements.txt
    ├── Dockerfile
    └── kubernetes/
        ├── postgres-deployment.yml
        ├── postgres-service.yml
        ├── todo-deployment.yml
        └── todo-service.yml

------------------------------------------------------------------------

## ⚙️ Prerequisites

-   Docker installed
-   Minikube installed
-   kubectl installed
-   Docker Hub account

------------------------------------------------------------------------

## 🚀 How to Run Locally

### Step 1 --- Start Minikube

``` bash
minikube start
```

### Step 2 --- Deploy to Kubernetes

``` bash
kubectl apply -f todo-app/kubernetes/
```

### Step 3 --- Watch Pods Start

``` bash
kubectl get pods --watch
```

### Step 4 --- Get Application URL

``` bash
minikube service todo-service --url
```

### Step 5 --- Open URL in Browser ✅

------------------------------------------------------------------------

## 🛑 How to Stop

``` bash
minikube stop
```

------------------------------------------------------------------------

## 🗑️ How to Delete Everything

``` bash
kubectl delete -f todo-app/kubernetes/
```

------------------------------------------------------------------------

## 🔄 CI/CD Pipeline

**Pipeline file:**

    .github/workflows/todo-app.yml

### Triggers Automatically When:

-   Code is pushed to main branch
-   Changes are inside todo-app/ folder

### Pipeline Steps:

1.  Checkout code
2.  Login to Docker Hub
3.  Build Docker image
4.  Push image to Docker Hub as `saqib321/todo-app:latest`

------------------------------------------------------------------------

## 🔐 Required GitHub Secrets

-   DOCKER_USERNAME --- Your Docker Hub username
-   DOCKER_PASSWORD --- Your Docker Hub password

------------------------------------------------------------------------

## 🔁 Deploy New Version Manually

``` bash
kubectl set image deployment/todo-app todo-app=saqib321/todo-app:latest
kubectl rollout status deployment/todo-app
minikube service todo-service --url
```

------------------------------------------------------------------------

## 🏗️ Kubernetes Architecture

Browser\
↓\
todo-service (NodePort :30001)\
↓\
todo-app Pod (Flask :5000)\
↓\
postgres-db Service (ClusterIP :5432)\
↓\
postgres-db Pod (PostgreSQL)

------------------------------------------------------------------------

## 🔑 Environment Variables

POSTGRES_USER=admin\
POSTGRES_PASSWORD=secret\
POSTGRES_DB=tododb\
DB_HOST=postgres-db\
DB_USER=admin\
DB_PASSWORD=secret\
DB_NAME=tododb

------------------------------------------------------------------------

## 🐛 Debugging Commands

``` bash
kubectl get pods
kubectl logs <pod-name>
kubectl describe pod <pod-name>
kubectl rollout undo deployment/todo-app
kubectl exec -it <postgres-pod-name> -- psql -U admin -d tododb
```

------------------------------------------------------------------------

## ⚠️ Important Notes

-   URL changes every Minikube restart --- always run:
    `minikube service todo-service --url`
-   Data is lost when Pods are deleted --- PersistentVolumes required
    for production
-   Always apply postgres files before todo-app files

------------------------------------------------------------------------

Made with ❤️ using DevOps best practices.
