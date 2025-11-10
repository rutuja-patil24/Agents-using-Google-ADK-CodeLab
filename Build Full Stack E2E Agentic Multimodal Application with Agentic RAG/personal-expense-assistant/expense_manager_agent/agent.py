# expense_manager_agent/agent.py
import os
from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from settings import get_settings

# Tools: plain callables (no FunctionTool wrappers)
from expense_manager_agent.tools import (
    store_receipt_data,
    get_receipt_data_by_image_id,
    search_receipts_by_metadata_filter,
    search_relevant_receipts_by_natural_language_query,
)

# Single callback hook (not "callbacks=[...]", use before_model_callback)
from expense_manager_agent.callbacks import modify_image_data_in_history

# --- Env & settings ---
SETTINGS = get_settings()
os.environ["GOOGLE_CLOUD_PROJECT"] = SETTINGS.GCLOUD_PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = SETTINGS.GCLOUD_LOCATION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"

# --- Load prompt from markdown next to this file ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(CURRENT_DIR, "task_prompt.md")
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    TASK_PROMPT = f.read()

# IMPORTANT: ADK CLI expects this variable name
root_agent = Agent(
    name="expense_manager_agent",
    # Use a model that exists in Vertex us-central1
    # (The codelab's preview model string is retired)
    model="gemini-2.5-flash",
    description=(
        "Personal expense agent to help users track expenses, analyze receipts, "
        "and manage their financial records."
    ),
    instruction=TASK_PROMPT,
    tools=[
        store_receipt_data,
        get_receipt_data_by_image_id,
        search_receipts_by_metadata_filter,
        search_relevant_receipts_by_natural_language_query,
    ],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            thinking_budget=2048,
        )
    ),
    # Use the single before_model_callback hook (not 'callbacks')
    before_model_callback=modify_image_data_in_history,
)
