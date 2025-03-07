# pylint: disable=invalid-name
"""
The homepage of the Streamlit app, showing menus and links.
"""

import streamlit as st


def home_page():
    """The homepage of the Streamlit app."""
    st.set_page_config(page_title="Vertex AI")
    st.title("Google Cloud | Generative AI")
    st.markdown("This is a demo application for Google Cloud Vertex AI.")

    st.header("Demos")
    st.markdown("Select a demo page below to get started.")
    st.page_link("app/Currency.py", label="Exchange Rate", icon="💰")
    st.page_link("app/HotelTags.py", label="Hotel Tags", icon="🏷️")
    st.page_link("app/TripPlanner.py", label="Trip Planner", icon="✈️")

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

st.logo("./static/google-cloud.png")
pg = st.navigation({
    "Welcome": [
        st.Page(home_page, title="Home", icon="🏠")
    ],
    "English Demos": [
        st.Page("app/Currency.py", title="Exchange Rate", icon="💰"),
        st.Page("app/TripPlanner.py", title="Trip Planner", icon= "✈️")
    ],
    "Japanese Demos": [
        st.Page("app/HotelTags.py", title="ホテルタグ (Hotel Tags)", icon="🏷️"),
    ]
})
pg.run()
