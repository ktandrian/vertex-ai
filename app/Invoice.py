# pylint: disable=invalid-name
"""
Demo for multilingual invoice data extraction using Google Vertex AI and Gemini model.
"""

import json
import streamlit as st
from decouple import config
from google import genai
from google.genai import types

PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")
REGION = "us-central1"
MODEL = "gemini-2.0-flash-001"

def generate_multimodal(file):
    """Generates extracted data using the Gemini multimodal model."""
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=REGION
    )

    text1 = types.Part.from_text(text="""
    Extract the following information from the provided invoice image(s).
    If a field is not present or cannot be reliably determined, leave it blank.
    Ensure numerical values are extracted with appropriate decimal precision and presented as number.
    Follow the output format as indicated in the sample.

    Extracted Information:
    * Supplier Name: (String) The trading name prominently displayed on the invoice.
    * Supplier Legal Name: (String) The full, legally registered name of the supplier, including the branch.
    * Invoice Date: (String) Day, Month, and Year the invoice was issued. Format as DD-MMM-YYYY, e.g., 11-Oct-2023
    * Invoice No.: (String) The unique identifier for the invoice).
    * Invoice Currency: (String) The currency the invoice is denominated in, usually follows the language -- VND, THB, IDR, etc.
    * Invoice Amount (excluding VAT): (Number) The total value of goods/services before VAT/tax.
    * Invoice Service Charge: (Number) If any, find the service charge amount in the invoice.
    * Invoice VAT Amount: (Number) The total amount of VAT/tax charged.
    * Invoice Amount (including VAT): (Number) The final total amount due, including VAT/tax.

    Pay attention to the thousand separators when normalizing string to number.

    Return the result in JSON format.
    ```
    {
        "Supplier Name": "...",
        "Supplier Legal Name": "...",
        "Invoice Date": {
            "extracted_value": "...",
            "normalized_value": "DD-MMM-YYYY"    
        },
        "Invoice No.": "...",
        "Invoice Currency": "IDR/THB/VND/...",
        "Invoice Amount (excluding VAT)": {
            "extracted_value": "...",
            "normalized_value": "..."  // number
        },
        "Invoice Service Charge": {
            "extracted_value": "...",
            "normalized_value": "..."  // number
        },
        "Invoice VAT Amount": {
            "extracted_value": "...",
            "normalized_value": "..."  // number
        },
        "Invoice Amount (including VAT)": {
            "extracted_value": "...",
            "normalized_value": "..."  // number
        }
    }
    ```
    
    Notes on Thai Invoices:
    * Thai invoices dates might be in Buddhist Era (BE) format, which is 543 years ahead of the Gregorian calendar.
    * Be mindful of the date format and convert it to DD-MMM-YYYY.
    """
    )

    file_content = file.read()
    mime_type = file.type

    contents = [
        types.Content(
            role="user",
            parts=[
                text1,
                types.Part.from_bytes(data=file_content, mime_type=mime_type)
            ]
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.8,
        max_output_tokens=1024,
        response_modalities=["TEXT"],
        safety_settings=[types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="OFF"
        )],
        response_mime_type = "application/json",
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=generate_content_config,
    )
    return response.text

st.set_page_config(page_title="Invoice Data Extraction", page_icon="💲")
st.title("Invoice Data Extraction 💲")
st.markdown("Extracting data from invoice document.")

uploaded_file = st.file_uploader("Upload Invoice", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    if st.button("Extract Data"):
        with st.spinner("Extracting data..."):
            extracted_data = generate_multimodal(uploaded_file)
            # Parse the output string to JSON
            try:
                extracted_json = json.loads(extracted_data)
                st.json(extracted_json)
            except json.JSONDecodeError:
                st.error("Error: Could not parse extracted data as JSON.")
                st.write(extracted_data)  # Display the raw output for debugging
