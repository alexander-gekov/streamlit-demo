import streamlit as st
import requests
import re
from r2r import R2RClient

# Initialize API settings
R2R_API_URL = "https://r2r-server.talsight.com/v2/rag"
API_TOKEN = ""
st.title("Parliament AI")

client = R2RClient("https://r2r-server.talsight.com")

health_response = client.health()

login_response = client.login("admin@example.com", "")

api_token = login_response.get("results").get("access_token").get("token")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": prompt
        }

        with requests.post(R2R_API_URL, json=payload, headers=headers, stream=True) as response:
            response.raise_for_status()
            completion = response.json().get('results').get('completion').get('choices')[0].get('message').get('content')
            results = response.json().get('results').get('search_results').get('vector_search_results')
            st.markdown(completion)
            
    st.session_state.messages.append({"role": "assistant", "content": completion})