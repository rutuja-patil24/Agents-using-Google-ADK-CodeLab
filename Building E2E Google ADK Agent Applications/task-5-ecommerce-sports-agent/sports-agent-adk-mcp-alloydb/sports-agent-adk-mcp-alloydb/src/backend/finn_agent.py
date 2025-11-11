import os, logging
from dotenv import load_dotenv
from fastapi import Request
from google.adk import Agent

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService

from google.adk.tools.toolbox_toolset import ToolboxToolset

from google.adk.models import Gemini
from google.genai import types
import vertexai

load_dotenv()



logger = logging.getLogger(__name__)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION   = os.getenv("GOOGLE_CLOUD_LOCATION")

prompt = """
You're Finn, an AI Sport shopping assistant for GenAI Sports.
# ... (keep your full instruction exactly as you had it) ...
"""

# Shared services
session_service   = InMemorySessionService()
artifacts_service = InMemoryArtifactService()

vertexai.init(project=PROJECT_ID, location=LOCATION)

llm = Gemini(model="gemini-2.5-flash")

async def process_message(message: str, history: list, session_id: str, user_id: str, id_token: str | None = None):
    async def get_auth_token():
        # Accept "Bearer X" or raw id_token
        if id_token and id_token.startswith("Bearer "):
            return id_token[len("Bearer "):]
        return id_token or ""

    toolbox = ToolboxToolset(
        server_url="https://toolbox-736220893495.us-central1.run.app/",
        toolset_name="my-toolset",
        auth_token_getters={"google_signin": get_auth_token},
    )

    agent = Agent(
        name="finn",
        model=llm,
        instruction=prompt,
        tools=[toolbox],
    )

    runner = Runner(
        app_name="finn",
        agent=agent,
        session_service=session_service,
        artifact_service=artifacts_service,
    )

    # ensure session exists
    sess = session_service.sessions.get(session_id)
    if sess is None:
        sess = await session_service.create_session(
            state={}, app_name="finn", user_id=user_id, session_id=session_id
        )

    content = types.Content(role="user", parts=[types.Part(text=message)])


    async def event_stream():
        async for event in runner.run_async(session_id=session_id, user_id=user_id, new_message=content):
            for part in event.content.parts:
                if part.text:
                    yield part.text

    return event_stream
