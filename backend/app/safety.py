def calculate_confidence(score: float) -> dict:
    """
    FAISS score is distance-based.
    Lower score means better match.
    """

    if score < 0.75:
        return {"label": "High", "value": 0.9}

    if score < 1.0:
        return {"label": "Medium", "value": 0.7}

    return {"label": "Low", "value": 0.4}


def should_refuse(score: float, source_count: int) -> bool:
    if source_count < 2:
        return True

    if score > 1.1:
        return True

    return False