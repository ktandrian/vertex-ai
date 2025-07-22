# pylint: disable=invalid-name
"""
Demo for employee claim data extraction using Google Vertex AI and Gemini model.
"""

import json
import streamlit as st
from google.genai import types
from lib.vertex_ai import get_vertex_ai_client

MODEL = "gemini-2.0-flash-001"

def generate_multimodal(file):
    """Generates extracted data using the Gemini multimodal model."""
    client = get_vertex_ai_client()

    text1 = types.Part.from_text(text="""
    You are an expert financial document data extractor. Your task is to analyze the provided document (which could be an invoice, payment request, or email related to an expense) and extract specific financial details.

    **Strictly follow these instructions:**

    1.  **Output Format:** Return the extracted information as a single JSON object.
    2.  **Field Definitions & Extraction Logic:**
        *   `Category Claim`:
            *   **Definition:** Classify the primary purpose of the expense.
            *   **Options:** `Flights`, `Meal`, `Accommodation`, `Service Fee`, `Other Fee`.
            *   **Logic:**
                *   `Flights`: Look for keywords like "flight," "tiket pesawat," "airline," "booking penerbangan."
                *   `Meal`: Look for "meal," "makan," "restoran," "catering," "food."
                *   `Accommodation`: Look for "hotel," "inap," "penginapan," "akomodasi," "resort."
                *   `Service Fee`: Look for "service," "training," "certification," "consulting," "jasa," "ujian," "profesi," "membership," "license." This is for non-physical goods or specific professional services.
                *   `Other Fee`: Use this if none of the above categories fit.
        *   `Employee Name`:
            *   **Definition:** The name of the employee primarily associated with this expense (e.g., preparer, recipient, approver, or participant).
            *   **Logic:** Prioritize the "Prepared by," "To," "From," or "DITUJUKAN KEPADA" (Addressed to) fields for individual names. If multiple names, pick the most relevant one initiating or receiving the expense.
        *   `Item Detail`:
            *   **Definition:** A concise description of the specific goods or services purchased/rendered.
            *   **Logic:** Extract descriptive text from itemized lists, service descriptions, or the main purpose mentioned in the document (e.g., "Ujian Online Sertifikasi Profesi Penagihan" or "SPPI Certification").
        *   `Total Amount Due`:
            *   **Definition:** The final, total amount that needs to be paid, including all taxes and fees.
            *   **Logic:** Look for "Total Tagihan," "Total Yang Harus Dibayar," "Invoice Amount," or "Amount (including VAT/Tax)." Exclude sub-totals or individual item amounts if a final total is present. Ensure the currency symbol (Rp) is noted, but only extract the numerical value.
        *   `Invoice Number`:
            *   **Definition:** The unique identification number for the invoice or receipt.
            *   **Logic:** Look for "No Invoice," "Invoice Number," "INV-," "Receipt No.," or similar identifiers. If a "Faktur Pajak" (Tax Invoice) number is present *and* linked to the main invoice, capture the primary invoice number.
        *   `Transaction Date`:
            *   **Definition:** The date when the transaction occurred or the invoice was issued.
            *   **Logic:** Extract from "Tanggal Invoice," "Invoice Date," "Date," or the date associated with the primary document issuance. Format as `YYYY-MM-DD`.
        *   `Vendor Name`:
            *   **Definition:** The name of the company or entity that provided the goods or services.
            *   **Logic:** Look for "Vendor Name," the company logo/name at the top of an invoice, or "PT." followed by a company name.
        *   `Currency`:
            *   **Definition:** The currency of the amount.
            *   **Logic:** Infer from currency symbols (e.g., "Rp" for IDR), or explicit mentions.
              *   `IDR` for Rupiah
              *   `USD` for US Dollar
              *   `EUR` for Euro
              *   If not explicitly found, assume IDR based on the sample.
        *   `Document Type`:
            *   **Definition:** The type of document provided.
            *   **Options:** `Invoice`, `Payment Request`, `Email`, `Tax Invoice`, `Other`.

    3.  **Handling Missing Data:** If any requested data point is not found in the document, assign its value as `null`. Do not make assumptions for missing fields.

    **Example of Expected JSON Output (based on provided Document 1 - ALSPPI Invoice):**

    ```json
    {
      "Category Claim": "Service Fee",
      "Employee Name": "Nurul Hikmah",
      "Item Detail": "Ujian Online Sertifikasi Profesi Penagihan",
      "Total Amount Due": "1526000",
      "Invoice Number": "INV/SPPI-00217/111/400/E/III/25",
      "Transaction Date": "2025-03-07",
      "Vendor Name": "ALSPPI PT Sertifikasi Profesi Pembiayaan Indonesia",
      "Currency": "IDR",
      "Document Type": "Invoice"
    }
    Now, process the following document:
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
        max_output_tokens=2048,
        response_modalities=["TEXT"],
        safety_settings=[types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="BLOCK_NONE"
        ), types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="BLOCK_NONE"
        ), types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="BLOCK_NONE"
        ), types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_NONE"
        )],
        response_mime_type = "application/json",
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=generate_content_config,
    )
    return response.text

st.set_page_config(page_title="Employee Claim", page_icon="📄")
st.title("Employee Claim 📄")
st.markdown("Extracting data from an employee claim document.")

uploaded_file = st.file_uploader("Upload Claim Document", type=["pdf", "png", "jpg", "jpeg"])

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
