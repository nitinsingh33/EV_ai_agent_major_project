from core.supabase import supabase
from llm.gemini import answer

def company_answer(query: str) -> str:
    # Simple keyword extraction (improve as needed)
    keywords = ["model_name", "price", "sales", "features"]
    rows = supabase.table("company_data").select("*").execute().data
    context = []
    for row in rows:
        context.append(
            f"Model: {row['model_name']}\nPrice: {row['price']}\nSales: {row['sales']}\nFeatures: {row['features']}"
        )
    prompt = (
        "Use ONLY the provided company data below to answer the query. "
        "Do not guess or hallucinate. If the answer is not present, reply 'Not available in company data.'\n\n"
        f"Company Data:\n{chr(10).join(context)}\n\nQuery: {query}"
    )
    return answer(query, [], "company", custom_prompt=prompt)