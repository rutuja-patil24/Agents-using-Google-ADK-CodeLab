# Currency Agent using ADK with MCP and A2A

This task implements the **Currency Conversion Agent** from Google’s official codelab and demonstrates the integration of:

| Concept | Purpose |
|---------|----------|
| **ADK (Agents Development Kit)** | Framework to build and run AI agents |
| **MCP (Model Context Protocol)** | Provides tools & capabilities to the agent in a structured way |
| **A2A (Agent-to-Agent Protocol)** | Enables invoking the agent through an API and supports interoperability |

🔗 **Codelab Link**: https://codelabs.developers.google.com/codelabs/currency-agent

---

## 🎯 Objective

The goal of this task is to build an AI agent that converts currency values between countries. The agent uses an **MCP tool** to perform the actual conversion logic and exposes this functionality through **A2A**, so other agents or services can interact with it.

---


## 🎥 Demo Video

 **Watch Execution Demo**  : https://youtu.be/rieasZEzFPM
 

---
## 🧠 Theory Behind This Task

### What is MCP (Model Context Protocol)?

MCP is a standard protocol used to **safely expose tools to LLM-based agents**. Think of it like giving the agent plugins—each plugin is a tool with a defined schema. In this project:
- The tool is **`convert_currency`**
- It accepts structured JSON input via schema
- It validates inputs using MCP before execution

This ensures **controlled interaction** between the agent and tools.

---

### What is A2A (Agent-to-Agent)?

The **A2A protocol** lets agents communicate through a standard API interface. For this task:
- The agent runs on a **local A2A server (`adk api_server`)**
- Other agents or scripts can trigger conversion via HTTP calls

---

## 📁 Folder Structure

```
task-2-currency-agent-mcp/
├─ currency_agent/
│ ├─ agent.yaml # Agent configuration
│ ├─ main.py # Agent startup file
│ ├─ mcp/
│ │ ├─ tools.yaml # MCP tool definition
│ │ └─ schemas/ # JSON schema for validation
└─ README.md # Documentation
```
## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
## 2. Configure Environment

Copy .env.example to .env:
```
cp .env.example .env
```
## Run the Currency Agent
Start the A2A Agent Server
```
adk api_server --a2a --port 8002 ./currency_agent
```
## Currency Conversion Demo
1: Run the CLI Demo
```
python ./currency_agent/demo_cli.py --from USD --to EUR --amount 50
```
2: Use cURL Request (HTTP)
```
curl -X POST http://localhost:8002/a2a/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "currency-agent",
    "action": "convert_currency",
    "input": {
      "from": "USD",
      "to": "INR",
      "amount": 10
    }
  }'
```
## ✅ Example Output:
```
{
  "result": {
    "from": "USD",
    "to": "INR",
    "amount": 10,
    "rate": 82.5,
    "converted": 825.0
  }
}
```

