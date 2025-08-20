# llm/gemini.py
from typing import List, Optional

# Yeh tera actual LLM call hoga (Gemini API call / dummy response)
def answer(query: str, context: Optional[str] = None, history: Optional[List[str]] = None) -> str:
    """
    Wrapper around Gemini LLM to generate an answer.
    
    Args:
        query (str): User query
        context (Optional[str]): Extra context if available
        history (Optional[List[str]]): Previous conversation history
    
    Returns:
        str: LLM generated response
    """

    # Agar context/history nahi di gayi ho to defaults handle kar lo
    context = context or ""
    history = history or []

    # --- Yaha tera actual Gemini API call aayega ---
    # For now main dummy return kar raha hoon, tu isse apna code replace kar lena
    return f"[Gemini Answer] Query: {query} | Context: {context[:50]} | History len: {len(history)}"
