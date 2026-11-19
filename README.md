# Kubernetes Network Troubleshooting Assignment

## 1. Project Overview

This project demonstrates Kubernetes networking and troubleshooting using a local Kind cluster.

Application communication flow:

`Client → Frontend → Backend`

**Environment:**
- OS: Windows 11 with Ubuntu 24.04 on WSL2
- Container runtime: Docker Engine
- Kubernetes: Kind
- Kubernetes version: v1.37.0
- Container images: Python 3.12-slim

## 2. Application Architecture

Three workloads were deployed:

- **Client:** Sends HTTP requests to the frontend.
- **Frontend:** Receives client requests and communicates with the backend.
- **Backend:** Returns a JSON health response.

Kubernetes Services:
- Frontend: Port 8080
- Backend: Port 5000

## 3. Initial Connectivity Verification

Initially, both communication paths worked:

- Client → Frontend: SUCCESS
- Frontend → Backend: SUCCESS

The client received:

```json
{
  "service": "frontend",
  "backend_response": {
    "service": "backend",
    "status": "healthy",
    "message": "Hello from Backend!"
  }
}
```

## 4. Intentional Networking Failure

An incorrect Service selector was introduced.

Original backend Service selector:

```yaml
selector:
  app: backend
```

Modified selector:

```yaml
selector:
  app: backend-broken
```

The backend Pod retained its original label:

```yaml
app: backend
```

## 5. Symptom

Frontend-to-backend communication failed.

The client received:

`HTTP Error 502: Bad Gateway`

The backend Pod continued running with status `1/1 Running`.

## 6. Investigation

The following commands were used:

```bash
kubectl get pods -o wide
kubectl get svc
kubectl get pods --show-labels
kubectl describe svc backend
kubectl get endpointslices -l kubernetes.io/service-name=backend
kubectl logs deployment/frontend
```

## 7. Observations

- Backend Pod was healthy.
- Backend Service existed.
- Service selector did not match the backend Pod label.
- Backend EndpointSlice had no ready endpoint.
- Frontend could not connect to the backend.

## 8. Root Cause

The backend Service had an incorrect selector (`app: backend-broken`), while the backend Pod had the label `app: backend`.

Because of this mismatch, Kubernetes could not associate the Service with the backend Pod.

The Service therefore had no ready backend endpoint.

## 9. Resolution

Restored the correct selector:

```bash
kubectl patch service backend -p '{"spec":{"selector":{"app":"backend"}}}'
```

The backend EndpointSlice then showed the backend Pod IP and port 5000.

## 10. Final Verification

Executed:

```bash
kubectl exec deployment/client -- python -c 'import urllib.request; print(urllib.request.urlopen("http://frontend:8080", timeout=5).read().decode())'
```

The expected backend health response was received successfully.

Final result:

- Client → Frontend: SUCCESS
- Frontend → Backend: SUCCESS
- Backend Pod: Running
- Backend Service Endpoint: Restored

## 11. Evidence

The `evidence/` directory contains baseline, failure and recovery outputs.

## 12. Conclusion

This assignment demonstrates Kubernetes Services, Pod labels, Service selectors, EndpointSlices, service discovery and application connectivity troubleshooting.

The issue was resolved by identifying and correcting a Service selector mismatch.

Troubleshooting methodology:

**Observe → Investigate → Identify → Fix → Verify**
