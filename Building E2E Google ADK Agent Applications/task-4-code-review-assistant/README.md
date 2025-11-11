# Code Review Assistant Agent  
## Building a Production AI Code Review Assistant with Google ADK  

This folder contains my implementation of the codelab **“Building a Production AI Code Review Assistant with Google ADK”** which guides you through building a full-stack multi-agent system for reviewing and fixing Python code. :contentReference[oaicite:1]{index=1}

---
## 📹 Demo Video

🎥 Demo Walkthrough: https://youtu.be/hHN-l7o4r7o

---

## 📌 What This Project Does  
- Parses and analyses Python code structure using AST tools. :contentReference[oaicite:2]{index=2}  
- Runs style checks (e.g., PEP 8 compliance) and test execution to detect failures. :contentReference[oaicite:3]{index=3}  
- Synthesises actionable feedback and optionally suggests/fixes code issues. :contentReference[oaicite:4]{index=4}  
- Deploys the agent via cloud infrastructure (Local, Cloud Run or Agent Engine) with session persistence, telemetry, and production-grade architecture. :contentReference[oaicite:5]{index=5}  

---

## 🗂 Folder Structure  
```
task-4-code-review-assistant/
├── agent.py ← Root ADK agent definition
├── code_review_assistant/ ← Main Python package
│ ├── tools.py ← Custom tools: AST analysis, style checker, test runner
│ ├── sub_agents/ ← Sub-agents for pipeline stages
│ ├── config.py ← Environment & model configuration
│ └── …
├── requirements.txt ← Python dependencies
├── .env.example ← Environment variable template
├── deploy.sh ← Deployment script for Cloud Run / Agent Engine
├── tests/ ← Unit/integration tests
└── README.md ← (this file)
```

---

## 🔧 Setup & Run Instructions  
1. **Clone the repository / Navigate to this folder**
   
   ```bash
   git clone https://github.com/YOUR_USERNAME/adk-agents-assignment.git  
   cd adk-agents-assignment/task-4-code-review-assistant
   ```
2. Create and activate a virtual environment
   ```
   python3 -m venv .venv  
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt  
   pip install -e .
   ```
4. Configure environment
   ```
   cp .env.example .env  
    # Then edit .env and set:
    # GOOGLE_CLOUD_PROJECT=your-project-id
    # GOOGLE_CLOUD_LOCATION=us-central1
    # GOOGLE_GENAI_USE_VERTEXAI=TRUE
   ```
5. Local test
    ```
    adk web code_review_assistant  
    # Navigate to http://localhost:8000 in your browser
    ```

    
     


   

   

