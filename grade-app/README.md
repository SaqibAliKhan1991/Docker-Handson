Practice Project: Student Grade Calculator
### A Flask Web Application Containerized with Docker

---

## 📋 What I Built

A Student Grade Calculator web app with multiple routes, built from scratch as hands-on Docker practice.

---

## 📁 Project Structure

```
grade-app/
├── app.py               # Flask web application
├── requirements.txt     # Python dependencies
└── Dockerfile           # Container build instructions
```

---

## 📝 Files

### app.py
```python
from flask import Flask, request

app = Flask(__name__)

# Sample data
students = [
    {"name": "Ahmed", "grade": 85},
    {"name": "Sara", "grade": 92},
    {"name": "Ali", "grade": 78}
]

@app.route('/')
def home():
    result = '<h1>Student Grade Calculator</h1>'
    result += '<h2>All Students:</h2>'
    for s in students:
        result += f'<p>{s["name"]} → Grade: {s["grade"]}</p>'
    return result

@app.route('/add')
def add():
    name = request.args.get('name', 'Unknown')
    grade = int(request.args.get('grade', 0))
    students.append({"name": name, "grade": grade})
    return f'<h2>Added {name} with grade {grade}</h2>'

@app.route('/average')
def average():
    avg = sum(s['grade'] for s in students) / len(students)
    return f'<h2>Class Average: {avg:.2f}</h2>'

@app.route('/highest')
def highest():
    top = max(students, key=lambda s: s['grade'])
    return f'<h2>Highest Grade: {top["name"]} with {top["grade"]}</h2>'

@app.route('/lowest')
def lowest():
    low = min(students, key=lambda s: s['grade'])
    return f'<h2>Lowest Grade: {low["name"]} with {low["grade"]}</h2>'

@app.route('/health')
def health():
    return {'status': 'ok', 'students': len(students)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### requirements.txt
```
flask==3.0.0
```

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

---

## 🚀 Build and Run

```bash
# Build the image
docker build -t grade-app .

# Run the container
docker run -d -p 5000:5000 --name my-grade grade-app

# Check it's running
docker ps

# Stop and remove
docker stop my-grade
docker rm my-grade
```

---

## 🌐 Available Routes

| Route | Description | Example |
|-------|-------------|---------|
| `/` | Show all students and grades | `http://localhost:5000` |
| `/add` | Add a new student | `http://localhost:5000/add?name=Saqib&grade=95` |
| `/average` | Show class average | `http://localhost:5000/average` |
| `/highest` | Show highest grade | `http://localhost:5000/highest` |
| `/lowest` | Show lowest grade | `http://localhost:5000/lowest` |
| `/health` | Health check | `http://localhost:5000/health` |

---

## 🧪 Testing the Routes

```bash
# See all students
http://localhost:5000

# Add yourself as a student
http://localhost:5000/add?name=Saqib&grade=95

# Check class average after adding
http://localhost:5000/average

# Who has the highest grade?
http://localhost:5000/highest

# Who has the lowest grade?
http://localhost:5000/lowest

# Health check — also shows total students
http://localhost:5000/health
```

---

## 📊 Sample Output

```
Home page:
  Student Grade Calculator
  All Students:
  Ahmed → Grade: 85
  Sara  → Grade: 92
  Ali   → Grade: 78
  Saqib → Grade: 95

Average:  Highest Grade: Saqib with 95
Lowest:   Lowest Grade: Ali with 78
Health:   {"status": "ok", "students": 4}
```

---

## 🐛 Errors Encountered and Fixed

**Error 1 — Port already allocated:**
```
Bind for 0.0.0.0:5000 failed: port is already allocated
```
Fix: Another container was using port 5000
```bash
docker stop my-flask   # stop the other container first
docker run -d -p 5000:5000 --name my-grade grade-app
```

**Error 2 — Container name conflict:**
```
Conflict. The container name "/my-grade" is already in use
```
Fix: Remove the old container first
```bash
docker rm my-grade
docker run -d -p 5000:5000 --name my-grade grade-app
```

---

## 💡 Key Lessons Reinforced

```
1. Always stop containers using a port before running a new one
2. Always rm a container before reusing its name
3. requirements.txt lists packages → pip installs them + dependencies
4. Dockerfile order matters → requirements first, code last
5. Build cache makes rebuilds fast → 1.8s vs first build
6. host='0.0.0.0' required in Flask → allows outside connections
```

---

## ⚡ Build Cache in Action

```
[2/5] WORKDIR /app              → CACHED ✅
[3/5] COPY requirements.txt .   → CACHED ✅
[4/5] RUN pip install           → CACHED ✅ (Flask already installed)
[5/5] COPY . .                  → rebuilt ⚡ (new code)
Total build time: 1.8 seconds
```



