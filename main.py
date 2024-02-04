from fastapi import FastAPI, HTTPException
import aiohttp
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import replicate

load_dotenv()
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

app = FastAPI()

class AIRequest(BaseModel):
    prompt: str

#rapid api
# async def send_post_request(url, json_data, headers):
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, json=json_data, headers=headers) as response:
#                 if 'application/json' in response.headers.get('Content-Type', ''):
#                     return await response.json()
#                 else:
#                     return await response.text()
#     except aiohttp.ClientConnectorError as e:
#         raise HTTPException(status_code=500, detail=f"Connection error: {e}")

# @app.post("/generate-ai-response/")
# async def generate_ai_response(request: AIRequest):
    # url = "https://meta-llama-2-ai.p.rapidapi.com/"
    # payload = {
    #     "model": "meta-llama/Llama-2-70b-chat-hf",
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": request.prompt
    #         }
    #     ]
    # }
    # headers = {
    #     "Content-Type": "application/json",
    #     "X-RapidAPI-Key": RAPID_API_KEY,  # Using the API key from the environment variable
    #     "X-RapidAPI-Host": "meta-llama-2-ai.p.rapidapi.com"
    # }

    # response = await send_post_request(url, payload, headers)
    # print(f'{response  = } llama2')
    # return response

async def send_replicate_request(model_name, input_data):
    try:
        # Use replicate to make requests to the Replicate API
        result = replicate.run(model_name, input=input_data)
        return result
    except Exception as e:
        return e
        raise HTTPException(status_code=500, detail=f"Replicate API error: {e}")
        

@app.post("/generate-ai-response/")
async def generate_ai_response(request: AIRequest):
    # model_name = "meta/llama-2-7b-chat"

    # input_data = {
    #     "debug": False,
    #     "top_k": -1,
    #     "top_p": 1,
    #     "prompt": request.prompt,
    #     "temperature": 0.75,
    #     "system_prompt": "Your system prompt here...",  # Replace with your system prompt
    #     "max_new_tokens": 800,
    #     "min_new_tokens": -1,
    #     "repetition_penalty": 1
    # }

    # response = await send_replicate_request(model_name, input_data)
    # print(f'{response  = } Replicate API')
    # return response
    #mixtral 
    model_name = "mistralai/mixtral-8x7b-instruct-v0.1"

    input_data = {
        "top_k": 50,
        "top_p": 0.9,
        "prompt": request.prompt,
        "temperature": 0.6,
        "max_new_tokens": 1024,
        "prompt_template": "<s>[INST] {prompt} [/INST] ",
        "presence_penalty": 0,
        "frequency_penalty": 0
    }

    response = await send_replicate_request(model_name, input_data)
    print(f'{response  = } Replicate API')
    return response

#Health Check Endpoint
@app.get("/health")
def read_health():
    return {"status": "healthy"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 6000)))