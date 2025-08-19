from fastapi import APIRouter, Query
from core.supabase import supabase

router = APIRouter()

@router.get("/company/search")
async def search_company(model_name: str = Query(None)):
    query = supabase.table("company_data").select("*")
    if model_name:
        query = query.eq("model_name", model_name)
    result = query.execute()
    return {"results": result.data}