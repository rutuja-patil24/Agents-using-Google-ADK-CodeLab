# 🚀 Personal Expense Assistant — Multimodal AI Agent  
### Gemini + ADK + Firestore + Cloud Run

A fully multimodal **Personal Expense Manager** built using **Google’s Agent Development Kit (ADK)**, **Gemini models**, **Firestore**, **Vector Search**, and **Cloud Run**.  
The assistant extracts structured data from **receipt images**, stores them in Firestore, and allows natural-language queries about your spending.

---

## 🎥 Demo Video

👉 **Watch the full project demo:**  
https://youtu.be/-7UO6zZYVWM

---
## ✅ Features

- 📸 Extract structured data from receipt images  
- 💬 Natural-language expense queries  
- 🔎 Vector search on receipt descriptions  
- 🗂 Store metadata + images in Firestore + GCS  
- 🧠 Gemini + ADK agent with custom tools  
- 🌐 One-container deployment to Cloud Run  
- 🖥 Gradio frontend + FastAPI backend  

---

## 📁 Project Structure

```
personal-expense-assistant/
│
├── backend.py
├── frontend.py
├── expense_manager_agent/
│ ├── agent.py
│ ├── callbacks.py
│ ├── tools.py
│ ├── task_prompt.md
│
├── settings.yaml
├── supervisord.conf
├── Dockerfile
└── README.md

```


---

## 🧠 Architecture Overview
```

User (Web/Mobile)
        │
        ▼
┌──────────────────────────────────┐
│        Gradio Frontend           │
└──────────────────────────────────┘
        │  (HTTP)
        ▼
┌──────────────────────────────────┐
│      FastAPI Backend             │
│   - Manages chat requests        │
│   - Sends images + text to ADK   │
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│      ADK Agent (Gemini)          │
│  - Extracts receipt data         │
│  - Calls Firestore/GCS tools     │
│  - Executes search queries       │
└──────────────────────────────────┘
        │
 ┌──────┴───────────────┐
 │                      │
 ▼                      ▼
GCS (Images)      Firestore (Metadata + Vectors)

```

## ⚙️ Prerequisites

- Google Cloud account  
- Billing enabled  
- Firestore in Native Mode (`us-central1`)  
- Cloud Run + Cloud Build APIs enabled  
- Python 3.12 via `uv`  
- Cloud Shell recommended  

---


## 🛠 Installation (Cloud Shell)

### 1. Clone repository
```
git clone https://github.com/alphinside/personal-expense-assistant-adk-codelab-starter.git personal-expense-assistant
cd personal-expense-assistant
```
### 2. Install UV
```
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env
uv python install 3.12
```
### 3. Install project dependencies
```
3. Install project dependencies
```
## 📦 Configure Firestore + GCS

### 1. Enable services

```
gcloud services enable \
  aiplatform.googleapis.com \
  firestore.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com
```
### 2. Create GCS bucket for images

```
PROJECT_ID=$(gcloud config get-value project)
BUCKET="personal-expense-assistant-$PROJECT_ID"
gsutil mb -l us-central1 gs://$BUCKET
```
### 3. Create Firestore composite indexes

```
gcloud firestore indexes composite create \
  --collection-group="personal-expense-assistant-receipts" \
  --field-config field-path=total_amount,order=ASCENDING \
  --field-config field-path=transaction_time,order=ASCENDING \
  --field-config field-path=_name,order=ASCENDING
```
## ▶️ Run Agent Locally

```
uv run adk run expense_manager_agent
```

## 🌐 Deploy to Cloud Run

```
gcloud run deploy personal-expense-assistant \
  --source . \
  --port=8080 \
  --allow-unauthenticated \
  --env-vars-file=settings.yaml \
  --memory 1024Mi \
  --region us-central1
```

## 🧪 Example Queries

- “Show all receipts from Starbucks.”

- “Find purchases above $100.”

- “Show everything I bought last weekend.”

- “Search receipts that include chicken.”




