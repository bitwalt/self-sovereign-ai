"""
Fastapi app that start a server and have one single endpoint that receivce a dict of {"model", "messages": "" }
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import openai
from pydantic import BaseModel
import logging

app = FastAPI(access_log=True)
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add a logger for FastAPI requests
logger = logging.getLogger('uvicorn')

class Message(BaseModel):
    model: str
    messages: list 
    
@app.post("/v1/chat/completions")
async def process_messages(data: Message):
    model = data.model
    messages = data.messages
    assert model == "gpt-3.5-turbo", "Model not found"
    assert messages, "Messages not found"
    try:
        response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.1,
                max_tokens=300,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        return response
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(status_code=500, content={"message": "Unable to get response from OpenAI"})
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)