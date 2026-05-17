from groq import Groq
import os


class GroqRetentionAgent:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_response(self, prompt):

        try:

            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an enterprise AI customer retention assistant. "
                            "You help SaaS companies reduce churn and improve customer satisfaction. "
                            "Give intelligent, personalized, professional responses."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            return completion.choices[0].message.content

        except Exception as e:

            return f"AI Error: {str(e)}"