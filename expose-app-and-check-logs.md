Expose App and Check Logs
**Kubernetes Basics | DevOps Roadmap
---

## 🎯 Goal
Learn how to expose your app so it can be accessed from browser, and how to read logs for debugging.

---

## 🌐 Why We Need to Expose an App

By default Pods are only accessible **inside** the Kubernetes cluster. Nobody outside can reach them. We need to create a **Service** to expose the app so you can access it in your browser.

```
Without Service:
Browser → ❌ cannot reach Pod directly

With Service:
Browser → Service → Pod ✅
```

---

## 📡 Three Types of Services — Simply Explained

### 1. ClusterIP — Internal Only
```
Think of it like an internal office phone number
Only people INSIDE the office can call it
Nobody outside the office can reach it

Used for: databases, internal services
Example: postgres-db Service
         only student-app Pod can talk to it
         you cannot open it in browser ❌
```

### 2. NodePort — Accessible from Outside
```
Think of it like a public phone number
Anyone outside CAN call it
But they need to know the exact port number

Used for: learning and local development
Example: student-app-service
         you can open it in browser ✅
         via port 30000
```

### 3. LoadBalancer — Cloud Production
```
Think of it like a receptionist at a big company
Has a real public address (IP)
Automatically distributes traffic to many Pods
Anyone in the world can reach it

Used for: real production apps on AWS, Azure, GCP
Example: yourapp.com → LoadBalancer → Pods
         we use this in Week 9 (AWS) ⏳
```

---

## 📊 Service Types Comparison

| Type | Who Can Access | Used For | Example |
|---|---|---|---|
| ClusterIP | Inside cluster only | Databases, internal services | postgres-db |
| NodePort | Outside via specific port | Local learning | student-app-service |
| LoadBalancer | Anyone in the world | Real production | yourapp.com |

---

## 🔄 How Traffic Flows

```
NodePort Example:
─────────────────
Browser (Windows)
    ↓
http://127.0.0.1:30000
    ↓
student-app-service (NodePort)
Fixed address, always available
    ↓
student-app Pod (Flask :5000)
Temporary, IP changes on restart
    ↓
Response back to browser ✅


ClusterIP Example:
──────────────────
student-app Pod
    ↓
postgres-db (ClusterIP :5432)
Internal hostname only
    ↓
postgres-db Pod
    ↓
Data returned to student-app ✅
```

---

## 🛠️ Two Ways to Create a Service

### Way 1 — YAML File (Professional ✅)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: student-app-service
spec:
  type: NodePort
  selector:
    app: student-app
  ports:
  - port: 80
    targetPort: 5000
    nodePort: 30000      ← you choose the port
```

```bash
kubectl apply -f student-service.yml
```

### Way 2 — kubectl expose (Quick, for testing only)
```bash
kubectl expose deployment student-app --type=NodePort --port=5000
```

---

## 🔍 Difference Between Two Ways

| | YAML Way | expose Way |
|---|---|---|
| Port | You choose (30000) | Kubernetes chooses randomly |
| Name | You choose | Same as deployment name |
| Reusable | Yes, saved in file | No, just a command |
| Professional | ✅ Yes | ❌ No |

---

## 📋 Service Commands

```bash
# Check all services
kubectl get services

# Full details of a service
kubectl describe service student-app-service

# Create service via expose (testing only)
kubectl expose deployment student-app --type=NodePort --port=5000

# Delete a service
kubectl delete service student-app-service

# Get app URL
minikube service student-app-service --url
```

---

## 🔎 Reading kubectl describe service

```
Name:       student-app-service  → Service name
Type:       NodePort             → accessible from browser
IP:         10.109.24.127        → Service fixed IP

Selector:   app=student-app      → finds Pods with this label
                                   forwards traffic to them

Port:       80                   → Service listens here
TargetPort: 5000                 → forwards to Flask app
NodePort:   30000                → port you visit in browser

Endpoints:  10.244.0.71:5000     → actual Pod IP
                                   changes when Pod restarts
                                   Service finds it automatically ✅
```

---

## 📝 Log Commands

```bash
# See all logs
kubectl logs <pod-name>

# Follow logs in real time
kubectl logs <pod-name> -f

# See last 50 lines only
kubectl logs <pod-name> --tail=50
```

---

## 🔎 Reading Logs

```
Database ready!                         → connected to postgres ✅
* Serving Flask app 'app'               → Flask started ✅
* Running on http://10.244.0.71:5000    → Pod IP address

GET / HTTP/1.1" 200     → someone visited homepage ✅
POST /register HTTP/1.1" 302 → someone submitted a form ✅
GET /favicon.ico" 404   → browser looked for icon, harmless ✅
```

---

## 📊 HTTP Methods and Status Codes

### Methods
| Method | Meaning | Example |
|---|---|---|
| GET | Reading a page | Opening homepage |
| POST | Sending data | Submitting a form |

### Status Codes
| Code | Meaning |
|---|---|
| 200 | OK, everything worked ✅ |
| 302 | Redirect (go to another page) |
| 404 | Page not found ❌ |
| 500 | Server error ❌ |

---

## 🐛 Debugging with Logs

```
Something went wrong?
        ↓
Step 1: kubectl get pods
        check if Pod is Running

Step 2: kubectl logs <pod-name>
        see what error message appears

Step 3: kubectl logs <pod-name> -f
        follow logs in real time
        reproduce the error
        see exact line that fails

Step 4: kubectl describe pod <pod-name>
        check Events section
        see what Kubernetes did

