#user intent classification/request type detect krna 
from typing import Literal

def classify(query: str) -> Literal['pricing', 'strategy', 'product', 'company', 'general']:
    query_lower = query.lower()
    # Priority order: pricing > strategy > product > company > general
    pricing_keywords = ["price", "cost", "fee", "charge", "pricing", "rate"]
    strategy_keywords = ["strategy", "plan", "roadmap", "approach", "vision"]
    product_keywords = ["product", "feature", "spec", "specification", "version", "release"]
    company_keywords = ["company", "organization", "corporate", "business", "team", "employee"]

    for kw in pricing_keywords:
        if kw in query_lower:
            return "pricing"
    for kw in strategy_keywords:
        if kw in query_lower:
            return "strategy"
    for kw in product_keywords:
        if kw in query_lower:
            return "product"
    for kw in company_keywords:
        if kw in query_lower:
            return "company"
    return "general"