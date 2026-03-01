# DevOps Roadmap — CI/CD with GitHub Actions

![Build and Push Docker Image](https://github.com/SaqibAliKhan1991/Docker-Handson/actions/workflows/docker-build.yml/badge.svg)
![Flask App CI/CD](https://github.com/SaqibAliKhan1991/Docker-Handson/actions/workflows/flask-app.yml/badge.svg)
![DevOps Scripts CI/CD](https://github.com/SaqibAliKhan1991/Docker-Handson/actions/workflows/devops-scripts.yml/badge.svg)


## What is This Repository?

This repository contains my complete DevOps learning journey — from Linux basics to CI/CD pipelines. Every project is containerized with Docker and automatically built and pushed to Docker Hub using GitHub Actions.

---

## CI/CD Pipelines

| Pipeline | Project | Triggers When | Docker Hub |
|----------|---------|---------------|------------|
| docker-build.yml | student-app | student-app/** changes | saqib321/student-app |
| flask-app.yml | flask-app | flask-app/** changes | saqib321/flask-app |
| devops-scripts.yml | devops-scripts | devops-scripts/** changes | saqib321/devops-scripts |

---

## How the Pipeline Works

```
Developer pushes code to GitHub
            ↓
GitHub Actions triggers automatically
            ↓
Runner (free Ubuntu computer) starts
            ↓
Step 1: Checkout code
Step 2: Build Docker image
Step 3: Run health check test
Step 4: If test passes → Push to Docker Hub
Step 5: Runner deleted
            ↓
Docker Hub has fresh image automatically ✅
```

---

## Projects

### student-app — Full Stack Flask + PostgreSQL

A complete student registration system with Flask backend and PostgreSQL database.

**Tech Stack:** Python, Flask, PostgreSQL, Docker, Docker Compose

**Pipeline steps:**
- Build Docker image
- Start PostgreSQL on Runner
- Start student-app linked to PostgreSQL
- Health check test with curl
- Push to Docker Hub with :latest and commit SHA tags

```bash
# Pull and run locally
docker compose up -d
curl http://localhost:5000/health
```

---

### flask-app — Simple Flask Application

A lightweight Flask application demonstrating bind mounts and live editing.

**Tech Stack:** Python, Flask, Docker

**Pipeline steps:**
- Build Docker image
- Run container and health check
- Push to Docker Hub

```bash
# Pull and run locally
docker pull saqib321/flask-app:latest
docker run -d -p 5000:5000 saqib321/flask-app:latest
curl http://localhost:5000/health
```

---

### devops-scripts — System Monitoring Scripts

Three Python scripts for system monitoring, disk usage and log backup — containerized and automated.

**Scripts:**
- `monitor.py` — CPU, memory and system monitoring
- `disk_usage.py` — Disk usage reporting
- `backup_logs.py` — Log backup automation

**Pipeline steps:**
- Build Docker image
- Run monitor.py as test
- Run disk_usage.py as test
- Push to Docker Hub

```bash
# Pull and run locally
docker pull saqib321/devops-scripts:latest
docker run --rm saqib321/devops-scripts:latest
docker run --rm saqib321/devops-scripts:latest python scripts/disk_usage.py
```

---

## GitHub Actions Key Concepts

| Concept | Meaning |
|---------|---------|
| Workflow | Complete automation script (.yml file) |
| Trigger | Event that starts the pipeline (push, schedule) |
| Job | Group of steps running on one Runner |
| Step | One single instruction (run or uses) |
| Action | Pre-built reusable tool (actions/checkout@v3) |
| Runner | Free temporary Ubuntu computer provided by GitHub |

---

## Secrets Used

Secrets are stored securely in GitHub repository Settings → Secrets → Actions.

| Secret Name | Purpose |
|-------------|---------|
| DOCKERHUB_USERNAME | Docker Hub login username |
| DOCKERHUB_TOKEN | Docker Hub login password |

> Passwords are never stored in pipeline files. Always use GitHub Secrets.

---

## Version Tagging

Every successful pipeline push creates two Docker image tags:

```
saqib321/student-app:latest         # always newest version
saqib321/student-app:6f8afbca...    # specific commit SHA
```

This allows rolling back to any previous version if something breaks.

---

## Repository Structure

```
Docker-Handson/
├── .github/
│   └── workflows/
│       ├── docker-build.yml      # student-app CI/CD pipeline
│       ├── flask-app.yml         # flask-app CI/CD pipeline
│       └── devops-scripts.yml    # devops-scripts CI/CD pipeline
├── student-app/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── docker-compose.yml
├── flask-app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── devops-scripts/
│   ├── scripts/
│   │   ├── monitor.py
│   │   ├── disk_usage.py
│   │   └── backup_logs.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

---

## Docker Hub

All images are publicly available on Docker Hub:

- [saqib321/student-app](https://hub.docker.com/r/saqib321/student-app)
- [saqib321/flask-app](https://hub.docker.com/r/saqib321/flask-app)
- [saqib321/devops-scripts](https://hub.docker.com/r/saqib321/devops-scripts)


