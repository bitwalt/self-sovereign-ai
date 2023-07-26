import json
from dataclasses import dataclass
from typing import Any, Dict, List

import requests
import streamlit as st
from langchain.schema import (AIMessage, ChatMessage, HumanMessage,
                              SystemMessage)

from config import PREM_MODELS
from schemas import L402, ClientQuery


@dataclass
class Proxy402:
    proxy_url: str
    auth_mode: str
    ai_mode: str = "chat"

    def get_data_from_langchain(
        self, messages: List[ChatMessage]
    ) -> List[Dict[str, Any]]:
        message_data = []
        for message in messages:
            if isinstance(message, HumanMessage):
                message_data.append({"role": "user", "content": message.content})
            elif isinstance(message, SystemMessage):
                message_data.append({"role": "system", "content": message.content})
            elif isinstance(message, AIMessage):
                message_data.append({"role": "assistant", "content": message.content})
            elif isinstance(message, ChatMessage):
                message_data.append({"role": message.role, "content": message.content})
            else:
                raise ValueError(f"Message type {type(message)} not supported")
        return message_data

    def get_url(self, ai_mode: str = "chat", model_name: str = "gpt-3.5-turbo"):
        api_base = ""
        if model_name in PREM_MODELS.keys():
            api_base += "/prem"
        api_base += "/v1"

        if ai_mode == "chat":
            return f"{self.proxy_url}{api_base}/chat/completions"
        elif ai_mode == "embedding":
            return f"{self.proxy_url}{api_base}/embedding"
        elif ai_mode == "image":
            return f"{self.proxy_url}{api_base}/image"
        else:
            raise ValueError(f"Mode {self.ai_mode} not supported")

    def chat(self, model_name: str, messages: List[ChatMessage], l402: L402 = None):
        url = self.get_url(self.ai_mode, model_name)
        headers = {}
        data = {
            "model": model_name,
            "messages": self.get_data_from_langchain(messages),
        }

        if l402 and l402.preimage:
            # User has paid for the model
            tag = "L402" if self.auth_mode == "matador" else "LSAT"
            headers["Authorization"] = f"{tag} {l402.token}:{l402.preimage}"
            response = requests.post(
                url, headers=headers, data=json.dumps(data), verify=False
            )
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                return result
            else:
                raise ValueError(
                    f"Expected status code 200, but received: {response.status_code}, text: {response.text}"
                )
        # User has not paid
        if self.auth_mode == "L402":
            response = requests.get(url, verify=False)
        elif self.auth_mode == "matador":
            response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 402:
            return {
                "L402": L402.from_headers(response.headers, proxy_mode=self.auth_mode)
            }
        else:
            raise ValueError(
                f"Expected status code 402, but received: {response.status_code}, text: {response.text}"
            )

    def embedding(
        self, model_name: str, messages: List[ChatMessage], l402: L402 = None
    ):
        pass

    def image(self, model_name: str, messages: List[ChatMessage], l402: L402 = None):
        pass
