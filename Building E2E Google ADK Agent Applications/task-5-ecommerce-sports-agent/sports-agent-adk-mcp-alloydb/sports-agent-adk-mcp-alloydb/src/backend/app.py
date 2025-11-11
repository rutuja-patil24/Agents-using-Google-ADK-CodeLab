# src/backend/app.py
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

async def health(request):
    return JSONResponse({"status": "healthy"})

async def root(request):
    return PlainTextResponse("OK")

async def test(request):
    return JSONResponse({"status": "ok", "message": "Backend is running"})

routes = [
    Route("/", root, methods=["GET"]),
    Route("/health", health, methods=["GET"]),
    Route("/test", test, methods=["GET"]),
]

app = Starlette(debug=False, routes=routes)

# --- Keep your ADK code below, but don't wire /chat until deps are ready ---
# from dotenv import load_dotenv
# from google.adk import Agent
# from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService
# from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
# from google.adk.tools.toolbox_toolset import ToolboxToolset
# from google.adk.models import Gemini
# from google.genai import types
# import vertexai, os, logging
# ... (leave as-is for later)
