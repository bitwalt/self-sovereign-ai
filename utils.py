import base64
import io
import json
import os
from typing import Dict, List

import qrcode
import requests
import yaml
from PIL import Image

from schemas import PromptModel

CHAT_MODELS = "./data/models.yml"


def load_prompt_models() -> Dict[str, PromptModel]:
    models = {}
    # load yaml config
    with open(CHAT_MODELS, "r") as f:
        config_yaml = yaml.safe_load(f)

        for value in config_yaml["models"].values():
            model = PromptModel(
                name=value["name"],
                welcome_message=value["welcome_message"],
                prompt_start=value["prompt_start"],
            )
            models[value["name"]] = model
    return models


def get_download_link(json_data, filename, text):
    data = json.dumps(json_data)
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'
    return href


def get_sat_price():
    # Get price of 1 BTC from bitfinex
    response = requests.get("https://api-pub.bitfinex.com/v2/ticker/tBTCUSD")
    btc_price = response.json()[2]
    assert btc_price > 0, "BTC price cannot be zero"
    # return price of 1 sat in usd
    return btc_price / 10**8


def generate_qr(url: str):
    # Genera il codice QR
    img = qrcode.make(url)
    # Covert image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    # Reimposta la posizione del cursore all'inizio del file
    img_bytes.seek(0)
    # Leggi l'immagine da BytesIO
    img = Image.open(img_bytes)
    return img
