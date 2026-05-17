class RetentionAgent:

    def analyze_customer(self, data, churn_probability):

        issues = []

        recommendations = []

        risk_level = "LOW"

        # -------------------------
        # Detect Problems
        # -------------------------

        if data["LoginFrequency"] < 5:

            issues.append(
                "Low login frequency detected"
            )

            recommendations.append(
                "Send product engagement campaign"
            )

        if data["SupportTickets"] > 5:

            issues.append(
                "High support ticket volume"
            )

            recommendations.append(
                "Assign dedicated support manager"
            )

        if data["MonthlyRevenue"] < 100:

            issues.append(
                "Low customer spending"
            )

            recommendations.append(
                "Offer premium feature trial"
            )

        if data["SubscriptionLength"] < 6:

            issues.append(
                "New customer with low retention history"
            )

            recommendations.append(
                "Provide onboarding assistance"
            )

        # -------------------------
        # Risk Levels
        # -------------------------

        if churn_probability > 0.8:

            risk_level = "HIGH"

            recommendations.append(
                "Offer immediate retention discount"
            )

        elif churn_probability > 0.5:

            risk_level = "MEDIUM"

        # -------------------------
        # Final Summary
        # -------------------------

        summary = (
            f"Customer classified as {risk_level} churn risk."
        )

        return {
            "risk_level": risk_level,
            "issues_detected": issues,
            "recommendations": recommendations,
            "summary": summary
        }