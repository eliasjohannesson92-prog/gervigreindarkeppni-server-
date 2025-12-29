from typing import Any, Dict

from challenges.nlp.predict import predict as nlp_predict
from challenges.image.predict import predict as image_predict
from challenges.rl.predict import predict as rl_predict


def dispatch_predict(challenge: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    challenge = (challenge or "").lower().strip()

    if challenge == "nlp":
        return nlp_predict(payload)
    if challenge == "image":
        return image_predict(payload)
    if challenge == "rl":
        return rl_predict(payload)

    raise ValueError("Invalid CHALLENGE. Use one of: nlp | image | rl")
