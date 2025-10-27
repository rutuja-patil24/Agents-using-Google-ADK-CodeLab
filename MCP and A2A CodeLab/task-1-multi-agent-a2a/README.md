# Create a Multi-Agent System with ADK, deploy to Agent Engine, and use A2A

> **Based on** the Google Codelab “Create multi agent system with ADK, deploy in Agent Engine and get started with A2A protocol”.

This repo walks you through:

1) Building an agent (and a small multi-agent workflow) with **Google ADK**  
2) Running it locally in the **ADK Dev UI**  
3) Deploying to **Vertex AI Agent Engine**  
4) Exposing the agent over the **Agent-to-Agent (A2A)** protocol and testing it with `curl`  
5) (Optional) Calling your deployed Agent Engine remotely from Python

---
## 🎥 **Demo Video:**   https://youtu.be/_ChNITXDPeg  
---
## ✨ What you’ll build

- An ADK app (e.g., `image_scoring`) that generates an image and evaluates it — or your own custom agents.
- An A2A server that wraps the ADK app and exposes:
  - `/.well-known/agent.json` (agent card/metadata)
  - `POST /a2a/<agent_id>` (inference endpoint)

---

## 🧰 Prerequisites

- **Google Cloud project** with **billing enabled**
- You have **Owner** (or Admin) on the project
- **APIs enabled**:
  - Vertex AI API: `aiplatform.googleapis.com`
  - Artifact Registry API
  - Cloud Storage
  - Cloud Build
  - Cloud Run (optional, if you host MCP or extra services)
- **Tools**
  - Cloud Shell (or local: Python 3.11/3.12 + `uv`/`pip`, `gcloud`, `gsutil`)
  - `adk` (installed below)

---

## 🗂 Repo layout (suggested)

.
├── image_scoring/ # your ADK app

│ ├── agent.py

│ ├── requirements.txt

│ └── ... (tools, flows, etc.)

├── image_scoring_adk_a2a_server/ # A2A wrapper for the app

│ ├── remote_a2a/

│ │ └── image_scoring/

│ │ └── agent.json # A2A agent card

│ ├── a2a_agent.py

│ └── init.py

├── testclient/

│ └── remote_test.py # (optional) Python client for Agent Engine

└── README.md


> Your folder names can differ; just keep the **A2A “agents dir”** (e.g., `remote_a2a/`) as a real directory on disk.

---

## 🔧 Setup

### 1) Configure project & bucket

```bash
# In Cloud Shell (or local terminal after `gcloud auth login`)
export GOOGLE_CLOUD_PROJECT="<YOUR_PROJECT_ID>"
export GOOGLE_CLOUD_LOCATION="us-central1"    # or your region
export GCS_BUCKET_NAME="<YOUR_UNIQUE_BUCKET>" # e.g. my-adk-bucket-us

gcloud config set project $GOOGLE_CLOUD_PROJECT
gsutil mb -l ${GOOGLE_CLOUD_LOCATION} gs://${GCS_BUCKET_NAME} || true
```

2) Install ADK & Python deps
```
# Install ADK CLI
python3 -m pip install --upgrade "google-adk>=0.6.0" google-genai vertexai google-cloud-aiplatform

# (Optional) if your app uses uv/poetry, install those as well
python3 -m pip install uv
```
▶️ Run locally in the ADK Dev UI

From the repo root (where your image_scoring app folder lives):
```
adk web
```

Open the printed URL (usually http://127.0.0.1:8000/dev-ui/ in Cloud Shell preview).
Select your app (e.g., image_scoring), create a session, and try a prompt.

⬆️ Deploy the app to Vertex AI Agent Engine
```
Export env (used by many code snippets & the ADK tooling):

export GOOGLE_CLOUD_PROJECT="<YOUR_PROJECT_ID>"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GCS_BUCKET_NAME="gs://${GCS_BUCKET_NAME}"      # include gs:// for deploy helpers


Package & deploy (two common paths):

Option A — Use the codelab’s ADK packaging helpers

If your app includes a deploy.py or you’re following the exact codelab steps, run those commands (they upload artifacts to your bucket, then create the Reasoning Engine).
```
🌐 Expose your ADK app over A2A

1) Create a service account (only if you want the A2A server to use SA creds)
```bash
cd image_scoring_adk_a2a_server

gcloud iam service-accounts create adk-a2a-sa \
  --display-name="ADK A2A server"

# Minimal roles for Vertex AI + GCS artifacts (adjust to your needs)
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member="serviceAccount:adk-a2a-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gsutil iam ch serviceAccount:adk-a2a-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com:objectAdmin \
  gs://${GCS_BUCKET_NAME##gs://}

# Create a key in the A2A server folder (the server will read ./key.json)
gcloud iam service-accounts keys create key.json \
  --iam-account adk-a2a-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com
```
2) Start the A2A server

Important: run this from the folder that contains the remote_a2a/ directory.
```
# Ensure env (optional but convenient)
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/key.json"
export GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT
export GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION
export GCS_BUCKET_NAME=${GCS_BUCKET_NAME##gs://}  # plain bucket name for tools
```
# Start the A2A API server on port 8001
```
adk api_server --a2a --port 8001 remote_a2a

```
You should see Uvicorn running on http://127.0.0.1:8001.

3) Verify the agent card
```
curl -s http://localhost:8001/a2a/image_scoring/.well-known/agent.json | jq

5) Send a request
curl -s -X POST http://localhost:8001/a2a/image_scoring \
  -H "Content-Type: application/json" \
  -d '{
    "id": "uuid-123",
    "params": {
      "message": {
        "messageId": "msg-456",
        "parts": [{"text": "Create an image of a flower field"}],
        "role": "user"
      }
    }
  }' | jq

```
You should receive a JSON-RPC response with status.state of running → completed (or useful error if something’s missing).

