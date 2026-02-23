— Docker Volumes & Networking
### Persist Data and Connect Containers to Each Other

---

## 📋 What I Built

A full stack Student Registration application with:
- **Flask web app** — registration form and student list
- **PostgreSQL database** — stores student data persistently
- **Docker Network** — containers communicate by name
- **Docker Volume** — data survives container deletion
- **Docker Compose** — start everything with one command

---

## 📁 Project Structure

```
student-app/
├── app.py               # Flask web application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build instructions
└── docker-compose.yml   # Multi-container orchestration
```

---

## 📝 Files

### app.py
```python
from flask import Flask, request, redirect
import psycopg2
import os
import time

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'postgres-db'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'secret'),
        database=os.environ.get('DB_NAME', 'mydb')
    )

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    grade INT
                )
            ''')
            conn.commit()
            cur.close()
            conn.close()
            print("Database ready!")
            return
        except Exception as e:
            print(f"Database not ready yet, retrying... ({e})")
            retries -= 1
            time.sleep(3)
    raise Exception("Could not connect to database after 5 retries")

@app.route('/')
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students ORDER BY id DESC')
    students = cur.fetchall()
    cur.close()
    conn.close()
    html = '''
    <h1>Student Registration</h1>
    <form action="/register" method="POST">
        <p>Name: <input type="text" name="name" required></p>
        <p>Grade: <input type="number" name="grade" required></p>
        <p><input type="submit" value="Register Student"></p>
    </form>
    <h2>Registered Students:</h2>
    '''
    for s in students:
        html += f'<p>ID: {s[0]} | Name: {s[1]} | Grade: {s[2]}</p>'
    return html

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    grade = request.form['grade']
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO students (name, grade) VALUES (%s, %s)', (name, grade))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
```

### requirements.txt
```
flask==3.0.0
psycopg2-binary==2.9.9
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

### docker-compose.yml
```yaml
services:

  postgres-db:
    image: postgres:15
    container_name: postgres-db
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - student-network

  student-app:
    build: .
    container_name: student-app
    ports:
      - "5000:5000"
    environment:
      DB_HOST: postgres-db
      DB_USER: admin
      DB_PASSWORD: secret
      DB_NAME: mydb
    depends_on:
      - postgres-db
    networks:
      - student-network

networks:
  student-network:
    driver: bridge

volumes:
  postgres-data:
```

---

## 🚀 Run with Docker Compose (Recommended)

```bash
# Start everything — network, volumes, both containers
docker compose up -d

# Check status
docker compose ps

# See logs
docker compose logs
docker compose logs -f              # follow live
docker compose logs student-app     # one service only

# Stop containers (keep them)
docker compose stop

# Start again
docker compose start

# Stop and remove containers + network
docker compose down

# Stop and remove everything including data
docker compose down -v
```

---

## 🔧 Run Manually (Without Compose)

```bash
# Build the image
docker build -t student-app .

# Create network
docker network create student-network

# Start database FIRST
docker run -d \
  --name postgres-db \
  --network student-network \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=mydb \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:15

# Start Flask app SECOND
docker run -d \
  --name student-app \
  --network student-network \
  -p 5000:5000 \
  student-app

# Open browser
# http://localhost:5000         → registration form
# http://localhost:5000/health  → health check
```

---

## 🏗️ Architecture

```
student-network (Docker private network)
├── student-app   → Flask web app
│   └── port 5000:5000 → accessible from browser
└── postgres-db   → PostgreSQL database
    └── port 5432  → internal only, not exposed to outside
        └── postgres-data volume → data persists here
```

---

## 🐙 Docker Compose Syntax Explained

```yaml
services:           # list of containers

  my-container:
    image: nginx        # use image from Docker Hub
    build: .            # OR build from Dockerfile
    container_name: x   # readable name (like --name)
    ports:
      - "8080:80"       # host:container (like -p)
    environment:        # env variables (like -e)
      KEY: value
    volumes:
      - data:/app/data  # mount volume (like -v)
    networks:
      - my-network      # join network (like --network)
    depends_on:
      - db              # start AFTER this service

networks:
  my-network:           # create this network
    driver: bridge

volumes:
  data:                 # create this volume
```

---

## 💾 Part 1: Docker Volumes

Containers lose all data when deleted. Volumes store data outside the container.

### Volume Commands
```bash
docker volume create my-data          # Create a volume
docker volume ls                      # List all volumes
docker volume inspect my-data         # See where it's stored
docker volume rm my-data              # Remove a volume
docker volume prune                   # Remove all unused volumes
```

### Proved Data Persistence
```bash
# Container 1 — write data
docker run --name c1 -v my-data:/app/data grade-app bash
echo "This survives!" > /app/data/test.txt
docker rm -f c1   # delete container

# Container 2 — data still there!
docker run --name c2 -v my-data:/app/data grade-app bash
cat /app/data/test.txt  # → "This survives!" ✅
```

### Bind Mounts — Live Code Editing
```bash
# Map your local folder into container
docker run -v $(pwd):/app flask-app

# Edit code on your machine → changes appear instantly
# No rebuild needed!
```

---

## 🌐 Part 2: Docker Networking

### Network Commands
```bash
docker network ls                          # List all networks
docker network create my-network           # Create custom network
docker network inspect my-network          # Inspect a network
docker network rm my-network               # Remove a network
docker run --network my-network myapp      # Run on specific network
```

### Container DNS — Talk by Name
```bash
# Both containers on same network
docker run -d --name web --network my-network nginx
docker run -d --name client --network my-network ubuntu

# From client — reach web by NAME (not IP!)
ping web          # Docker resolves automatically
curl http://web   # Gets nginx page ✅
```

---

## 💡 Key Lessons Learned

```
1. Volumes → data persists outside container
   Container deleted = data safe in volume ✅

2. Bind mounts → live code editing
   Edit locally → changes appear instantly in container

3. Custom networks → containers talk by name
   No hardcoded IPs — Docker DNS handles everything

4. depends_on → controls start order
   BUT does not wait for app to be READY
   Always add retry logic in your app!

5. Docker Compose → one command for everything
   docker compose up -d  = build + network + volume + start

6. Database should never be exposed outside
   postgres-db → 5432/tcp (internal only)
   student-app → 5000:5000 (browser accessible)
```

---

## 🧹 Cleanup

```bash
# With Compose
docker compose down -v

# Without Compose
docker rm -f student-app postgres-db
docker network rm student-network
docker volume rm postgres-data
```

