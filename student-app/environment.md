## Overview

This project follows the [12-Factor App](https://12factor.net/) methodology — configuration is stored in the environment, never hardcoded in the application code or Docker image.

| Before (Week 7) | After (Week 8) |
|---|---|
| DB_PASSWORD hardcoded in YAML | DB_PASSWORD stored in Kubernetes Secret |
| Password visible to anyone reading the file | Password hidden — shows only as byte count |
| To change config you must redeploy the app | Change ConfigMap or Secret, restart pods only |
| Secret accidentally pushed to GitHub | secret.yml excluded via .gitignore |

---

## Files

```
student-app/k8s/
├── configmap.yml     # Non-sensitive app configuration — safe to push
├── secret.yml        # Sensitive credentials — NOT on GitHub (.gitignore)
├── deployment.yml    # App deployment referencing both above
└── service.yml       # NodePort service exposing the app
```

---

## How It Works

When a Pod starts, Kubernetes automatically injects all values from ConfigMap and Secret as environment variables inside the container. The app reads them with `os.environ.get()` in Python.

```
configmap.yml + secret.yml
         |
     envFrom in deployment.yml
         |
Pod starts → Kubernetes injects all values as environment variables
         |
app.py reads with os.environ.get()
```

---

## ConfigMap — `configmap.yml`

Stores non-sensitive application configuration. Safe to push to GitHub.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: student-app-config
data:
  APP_NAME: student-app
  APP_PORT: '5000'
  DATABASE_HOST: localhost
  LOG_LEVEL: info
```

| Key | Value | Purpose |
|---|---|---|
| APP_NAME | student-app | Application identifier |
| APP_PORT | 5000 | Port the Flask app listens on |
| DATABASE_HOST | localhost | PostgreSQL host address |
| LOG_LEVEL | info | Application logging level |

```bash
kubectl apply -f student-app/k8s/configmap.yml
kubectl describe configmap student-app-config
```

---

## Secret — `secret.yml`

Stores sensitive credentials. **This file is NOT on GitHub.**

> ⚠️ If you clone this repository on a new machine, you must create `secret.yml` manually before deploying. The app will crash without it.

Create your `secret.yml` locally using this template:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: student-app-secret
type: Opaque
stringData:
  DB_PASSWORD: your_postgres_password_here
  DB_USER: your_postgres_user_here
  DB_NAME: your_database_name_here
  API_KEY: your_api_key_here
```

| Key | Purpose |
|---|---|
| DB_PASSWORD | PostgreSQL database password |
| DB_USER | PostgreSQL database username |
| DB_NAME | PostgreSQL database name |
| API_KEY | External API authentication key |

```bash
kubectl apply -f student-app/k8s/secret.yml

# Verify — shows key names but NOT values (correct behaviour)
kubectl describe secret student-app-secret
```

---

## Deployment Order

Always apply in this exact order. Deployment needs ConfigMap and Secret to exist before it starts.

```bash
# 1. Secret first
kubectl apply -f student-app/k8s/secret.yml

# 2. ConfigMap second
kubectl apply -f student-app/k8s/configmap.yml

# 3. Deployment last
kubectl apply -f student-app/k8s/deployment.yml

# 4. Service (any time)
kubectl apply -f student-app/k8s/service.yml
```

| Step | File | Why |
|---|---|---|
| 1 | secret.yml | Must exist before Deployment starts |
| 2 | configmap.yml | Must exist before Deployment starts |
| 3 | deployment.yml | Reads from both via envFrom on pod startup |
| 4 | service.yml | Exposes running pods — any time |

---

## Verify

```bash
# Check ConfigMap values
kubectl describe configmap student-app-config

# Check Secret exists (values show as byte count — this is correct)
kubectl describe secret student-app-secret

# Check pods are Running
kubectl get pods

# Verify env variables are injected inside the pod
kubectl exec -it <pod-name> -- env | grep -E "APP_NAME|APP_PORT|DB_PASSWORD|API_KEY"

# Check logs if something is wrong
kubectl logs <pod-name>
```

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| CrashLoopBackOff — password authentication failed | DB_PASSWORD in Secret does not match PostgreSQL password | Check postgres deployment with `kubectl describe deployment postgres-db` and update Secret to match |
| Error: configmap not found | ConfigMap applied after Deployment or wrong name | Apply configmap.yml first, check metadata.name matches configMapRef |
| Error: secret not found | Secret not created or wrong name | Create secret.yml and apply it |
| Pod running but app cannot read variables | envFrom missing or wrong indentation | Check deployment YAML — envFrom must be under container spec |

---

## Quick Start — New Machine

```bash
# 1. Start Minikube
minikube start --driver=docker

# 2. Deploy PostgreSQL
kubectl apply -f postgres/k8s/deployment.yml
kubectl apply -f postgres/k8s/service.yml

# 3. Create secret.yml locally (use template above)

# 4. Apply in order
kubectl apply -f student-app/k8s/secret.yml
kubectl apply -f student-app/k8s/configmap.yml
kubectl apply -f student-app/k8s/deployment.yml
kubectl apply -f student-app/k8s/service.yml

# 5. Get app URL
minikube service student-app-service --url
```

---

## Security Notes

- `secret.yml` is in `.gitignore` and must **never** be pushed to GitHub
- If `secret.yml` is accidentally pushed — rotate all credentials immediately, assume they are compromised
- Never hardcode passwords in `deployment.yml`, `app.py` or any file that goes to GitHub
- Use `git rm --cached secret.yml` to remove it from Git tracking if accidentally staged
- Kubernetes Secrets are base64 encoded not encrypted — anyone with kubectl access can decode them
- For production use HashiCorp Vault or AWS Secrets Manager instead of Kubernetes Secrets

---

