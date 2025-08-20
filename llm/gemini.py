#handle Gemini API integration
import google.generativeai as genai
import time
from core.config import config
from qdrant_client import QdrantClient

genai.configure(api_key=config.GEMINI_API_KEY)
client = QdrantClient(url=config.QDRANT_URL, check_compatibility=False)

def answer(query: str, context_snippets: list[dict], category: str, max_retries: int = 3, timeout: int = 20) -> str:
    context_text = ""
    for snippet in context_snippets:
        title = snippet.get("metadata", {}).get("filename", "Unknown")
        page = snippet.get("metadata", {}).get("start", "N/A")
        context_text += f"[Source:{title} p.{page}]\n{snippet['text']}\n\n"

    prompt = (
        f"Use provided context below to answer the following query about {category}.\n"
        "Do not reveal raw line-level numbers. Cite sources as [Source:title p.X].\n"
        "Answer in concise bullet points and include a 'Confidence' field at the end.\n\n"
        f"Context:\n{context_text}\n"
        f"Query: {query}\n"
    )

    retries = 0
    while retries < max_retries:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(
                prompt,
                generation_config={"temperature": 0.2},
                safety_settings={"category": "HARM_CATEGORY_UNSPECIFIED", "threshold": "BLOCK_NONE"},
                timeout=timeout
            )
            return response.text
        except Exception as e:
            retries += 1
            time.sleep(2)
            if retries == max_retries:
                raise RuntimeError(f"Gemini LLM failed after {max_retries} retries: {e}")