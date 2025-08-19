from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from rag.vectorstore import upsert
from data.ingest_pdf import parse_pdf
from data.ingest_csv import parse_csv

router = APIRouter()

@router.post("/ingest/files")
async def ingest_files(
    files: List[UploadFile] = File(...),
    category: str = Form(...)
):
    inserted = 0
    by_file = {}
    all_chunks = []
    for file in files:
        content = await file.read()
        filename = file.filename
        if filename.lower().endswith(".pdf"):
            chunks = parse_pdf(content, filename, category)
            all_chunks.extend(chunks)
            by_file[filename] = len(chunks)
            inserted += len(chunks)
        elif filename.lower().endswith(".csv"):
            rows = parse_csv(content, filename, category)
            by_file[filename] = len(rows)
            inserted += len(rows)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {filename}")
    if all_chunks:
        upsert(all_chunks)
    return {"inserted": inserted, "by_file": by_file}