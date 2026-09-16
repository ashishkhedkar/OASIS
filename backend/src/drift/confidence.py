def calculate_confidence(
    hours_back,
    max_backtrack_hours=6,
):
    """
    Estimate confidence for a candidate origin.

    Confidence decreases as the backtracking
    period becomes longer.
    """

    # Longer backtracking means greater uncertainty.
    confidence = 1.0 - (
        hours_back / max_backtrack_hours
    )

    return max(0.0, min(1.0, confidence))


if __name__ == "__main__":
    for hours in range(0, 7):
        confidence = calculate_confidence(hours)

        print(
            f"{hours}h back → "
            f"confidence: {confidence:.2f}"
        )