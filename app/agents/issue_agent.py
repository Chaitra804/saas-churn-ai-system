import random


class IssueAgent:

    def analyze_issues(self, issues, churn_probability):

        issues_lower = issues.lower()

        detected_issues = []

        recommendations = []

        summaries = []

        # --------------------------------
        # Technical Problems
        # --------------------------------

        if any(
            word in issues_lower
            for word in [
                "bug",
                "error",
                "crash",
                "slow",
                "lag"
            ]
        ):

            detected_issues.append(
                "Technical performance problems"
            )

            recommendations.extend([
                "Escalate issue to engineering team",
                "Provide priority technical support",
                "Offer temporary workaround"
            ])

            summaries.append(
                "Customer experiencing technical frustration."
            )

        # --------------------------------
        # UX Problems
        # --------------------------------

        if any(
            word in issues_lower
            for word in [
                "confusing",
                "hard",
                "difficult",
                "complex"
            ]
        ):

            detected_issues.append(
                "User experience difficulties"
            )

            recommendations.extend([
                "Provide onboarding walkthrough",
                "Share product tutorials",
                "Schedule customer success demo"
            ])

            summaries.append(
                "Customer struggling with product usability."
            )

        # --------------------------------
        # Support Problems
        # --------------------------------

        if any(
            word in issues_lower
            for word in [
                "support",
                "late",
                "response",
                "unhelpful"
            ]
        ):

            detected_issues.append(
                "Support dissatisfaction"
            )

            recommendations.extend([
                "Assign dedicated support manager",
                "Improve response time",
                "Initiate proactive outreach"
            ])

            summaries.append(
                "Customer unhappy with support experience."
            )

        # --------------------------------
        # High Risk Retention Actions
        # --------------------------------

        if churn_probability > 0.75:

            recommendations.extend([
                "Offer retention discount",
                "Escalate to customer success leadership",
                "Provide premium support access"
            ])

        # --------------------------------
        # Default
        # --------------------------------

        if not detected_issues:

            detected_issues.append(
                "General customer dissatisfaction"
            )

            recommendations.append(
                "Schedule customer feedback session"
            )

        # Remove duplicates
        recommendations = list(set(recommendations))

        # AI-style dynamic summary
        final_summary = random.choice([
            "Customer shows signs of disengagement.",
            "Customer retention risk is increasing.",
            "Immediate customer engagement is recommended.",
            "Customer satisfaction appears unstable."
        ])

        return {
            "detected_issues": detected_issues,
            "recommendations": recommendations,
            "summary": final_summary,
            "detailed_analysis": summaries
        }