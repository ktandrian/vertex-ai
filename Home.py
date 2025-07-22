# pylint: disable=invalid-name
"""
The homepage of the Streamlit app, showing menus and links.
"""

import streamlit as st
from lib.pages_config import LEARN_MORE_LINKS, PAGES


def home_page():
    """The homepage of the Streamlit app."""
    st.set_page_config(page_title="Vertex AI")
    st.title("Google Cloud | Generative AI")
    st.markdown("This is a demo application for Google Cloud Vertex AI.")

    st.header("Demos")
    st.markdown("Select a demo page below to get started.")
    for page in PAGES:
        st.page_link(page["path"], label=page["title"], icon=page["icon"])

    st.header("Learn More")
    st.markdown("Learn more about Vertex AI:")
    for link in LEARN_MORE_LINKS:
        st.page_link(link["url"], label=link["label"], icon=link["icon"])

    st.divider()
    st.markdown("2024 © KenTandrian. All rights reserved.")


st.logo("./static/google-cloud.png")

# Group pages for navigation
nav_groups = {"Welcome": [st.Page(home_page, title="Home", icon="🏠")]}
for page_config in PAGES:
    group = page_config["group"]
    if group not in nav_groups:
        nav_groups[group] = []

    nav_groups[group].append(
        st.Page(page_config["path"], title=page_config["title"], icon=page_config["icon"])
    )

pg = st.navigation(nav_groups)
pg.run()
