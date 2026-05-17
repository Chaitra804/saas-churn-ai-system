def predict_churn(hours_spent, issues):

    issues_lower = issues.lower()

    # -----------------------------------
    # Base Risk
    # -----------------------------------

    risk_score = 20

    reasons = []

    # -----------------------------------
    # Engagement Analysis
    # -----------------------------------

    if hours_spent <= 1:

        risk_score += 35

        reasons.append(
            "Very low platform engagement"
        )

    elif hours_spent <= 3:

        risk_score += 20

        reasons.append(
            "Low engagement detected"
        )

    elif hours_spent <= 6:

        risk_score += 10

        reasons.append(
            "Moderate engagement level"
        )

    else:

        risk_score -= 10

        reasons.append(
            "Healthy platform engagement"
        )

    # -----------------------------------
    # Technical Issue Severity
    # -----------------------------------

    technical_keywords = [
        "bug",
        "crash",
        "error",
        "slow",
        "lag",
        "freeze"
    ]

    technical_count = 0

    for word in technical_keywords:

        if word in issues_lower:

            technical_count += 1

    risk_score += technical_count * 8

    if technical_count > 0:

        reasons.append(
            f"{technical_count} technical issue(s) detected"
        )

    # -----------------------------------
    # UX Problems
    # -----------------------------------

    ux_keywords = [
        "confusing",
        "hard",
        "difficult",
        "complex"
    ]

    ux_count = 0

    for word in ux_keywords:

        if word in issues_lower:

            ux_count += 1

    risk_score += ux_count * 6

    if ux_count > 0:

        reasons.append(
            "User experience dissatisfaction detected"
        )

    # -----------------------------------
    # Support Dissatisfaction
    # -----------------------------------

    support_keywords = [
        "support",
        "late",
        "response",
        "unhelpful"
    ]

    support_count = 0

    for word in support_keywords:

        if word in issues_lower:

            support_count += 1

    risk_score += support_count * 5

    if support_count > 0:

        reasons.append(
            "Customer support dissatisfaction"
        )

    # -----------------------------------
    # Negative Sentiment
    # -----------------------------------

    negative_words = [
        "bad",
        "terrible",
        "hate",
        "worst",
        "annoying",
        "frustrated"
    ]

    negative_count = 0

    for word in negative_words:

        if word in issues_lower:

            negative_count += 1

    risk_score += negative_count * 7

    if negative_count > 0:

        reasons.append(
            "Strong negative sentiment detected"
        )

    # -----------------------------------
    # Normalize Score
    # -----------------------------------

    risk_score = max(1, risk_score)

    risk_score = min(95, risk_score)

    probability = round(risk_score / 100, 2)

    # -----------------------------------
    # Final Prediction
    # -----------------------------------

    churn_prediction = probability >= 0.50

    # -----------------------------------
    # Risk Levels
    # -----------------------------------

    if probability >= 0.80:

        risk_level = "CRITICAL"

    elif probability >= 0.60:

        risk_level = "HIGH"

    elif probability >= 0.40:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    return {
        "probability": probability,
        "risk_level": risk_level,
        "churn_prediction": churn_prediction,
        "reasons": reasons
    }