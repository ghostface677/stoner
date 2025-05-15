from fastapi import APIRouter, Request
from app.services.cohere_service import get_cohere_response

router = APIRouter()

@router.post("/completion")
async def completion(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return {"error": "Prompt is required"}

    try:
        answer = await get_cohere_response(prompt)
    except Exception as e:
        return {"error": str(e)}

    if not answer:
        answer = "🤖 Sorry, I do not have an answer for that. Please ask a question about biomedical equipment troubleshooting or maintenance."

    return {"result": answer}
