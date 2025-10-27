# 🍔🍕 Purchasing Concierge – Multi-Agent A2A System using Google ADK

This project implements a **multi-agent system** using the **Google Agent Developer Kit (ADK)** and **A2A (Agent-to-Agent) Protocol**. The **Purchasing Concierge** assists users in ordering from multiple remote seller agents such as burger and pizza sellers. The orchestrating agent is deployed to **Vertex AI Agent Engine**, while seller agents run on **Cloud Run**.

---
## 🎥 Demo Video : https://youtu.be/Resq17HiziE

---
## 🚀 Features

✅ Multi-Agent Orchestration using Google ADK  
✅ A2A Remote Agent Communication Protocol  
✅ Burger & Pizza Remote Seller Agents  
✅ Deployment to Google Cloud Run + Vertex AI Agent Engine  
✅ Interactive Gradio-based UI  
✅ Test script to validate A2A connectivity  

---

## 🏗️ Architecture
```
               ┌────────────────────────┐
               │ Purchasing Concierge   │
               │ (Agent Engine)         │
               └─────────┬──────────────┘
                         │ A2A Protocol
    ┌────────────────────┼───────────────────────┐
    │                                            │

    │                                            │
┌───────────────┐                     ┌────────────────┐
│ Burger Agent │                        │ Pizza Agent │
 │ Cloud Run │                           │ Cloud Run │
└───────────────┘                     └────────────────┘

```


---

## 📂 Project Structure
```
purchasing-concierge-a2a/
│── burger_seller_agent/ # Remote Burger Agent
│── pizza_seller_agent/ # Remote Pizza Agent
│── purchasing_concierge/ # Orchestrator logic using ADK
│── purchasing_concierge_ui.py # Chat UI (Gradio)
│── deploy_to_agent_engine.py # Deployment to Vertex AI Agent Engine
│── test_agent_engine.sh # Connectivity test script
│── requirements.txt
│── .env # Environment config
│── README.md
```


---

## ✅ Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.11+   |
| Google Cloud Project |
| Vertex AI Enabled |
| Cloud Run Enabled |
| A2A SDK + Google ADK Installed |

---

## 🔧 Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/alphinside/purchasing-concierge-intro-a2a-codelab-starter.git purchasing-concierge-a2a
cd purchasing-concierge-a2a

```

### 2. Create Virtual Environment
```
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```
### 3. Configure Environment Variables
```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
BURGER_SELLER_AGENT_URL=https://burger-agent-XXXX.run.app
PIZZA_SELLER_AGENT_URL=https://pizza-agent-XXXX.run.app
AGENT_ENGINE_RESOURCE_NAME=projects/XXX/locations/us-central1/reasoningEngines/XXXX
```

### Deploy Purchasing Concierge to Agent Engine

```
uv run deploy_to_agent_engine.py
```

#### This creates a Vertex AI Agent Engine and outputs the engine ID.
### ✅ Add it to .env:

```
AGENT_ENGINE_RESOURCE_NAME=projects/.../reasoningEngines/...
```
### ✅ Test Remote Calls

### Before starting UI:
```
bash test_agent_engine.sh
```
### 💬 Launch Chat UI
```
uv run purchasing_concierge_ui.py
```
### Open: http://localhost:8080
### Click predefined prompts or chat with the agent! 🎉


