# pylint: disable=invalid-name
"""
Singleton for the Vertex AI client.
"""

import streamlit as st
from decouple import config
from google import genai

PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")
REGION = "us-central1"

@st.cache_resource
def get_vertex_ai_client():
    """Returns a cached Vertex AI client."""
    return genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=REGION
    )
