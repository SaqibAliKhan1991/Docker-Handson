# 🐳 Docker Basics
### DevOps Learning Journey | Berlin, Germany

This repository contains hands-on Docker practice work completed as part of a 3-month DevOps roadmap transitioning from Technical Support Engineer to Junior DevOps Engineer.

---


## 📁 Project Structure

```
Docker-Practice/
├── my-first-image/
│   ├── Dockerfile
│   └── app.py
└── system-info/
    ├── Dockerfile
    └── app.py
```

---

## 🚀 Projects

### 1. my-first-image
A simple Python container that prints a custom message. Built to understand the core Docker workflow: write code → create Dockerfile → build image → run container.

**Build and run:**
```bash
cd my-first-image
docker build -t my-first-image .
docker run my-first-image
```

**Expected output:**
```
Hello from Saqib - Berlin DevOps Journey!
```

---

### 2. system-info
A Python container that displays live system information from inside the container — OS, version, CPU architecture, Python version.

**Build and run:**
```bash
cd system-info
docker build -t system-info .
docker run --name my-system system-info
```

**Expected output:**
```
========================================
   SYSTEM INFO - Docker Container
========================================
Date/Time : 2026-02-22 ...
OS        : Linux
OS Version: #1 SMP PREEMPT_DYNAMIC ...
Machine   : x86_64
Python    : 3.11.14
========================================
Developer : Saqib Ali Khan - Berlin
========================================
```

**Get inside the container:**
```bash
docker run -it --rm --name system-shell system-info bash
```

---

## 📚 Key Concepts Learned

### Image vs Container
```
IMAGE      = blueprint/template (stored on disk, read-only)
CONTAINER  = running instance of an image (active, isolated)

One image → many containers
Deleting a container never deletes the image
```

### Dockerfile Instructions
```dockerfile
FROM        # base image to start from
WORKDIR     # set working directory inside container
COPY        # copy files from host into container
RUN         # execute command during build
ENV         # set environment variable
EXPOSE      # document which port app listens on
CMD         # default command when container starts
```

### Essential Commands
```bash
# Images
docker images                    # list all images
docker pull nginx                # download image
docker build -t my-app .         # build image from Dockerfile
docker rmi my-app                # remove image
docker history nginx             # see image layers
docker inspect nginx             # detailed image metadata

# Containers
docker run -d -p 8080:80 --name my-nginx nginx   # run container
docker ps                        # list running containers
docker ps -a                     # list all containers
docker start my-nginx            # start stopped container
docker stop my-nginx             # stop running container
docker rm my-nginx               # remove container
docker logs my-nginx             # view container logs
docker logs -f my-nginx          # follow logs live
docker exec -it my-nginx bash    # get inside running container
docker stats                     # live resource usage

# Cleanup
docker container prune -f        # remove all stopped containers
docker image prune -f            # remove dangling images
docker system prune              # remove everything unused
```

### Docker Run Flags
```bash
-d          # detached — run in background
-p 8080:80  # port mapping HOST:CONTAINER
--name      # give container a readable name (always use this!)
-it         # interactive terminal (get inside container)
--rm        # auto-remove container when it exits
```

### Layer Caching
Docker caches each build layer. If a layer hasn't changed, it reuses the cache — making rebuilds faster.

**Best practice — order your Dockerfile correctly:**
```dockerfile
# Things that change RARELY → put at TOP (cached more)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Things that change OFTEN → put at BOTTOM (rebuilt more)
COPY . .
```

### Exit Codes
```
Exited (0)   → stopped successfully, no errors
Exited (1)   → stopped with an error
Exited (137) → container was forcefully killed
```

---

## 🛠️ Environment

- **OS:** Windows 11 + WSL2 (Ubuntu 22.04)
- **Docker:** Version 28.2.2
- **Setup:** Docker Desktop with WSL2 backend integration
- **Kernel:** 6.6.87.2-microsoft-standard-WSL2

---

## 📖 Resources

- [TechWorld with Nana — Docker Full Course (YouTube)](https://www.youtube.com/c/TechWorldwithNana)
- [Official Docker Documentation](https://docs.docker.com)
- [Play with Docker — Browser-based practice](https://labs.play-with-docker.com)
- [Docker Hub — Official images](https://hub.docker.com)

---
---

*Part of a 3-month DevOps roadmap — Technical Support Engineer → Junior DevOps Engineer*
*Berlin, Germany 🇩🇪*
