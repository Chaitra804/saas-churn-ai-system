from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.conversation_agent import GroqRetentionAgent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_agent = GroqRetentionAgent()

# ---------------------------------------------------
# REQUEST MODEL
# ---------------------------------------------------

class CustomerData(BaseModel):

    hours_spent: int
    issues: str


# ---------------------------------------------------
# CHURN ANALYSIS
# ---------------------------------------------------

def calculate_churn(hours_spent, issues):

    probability = 0.2

    reasons = []

    issues_lower = issues.lower()

    # Engagement Logic

    if hours_spent < 5:

        probability += 0.4

        reasons.append(
            "Low customer engagement detected"
        )

    elif hours_spent < 10:

        probability += 0.2

        reasons.append(
            "Moderate engagement level"
        )

    else:

        reasons.append(
            "Customer engagement is stable"
        )

    # Technical Issues

    if (
        "crash" in issues_lower
        or "bug" in issues_lower
        or "error" in issues_lower
    ):

        probability += 0.2

        reasons.append(
            "Application stability issues detected"
        )

    if "slow" in issues_lower:

        probability += 0.15

        reasons.append(
            "Platform performance issues"
        )

    # UX Issues

    if (
        "dashboard" in issues_lower
        or "confusing" in issues_lower
        or "difficult" in issues_lower
    ):

        probability += 0.15

        reasons.append(
            "Poor user experience detected"
        )

    # Customer Sentiment

    if (
        "bad" in issues_lower
        or "terrible" in issues_lower
        or "angry" in issues_lower
        or "frustrated" in issues_lower
    ):

        probability += 0.2

        reasons.append(
            "Negative customer sentiment identified"
        )

    # Cap Probability

    probability = min(probability, 0.95)

    # Risk Levels

    if probability >= 0.7:

        risk_level = "HIGH"

    elif probability >= 0.4:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    churn_prediction = probability >= 0.5

    # Ensure reasons always exist

    if len(reasons) == 0:

        reasons.append(
            "Customer behavior appears stable"
        )

    return {
        "probability": round(probability, 2),
        "risk_level": risk_level,
        "churn_prediction": churn_prediction,
        "reasons": reasons
    }


# ---------------------------------------------------
# ISSUE ANALYSIS
# ---------------------------------------------------

def analyze_issues(issues):

    issues_lower = issues.lower()

    detected_issues = []

    recommendations = []

    if "crash" in issues_lower:

        detected_issues.append(
            "Frequent application crashes"
        )

        recommendations.append(
            "Improve application stability and monitoring"
        )

    if "slow" in issues_lower:

        detected_issues.append(
            "Slow system performance"
        )

        recommendations.append(
            "Optimize backend infrastructure"
        )

    if "dashboard" in issues_lower:

        detected_issues.append(
            "Dashboard usability problems"
        )

        recommendations.append(
            "Redesign dashboard experience"
        )

    if (
        "support" in issues_lower
        or "response" in issues_lower
    ):

        detected_issues.append(
            "Customer support dissatisfaction"
        )

        recommendations.append(
            "Improve support response time"
        )

    if len(detected_issues) == 0:

        detected_issues.append(
            "General customer dissatisfaction"
        )

        recommendations.append(
            "Schedule customer feedback session"
        )

    return {
        "detected_issues": detected_issues,
        "recommendations": recommendations,
        "summary": (
            "Customer experience requires attention."
        )
    }


# ---------------------------------------------------
# ANALYZE ENDPOINT
# ---------------------------------------------------

@app.post("/analyze")

def analyze_customer(data: CustomerData):

    churn_analysis = calculate_churn(
        data.hours_spent,
        data.issues
    )

    issue_analysis = analyze_issues(
        data.issues
    )

    prompt = f"""
    Customer Analysis:

    Hours Spent:
    {data.hours_spent}

    Customer Issues:
    {data.issues}

    Churn Probability:
    {churn_analysis['probability']}

    Risk Level:
    {churn_analysis['risk_level']}

    Provide detailed retention recommendations.
    """

    ai_response = conversation_agent.generate_response(
        prompt
    )

    return {
        "churn_analysis": churn_analysis,
        "issue_analysis": issue_analysis,
        "ai_response": ai_response
    }


# ---------------------------------------------------
# CHAT ENDPOINT
# ---------------------------------------------------

@app.post("/chat")

def chat(data: dict):

    prompt = f"""
    Customer Context:

    Hours Spent:
    {data.get('hours_spent')}

    Issues:
    {data.get('issues')}

    Churn Probability:
    {data.get('probability')}

    User Question:
    {data.get('message')}

    Give intelligent SaaS retention guidance.
    """

    response = conversation_agent.generate_response(
        prompt
    )

    return {
        "response": response
    }


# ---------------------------------------------------
# ROOT
# ---------------------------------------------------

@app.get("/")

def home():

    return {
        "message": "Enterprise AI Retention Platform Running"
    }