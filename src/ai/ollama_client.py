import requests
import json
import os

def ollama_chat(prompt: str, model: str = "tinyllama") -> str:
    url = "http://127.0.0.1:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }
    try:
        with requests.post(url, json=data, stream=True) as response:
            response.raise_for_status()
            full_response = ""
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    try:
                        chunk = json.loads(decoded)
                        if "response" in chunk:
                            full_response += chunk["response"]
                    except json.JSONDecodeError:
                        continue
            return full_response.strip()
    except Exception as e:
        return f"[ERROR] Ollama request failed: {e}"
