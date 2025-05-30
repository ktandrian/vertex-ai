"""Deploy reasoning engine to Google Cloud Vertex AI"""

import requests
import vertexai
from decouple import config
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import LangchainAgent

DISPLAY_NAME = "Get Exchange Rate"
MODEL = "gemini-2.0-flash"
PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")
REGION = "us-central1"

# pylint: disable=duplicate-code
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
        timeout=10,
    )
    return response.json()


vertexai.init(
    project=PROJECT_ID,
    location=REGION,
    staging_bucket="gs://reasoning-engines-staging"
)

# Deploy the reasoning engine
remote_app = agent_engines.create(
    LangchainAgent(
        model=MODEL,
        tools=[get_exchange_rate],
        model_kwargs=model_kwargs,
    ),
    requirements=[
        "cloudpickle==3.1.1",
        "google-cloud-aiplatform[agent_engines,langchain]",
    ],
    display_name=DISPLAY_NAME,
)

print(remote_app.resource_name)
