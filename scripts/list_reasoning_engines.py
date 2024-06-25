"""Get all reasoning engine in a project."""

from decouple import config
from vertexai.preview import reasoning_engines
import vertexai

PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")
LOCATION = "us-central1" # Only available in us-central1 as per 2024-06-17.

vertexai.init(project=PROJECT_ID, location=LOCATION)
reasoning_engine_list = reasoning_engines.ReasoningEngine.list()
print(reasoning_engine_list)
