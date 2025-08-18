import time
from fastapi import APIRouter, Request, Depends
from core.intent import classify
from rag.vectorstore import search
from llm.gemini import answer

router = APIRouter()

def extract_citations(snippets):
    citations = []
    for s in snippets:
        meta = s.get("metadata", {})
        citations.append({
            "filename": meta.get("filename"),
            "page": meta.get("start"),
        })
    return citations

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query", "")
    if not query:
        return {"error": "Missing query."}
    start = time.time()
    category = classify(query)
    retrieved = search(query, top_k=5, filters={"category": category} if category != "general" else None)
    top_snippets = retrieved[:3]
    citations = extract_citations(top_snippets)
    llm_answer = answer(query, top_snippets, category)
    latency_ms = int((time.time() - start) * 1000)
    return {
        "category": category,
        "answer": llm_answer,
        "citations": citations,
        "latency_ms": latency_ms
    }