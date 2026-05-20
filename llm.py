# --- File: llm.py ---
import requests
import os
from dotenv import load_dotenv

load_dotenv()

AI_SETTINGS = {
    "persona": "You are a professional assistant. Answer strictly based on the provided context.",
    "rules": [
        "Answer strictly based on the provided context.",
        "If the answer is not in the context, say exactly: 'I don't have that information in my knowledge base.'",
        "Keep answers concise and professional."
    ]
}

POLLINATIONS_KEY = os.getenv("POLLINATIONS_API_KEY", "")

def answer_question(query: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    rules_list = "\n".join([f"- {rule}" for rule in AI_SETTINGS["rules"]])
    
    system_prompt = f"{AI_SETTINGS['persona']}\n\nRULES:\n{rules_list}"
    user_prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"

    headers = {"Content-Type": "application/json"}
    if POLLINATIONS_KEY:
        headers["Authorization"] = f"Bearer {POLLINATIONS_KEY}"

    try:
        response = requests.post(
            "https://text.pollinations.ai/openai",
            headers=headers,
            json={
                "model": "openai",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "private": True
            },
            timeout=60
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
