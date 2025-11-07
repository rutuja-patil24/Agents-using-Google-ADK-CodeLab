# 🚀 Gemini CLI on ADK — Automated Code Intelligence Agent

This project integrates **Gemini CLI’s non-interactive mode** into a **Google ADK (Agent Development Kit)** agent, enabling powerful automated development workflows such as:

- Intelligent file selection  
- Codebase analysis  
- Automated refactoring  
- Test generation  
- File editing  
- Development command execution  

The result is an agent that behaves like a **developer assistant** capable of understanding your full codebase and executing complex tasks autonomously.

---

# 📽️ **Demo Video**
Watch the full walkthrough of this project here:

🔗 **Demo Video:** https://youtu.be/IK9lCYdF8dQ  

---

# 📌 **Key Features**

### ✅ 1. Gemini CLI Integration  
- Uses Gemini CLI’s non-interactive mode  
- Automatically discovers relevant project files  
- Performs deep code analysis with full context  

### ✅ 2. Automated Software Development Tasks  
- Generate test plans  
- Create unit tests  
- Explain code modules  
- Suggest improvements  
- Refactor code  
- Perform file editing  

### ✅ 3. ADK Integration  
- Exposes Gemini CLI as a tool inside the agent  
- Works inside **ADK Dev UI (FastAPI server)**  
- Also supports **command-line chat mode**  

### ✅ 4. Cloud-Ready Deployment  
- Includes Cloud Build + Cloud Run deployment configs  
- Runs as an interactive multi-agent backend service  

---

# 📂 **Project Structure**

```

gemini-cli-on-adk/
├── app/ # Core ADK agent + Gemini CLI tool
│ ├── agent.py # Main agent with CLI integration
│ ├── server.py # FastAPI dev server for ADK Dev UI
│ └── utils/ # Helper utilities
├── deployment/ # Cloud Run deployment configs
├── notebooks/ # Experiments & testing
├── tests/ # Unit tests generated/meant for automation
├── cloudbuild.yaml # Cloud Build pipeline
├── Dockerfile # Container image build config
├── pyproject.toml # Dependencies (Poetry)
└── README.md

```

# 🛠️ Installation & Setup
### 1️⃣ Clone the Repository
```
git clone https://github.com/your-username/gemini-cli-on-adk.git
cd gemini-cli-on-adk
```
### 2️⃣ Install Dependencies (Poetry)
```
pip install -U pip poetry
poetry install --no-root
```
### 3️⃣ Create a .env File
```
cat > .env << 'EOF'
# Gemini CLI Configuration
GEMINI_CLI_BIN="gemini"
GEMINI_CLI_TIMEOUT="120"
EOF
```
## ▶️ Running the Project
### ✅ Option 1 — Run Agent in CLI Mode
```
poetry run adk run app

```
```
Running agent root_agent, type exit to exit.
```
### ✅ Option 2 — Run ADK Dev UI (FastAPI)

```
poetry run uvicorn app.server:app --host 0.0.0.0 --port 8080

```
Then open Web Preview:

```
https://8080-<your-cloudshell-id>.cloudshell.dev/dev-ui/

```
Select:

- app → this activates the main agent.


### 💬 Example Queries You Can Run

Inside Dev UI or CLI:

✅ Explain Codebase
```
Explain this codebase.
```
✅ Generate Test Plan
```
Generate a test plan for this project.
```
✅ Create Unit Tests
```
Create unit tests for app/agent.py.
```
#🧱 Architecture Overview

```
User
   │
   ▼
ADK Agent (app/agent.py)
   │        \
   │         → Gemini CLI Tool Wrapper
   │                  │
   │                  ▼
   │        Gemini CLI (Non-interactive Mode)
   │                  │
   ▼                  ▼
FastAPI Dev UI   Automated Code Actions
```

### Gemini CLI handles:
- file discovery
- contextual reasoning
- code rewriting

### The agent handles:
- conversation
- tool invocation
- file updates





