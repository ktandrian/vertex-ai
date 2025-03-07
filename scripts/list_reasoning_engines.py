"""Get all reasoning engines in a project."""

import vertexai
from decouple import config
from vertexai.preview.reasoning_engines import ReasoningEngine

PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")
LOCATION = "us-central1" # Only available in us-central1 as per 2024-06-17.

vertexai.init(project=PROJECT_ID, location=LOCATION)
reasoning_engine_list = ReasoningEngine.list()
print(reasoning_engine_list)
