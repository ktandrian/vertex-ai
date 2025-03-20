# pylint: disable=invalid-name
"""
Demo for e-bukti potong data extraction using Google Vertex AI and Gemini model.
"""

import json
import streamlit as st
from decouple import config
from google import genai
from google.genai import types

PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")
REGION = "us-central1"
MODEL = "gemini-2.0-flash-001"

# pylint: disable=duplicate-code
def generate_multimodal(file_content):
    """Generates extracted data using the Gemini multimodal model."""
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=REGION
    )

    text1 = types.Part.from_text(text="""
    Analyze the provided Indonesian Bukti Pemotongan/Pemungutan Form and extract the following information.
    Ensure numerical values are extracted with appropriate decimal precision.
    Return the data in JSON format. Ensure data is extracted accurately and formatted as specified below:

    **Extracted Information:**

    * **HEADER**:
      * **EBUPOT NOMOR:** (String) The EBUPOT number.
    * **SECTION A**:
      * **NPWP:** (String, without spaces) The Nomor Pokok Wajib Pajak.
      * **NIK:** (String) The Nomor Induk Kependudukan.
      * **NAMA:** (String) The name of the taxpayer.
    * **SECTION B**:
      * **MASA PAJAK:** (String) The tax period (mm-yyyy).
      * **DPP:** (Number) The Dasar Pengenaan Pajak.
      * **TARIF:** (Number) The tax rate.
      * **PPh DTP:** (Number) The Pajak Penghasilan Ditanggung Pemerintah.
      * **Keterangan Kode Objek Pajak:** (String) The description of the tax object code.
      * **Nomor Dokumen Referensi:** (String) The reference document number.
      * **Nama Dokumen:** (String) The document name.
      * **Tanggal Dokumen:** (String, format: dd-mm-yyyy) The document date.
    * **SECTION C**:
      * **NPWP Pemotong:** (String, without spaces) The withholding agent's NPWP.
      * **NAMA Pemotong:** (String) The withholding agent's name.
      * **Tanggal:** (String, format: dd-mm-yyyy) The document date.

    **Important Considerations for Extraction:**

    * Carefully locate and extract the `PPh DTP` value from the table in section B.
    * Ensure that NPWP values are extracted without any spaces.
    * Pay close attention to date formats and convert them to dd-mm-yyyy.
    * If a value is not present in the document, return `null` for that field in the JSON.

    **Output Format:**

    ```json
    {
        "Header": {
            "NOMOR": "...",
        },
        "Section A - IDENTITAS WAJIB PAJAK YANG DIPOTONG/DIPUNGUT": {
            "NPWP": "...", // without spaces
            "NIK": "...",
            "NAMA": "..."
        },
        "Section B - PAJAK PENGHASILAN YANG DIPOTONG/DIPUNGUT": {
            "MASA PAJAK": "...",
            "DPP": "...",
            "TARIF": "...",
            "PPh DTP": "...",
            "Keterangan Kode Objek Pajak": "...",
            "Nomor Dokumen Referensi": "...",
            "Nama Dokumen": "...",
            "Tanggal Dokumen": "dd-mm-yyyy"
        },
        "Section C - IDENTITAS PEMOTONG/PEMUNGUT": {
            "NPWP Pemotong": "...", // without spaces
            "NAMA Pemotong": "...",
            "Tanggal": "dd-mm-yyyy"
        }
    }
    ```

    Document:""")

    contents = [
        types.Content(
            role="user",
            parts=[
                text1,
                types.Part.from_bytes(data=file_content, mime_type="application/pdf")
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

st.set_page_config(page_title="E-Bukti Potong", page_icon="💲")
st.title("E-Bukti Potong 💲")
st.markdown("Extracting data from electronic bukti potong document.")

uploaded_file = st.file_uploader("Upload e-Bukti Potong", type="pdf")

if uploaded_file is not None:
    # Read the file content as bytes
    file = uploaded_file.read()

    if st.button("Extract Data"):
        with st.spinner("Extracting data..."):
            extracted_data = generate_multimodal(file)
            # Parse the output string to JSON
            try:
                extracted_json = json.loads(extracted_data)
                st.json(extracted_json)
            except json.JSONDecodeError:
                st.error("Error: Could not parse extracted data as JSON.")
                st.write(extracted_data)  # Display the raw output for debugging
