import streamlit as st
import requests
import time
import pandas as pd
import plotly.express as px
import numpy as np

# =========================
# CONFIG
# =========================
API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="Banking AI Observability",
    layout="wide"
)

st.title("🚀 Banking AI Production Observability Dashboard")
st.caption("RAG + Agent + Memory + Performance Monitoring")

# =========================
# STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []


# =========================
# API CALL
# =========================
def call_api(question: str):

    start = time.time()

    try:
        res = requests.post(
            API_URL,
            json={"question": question},
            timeout=20
        )

        data = res.json()

        return (
            data.get("answer", ""),
            data.get("strategy", "unknown"),
            round(time.time() - start, 3),
            False
        )

    except Exception as e:
        return str(e), "error", round(time.time() - start, 3), True


# =========================
# METRICS
# =========================
history = st.session_state.history

col1, col2, col3, col4, col5 = st.columns(5)

if history:
    df = pd.DataFrame(history)

    col1.metric("Requests", len(df))
    col2.metric("Avg Latency", round(df["latency"].mean(), 3))
    col3.metric("Error Rate", f"{round(df['error'].mean()*100, 2)}%")
    col4.metric("P95 Latency", round(np.percentile(df["latency"], 95), 3))
    col5.metric("Success Rate", f"{round((1-df['error'].mean())*100, 2)}%")

else:
    col1.metric("Requests", 0)
    col2.metric("Avg Latency", 0)
    col3.metric("Error Rate", "0%")
    col4.metric("P95 Latency", 0)
    col5.metric("Success Rate", "0%")


# =========================
# CHAT
# =========================
st.markdown("---")
st.subheader("💬 Live Query Testing")

query = st.text_input("Ask Banking AI")

if st.button("Send") and query:

    answer, strategy, latency, error = call_api(query)

    st.session_state.history.append({
        "query": query,
        "answer": answer,
        "strategy": strategy,
        "latency": latency,
        "error": error,
        "length": len(answer),
        "timestamp": time.time()
    })

    st.success("Logged")


# =========================
# STRATEGY HEALTH
# =========================
st.markdown("---")
st.subheader("🧠 Strategy Health")

if history:

    df = pd.DataFrame(history)

    fig = px.histogram(
        df,
        x="strategy",
        color="error",
        title="Strategy vs Error Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================
# LATENCY DISTRIBUTION
# =========================
st.subheader("⚡ Latency Distribution")

if history:

    df = pd.DataFrame(history)

    fig = px.box(
        df,
        y="latency",
        points="all",
        title="Latency Spread"
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================
# QUALITY SCORE (SMARTER)
# =========================
st.subheader("🧠 Response Quality Score")

if history:

    df = pd.DataFrame(history)

    def quality(row):
        if row["error"]:
            return 0.2
        if "don't have enough" in row["answer"].lower():
            return 0.3
        if row["length"] > 300:
            return 0.9
        if row["length"] > 100:
            return 0.7
        return 0.5

    df["quality"] = df.apply(quality, axis=1)

    st.metric("Avg Quality Score", round(df["quality"].mean(), 2))

    st.progress(df["quality"].mean())


# =========================
# SEARCH LOGS
# =========================
st.markdown("---")
st.subheader("📊 Full Logs")

if history:

    df = pd.DataFrame(history)

    search = st.text_input("Search Query Logs")

    if search:
        df = df[df["query"].str.contains(search, case=False)]

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download Logs",
        df.to_csv(index=False),
        file_name="logs.csv"
    )


# =========================
# SYSTEM LOAD SIMULATION
# =========================
st.markdown("---")
st.subheader("⚡ Load Test")

test_cases = [
    "what is kyc",
    "how to open account",
    "how to apply loan",
    "how to block card",
    "credit vs debit card"
]

if st.button("Run Load Test"):

    results = []

    for q in test_cases:

        answer, strategy, latency, error = call_api(q)

        results.append({
            "question": q,
            "strategy": strategy,
            "latency": latency,
            "error": error,
            "score": 1 if not error else 0.2
        })

    df = pd.DataFrame(results)

    st.dataframe(df)

    st.plotly_chart(
        px.bar(df, x="question", y="latency", color="strategy")
    )

    st.success(f"System Health Score: {df['score'].mean():.2f}")
