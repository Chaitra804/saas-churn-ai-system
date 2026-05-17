import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime

# ---------------------------------------------------
# BACKEND CONFIG (CHANGE ONLY HERE)
# ---------------------------------------------------

BACKEND_URL = "https://saas-churn-ai-system.onrender.com"

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Enterprise AI Retention Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "result" not in st.session_state:
    st.session_state.result = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#020617,#0f172a,#111827);
    color: white;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.main-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 800;
    color: #22d3ee;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.custom-card {
    background: rgba(17,24,39,0.92);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(34,211,238,0.15);
}

div.stButton > button {
    background: linear-gradient(90deg,#06b6d4,#0891b2);
    color: white;
    border-radius: 12px;
    width: 100%;
    font-weight: bold;
}

[data-testid="metric-container"] {
    background: rgba(17,24,39,0.92);
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:
    st.title("AI Retention Platform")
    st.markdown("""
- AI Churn Prediction
- Customer Analytics
- AI Assistant
- Retention Insights
""")
    st.success("System Online")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("<div class='main-title'>Enterprise AI Retention Platform</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>SaaS Churn Prediction System</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# INPUT
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("Customer Engagement")

    hours_spent = st.slider("Hours Spent", 0, 50, 5)
    health_score = min(100, hours_spent * 2)

    st.progress(health_score / 100)
    st.write(f"Health Score: {health_score}/100")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("Customer Issues")

    issues = st.text_area("Enter issues")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button("Analyze Customer"):

    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={
                "hours_spent": hours_spent,
                "issues": issues
            },
            timeout=30
        )

        response.raise_for_status()

        st.session_state.result = response.json()
        st.session_state.analysis_done = True

    except Exception as e:
        st.error(f"Backend Error: {e}")

# ---------------------------------------------------
# RESULTS
# ---------------------------------------------------

if st.session_state.analysis_done:

    result = st.session_state.result

    churn = result.get("churn_analysis", {})
    issue_analysis = result.get("issue_analysis", {})
    ai_response = result.get("ai_response", "No response")

    probability = churn.get("probability", 0)
    prediction_text = "YES" if churn.get("churn_prediction") else "NO"

    st.markdown("## Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Churn %", f"{int(probability*100)}%")
    with c2:
        st.metric("Risk", churn.get("risk_level", "N/A"))
    with c3:
        st.metric("Churn", prediction_text)
    with c4:
        st.metric("Health", f"{health_score}/100")

    tabs = st.tabs(["Overview", "Analytics", "AI Assistant"])

    # ---------------- OVERVIEW ----------------
    with tabs[0]:

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            title={'text': "Churn Risk"},
            gauge={'axis': {'range': [0, 100]}}
        ))

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Reasons")
        for r in churn.get("reasons", []):
            st.write("•", r)

    # ---------------- ANALYTICS ----------------
    with tabs[1]:

        df = pd.DataFrame({
            "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            "Engagement": [random.randint(1,10) for _ in range(7)]
        })

        fig = px.line(df, x="Day", y="Engagement", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- CHATBOT ----------------
    with tabs[2]:

        st.subheader("AI Assistant")

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        prompt = st.chat_input("Ask AI...")

        if prompt:

            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            with st.chat_message("user"):
                st.write(prompt)

            try:
                r = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={
                        "message": prompt,
                        "hours_spent": hours_spent,
                        "issues": issues,
                        "probability": probability
                    },
                    timeout=60
                )

                if r.status_code == 200:
                    ai_reply = r.json().get("response", "No response")
                else:
                    ai_reply = f"Error {r.status_code}"

            except Exception as e:
                ai_reply = f"Connection Error: {e}"

            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_reply
            })

            with st.chat_message("assistant"):
                st.write(ai_reply)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.markdown("Enterprise AI Retention System • Streamlit + FastAPI + AI Agents")