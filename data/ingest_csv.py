import uuid
import csv
from typing import List, Dict
from io import StringIO

def parse_csv(file_bytes: bytes, filename: str, category: str) -> List[Dict]:
    text_io = StringIO(file_bytes.decode("utf-8"))
    reader = csv.DictReader(text_io)
    chunks = []
    for idx, row in enumerate(reader):
        lines = [f"{col}: {val}" for col, val in row.items()]
        chunk_text = "\n".join(lines)
        chunk_id = str(uuid.uuid5(
            uuid.NAMESPACE_DNS,
            f"{filename}:{category}:{idx}"
        ))
        chunks.append({
            "id": chunk_id,
            "text": chunk_text,
            "metadata": {
                "filename": filename,
                "category": category,
                "row": idx
            }
        })
    return chunks