#csv data ingestion pipelines (csv parse into vectorestore DB)
import uuid
import csv
from typing import List, Dict
from io import StringIO
from core.supabase import supabase

def parse_csv(file_bytes: bytes, filename: str, category: str) -> List[Dict]:
    text_io = StringIO(file_bytes.decode("utf-8"))
    reader = csv.DictReader(text_io)
    rows = []
    for idx, row in enumerate(reader):
        data = {
            "id": str(uuid.uuid4()),
            "model_name": row.get("model_name"),
            "price": float(row.get("price") or 0),
            "sales": int(row.get("sales") or 0),
            "features": row.get("features"),
        }
        supabase.table("company_data").insert(data).execute()
        rows.append(data)
    return rows
