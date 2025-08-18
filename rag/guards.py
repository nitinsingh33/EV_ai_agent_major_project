import re
from core.config import config

def redact(text: str) -> str:
    if not config.SAFE_MODE:
        return text
    # Mask ₹ amounts (e.g., ₹123, ₹12,345.67)
    text = re.sub(r"₹\s?\d[\d,\.]*", "₹[REDACTED]", text)
    # Mask raw unit counts (e.g., "123 units", "456 cars", "789 pieces")
    text = re.sub(r"\b\d{2,} (units?|cars?|pieces?|items?|orders?)\b", "[REDACTED]", text, flags=re.IGNORECASE)
    return text

def sanitize_context(snippets: list[dict]) -> list[dict]:
    sanitized = []
    for s in snippets:
        redacted_text = redact(s.get("text", ""))
        # Drop chunk if more than 50% is redacted
        redacted_ratio = len(re.findall(r"\[REDACTED\]", redacted_text)) / (len(redacted_text.split()) or 1)
        if redacted_ratio < 0.5:
            s = s.copy()
            s["text"] = redacted_text
            sanitized.append(s)
    return sanitized