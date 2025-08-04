import os
import requests
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = "mistral-large-latest"
MISTRAL_TEMPERATURE = 0.5

def mistral_chat_completion(prompt: str) -> str:
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": MISTRAL_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": MISTRAL_TEMPERATURE,
    }
    resp = requests.post(url, headers=headers, json=data)
    if not resp.ok:
        raise RuntimeError(f"Mistral API error {resp.status_code}: {resp.text}")
    return resp.json()["choices"][0]["message"]["content"]
