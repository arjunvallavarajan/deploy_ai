"""
Simple AI logic used for teaching.

This is intentionally lightweight so students can focus on app-building.
Later, you can replace this with an ML model, transformer model, or LLM API.
"""

POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "love", "fast",
    "helpful", "perfect", "happy", "smooth", "easy", "resolved"
}

NEGATIVE_WORDS = {
    "bad", "poor", "terrible", "hate", "slow", "broken", "angry",
    "delay", "delayed", "refund", "issue", "problem", "worst",
    "damaged", "cracked", "missing", "charged", "twice"
}

SAFETY_WORDS = {
    "swollen", "leaking", "smoking", "burning", "overheating",
    "hot", "fire", "spark", "punctured", "bulging"
}


def predict_sentiment(text: str) -> dict:
    """
    Convert customer text into a simple sentiment prediction.

    Returns a dictionary because APIs and UI apps can easily display
    or serialize dictionaries as JSON.
    """
    if not text or not text.strip():
        return {
            "label": "EMPTY_INPUT",
            "score": 0.0,
            "safety_flag": False,
            "recommended_action": "Please enter a customer message."
        }

    import string

    words = text.lower().split()

    # Clean punctuation to handle quotes, brackets, and other symbols
    cleaned_words = [word.strip(string.punctuation) for word in words]

    positive_hits = [word for word in cleaned_words if word in POSITIVE_WORDS]
    negative_hits = [word for word in cleaned_words if word in NEGATIVE_WORDS]
    safety_hits = [word for word in cleaned_words if word in SAFETY_WORDS]

    if safety_hits:
        return {
            "label": "NEGATIVE",
            "score": 0.95,
            "safety_flag": True,
            "recommended_action": "Escalate to a specialist safety team."
        }

    score_value = len(positive_hits) - len(negative_hits)

    if score_value > 0:
        return {
            "label": "POSITIVE",
            "score": min(0.60 + score_value * 0.10, 0.99),
            "safety_flag": False,
            "recommended_action": "Thank the customer and capture positive feedback."
        }

    if score_value < 0:
        return {
            "label": "NEGATIVE",
            "score": min(0.60 + abs(score_value) * 0.10, 0.99),
            "safety_flag": False,
            "recommended_action": "Route the issue to a support agent."
        }

    return {
        "label": "NEUTRAL",
        "score": 0.50,
        "safety_flag": False,
        "recommended_action": "Ask for more information."
    }


def generate_customer_reply(customer_text: str, prediction: dict) -> str:
    """
    Create a simple customer-facing response from the prediction.
    """
    if prediction.get("safety_flag"):
        return (
            "Please do not pack or ship the device. "
            "Your message may indicate a safety issue, so a specialist "
            "support team should review it."
        )

    label = prediction.get("label")

    if label == "POSITIVE":
        return "Thank you for your feedback. We are glad the experience was positive."

    if label == "NEGATIVE":
        return "We are sorry about the issue. A support agent should review your case."

    if label == "NEUTRAL":
        return "Thank you for the message. Please share more details so we can guide you."

    return "Please provide a valid customer message."
