"""
Agent Engine application wrapper.
This file prepares the agent for deployment to Vertex AI Agent Engine.
"""

from vertexai import agent_engines
from code_review_assistant.agent import root_agent

# Wrap the agent in an AdkApp object for Agent Engine deployment
app = agent_engines.AdkApp(agent=root_agent, enable_tracing=True)