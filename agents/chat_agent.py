import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import initialize_agent, Tool, load_tools

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

tools = load_tools(["requests_all"], allow_dangerous_tools=True)
  
model = ChatOpenAI(model='gpt-4', openai_api_key=openai_api_key)
agent = initialize_agent(llm=model,
                         tools=tools,
                         agent_type="zero-shot-react-description", 
                         verbose=True)

