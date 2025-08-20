import time
from fastapi import APIRouter, Request
from pydantic import BaseModel
from llm.gemini import answer   # apna LLM wrapper import karo

router = APIRouter()

# ✅ Input validation with Pydantic
class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat(req: ChatRequest):
    query = req.query.strip()
    if not query:
        return {"error": "Missing query."}

    start = time.time()

    try:
        # ✅ Safely call LLM
        llm_answer = answer(query)

        if not llm_answer:
            llm_answer = "No response generated from LLM."

    except Exception as e:
        # ✅ Prevent 500 crash, return clean error
        return {"error": f"LLM call failed: {str(e)}"}

    latency_ms = int((time.time() - start) * 1000)

    return {
        "category": "general",
        "answer": llm_answer,
        "citations": [],   # abhi koi docs nahi
        "latency_ms": latency_ms
    }
