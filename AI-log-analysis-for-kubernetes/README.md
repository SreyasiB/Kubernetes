# Kubernetes Log Analysis Agent

## Project Overview

AI-powered Kubernetes troubleshooting assistant using Gemini and GKE.

This project collects logs, events, and telemetry from Kubernetes resources and sends them to Gemini for AI-driven Root Cause Analysis (RCA), troubleshooting guidance, and suggested remediation commands.

---

## Features

- AI-powered Kubernetes troubleshooting
- Works with GKE clusters
- CLI-based workflow
- Uses Gemini for incident analysis
- Supports multiple Kubernetes resources
- Built using free-tier compatible services

---

## Supported Kubernetes Resources

- Pod
- Deployment
- Service
- Ingress
- Node

---

## Architecture

```text
Local Machine / Cloud Shell
        ↓
Python CLI Agent
        ↓
kubectl
        ↓
Collect Logs + Events + Signals
        ↓
Gemini API
        ↓
AI RCA + Suggested Fixes
```

---

## Prerequisites

You need:

- Google Cloud account
- GKE cluster
- kubectl configured
- Python 3.10+
- Enabled APIs:
  - Kubernetes Engine API
  - Generative Language API

---

## 1. Create GKE Cluster
Cloud Shell recommended for easiest setup.

Example:

```bash
#Create the cluster
gcloud container clusters create-auto ai-agent-cluster \
  --region us-central1

#Connect to cluster
gcloud container clusters get-credentials ai-agent-cluster \
  --region us-central1

#Verify:
kubectl get nodes

#Create namespace
kubectl create namespace gke-log-analysis-agent
```

---

## Project Structure

```text
ai-log-analysis-for-kubernetes/
│
├── agent.py
├── prompt.py
├── formatter.py
├── requirements.txt
├── sample-output/
│
├── resources/
│   │
│   ├── __init__.py
│   │
│   ├── shared/
│   │   ├── __init__.py
│   │   ├── command.py
│   │   └── parsers.py
│   │
│   ├── pod/
│   │   ├── __init__.py
│   │   └── collector.py
│   │
│   ├── deployment/
│   │   ├── __init__.py
│   │   └── collector.py
│   │
│   ├── service/
│   │   ├── __init__.py
│   │   └── collector.py
│   │
│   ├── ingress/
│   │   ├── __init__.py
│   │   └── collector.py
│   │
│   └── node/
│       ├── __init__.py
│       └── collector.py
│
├── k8s-manifests/
│   ├── broken-deployment.yaml
│   ├── broken-service.yaml
│   └── broken-ingress.yaml
```

---

## 2. Clone Repository

```bash
git clone https://github.com/SreyasiB/AI-log-analysis-for-kubernetes.git

cd ai-log-analysis-for-kubernetes
```

---

## 3. Create Virtual Environment

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---


# 8. Install Dependencies
```bash
pip install -r requirements.txt
```
---

# 9. Create Gemini API Key

Open the below link with the same email account:

```text
https://aistudio.google.com/
```

Generate an API key.

---

# 10. Set up environment variable
```bash
export GEMINI_API_KEY=YOUR_API_KEY
```

IMPORTANT:
- Never commit API Key
- Never hardcode secrets

---

## Run The Agent

#### Analyze Pod

```bash
python agent.py \
  --resource pod \
  --name POD_NAME \
  --namespace NAMESPACE
```

---

#### Analyze Deployment

```bash
python agent.py \
  --resource deployment \
  --name DEPLOYMENT_NAME \
  --namespace NAMESPACE
```

---

#### Analyze Service

```bash
python agent.py \
  --resource service \
  --name SERVICE_NAME \
  --namespace NAMESPACE
```

---

#### Analyze Ingress

```bash
python agent.py \
  --resource ingress \
  --name INGRESS_NAME \
  --namespace NAMESPACE
```

---

#### Analyze Node

```bash
python agent.py \
  --resource node \
  --name NODE_NAME
```

---

# Common Issues

| Issue | Example Error | Fix |
|---|---|---|
| Gemini API quota exceeded | `429 RESOURCE_EXHAUSTED` | Enable billing, wait for quota reset, or reduce requests |
| Gemini model not found | `404 model not found` | Update to a supported model like `gemini-2.5-flash` |
| kubectl not connected to cluster | `connection refused` or permission errors | Re-run `gcloud container clusters get-credentials` |
| Virtual environment not activated | `ModuleNotFoundError` | Run `source venv/bin/activate` |
| Missing Python dependencies | `No module named ...` | Run `pip install -r requirements.txt` |
| Missing API key | `GEMINI_API_KEY environment variable not set` | Set the API key as environment variable |
| Unsupported resource type | `Unsupported resource` | Use supported resources only |
| Incorrect namespace | `NotFound` errors | Verify namespace using `kubectl get ns` |





