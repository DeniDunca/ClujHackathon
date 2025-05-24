import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

MODEL = "asi1-mini"
URL = "https://api.asi1.ai/v1/chat/completions"
API_KEY = os.getenv('ASI_ONE_KEY')

def call_asi_one_chatbot(messages):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": 0.2,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "max_tokens": 500,
        "stream": False
    })
    response = requests.post(URL, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
    else:
        return f"Error: {response.status_code}, {response.text}"