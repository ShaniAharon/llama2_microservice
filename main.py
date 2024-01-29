from fastapi import FastAPI, HTTPException
import aiohttp
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

app = FastAPI()

class AIRequest(BaseModel):
    prompt: str

async def send_post_request(url, json_data, headers):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data, headers=headers) as response:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    return await response.json()
                else:
                    return await response.text()
    except aiohttp.ClientConnectorError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {e}")

@app.post("/generate-ai-response/")
async def generate_ai_response(request: AIRequest):
    url = "https://meta-llama-2-ai.p.rapidapi.com/"
    payload = {
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "messages": [
            {
                "role": "user",
                "content": request.prompt
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,  # Using the API key from the environment variable
        "X-RapidAPI-Host": "meta-llama-2-ai.p.rapidapi.com"
    }

    response = await send_post_request(url, payload, headers)
    print(f'{response  = } llama2')
    return response

#Health Check Endpoint
@app.get("/health")
def read_health():
    return {"status": "healthy"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 6000)))