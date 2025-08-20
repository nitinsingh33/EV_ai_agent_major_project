from llm import gemini

@router.post("/chat")
async def chat(request: Request):
    body = await request.json()
    query = body.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    try:
        response = gemini.answer(query)   # context/history optional hai
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM call failed: {str(e)}")
