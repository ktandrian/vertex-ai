# pylint: disable=invalid-name
"""
Demo for employee claim data extraction using Google Vertex AI and Gemini model.
"""

import json
import streamlit as st
from google.genai import types
from lib.vertex_ai import get_vertex_ai_client

MODEL = "gemini-2.5-flash"

def generate_multimodal(file):
    """Generates extracted data using the Gemini multimodal model."""
    client = get_vertex_ai_client()

    text1 = types.Part.from_text(text="""
    You are an AI agent specialized in multi-language financial document data extraction.
    Your task is to analyze the provided document (which could be an invoice, payment request, email, or other financial record) and extract specific financial details.

    Strictly follow these instructions:
    1.  **Output Format:** Return the extracted information as a single JSON object.
    2.  **Field Definitions & Extraction Logic:**
        *   `Claim Category`:
            *   **Definition:** Classify the primary purpose of the expense.
            *   **Options:** `Flights`, `Meal`, `Accommodation`, `Service Fee`, `Other Fee`.
            *   **Logic:**
                *   `Flights`: Look for terms like "flight," "airfare," "ticket," "airline," "travel," "transportation (air)."
                *   `Meal`: Look for terms like "meal," "food," "dining," "restaurant," "catering," "provision."
                *   `Accommodation`: Look for terms like "hotel," "lodging," "stay," "resort," "guesthouse," "rent (room/apartment)."
                *   `Service Fee`: This category is for non-physical goods, professional services, subscriptions, or membership fees. Look for terms like "service," "fee," "consultation," "training," "certification," "membership," "license," "subscription," "commission," "management fee," "professional fee," "guarantee fee."
                *   `Other Fee`: Use this if none of the above categories fit the primary purpose of the expense.
        *   `Employee Name`:
            *   **Definition:** The name of the individual primarily associated with this expense (e.g., preparer, recipient, approver, participant, or the person being reimbursed).
            *   **Keywords/Logic:** Look for fields like "Prepared by," "Submitted by," "Recipient," "To," "From (individual)," "Attn:", names above or near signatures, names in email 'From' or 'To' fields, or names listed as participants in a service. Prioritize the most relevant name initiating or receiving the expense/service.
        *   `Items`:
            *   **Definition:** An array of objects, where each object represents a single line item from the document.
            *   **Logic:**
                *   Identify tables or lists that detail individual goods or services.
                *   For each item, extract:
                    *   `description` (string): A concise text detailing the item or service. Prioritize the primary description.
                    *   `quantity` (string or number): The number of units for the item. Extract as present (e.g., "4" or "3"). If not clearly numerical or unavailable, set to `null`.
                    *   `unit_price` (string or number): The cost per unit for the item. Extract as numerical value. If not clearly numerical or unavailable, set to `null`.
                    *   `line_total` (string or number): The total cost for that specific item line (quantity * unit_price, or direct line total). Extract as numerical value.
                *   If no clear itemized list is present, try to infer a single item based on the main purpose/description of the document. If no items can be extracted, the array should be empty `[]`.
        *   `Total Amount Due`:
            *   **Definition:** The final, total monetary amount that needs to be paid, including all taxes and fees.
            *   **Keywords/Logic:** Look for terms like "Total," "Grand Total," "Amount Due," "Total Payable," "Invoice Total," "Balance Due." This is typically the largest monetary value presented as the final sum. Extract only the numerical value.
        *   `Invoice Number`:
            *   **Definition:** The unique identification number for the invoice, receipt, or payment request.
            *   **Keywords/Logic:** Look for "Invoice No.," "Inv. #," "Receipt No.," "Document No.," "Reference No.," "Number," "Bill No." or common prefixes like `INV-`, `REF-`, `DOC-` followed by an alphanumeric sequence. If multiple numbers are present (e.g., a tax invoice number and a main invoice number), prioritize the primary invoice/document number.
        *   `Transaction Date`:
            *   **Definition:** The date when the document was issued, the transaction occurred, or the expense was incurred.
            *   **Keywords/Logic:** Look for "Date," "Invoice Date," "Issue Date," "Prepared Date," "Document Date."
            *   **Format:** `YYYY-MM-DD`.
        *   `Vendor Name`:
            *   **Definition:** The full legal name of the company or entity that provided the goods or services and issued the document.
            *   **Keywords/Logic:** Typically found at the top of an invoice, near a company logo, in fields like "Vendor Name," "Supplier," "Issued By," "From." Look for common legal entity indicators (e.g., Inc., Ltd., LLC, Co., S.A., K.K., PT).
        *   `Currency`:
            *   **Definition:** The currency of the total amount.
            *   **Keywords/Logic:** Infer from currency symbols (e.g., $, €, £, ¥, Rp), or explicit mentions like "USD," "EUR," "JPY," "IDR." If the symbol is ambiguous (like '$'), try to identify the country or other currency hints within the document. If no currency symbol or code is found, set to `null`.

    3.  **Handling Missing Data:** If any requested data point is not found in the document, assign its value as `null`. Do not make assumptions for missing fields.

    **Example of Expected JSON Output (based on provided Document 1 - ALSPPI Invoice):**

    ```json
    {
        "Category Claim": "Service Fee",
        "Employee Name": "John Doe",
        "Items": [
            {
                "description": "Software License Renewal - User A",
                "quantity": 1,
                "unit_price": 500.00,
                "line_total": 500.00
            },
            {
                "description": "Premium Support Package",
                "quantity": null,
                "unit_price": null,
                "line_total": 750.00
            }
        ],
        "Total Amount Due": "1250.00",
        "Invoice Number": "INV-2024-00123",
        "Transaction Date": "2024-01-15",
        "Vendor Name": "Tech Solutions Inc.",
        "Currency": "USD"
    }
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
        max_output_tokens=65535,
        response_modalities=["TEXT"],
        safety_settings=[types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_NONE
        ), types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE
        ), types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE
        ), types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_NONE
        )],
        response_mime_type = "application/json",
        thinking_config=types.ThinkingConfig(
            thinking_budget=0,
        ),
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
