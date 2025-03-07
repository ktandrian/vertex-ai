"""Delete a reasoning engine in a project."""

import vertexai
from decouple import config
from vertexai.preview.reasoning_engines import ReasoningEngine

PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")
vertexai.init(project=PROJECT_ID, location="us-central1")

# TODO: change the Agent Engine ID
reasoning_engine_id = "1234567890123456"
reasoning_engine = ReasoningEngine(reasoning_engine_id)
reasoning_engine.delete()
