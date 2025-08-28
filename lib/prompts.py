"""
This module contains the prompt templates for the two-stage employee claim
processing workflow using the Gemini model.

- STAGE 1: Extracts raw data and global context from the entire document.
- STAGE 2: Classifies a single line item using the context from Stage 1.
"""

import json

# --- STAGE 1: CONTEXTUAL EXTRACTION PROMPT ---

PROMPT_STAGE_1_EXTRACTION = """
You are a highly advanced AI agent specializing in financial data processing. Your task is to meticulously analyze an employee expense report and transform it into a single, structured JSON object that captures both top-level context and a list of all individual expense items.

**Core Instructions:**
1.  **Analyze the Entire Document:** Read the whole document, including all pages, to understand its overall context before extracting any details. Note flight paths, meeting agendas, and locations mentioned.
2.  **Output Format:** Your entire output must be a single, valid JSON object. Do not include any explanatory text, markdown formatting like ```json, or any text before or after the JSON object.

**JSON Object Schema & Extraction Logic:**
The root JSON object must have two main keys: "global_context" and "items".

1.  **`global_context` (object):** A summary of the entire document.
    *   **`report_title`** (string): The full, unmodified title of the expense report.
        *   **Extraction based on Title Format:** The `report_title` has a strict comma-separated format: `employee_id, entity, profit_center, cost_center, report_desc, total`. Use this format to accurately extract the `employee_id`, `entity`, `profit_center`, and `cost_center` fields.
    *   **`employee_id`** (string): Extracted from the title format.
    *   **`employee_name`** (string): The full name of the employee, usually found in the 'From' or 'created by' fields.
    *   **`entity`** (string): Extracted from the title format.
    *   **`profit_center`** (string): Extracted from the title format. Abbreviate if necessary (e.g., 'Shared Service' becomes 'SS').
    *   **`cost_center`** (string): Extracted from the title format.
    *   **`travel_event_start_date`** (string): The overall start date of the trip (YYYY-MM-DD).
    *   **`travel_event_end_date`** (string): The overall end date of the trip (YYYY-MM-DD).
    *   **`summary`** (string): A summary of the trip's purpose.
    *   **`key_locations`** (array of strings): A list of all cities, countries, or airport codes mentioned.

2.  **`items` (array):** An array of objects, where each object represents one raw, unclassified expense line item. For each item, extract only:
    *   **`merchant`** (string)
    *   **`description`** (string)
    *   **`original_currency`** (string): in currency code format.
    *   **`original_amount`** (number)
    *   **`entity_currency`** (string): in currency code format.
    *   **`entity_amount`** (number)
    *   **`transaction_date`** (string, YYYY-MM-DD)
    *   **`transaction_time`** (string, HH:MM)

**IMPORTANT:** Do not attempt to classify the items in this step. Your only job is to extract the raw data and the global context as specified.
"""


# --- STAGE 2: CONTEXT-AWARE CLASSIFICATION PROMPT ---

def get_stage_2_classification_prompt(
    item_to_classify: dict,
    global_context: dict,
    options_string: str
) -> str:
    """
    Generates the dynamic prompt for the second stage of the workflow.

    This function creates a rich, context-aware prompt that asks Gemini to classify
    a single item using the global context of the entire document.

    Args:
        item_to_classify: A dictionary representing the single raw expense item.
        global_context: The context object extracted during Stage 1.
        options_string: A formatted string of all possible classification keys and
                        their descriptions.

    Returns:
        A formatted prompt string ready to be sent to the Gemini API.
    """
    prompt = f"""
You are an expert AI classification engine. Your task is to analyze an expense item and classify it using the overall trip context provided.

**Instructions:**
1.  First, understand the `global_context` of the entire expense report. Pay close attention to the summary and key locations.
2.  Then, carefully analyze the specific `item_to_classify`.
3.  Using BOTH the global context and the specific item details, select the single best `classification_key` from the `CLASSIFICATION_OPTIONS` list. For example, use the `key_locations` and `summary` from the context to determine if a flight or hotel is "Domestic" or "Overseas".
4.  Your entire output must be **only the chosen `classification_key` string** and nothing else. Do not add any explanation or formatting.

---
**EXAMPLE**
---

**`global_context`**:
{{
  "report_title": "Business trip to SG 24 - 27 Mar 2025",
  "key_locations": ["SG", "Singapore", "CGK", "SIN", "Jakarta"]
}}

**`item_to_classify`**:
{{
  "merchant": "Garuda Indonesia",
  "description": "Flight ticket CGK - SIN",
  "original_currency": "IDR"
}}

**`CLASSIFICATION_OPTIONS`**:
(List of all options would be here)

**Expected Output:**
Business-Travel_Travel-Overseas-Flight

---
**TASK**
---

**`global_context`**:
{json.dumps(global_context, indent=2)}

**`item_to_classify`**:
{json.dumps(item_to_classify, indent=2)}

**`CLASSIFICATION_OPTIONS`**:
{options_string}

**Output:**
"""
    return prompt
