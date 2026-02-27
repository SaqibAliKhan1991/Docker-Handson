Mini-Project: Containerized DevOps Scripts
### System Monitoring Tools Packaged with Docker

---

## 📋 What I Built

Three Python system monitoring scripts containerized into a single Docker image. Anyone can run these scripts on any machine with just one Docker command — no Python installation needed.

**Docker Hub:** `docker pull saqib321/devops-scripts:v1.0`

---

## 📁 Project Structure

```
devops-scripts/
├── scripts/
│   ├── monitor.py       # CPU/memory/disk health monitor
│   ├── disk_usage.py    # Detailed disk usage report
│   └── backup_logs.py   # System log backup tool
├── requirements.txt     # Python dependencies
└── Dockerfile           # Container build instructions
```

---

## 📝 Files

### scripts/monitor.py
```python
import psutil
import datetime

def check_system():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f'[{timestamp}] System Health Check')
    print(f'  CPU Usage:    {cpu}%')
    print(f'  Memory Used:  {memory.percent}% ({memory.used // 1024**2} MB used)')
    print(f'  Disk Used:    {disk.percent}%')

    if cpu > 80:
        print('  ALERT: High CPU usage!')
    if memory.percent > 85:
        print('  ALERT: High memory usage!')
    if disk.percent > 90:
        print('  ALERT: Low disk space!')

if __name__ == '__main__':
    check_system()
```

### scripts/disk_usage.py
```python
import psutil
import datetime

def check_disk():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] Disk Usage Report')
    print('-' * 40)

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f'  Partition:  {partition.mountpoint}')
            print(f'  Total:      {usage.total // 1024**3} GB')
            print(f'  Used:       {usage.used // 1024**3} GB')
            print(f'  Free:       {usage.free // 1024**3} GB')
            print(f'  Usage:      {usage.percent}%')
            if usage.percent > 90:
                print(f'  ALERT: Low disk space on {partition.mountpoint}!')
            print('-' * 40)
        except PermissionError:
            pass

if __name__ == '__main__':
    check_disk()
```

### scripts/backup_logs.py
```python
import os
import shutil
import datetime

def backup_logs():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_dir = f'/tmp/backup_{timestamp}'
    os.makedirs(backup_dir, exist_ok=True)

    log_files = [
        '/var/log/syslog',
        '/var/log/auth.log',
        '/var/log/kern.log'
    ]

    print(f'[{timestamp}] Log Backup Started')
    print(f'  Backup folder: {backup_dir}')
    print('-' * 40)

    backed_up = 0
    for log_file in log_files:
        if os.path.exists(log_file):
            shutil.copy2(log_file, backup_dir)
            print(f'  Backed up: {log_file}')
            backed_up += 1
        else:
            print(f'  Skipped:   {log_file} (not found)')

    print('-' * 40)
    print(f'  Total backed up: {backed_up} files')
    print(f'  Backup complete!')

if __name__ == '__main__':
    backup_logs()
```

### requirements.txt
```
psutil==5.9.6
```

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/

CMD ["python", "scripts/monitor.py"]
```

---

## 🚀 Build and Run

```bash
# Build the image
docker build -t devops-scripts .

# Run default script (monitor.py)
docker run devops-scripts

# Run disk usage report
docker run devops-scripts python scripts/disk_usage.py

# Run log backup
docker run devops-scripts python scripts/backup_logs.py

# Run interactively to explore
docker run -it devops-scripts bash
```

---

## 🐳 Pull from Docker Hub

```bash
# Pull the image
docker pull saqib321/devops-scripts:v1.0

# Run monitor
docker run saqib321/devops-scripts:v1.0

# Run disk check
docker run saqib321/devops-scripts:v1.0 python scripts/disk_usage.py

# Run backup
docker run saqib321/devops-scripts:v1.0 python scripts/backup_logs.py
```

---

## 📊 Sample Output

**monitor.py:**
```
[2026-02-24 21:14:34] System Health Check
  CPU Usage:    14.3%
  Memory Used:  12.8% (792 MB used)
  Disk Used:    0.8%
```

**disk_usage.py:**
```
[2026-02-24 21:14:37] Disk Usage Report
----------------------------------------
  Partition:  /
  Total:      1006 GB
  Used:       7 GB
  Free:       947 GB
  Usage:      0.8%
----------------------------------------
```

**backup_logs.py:**
```
[2026-02-24_21-14-43] Log Backup Started
  Backup folder: /tmp/backup_2026-02-24_21-14-43
----------------------------------------
  Backed up: /var/log/syslog
  Backed up: /var/log/auth.log
----------------------------------------
  Total backed up: 2 files
  Backup complete!
```

---

## ⚡ Understanding Layer Caching

Docker saves each build layer. When you rebuild, only changed layers rebuild.

```
Dockerfile order:                    What happens on rebuild:
──────────────────────────────────   ────────────────────────────────
FROM python:3.11-slim                CACHED ✅ (never changes)
WORKDIR /app                         CACHED ✅ (never changes)
COPY requirements.txt .              CACHED ✅ (rarely changes)
RUN pip install ...                  CACHED ✅ (skips 4.8 seconds!)
COPY scripts/ ./scripts/             REBUILT ⚡ (scripts changed)
```

**Golden Rule:**
```
Things that change RARELY  → put at TOP    (cached, fast rebuilds)
Things that change OFTEN   → put at BOTTOM (only these rebuild)
```

**Result:**
```
First build:   7.8 seconds  (pip install runs)
Second build:  1-2 seconds  (pip install cached)
```

---

## 💡 Key Lessons Learned

```
1. CMD = default command
   docker run devops-scripts                    → runs monitor.py
   docker run devops-scripts python disk_usage.py → overrides CMD

2. --no-cache-dir = pip flag (different from Docker cache!)
   Tells pip: don't save downloaded packages inside image
   Keeps image size smaller

3. psutil = Python library that reads system metrics
   CPU, memory, disk — all from one library

4. Dockerfile layer order = critical for fast rebuilds
   requirements.txt BEFORE code files = pip install cached

5. v1.0 tag = versioning your images
   Always tag releases with version numbers
   latest = newest, v1.0 = specific release
```

---

## 🏷️ Docker Hub Push Workflow

```bash
# Tag with version number
docker tag devops-scripts saqib321/devops-scripts:v1.0

# Push to Docker Hub
docker push saqib321/devops-scripts:v1.0

# Anyone can now run your scripts with:
docker run saqib321/devops-scripts:v1.0
```
# pipeline added
