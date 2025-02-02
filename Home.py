# pylint: disable=invalid-name
"""
The homepage of the Streamlit app, showing menus and links.
"""

import streamlit as st

st.set_page_config(page_title="Vertex AI")
st.logo("./static/google-cloud.png")
st.title("Google Cloud | Generative AI")
st.markdown("This is a demo application for Google Cloud Vertex AI.")

st.header("Demos")
st.markdown("Select a demo page below to get started.")
st.page_link("pages/TanyaPajak.py", label="TanyaPajak", icon="🔎")
st.page_link("pages/TripPlanner.py", label="TripPlanner", icon="✈️")

st.header("Learn More")
st.markdown("Learn more about Vertex AI:")
st.page_link("https://cloud.google.com/vertex-ai", label="About Vertex AI", icon="☁️")
st.page_link(
    "https://cloud.google.com/vertex-ai/docs/", label="Vertex AI Docs", icon="📖"
)
st.page_link(
    "https://cloud.google.com/vertex-ai/pricing", label="Vertex AI Pricing", icon="💰"
)
st.page_link(
    "https://ai.google.dev",
    label="Build with Gemini | Google AI for Developers",
    icon="💡",
)

st.divider()
st.markdown("2024 © KenTandrian. All rights reserved.")
