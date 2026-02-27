![Build and Push Docker Image](https://github.com/SaqibAliKhan1991/Docker-Handson/actions/workflows/docker-build.yml/badge.svg)
![Flask App CI/CD](https://github.com/SaqibAliKhan1991/Docker-Handson/actions/workflows/flask-app.yml/badge.svg)
![DevOps Scripts CI/CD](https://github.com/SaqibAliKhan1991/Docker-Handson/actions/workflows/devops-scripts.yml/badge.svg)
### Build a Real Python Flask Web Application with Docker

---

## 📋 What I Built

A real Flask web application containerized with Docker, serving two routes:
- `/` — Home page with HTML response
- `/health` — Health check endpoint returning JSON

---

## 📁 Project Structure

```
flask-app/
├── app.py               # Flask web application
├── requirements.txt     # Python dependencies
└── Dockerfile           # Container build instructions
```

---

## 📝 Files

### app.py
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello from Docker!</h1><p>Saqib Ali Khan - Berlin DevOps Journey 🚀</p>'

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### requirements.txt
```
flask==3.0.0
```

### Dockerfile
```dockerfile
# Base image: Python 3.11 slim (small size)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Tell Docker this container listens on port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
```

---

## 🚀 Build and Run

```bash
# Build the image
docker build -t flask-app .

# Run the container
docker run -d -p 5000:5000 --name my-flask flask-app

# Check it's running
docker ps

# Open in browser
# http://localhost:5000
# http://localhost:5000/health

# Check logs
docker logs my-flask

# Stop and remove
docker stop my-flask
docker rm my-flask
```

---

## 📚 Dockerfile Instructions Learned

| Instruction | What it does |
|---|---|
| `FROM python:3.11-slim` | Start from Python base image |
| `WORKDIR /app` | Set working directory inside container |
| `COPY requirements.txt .` | Copy requirements file first |
| `RUN pip install -r requirements.txt` | Install dependencies |
| `COPY . .` | Copy rest of application code |
| `EXPOSE 5000` | Document which port app listens on |
| `CMD ["python", "app.py"]` | Default command when container starts |

---

## ⚡ Layer Caching — Why Order Matters

```
First build:                         Second build (code change only):
────────────────────────────────     ────────────────────────────────
FROM python:3.11-slim      ✅        FROM python:3.11-slim  → CACHED ✅
WORKDIR /app               ✅        WORKDIR /app           → CACHED ✅
COPY requirements.txt      ✅        COPY requirements.txt  → CACHED ✅
RUN pip install  → 5.4s   ✅        RUN pip install        → CACHED ✅
COPY . .                   ✅        COPY . .               → rebuilt ⚡
Total: 8.7 seconds                  Total: 1.4 seconds
```

**Golden Rule:**
```
Things that change RARELY  → put at TOP    (cached more often)
Things that change OFTEN   → put at BOTTOM (rebuilt when needed)
```

---

## 📦 What is requirements.txt?

A shopping list for Python packages. Instead of installing packages one by one:

```bash
# Without requirements.txt
pip install flask
pip install requests
pip install sqlalchemy
# ... manually one by one

# With requirements.txt
pip install -r requirements.txt  # installs everything at once
```

**Why use exact versions:**
```
flask==3.0.0   → install EXACTLY this version (safe, predictable)
flask>=3.0.0   → install this version or higher (risky)
flask          → install latest (dangerous in production)
```

**pip installs dependencies automatically:**
```
You ask for:  flask==3.0.0
pip installs: flask + werkzeug + jinja2 + click + itsdangerous + markupsafe
```

---

## 🐛 Bugs Fixed Today

**Bug 1 — Missing import:**
```python
# Wrong — Flask not imported
app = Flask(__name__)

# Correct — always import first
from flask import Flask
app = Flask(__name__)
```

**Bug 2 — Missing dot in build command:**
```bash
docker build -t flask-app    # Wrong — missing .
docker build -t flask-app .  # Correct ✅
```

**Bug 3 — Typo in image name:**
```bash
docker run my-flasp-app   # Wrong — typo
docker run my-flask-app   # Correct ✅
```

---

## 💡 Key Lessons Learned

```
1. Always copy requirements.txt BEFORE your code
   → pip install gets cached, saves time on every rebuild

2. Always use exact versions in requirements.txt
   → same behaviour on every machine, every time

3. requirements.txt works everywhere
   → Docker, local machine, colleague's machine, CI/CD pipeline

4. EXPOSE is just documentation
   → actual port mapping happens with -p flag in docker run

5. host='0.0.0.0' in Flask is required
   → allows connections from outside the container
   → without it Flask only accepts connections from inside container
```


