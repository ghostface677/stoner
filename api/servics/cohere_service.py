import httpx
from app.core.config import COHERE_API_KEY

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are an expert assistant specialized ONLY in biomedical equipment repair, service, and maintenance. "
        "Answer ONLY questions related to biomedical equipment troubleshooting, repair, servicing, and maintenance. "
        "If the question is outside this domain, politely respond that you can only assist with biomedical equipment."
    ),
}


async def get_cohere_response(user_prompt: str) -> str:
    messages = [
        SYSTEM_MESSAGE,
        {"role": "user", "content": user_prompt}
    ]

    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "command-nightly",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 300,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            "https://api.cohere.ai/v1/chat",
            json=body,
            headers=headers,
        )
        response.raise_for_status()
        res_json = response.json()

    # Extract response text robustly
    bot_reply = (
        res_json.get("text") or
        (res_json.get("generations", [{}])[0].get("text") if "generations" in res_json else None) or
        res_json.get("message") or
        ""
    )
    return bot_reply.strip()
