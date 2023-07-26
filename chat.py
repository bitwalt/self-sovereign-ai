from typing import List

import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage

from config import PREM_MODELS, TOKEN_LIMIT
from proxy_402 import Proxy402
from schemas import L402

is_openai = lambda url: url.startswith("https://api.openai.com")


def get_api_base(api_base: str, model_name: str):
    if is_openai(api_base):
        return api_base
    else:
        model_port = PREM_MODELS.get(model_name, None)
        if not model_port:
            raise ValueError(f"Model {model_name} not found")
        return f"{api_base}:{model_port}/v1"


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


class ChatGateway:
    def __init__(
        self, api_key: str, api_base: str, model_name: str, proxy_402: Proxy402 = None
    ):
        self._api_key = api_key
        self._is_openai = is_openai(api_base)
        self.api_base = get_api_base(api_base, model_name)
        self.model_name = model_name
        self._proxy_402 = proxy_402

    def chat(self, messages: List[ChatMessage], l402: L402 = None):
        if self._proxy_402:
            # Return the response from the 402 proxy
            return self._proxy_402.chat(self.model_name, messages, l402)

        # OpenAI or Prem
        st_callback = StreamlitCallbackHandler(st.container())
        llm = ChatOpenAI(
            openai_api_base=self.api_base,
            openai_api_key=self._api_key,
            streaming=True,
            callbacks=[st_callback],
            max_tokens=TOKEN_LIMIT if self._is_openai else 128,
        )
        response = llm(messages)
        return response.content

    def add_402_proxy(self, proxy: Proxy402):
        self._proxy_402 = proxy
