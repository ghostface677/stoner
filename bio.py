import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not found in environment variables. Please set it in your .env file.")

SYSTEM_MESSAGE = {"role": "system", "content": "You are a helpful assistant."}

@app.post("/api/completion")
async def completion(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "").strip()

    print("DEBUG: user_prompt:", user_prompt)  # Debug print
    if not user_prompt:
        return {"error": "Prompt is required"}

    messages = [
        SYSTEM_MESSAGE,
        {"role": "user", "content": user_prompt}
    ]

    body = {
        "model": "command-nightly",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 300,
    }

    print("DEBUG: Sending to Cohere:", body)

    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.post(
                "https://api.cohere.ai/v1/chat",
                json=body,
                headers=headers,
            )
            response.raise_for_status()
            res_json = response.json()

        except httpx.HTTPStatusError as exc:
            return {"error": f"Cohere API error: {exc.response.text}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

        print("DEBUG: Cohere response:", res_json)

        bot_reply = (
            res_json.get("text")
            or (res_json.get("generations", [{}])[0].get("text") if "generations" in res_json else None)
            or res_json.get("message")
            or res_json.get("response")
            or ""
        )

        if not bot_reply or not bot_reply.strip():
            bot_reply = "🤖 Sorry, I do not have an answer for that."

        return {"result": bot_reply}
