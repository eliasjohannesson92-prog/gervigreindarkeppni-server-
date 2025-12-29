from typing import Any, Dict

def predict(payload: Dict[str, Any]) -> Dict[str, Any]:
    state = payload.get("rl_state") or {}
    keys = list(state.keys()) if isinstance(state, dict) else []
    return {"action": 0, "state_keys_preview": keys[:10]}
