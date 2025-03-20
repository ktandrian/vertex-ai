# pylint: disable=invalid-name
"""
Demo for Reasoning Engine use case using Google Vertex AI and Frankfurter API.
"""

import datetime

import requests
import streamlit as st
from currency_codes import get_currency_by_code
from decouple import config
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from vertexai import agent_engines
# from vertexai.preview.reasoning_engines import LangchainAgent

AGENT_ENGINE_ID = config("AGENT_ENGINE_ID", default="YOUR_AGENT_ENGINE_ID")
PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")

model = "gemini-2.0-flash"
currencies = [
    "USD", "JPY", "BGN", "CZK", "DKK",
    "GBP", "HUF", "PLN", "RON", "SEK",
    "CHF", "ISK", "NOK", "TRY", "AUD",
    "BRL", "CAD", "CNY", "HKD", "IDR",
    "ILS", "INR", "KRW", "MXN", "MYR",
    "NZD", "PHP", "SGD", "THB", "ZAR"
]

def currency_label(c: str):
    """Return the currency code followed by currency name."""
    return f"{c} ({get_currency_by_code(c).name})"

safety_settings = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}

model_kwargs = {
    "temperature": 0.28,
    "max_output_tokens": 1000,
    "top_p": 0.95,
    "top_k": 40,
    "safety_settings": safety_settings,
}

def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
):
    """Retrieves the exchange rate between two currencies on a specified date.

    Uses the Frankfurter API (https://api.frankfurter.app/) to obtain
    exchange rate data.

    Args:
        currency_from: The base currency (3-letter currency code).
            Defaults to "USD" (US Dollar).
        currency_to: The target currency (3-letter currency code).
            Defaults to "EUR" (Euro).
        currency_date: The date for which to retrieve the exchange rate.
            Defaults to "latest" for the most recent exchange rate data.
            Can be specified in YYYY-MM-DD format for historical rates.

    Returns:
        dict: A dictionary containing the exchange rate information.
            Example: {"amount": 1.0, "base": "USD", "date": "2023-11-24",
                "rates": {"EUR": 0.95534}}
    """
    response = requests.get(
        f"https://api.frankfurter.app/{currency_date}",
        params={"from": currency_from, "to": currency_to},
        timeout=10
    )
    return response.json()

# Development
# agent = LangchainAgent(
#     model=model,
#     tools=[get_exchange_rate],
#     model_kwargs=model_kwargs,
# )
# Production
agent = agent_engines.get(
    f"projects/{PROJECT_ID}/locations/us-central1/reasoningEngines/{AGENT_ENGINE_ID}"
)

st.set_page_config(page_title="Exchange Rate", page_icon="💰")
st.title("Exchange Rate")
st.markdown(
    "The ultimate exchange rate checker powered by Google Vertex AI Reasoning Engine, "
    "Langchain and Gemini model."
)
st.divider()

col1, col2 = st.columns(2)
currency_f = col1.selectbox(
    "From",
    currencies,
    format_func=currency_label
)
currency_t = col2.selectbox(
    "To",
    filter(lambda x: x != currency_f, currencies),
    format_func=currency_label
)
d = st.date_input(
    "Date", 
    datetime.date.today(),
    format="YYYY-MM-DD",
    max_value=datetime.date.today(),
    min_value=datetime.date(1999, 1, 4)
)

if st.button("Convert", type="primary"):
    # pylint: disable=no-member
    q_response = agent.query(
        input=f"What is the exchange rate from {currency_f} to {currency_t} currency as of {d}?"
    )
    st.write(q_response["output"])
