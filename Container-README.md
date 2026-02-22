# 🐳 Day 31 — Docker Containers
### Start, Stop, Logs, Exec and Container Management

---

## 📋 Container Lifecycle

A container goes through 4 states:

```
Created  → exists but not started
Running  → actively running
Stopped  → stopped, still exists on disk
Removed  → deleted permanently, gone forever
```

### Lifecycle Commands

```bash
docker create --name my-container nginx   # Create without starting
docker start my-container                 # Start a created/stopped container
docker stop my-container                  # Stop a running container
docker rm my-container                    # Remove a stopped container
```

---

## 📚 Essential Container Commands

### Listing Containers
```bash
docker ps              # List RUNNING containers only
docker ps -a           # List ALL containers including stopped
```

### Running Containers
```bash
docker run -d -p 8080:80 --name my-nginx nginx   # Run in background
docker run -it --name my-shell ubuntu bash        # Run interactively
docker run -it --rm --name my-shell ubuntu bash   # Auto-remove when done
```

### Managing Containers
```bash
docker stop my-nginx      # Gracefully stop (can restart later)
docker start my-nginx     # Start a stopped container
docker restart my-nginx   # Stop then start in one command
docker rm my-nginx        # Remove a stopped container
docker rm -f my-nginx     # Force remove a RUNNING container
```

### Logs
```bash
docker logs my-nginx            # View all logs at once
docker logs -f my-nginx         # Follow logs live (Ctrl+C to stop)
docker logs --tail 5 my-nginx   # Show last 5 lines only
```

### Getting Inside a Container
```bash
docker exec -it my-nginx bash   # Open bash inside running container
```

### Monitoring
```bash
docker stats                    # Live CPU/memory usage of all containers
docker inspect my-nginx         # Detailed JSON info about a container
```

### Cleanup
```bash
docker container prune -f       # Remove all stopped containers
docker system prune             # Remove everything unused
```

---

## 🔍 Reading `docker ps` Output

```
CONTAINER ID   IMAGE   STATUS          PORTS                   NAMES
88f18ab6aede   nginx   Up 7 minutes    0.0.0.0:8080->80/tcp    my-nginx
```

| Column | Meaning |
|--------|---------|
| CONTAINER ID | Unique ID — use first 4 chars in commands |
| IMAGE | Image it was built from |
| STATUS | Current state (Up / Exited / Created) |
| PORTS | HOST:CONTAINER port mapping |
| NAMES | Container name |

---

## 📊 Reading `docker stats` Output

```
NAME       CPU %   MEM USAGE / LIMIT     MEM %   NET I/O
my-nginx   0.00%   8.895MiB / 7.664GiB   0.11%   6.14kB / 2.18kB
```

| Column | Meaning |
|--------|---------|
| CPU % | Current CPU usage |
| MEM USAGE | Memory used / total available |
| MEM % | Memory usage percentage |
| NET I/O | Network traffic in / out |

---

## 📝 Reading Nginx Logs

```
172.17.0.1 - - [22/Feb/2026:20:31:29] "GET / HTTP/1.1" 304 0
```

| Part | Meaning |
|------|---------|
| 172.17.0.1 | IP address that made the request |
| GET / | Requested the home page |
| HTTP/1.1 | Protocol used |
| 304 | Response code (304 = cached, 200 = full response) |

---

## 🔑 Exit Codes

```
Exited (0)    → stopped successfully, no errors
Exited (1)    → stopped with an error
Exited (137)  → container was forcefully killed
```

---

## ⚡ Key Differences

```
docker run   → creates a BRAND NEW container from image
docker start → starts an EXISTING stopped container
docker exec  → gets inside an ALREADY RUNNING container
docker rm    → removes stopped container (must stop first)
docker rm -f → force removes even a running container
```

---

## 💡 Important Lessons Learned

**Containers are ephemeral:**
```
Images  → stay on disk until you delete them
Containers → temporary, create and remove as needed
```

**exec does not stop the container:**
```bash
docker exec -it my-nginx bash
# explore inside...
exit
# nginx is STILL running!
docker ps  # confirms it
```

**Inside a container you see a different OS:**
```
Your WSL  → Ubuntu 22.04
nginx container → Debian GNU/Linux 13 (trixie)
Containers are fully isolated environments
```

**PID 1 is always the main process:**
```
PID 1 = nginx master process
If PID 1 dies → entire container stops
That's why nginx runs with "daemon off;"
```

---

## 🛠️ Environment

- **OS:** Windows 11 + WSL2 (Ubuntu 22.04)
- **Docker:** Version 28.2.2
- **Kernel:** 6.6.87.2-microsoft-standard-WSL2

---

## 🗺️ Roadmap Progress

```

