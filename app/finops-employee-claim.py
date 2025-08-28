# pylint: disable=invalid-name
"""
Main application file for the Employee Claim Data Extraction demo.

This application uses a context-aware, two-stage process for maximum accuracy:
1.  **Stage 1 (Extraction):** A single API call extracts raw data and global document
    context from the uploaded file.
2.  **Stage 2 (Classification):** A separate, targeted API call is made for each
    line item, providing it with the global context to make a highly accurate
    classification.
"""

import json
import pandas as pd
import streamlit as st
from google.genai import types
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from lib.categorize_expense import CATEGORIES_MAP
from lib.prompts import PROMPT_STAGE_1_EXTRACTION, get_stage_2_classification_prompt
from lib.vertex_ai import get_vertex_ai_client

# --- Configuration ---
MODEL = "gemini-2.5-flash"
CLIENT = get_vertex_ai_client()
MAX_WORKERS = 10

FINAL_CONTEXT_FIELDS_TO_KEEP = [
    'report_title', 'employee_id', 'employee_name', 'entity', 'cost_center',
    'profit_center', 'travel_event_start_date', 'travel_event_end_date'
]
COLUMN_ORDER = [
    'report_title', 'employee_id', 'employee_name', 'entity', 'cost_center', 'profit_center',
    'travel_event_start_date', 'travel_event_end_date', 'transaction_date', 'transaction_time',
    'Category Claim', 'Sub Category', 'COA', 'merchant', 'description', 'original_currency',
    'original_amount', 'entity_currency', 'entity_amount'
]

# --- Functions (These remain unchanged) ---
def categorize_expense(classification_key: str, raw_expense_item: dict) -> dict:
    category_details = CATEGORIES_MAP.get(classification_key, CATEGORIES_MAP["Default_Uncategorized"])
    raw_expense_item.update(category_details)
    return raw_expense_item

def call_gemini_api_for_extraction(file_bytes, mime_type):
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=PROMPT_STAGE_1_EXTRACTION), types.Part.from_bytes(data=file_bytes, mime_type=mime_type)])]
    response = CLIENT.models.generate_content(model=MODEL, contents=contents, config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1))
    return response.text

def call_gemini_api_for_classification(prompt: str) -> str:
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
    response = CLIENT.models.generate_content(model=MODEL, contents=contents, config=types.GenerateContentConfig(temperature=0.0))
    return response.text.strip()

def classify_and_process_item(item, global_context, options_string):
    item_to_classify = {"merchant": item.get("merchant"), "description": item.get("description"), "original_currency": item.get("original_currency")}
    prompt_stage_2 = get_stage_2_classification_prompt(item_to_classify, global_context, options_string)
    classification_key = call_gemini_api_for_classification(prompt_stage_2)
    processed_item = categorize_expense(classification_key, item)
    final_context_to_add = {key: global_context.get(key) for key in FINAL_CONTEXT_FIELDS_TO_KEEP}
    processed_item.update(final_context_to_add)
    return processed_item

# --- Main Application UI and Logic ---
st.set_page_config(page_title="Employee Claim", page_icon="📄", layout="wide")
st.title("📄 Employee Claim Processor")
st.markdown("Upload a claim document to extract and classify all line items using a **parallelized**, context-aware, two-stage AI pipeline.")

# --- SESSION STATE INITIALIZATION ---
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'raw_stage1_output' not in st.session_state:
    st.session_state.raw_stage1_output = None

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload Claim Document", type=["pdf", "png", "jpg", "jpeg"])

# When a new file is uploaded, reset the state
if uploaded_file is not None and (st.session_state.get('uploaded_file_id') != uploaded_file.file_id):
    st.session_state.processing_complete = False
    st.session_state.processed_data = None
    st.session_state.raw_stage1_output = None
    st.session_state.uploaded_file_id = uploaded_file.file_id

# --- Processing Logic ---
if uploaded_file is not None:
    if st.button("Process Document", type="primary"):
        # --- STAGE 1: EXTRACTION ---
        with st.spinner("Stage 1: Extracting raw data and global context..."):
            try:
                # Read file bytes once
                file_bytes = uploaded_file.getvalue()
                mime_type = uploaded_file.type
                
                raw_data_str = call_gemini_api_for_extraction(file_bytes, mime_type)
                raw_data_json = json.loads(raw_data_str)
                st.session_state.raw_stage1_output = raw_data_json # Store raw output
                
                global_context = raw_data_json.get("global_context", {})
                raw_items = raw_data_json.get("items", [])

            except Exception as e:
                st.error(f"An error occurred during Stage 1: {e}")
                st.stop()

        # --- STAGE 2: PARALLEL CLASSIFICATION ---
        if raw_items:
            final_processed_report = []
            st.info(f"Stage 1 complete. Found {len(raw_items)} line items. Starting parallel classification...")
            with st.spinner(f"Stage 2: Classifying {len(raw_items)} items in parallel..."):
                options_string = "\n".join([f"{key}: {value.get('Category Description', '')}" for key, value in CATEGORIES_MAP.items()])
                
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_item = {executor.submit(classify_and_process_item, item, global_context, options_string): item for item in raw_items}
                    
                    for future in tqdm(as_completed(future_to_item), total=len(raw_items), desc="Classifying Items"):
                        try:
                            processed_item = future.result()
                            final_processed_report.append(processed_item)
                        except Exception as e:
                            item = future_to_item[future]
                            st.error(f"Error classifying item '{item.get('description')}': {e}")

            # --- STORE FINAL RESULT IN SESSION STATE ---
            st.session_state.processed_data = final_processed_report
            st.session_state.processing_complete = True
            st.rerun() # Force a rerun to jump to the display logic immediately
        else:
            st.warning("No line items were found in the document.")
            st.session_state.processing_complete = True # Mark as complete to avoid re-running

# --- Display Logic ---
if st.session_state.processing_complete:
    st.header("✅ Final Processed Report", divider="rainbow")
    
    # Display the raw Stage 1 output if it exists
    if st.session_state.raw_stage1_output:
        with st.expander("Show Stage 1 Raw Output (includes temporary context)"):
            st.json(st.session_state.raw_stage1_output)

    # Check if there is data to display
    if st.session_state.processed_data:
        st.success("Document processed successfully!")
        
        output_format = st.radio(
            "Select Output Format:",
            ("Table", "JSON"),
            horizontal=True,
            key='output_format_selector' # A key makes the widget more stable
        )

        if output_format == "JSON":
            st.json(st.session_state.processed_data)
        else:
            df = pd.DataFrame(st.session_state.processed_data)
            existing_columns = [col for col in COLUMN_ORDER if col in df.columns]
            st.dataframe(df[existing_columns], use_container_width=True, hide_index=True)
    else:
        st.info("Processing is complete, but no line items were found to display.")
