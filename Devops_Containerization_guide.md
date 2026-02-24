# 🐳 DevOps Guide — How to Containerize Any Application
### What Every DevOps Engineer Needs to Know

---

## 📋 Overview

As a DevOps Engineer you don't write the application code — developers do that. Your job is to take their code and containerize it so it runs anywhere, on any machine, every time.

```
Developer gives you:          You give back:
├── app.py                    ├── Dockerfile
├── requirements.txt    →     ├── docker-compose.yml
└── "works on my machine"     └── "works everywhere"
```

---

## 🔍 DevOps Checklist — Containerizing Any App

```
□ What language?        → choose correct base image
□ What port?            → set EXPOSE and -p flag
□ What packages?        → COPY package file + RUN install
□ What env variables?   → set in docker-compose.yml
□ How to start?         → set CMD in Dockerfile
□ Any database?         → add db service in compose
□ Any volumes needed?   → add volumes for persistence
```

---

## 1️⃣ Identify the Language

Every language has its own base image in Docker:

```dockerfile
# Python app
FROM python:3.11-slim

# Node.js app
FROM node:18-slim

# Java app
FROM openjdk:17-slim

# Go app
FROM golang:1.21-slim
```

### How to identify the language:

```
See app.py, requirements.txt   → Python app
See package.json, index.js     → Node.js app
See pom.xml, .java files       → Java app
See go.mod, main.go            → Go app
```

---

## 2️⃣ Find the Port

Every framework has a default port:

```
Flask (Python)     → 5000
Django (Python)    → 8000
Express (Node.js)  → 3000
React (Node.js)    → 3000
Spring (Java)      → 8080
nginx              → 80
PostgreSQL         → 5432
MySQL              → 3306
MongoDB            → 27017
Redis              → 6379
```

### How to find the port in code:

```python
# Python — look in app.py
app.run(host='0.0.0.0', port=5000)
                              ↑
                         your port
```

```javascript
// Node.js — look in index.js or server.js
app.listen(3000)
           ↑
      your port
```

```bash
# Sometimes in .env file
PORT=8080
```

---

## 3️⃣ Find the Packages

Every language has its own package file:

| Language | Package File | Install Command |
|----------|-------------|-----------------|
| Python | requirements.txt | pip install -r requirements.txt |
| Node.js | package.json | npm install |
| Java | pom.xml | mvn install |

### In Dockerfile:

```dockerfile
# Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Node.js
COPY package.json .
RUN npm install

# Java
COPY pom.xml .
RUN mvn install
```

---

## 4️⃣ Find Environment Variables

Environment variables are settings passed to the app at runtime — passwords, hostnames, ports. Never hardcoded in code.

### How to find them in code:

```python
# Python — look for os.environ
import os
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'secret')
PORT = os.environ.get('PORT', 5000)
```

```javascript
// Node.js — look for process.env
const DB_HOST = process.env.DB_HOST
const PORT = process.env.PORT || 3000
```

### How to pass them in Docker:

```bash
# docker run
docker run -e DB_HOST=postgres-db -e PORT=5000 myapp
```

```yaml
# docker-compose.yml
environment:
  DB_HOST: postgres-db
  DB_PASSWORD: secret
  PORT: 5000
```

### Common environment variables:

```
DB_HOST       → database hostname
DB_PORT       → database port
DB_USER       → database username
DB_PASSWORD   → database password
DB_NAME       → database name
PORT          → which port app listens on
SECRET_KEY    → app security key
DEBUG         → true/false for debug mode
NODE_ENV      → development/production
```

---

## 5️⃣ Find the Start Command

### How to find it:

```python
# Python — bottom of app.py
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Start command: python app.py
```

```json
// Node.js — package.json scripts section
"scripts": {
  "start": "node index.js"
}
// Start command: npm start
```

### In Dockerfile CMD:

```dockerfile
# Python
CMD ["python", "app.py"]

# Node.js
CMD ["node", "index.js"]
# or
CMD ["npm", "start"]

# Java
CMD ["java", "-jar", "app.jar"]
```

---

## 📋 Quick Reference Card

| Language | Base Image | Package File | Start Command |
|----------|-----------|--------------|---------------|
| Python | python:3.11-slim | requirements.txt | python app.py |
| Node.js | node:18-slim | package.json | npm start |
| Java | openjdk:17-slim | pom.xml | java -jar app.jar |
| Go | golang:1.21-slim | go.mod | ./main |
| nginx | nginx:latest | none | automatic |
| PostgreSQL | postgres:15 | none | automatic |

---

## 🔧 Real World Example — Python App

Developer gives you a Flask app. You containerize it.

**Step 1 — Identify language:**
```
See app.py, requirements.txt → Python app
Base image: python:3.11-slim
```

**Step 2 — Find port:**
```python
app.run(host='0.0.0.0', port=5000)  → port 5000
```

**Step 3 — Find packages:**
```
requirements.txt:
flask==3.0.0
psycopg2-binary==2.9.9
```

**Step 4 — Find environment variables:**
```python
DB_HOST = os.environ.get('DB_HOST', 'postgres-db')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'secret')
```

**Step 5 — Find start command:**
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# → python app.py
```

**Write Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

**Write docker-compose.yml:**
```yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      DB_HOST: postgres-db
      DB_PASSWORD: secret
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  db-data:
```

---

## 🔧 Real World Example — Node.js App

Developer gives you a Node.js app. You containerize it.

**Step 1 — Identify language:**
```
See package.json, index.js → Node.js app
Base image: node:18-slim
```

**Step 2 — Find port:**
```javascript
app.listen(3000)  → port 3000
```

**Step 3 — Find packages:**
```json
"dependencies": {
  "express": "4.18.0",
  "mongoose": "7.0.0"
}
```

**Step 4 — Find environment variables:**
```javascript
const DB_HOST = process.env.DB_HOST
const PORT = process.env.PORT || 3000
```

**Step 5 — Find start command:**
```json
"scripts": {
  "start": "node index.js"
}
```

**Write Dockerfile:**
```dockerfile
FROM node:18-slim

WORKDIR /app

COPY package.json .
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

---

## 💡 Key Lessons

```
1. Developer writes code → you containerize it
   Your job: Dockerfile + docker-compose.yml

2. Always check for os.environ (Python) or process.env (Node)
   These are the environment variables you need to pass

3. Package file comes BEFORE install command in Dockerfile
   requirements.txt → pip install   (Python)
   package.json     → npm install   (Node.js)

4. host='0.0.0.0' is required in Flask
   Without it → app only accepts connections from inside container
   With it    → app accepts connections from outside container

5. Never hardcode passwords in Dockerfile
   Always use environment variables (-e or compose environment:)
```
