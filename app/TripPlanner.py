# pylint: disable=invalid-name
"""
Demo for Web UI generation using Google Vertex AI and Gemini Pro model.
"""

import os
import time
from decouple import config
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
import streamlit as st
import vertexai

PROJECT_ID = config("PROJECT_ID", default="YOUR_PROJECT_ID")
REGION = config("REGION", default="us-central1")
MODEL = config("MODEL", default="gemini-1.0-pro-001")

os.environ["PROJECT_ID"] = PROJECT_ID
os.environ["REGION"] = REGION
os.environ["MODEL"] = MODEL

template = """You are an AI Trip Planner.
You are a helpful and informative bot that answers the questions using text from reference information provided below.
Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
However, you are talking to a non-technical audience, so be sure to break down complicated concepts and strike a friendly and conversational tone.
You will provide with location and weather conditions of the place of your journey.
You will tell about popular places of the location, cultural gems and cuisine.
Also you will be provided with weather condition so you can tell about how to plan the journey.
Keep it about 300 words. Do not include pictures.
Here is an example how the answer should be, when location is Bangkok and weather is 24 C and 5% precipitation, 24 C and 0% precipitation and 26 C and 0% precipitation.

<div class="planner-wrapper">
    <h5>Welcome to the Vibrant Heart of Thailand: Bangkok</h5>
    <p>Prepare to be captivated by the vibrant streets, cultural gems, and delectable cuisine of Bangkok, Thailand.
    With temperatures hovering around 28°C to 35°C and low chances of rain during your visit, you'll enjoy
    pleasant weather for exploring this bustling metropolis.</p>
    <hr>
    <!-- Packing Essential -->
    <div class="planner-card">
        <div class="planner-icon" style="margin-bottom: 0.5rem;">
            <img src="app/static/packing-essentials.png" alt="Packing Essentials" height="32" width="32">
        </div>
        <div class="planner-info">
            <h5>Packing Essentials</h5>
            <p>To ensure a comfortable stay, pack light and breathable clothing. Shorts, t-shirts, and sandals are
            ideal for the warm and humid weather. Consider bringing a light jacket or cardigan for evenings or
            air-conditioned places. Remember to stay hydrated by carrying a reusable water bottle.</p>
        </div>
    </div>
    <!-- Iconic Landmarks -->
    <div class="planner-card">
        <div class="planner-icon" style="margin-bottom: 0.5rem;">
            <img src="app/static/landmarks.png" alt="Iconic Landmarks" height="32" width="32">
        </div>
        <div class="planner-info">
            <h5>Iconic Landmarks</h5>
            <p>Make sure to visit the Grand Palace, a stunning architectural complex that houses the Temple of the Emerald Buddha, Thailand's most sacred temple.
            Don't miss the opportunity to take a boat tour along the Chao Phraya River, offering breathtaking views of the city's skyline.</p>
        </div>
    </div>
    <!-- Cultural Gems -->
    <div class="planner-card">
        <div class="planner-icon" style="margin-bottom: 0.5rem;">
            <img src="app/static/culture.png" alt="Cultural Gems" height="32" width="32">
        </div>
        <div class="planner-info">
            <h5>Cultural Gems</h5>
            <p>Immerse yourself in the rich culture of Bangkok by visiting the Jim Thompson House, a beautiful traditional Thai house showcasing exquisite silk and home décor.
            Explore the vibrant Chatuchak Weekend Market, one of the largest weekend markets in the world, where you can find a vast array of local crafts, souvenirs, and street food.</p>
        </div>
    </div>
    <!-- Culinary Delights -->
    <div class="planner-card">
        <div class="planner-icon" style="margin-bottom: 0.5rem;">
            <img src="app/static/meal.png" alt="Culinary Delights" height="32" width="32">
        </div>
        <div class="planner-info">
            <h5>Culinary Delights</h5>
            <p>Indulge in Bangkok's vibrant street food scene, where you can savor authentic Thai flavors. Visit Yaowarat Road, Bangkok's Chinatown, renowned for its delicious street food stalls.
            For a more refined dining experience, try one of the many rooftop restaurants offering panoramic views of the city.</p>
        </div>
    </div>
</div>

Now provide the information and plan the trip about '{location}' and weather is '{weather}'. Write your answer in English only.
Always wrap the answer text with same html tags as provided in the example. Use same class in html tags as provided in example everytime.
Main div should always be planner-wrapper. Each category should be in planner-card div. Use same planner-icon html as provided. In planner-info, add the relevant answer.
Round off the temperature in answer. Write content within html tags in English only. Do not mention the travel dates. Answer in English only.
ANSWER:
"""


def LLM_init():
    """Initialize the VertexAI client and LLM chain."""
    vertexai.init(project=PROJECT_ID, location=REGION)
    model = VertexAI(model_name=MODEL, max_output_tokens=2048)
    prompt_from_template = PromptTemplate.from_template(template)
    chain = prompt_from_template | model
    return chain


st.set_page_config(page_title="Trip Planner", page_icon="🚌")
st.title("Trip Planner 🚌")
st.markdown(
    "The ultimate trip recommender powered by Google Vertex AI and Gemini model"
)

if "messages_ai_trip" not in st.session_state:
    st.session_state["messages_ai_trip"] = [
        {
            "role": "assistant",
            "content": "Hello, I am Gemini, your travel assistant. Where are you traveling to?",
        }
    ]

for msg in st.session_state.messages_ai_trip:
    if msg["role"] == "duration":
        st.success(msg["content"])
    else:
        st.chat_message(msg["role"]).write(
            msg["content"], unsafe_allow_html=(msg["role"] == "assistant")
        )

if prompt := st.chat_input():
    st.session_state.messages_ai_trip.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    elapsed = 0
    with st.status("Gemini is thinking...", expanded=True) as status:
        s_time = time.time()
        llm_chain = LLM_init()
        status.write(f"LLM initialized in {round(time.time() - s_time, 3)}s")
        msg = llm_chain.invoke(
            {"location": prompt, "weather": "29 C with 5% precipitation"}
        )
        e_time = time.time()
        elapsed = e_time - s_time
        status.update(
            label=f"Gemini replied in {round(elapsed, 3)}s.",
            state="complete",
            expanded=False,
        )

    st.session_state.messages_ai_trip.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg, unsafe_allow_html=True)

    elapsed_txt = f"Gemini replied in {round(elapsed, 3)}s."
    st.session_state.messages_ai_trip.append(
        {"role": "duration", "content": elapsed_txt}
    )
    st.success(elapsed_txt)
