import json
import os
import sys

import httpx
import requests

url = "https://localhost:8081/v1/chat/completions"

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Tell me how the sun works in 200 words"},
    ],
}
headers = {"Content-type": "application/json"}
token = ""
preimage = ""
headers["Authorization"] = f"LSAT {token}:{preimage}"
response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.headers)

print(response.text)
