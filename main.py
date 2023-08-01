import os
import re

import streamlit as st
from langchain.schema import ChatMessage

from chat import ChatGateway
from config import AI_PROVIDERS, AUTH_METHODS, MODELS, PROXIES
from proxy_402 import Proxy402
from utils import generate_qr, load_prompt_models


def init_cache():
    if "l402" not in st.session_state:
        st.session_state.l402 = None
    if "prompt_model" not in st.session_state:
        st.session_state.prompt_model = None
    if "client_query" not in st.session_state:
        st.session_state.client_query = None
    if "paid_request" not in st.session_state:
        st.session_state.paid_request = False


def write_chat():
    if "messages" in st.session_state:
        for msg in st.session_state.messages:
            if msg.role == "system":
                continue
            st.chat_message(msg.role).write(msg.content)


def app():
    st.title("Self Sovereign AI")
    st.write(
        "This is a demo of the 402 payment required flow. The user will be asked to pay for the service before they can use it."
    )
    #### Settings
    st.sidebar.subheader("Settings")
    api_key = os.getenv("OPENAI_API_KEY", "random_key")
    
    api_base = "https://api.openai.com/v1"
    model_name = "gpt-3.5-turbo"
    use_l402 = st.sidebar.checkbox("Use L402", value=True, key="use_l402")
    if use_l402:
        auth_mode = st.sidebar.selectbox(
            "Select L402 proxy", AUTH_METHODS, key="auth_mode"
        )
        proxy_url = st.sidebar.selectbox("Select proxy_url", PROXIES[auth_mode])
        if proxy_url == "Add":
            proxy_url = st.sidebar.text_input(
                "Add 402 Proxy url ", value="", key="proxy_url"
            )
        model_name = st.sidebar.selectbox("Select model", MODELS["openai"])

        proxy_402 = Proxy402(proxy_url=proxy_url, auth_mode=auth_mode)

    else:
        proxy_402 = None
        ai_provider = st.sidebar.selectbox(
            "Select AI Provider", AI_PROVIDERS, key="ai_provider"
        )
        if ai_provider == "openai":
            # Ask for openai api key
            api_key = st.sidebar.text_input("OpenAI API Key", value=api_key, type="password")
            if api_key == "":
                st.sidebar.warning("Please add your OpenAI API Key")
                return
        elif ai_provider == "premai":
            # Ask for premai url
            st.sidebar.warning("If your instance has not a GPU, it will take a while.")
            api_base = st.sidebar.text_input(
                "PremAI deamon", value="http://prem.cashai.space", key="premai_url"
            )
        model_name = st.sidebar.selectbox("Select model", MODELS[ai_provider])

    chat_gateway = ChatGateway(
        api_key=api_key,
        api_base=api_base,
        model_name=model_name,
        proxy_402=proxy_402,
    )

    if st.sidebar.button("Clean chat"):
        st.session_state["messages"] = []

    #### Chat App

    prompt_models = load_prompt_models()

    assistant_role = st.selectbox(
        label="Select assistant", key="role", options=[p for p in prompt_models.keys()]
    )

    prompt_model = prompt_models[assistant_role]

    clean_chat = False
    if st.session_state["prompt_model"] != prompt_model:
        st.session_state.prompt_model = prompt_model
        clean_chat = True

    with st.expander("Show Prompt"):
        st.write(prompt_model.prompt_start)

    if clean_chat or "messages" not in st.session_state:
        st.session_state["messages"] = [
            ChatMessage(role="system", content=prompt_model.prompt_start),
            ChatMessage(role="assistant", content=prompt_model.welcome_message),
        ]

    write_chat()

    if prompt := st.chat_input():
        # eg. a64eaee33ef9e8022c08f07cfb040f3d563bda313b92e26feb8b8a65d64bc953
        if "l402" in st.session_state and re.match(r"^[a-f0-9]{64}$", prompt):
            # Received a preimage
            l402 = st.session_state.l402
            l402.preimage = prompt
        else:
            # User query
            l402 = None
            st.session_state.messages.append(ChatMessage(role="user", content=prompt))
            st.chat_message("user").write(prompt)

        # st.write(st.session_state.messages)

        response = chat_gateway.chat(messages=st.session_state.messages, l402=l402)
        if "L402" in response:
            # 402 payment required
            with st.container():
                l402 = response["L402"]    
                st.chat_message("assistant").write(
                      f"This is your token: **{l402.token}** "
                )
                payment_req = f"lightning:{l402.invoice}"
                response_text = f"Scan the QR code with a LN wallet or click on this [Payment Link]({payment_req})"
                st.chat_message("assistant").write(response_text)
                qr_image = generate_qr(payment_req)
                st.chat_message("assistant").image(qr_image, width=300)
                st.chat_message("assistant").write(
                    "Please add the preimage of the payment"
                )
                st.session_state.l402 = l402
        else:
            # Normal response from AI
            ai_message = ChatMessage(role="assistant", content=response)
            st.chat_message("assistant").write(response)
            st.session_state.messages.append(ai_message)
            st.session_state.l402 = None


if __name__ == "__main__":
    init_cache()
    app()
