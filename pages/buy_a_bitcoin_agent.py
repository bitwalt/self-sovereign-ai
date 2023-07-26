"""
Pay an invoice in order to run an agent that will 
"""

import os

import streamlit as st
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.llms import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY", "random_key")
with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", type="password", value=openai_api_key
    )

if not openai_api_key:
    st.warning("Please add your OpenAI API Key")
    st.stop()


llm = OpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-3.5-turbo",
    temperature=0,
    streaming=True,
)
tools = load_tools(["ddg-search"])
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)
