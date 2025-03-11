"""Delete a reasoning engine in a project."""

import vertexai
from decouple import config
from vertexai.preview.reasoning_engines import ReasoningEngine

PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")
vertexai.init(project=PROJECT_ID, location="us-central1")

# Change the Agent Engine ID
REASONING_ENGINE_ID = "1234567890123456"
reasoning_engine = ReasoningEngine(REASONING_ENGINE_ID)
reasoning_engine.delete()
