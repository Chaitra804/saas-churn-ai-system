class RecommendationAgent:

    def recommend(self, churn_probability):

        if churn_probability > 0.8:

            return [
                "Offer premium discount",
                "Assign support manager",
                "Provide onboarding session"
            ]

        elif churn_probability > 0.5:

            return [
                "Send retention email",
                "Offer feature demo"
            ]

        else:

            return [
                "Customer likely to stay"
            ]