# 🏃‍♂️🛍️ Sports Shop Agent — ADK Agent with MCP Toolbox & AlloyDB

This repository demonstrates how to build and deploy **Finn — a Sports Shop AI Assistant** using:

- **Google Agent Development Kit (ADK)**
- **MCP Toolbox for Databases**
- **AlloyDB for PostgreSQL (AI-enabled)**
- **Cloud Run (backend + frontend)**

Finn can help users:

- Search sports products  
- View product details  
- Add/remove items from the shopping list  
- Find nearby stores  
- Place orders and update delivery methods  
- Check order status  

---

## 🚀 Overview

The Sports Shop Agent uses:

- **ADK** for conversational orchestration & tool calling  
- **MCP Toolbox** to expose SQL tools  
- **AlloyDB** as the backend store of products, stores, and orders  
- **React frontend** deployed on Cloud Run  

---

## 📹 Demo Video

🎥 Add your video link here.

---

## 🧭 Architecture Summary

```

User Query
      ↓
Finn — Sports Shop Agent (ADK)
      ↓
MCP Toolbox (tools.yaml)
      ↓
AlloyDB (sports store DB)
      ↓
Results → JSON → Conversational Response

```

---

## 🧩 Project Structure


```

sports-agent/
├── data/
│   └── store_backup.sql            # Sample sports store data
├── src/
│   ├── backend/                    # ADK agent backend (Finn)
│   │   ├── finn_agent.py
│   │   ├── Dockerfile
│   │   └── ...
│   ├── frontend/                   # React UI for the chat application
│   │   ├── src/
│   │   │   ├── pages/Home.jsx
│   │   │   ├── components/GoogleSignInButton.jsx
│   │   │   └── ...
│   ├── toolbox/                    # MCP Toolbox config
│   │   └── tools.yaml
└── README.md

```

---

# ⚙️ Setup Instructions (Google Cloud Shell)

### 0 — Clone the Repository

```bash
git clone https://github.com/mtoscano84/sports-agent-adk-mcp-alloydb.git
cd sports-agent-adk-mcp-alloydb
```

### 1 — Authenticate & Enable Required APIs

```
gcloud auth login
gcloud auth application-default login

export PROJECT_ID="<YOUR_PROJECT_ID>"
gcloud config set project $PROJECT_ID

gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  iam.googleapis.com \
  secretmanager.googleapis.com \
  alloydb.googleapis.com \
  aiplatform.googleapis.com

```

### 2 — Create AlloyDB Cluster, Instance, and Database

```
gcloud alloydb clusters create sports-cluster \
  --region=us-central1 \
  --network=default
```
```
gcloud alloydb instances create sports-primary \
  --cluster=sports-cluster \
  --region=us-central1 \
  --cpu-count=2 \
  --memory-size=8GB
```

### 3 — Load Sample Store Data
```
psql -h 127.0.0.1 -U postgres -d store -f data/store_backup.sql
```

## 📦 MCP Toolbox Deployment

### 4 — Configure tools.yaml

```
project: <PROJECT_ID>
region: us-central1
instance: sports-primary
database: store
```

### 5 - Deploy MCP Toolbox to Cloud Run

```
cd src/toolbox

gcloud iam service-accounts create toolbox-identity

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/alloydb.client"

gcloud secrets create tools --data-file=tools.yaml

```
```
gcloud run deploy toolbox \
  --image us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest \
  --region us-central1 \
  --service-account toolbox-identity \
  --set-secrets="/app/tools.yaml=tools:latest" \
  --args="--tools_file=/app/tools.yaml","--address=0.0.0.0","--port=8080" \
  --allow-unauthenticated
```
```
export MCP_TOOLBOX_URL=$(gcloud run services describe toolbox \
  --region us-central1 --format="value(status.url)")
```
## 🤖 Deploy ADK Agent Backend (Finn)

### 6 - Configure the Agent

```
TOOLBOX_URL = "<YOUR_TOOLBOX_URL>"
```

### 7 - Build & Deploy Backend

```
gcloud artifacts repositories create finn-agent-images \
  --repository-format=docker \
  --location=us-central1
```
```
gcloud builds submit src/backend/ \
  --tag us-central1-docker.pkg.dev/$PROJECT_ID/finn-agent-images/finn-agent
```
```
gcloud run deploy finn-agent \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/finn-agent-images/finn-agent \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=TRUE,MCP_TOOLBOX_URL=$MCP_TOOLBOX_URL"
```
```
export FINN_URL="<YOUR_FINN_AGENT_URL>"
```
## 🎨 Deploy the Frontend

### 8 - Update Frontend Config

Home.jsx

Replace the agent URL:

```
const AGENT_URL = "<YOUR_FINN_AGENT_URL>";
```
GoogleSignInButton.jsx

Replace your OAuth client ID:
```
client_id: "<YOUR_OAUTH_CLIENT_ID>"
```

### 9 - Build & Deploy the Frontend

```

gcloud artifacts repositories create finn-frontend-images \
  --repository-format=docker \
  --location=us-central1
```
```
gcloud builds submit src/frontend/ \
  --tag us-central1-docker.pkg.dev/$PROJECT_ID/finn-frontend-images/finn-frontend
```
```
gcloud run deploy finn-frontend \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/finn-frontend-images/finn-frontend \
  --region us-central1 \
  --allow-unauthenticated
```



---

## 🧪 Test the Agent

Try the following queries:

“Hello Finn!”

“Find me trail running shoes.”

“Show details for Ultra Glide.”

“Add Ultra Glide size 40 to my shopping list.”

“Place an order for my shopping list.”

“Check my order status.”

“Update my delivery method to Express Delivery.”

---


