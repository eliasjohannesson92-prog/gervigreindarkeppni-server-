from typing import Any, Dict

def predict(payload: Dict[str, Any]) -> Dict[str, Any]:
    b64 = payload.get("image_b64") or ""
    bytes_estimate = int(len(b64) * 3 / 4) if b64 else 0
    return {"label": "dummy", "score": 0.0, "bytes_estimate": bytes_estimate}
