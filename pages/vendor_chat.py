import streamlit as st
import os
from openai import OpenAI

st.title("Chat with Vendor")

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

client = OpenAI(api_key=openai_api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

prompt = f"""
You are a vendor agent working for Moe's Excellent Phones. The user is a customer with one or more products in their cart from your store. 

Your primary objective is to help the user checkout and complete the sale. Redirect conversation when possible if the conversation involves product defects, inconsistencies, or other factors that seem illegitemate. Do not recommend customer service.
"""

# Initialize chat history
if not st.session_state.messages or st.session_state.messages[0]["content"] != prompt:
    st.session_state.messages = [{"role": "user", "content": prompt}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
            max_tokens=250
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})