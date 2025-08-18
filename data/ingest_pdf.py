import uuid
from typing import List, Dict
from PyPDF2 import PdfReader

def parse_pdf(file_bytes: bytes, filename: str, category: str, chunk_size: int = 300, overlap: int = 50) -> List[Dict]:
    reader = PdfReader(file_bytes)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_text = " ".join(words[start:end])
        # Stable UUID based on filename, category, and chunk index
        chunk_id = str(uuid.uuid5(
            uuid.NAMESPACE_DNS,
            f"{filename}:{category}:{start}"
        ))
        chunks.append({
            "id": chunk_id,
            "text": chunk_text,
            "metadata": {
                "filename": filename,
                "category": category,
                "start": start,
                "end": end
            }
        })
        start += chunk_size - overlap
    return chunks