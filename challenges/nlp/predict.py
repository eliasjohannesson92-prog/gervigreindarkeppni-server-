from typing import Any, Dict

def predict(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = payload.get("text") or ""
    return {
        "prediction": "dummy",
        "echo": text,
        "tokens_estimate": len(str(text).split()),
    }
