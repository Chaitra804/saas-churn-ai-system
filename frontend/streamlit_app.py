import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime

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

/* Background */
.stApp {
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );
    color: white;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.98);
    border-right: 1px solid rgba(34,211,238,0.15);
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 3.8rem;
    font-weight: 800;
    color: #22d3ee;
    text-shadow: 0px 0px 25px rgba(34,211,238,0.5);
}

/* Subtitle */
.sub-title {
    text-align: center;
    color: #cbd5e1;
    font-size: 1.2rem;
    margin-bottom: 40px;
}

/* Cards */
.custom-card {
    background: rgba(17,24,39,0.92);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(34,211,238,0.15);
    box-shadow: 0px 0px 20px rgba(34,211,238,0.08);
    margin-bottom: 20px;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(
        90deg,
        #06b6d4,
        #0891b2
    );
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 20px;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

/* Metrics */
[data-testid="metric-container"] {
    background: rgba(17,24,39,0.92);
    border: 1px solid rgba(34,211,238,0.18);
    padding: 15px;
    border-radius: 18px;
    box-shadow: 0px 0px 15px rgba(34,211,238,0.08);
}

/* Footer */
.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("AI Retention Platform")

    st.markdown("---")

    st.markdown("""
### Enterprise Features

- AI Churn Prediction
- Customer Risk Analytics
- Conversational AI Assistant
- Retention Intelligence
- Sentiment Detection
- Engagement Analytics
- KPI Monitoring
- Downloadable Reports
""")

    st.markdown("---")

    st.success("System Status: Online")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown(
    """
    <div class='main-title'>
        Enterprise AI Retention Platform
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='sub-title'>
        Intelligent SaaS Churn Prediction & Customer Success Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------

left, right = st.columns(2)

with left:

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

    st.subheader("Customer Engagement")

    hours_spent = st.slider(
        "Hours Spent on Platform",
        0,
        50,
        5
    )

    health_score = max(0, min(100, hours_spent * 2))

    st.progress(health_score / 100)

    st.write(f"Customer Health Score: {health_score}/100")

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)

    st.subheader("Customer Issues")

    issues = st.text_area(
        "Describe customer issues",
        height=180,
        placeholder="Example: App crashes frequently and dashboard is confusing"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

analyze = st.button("Analyze Customer")

if analyze:

    payload = {
        "hours_spent": hours_spent,
        "issues": issues
    }

    try:

        response = requests.post(
            "http://127.0.0.1:8000/analyze",
            json=payload
        )

        st.session_state.result = response.json()
        st.session_state.analysis_done = True

    except Exception as e:

        st.error(f"Backend Error: {e}")

# ---------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------

if st.session_state.analysis_done:

    result = st.session_state.result

    churn = result["churn_analysis"]
    issue_analysis = result["issue_analysis"]
    ai_response = result["ai_response"]

    probability = churn["probability"]

    prediction_text = (
        "YES"
        if churn["churn_prediction"]
        else "NO"
    )

    # ---------------------------------------------------
    # KPI SECTION
    # ---------------------------------------------------

    st.markdown("## Executive Analytics Dashboard")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "Churn Probability",
            f"{int(probability * 100)}%"
        )

    with k2:
        st.metric(
            "Risk Level",
            churn["risk_level"]
        )

    with k3:
        st.metric(
            "Customer Churning",
            prediction_text
        )

    with k4:
        st.metric(
            "Health Score",
            f"{health_score}/100"
        )

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------

    tabs = st.tabs([
        "Overview",
        "Analytics",
        "AI Assistant",
        "Insights",
        "Customer Health"
    ])

    # ---------------------------------------------------
    # OVERVIEW TAB
    # ---------------------------------------------------

    with tabs[0]:

        c1, c2 = st.columns(2)

        with c1:

            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability * 100,
                title={'text': "Churn Risk"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': '#22d3ee'}
                }
            ))

            gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                height=350
            )

            st.plotly_chart(
                gauge,
                use_container_width=True
            )

        with c2:

            st.markdown(
                "<div class='custom-card'>",
                unsafe_allow_html=True
            )

            st.subheader("Top Churn Reasons")

            for reason in churn["reasons"]:
                st.write(f"• {reason}")

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    # ---------------------------------------------------
    # ANALYTICS TAB
    # ---------------------------------------------------

    with tabs[1]:

        chart1, chart2 = st.columns(2)

        with chart1:

            df = pd.DataFrame({
                "Day": [
                    "Mon", "Tue", "Wed",
                    "Thu", "Fri", "Sat", "Sun"
                ],
                "Engagement": [
                    random.randint(1, 10)
                    for _ in range(7)
                ]
            })

            fig = px.line(
                df,
                x="Day",
                y="Engagement",
                markers=True,
                title="Weekly Engagement Trend"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with chart2:

            pie = go.Figure(
                data=[go.Pie(
                    labels=["Retention", "Churn"],
                    values=[
                        100 - int(probability * 100),
                        int(probability * 100)
                    ]
                )]
            )

            pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )

            st.plotly_chart(
                pie,
                use_container_width=True
            )

    # ---------------------------------------------------
    # AI ASSISTANT TAB
    # ---------------------------------------------------

    with tabs[2]:

        st.markdown(
            "<div class='custom-card'>",
            unsafe_allow_html=True
        )

        st.subheader("Interactive AI Retention Assistant")

        # Chat history

        for msg in st.session_state.messages:

            with st.chat_message(msg["role"]):

                st.write(msg["content"])

        # Chat input

        prompt = st.chat_input(
            "Ask the AI retention assistant..."
        )

        if prompt:

            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            with st.chat_message("user"):

                st.write(prompt)

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "message": prompt,
                        "hours_spent": hours_spent,
                        "issues": issues,
                        "probability": probability
                    },
                    timeout=60
                )

                if response.status_code == 200:

                    ai_reply = response.json().get(
                        "response",
                        "No response generated."
                    )

                else:

                    ai_reply = (
                        f"Backend Error: "
                        f"{response.status_code}"
                    )

            except Exception as e:

                ai_reply = (
                    f"Connection Error: {str(e)}"
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_reply
            })

            with st.chat_message("assistant"):

                st.write(ai_reply)

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # ---------------------------------------------------
    # INSIGHTS TAB
    # ---------------------------------------------------

    with tabs[3]:

        st.markdown(
            "<div class='custom-card'>",
            unsafe_allow_html=True
        )

        st.subheader("Retention Insights")

        insights = [
            "Low engagement increases churn risk.",
            "Technical issues negatively impact retention.",
            "Fast support improves customer satisfaction.",
            "Customer onboarding reduces early churn.",
            "AI-driven engagement campaigns improve retention."
        ]

        for insight in insights:
            st.write(f"• {insight}")

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # ---------------------------------------------------
    # CUSTOMER HEALTH TAB
    # ---------------------------------------------------

    with tabs[4]:

        health_df = pd.DataFrame({
            "Category": [
                "Engagement",
                "Satisfaction",
                "Retention",
                "Activity",
                "Loyalty"
            ],
            "Score": [
                random.randint(40, 100),
                random.randint(40, 100),
                random.randint(40, 100),
                random.randint(40, 100),
                random.randint(40, 100)
            ]
        })

        radar = go.Figure()

        radar.add_trace(go.Scatterpolar(
            r=health_df["Score"],
            theta=health_df["Category"],
            fill='toself'
        ))

        radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title="Customer Health Radar"
        )

        st.plotly_chart(
            radar,
            use_container_width=True
        )

    # ---------------------------------------------------
    # DOWNLOAD REPORT
    # ---------------------------------------------------

    report = f"""
Enterprise AI Retention Report

Generated: {datetime.now()}

----------------------------------
CUSTOMER ANALYSIS
----------------------------------

Churn Probability: {int(probability * 100)}%
Risk Level: {churn['risk_level']}
Customer Churning: {prediction_text}

----------------------------------
DETECTED ISSUES
----------------------------------

{chr(10).join(issue_analysis['detected_issues'])}

----------------------------------
RECOMMENDATIONS
----------------------------------

{chr(10).join(issue_analysis['recommendations'])}

----------------------------------
AI RESPONSE
----------------------------------

{ai_response}
"""

    st.download_button(
        label="Download AI Retention Report",
        data=report,
        file_name="ai_retention_report.txt",
        mime="text/plain"
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(
    """
    <div class='footer'>
        Enterprise AI Retention Platform • FastAPI + Streamlit + AI Agents
    </div>
    """,
    unsafe_allow_html=True
)