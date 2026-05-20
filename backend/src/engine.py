from openai import AzureOpenAI

from hybrid_search import hybrid_search
from search import search_docs

# 👇 SAFE SECRET LOADING (IMPORTANT FIX)
from config import get_secret


# ============================
# AZURE CLIENT (SAFE INIT)
# ============================
client = AzureOpenAI(
    api_key=get_secret("openAI-key"),
    api_version="2024-02-01",
    azure_endpoint=get_secret("openAI-endpoint")
)

DEPLOYMENT_NAME = "gpt-4o"


# ============================
# MEMORY (SESSION LEVEL)
# ============================
memory_store = []


def save_to_memory(user_query, response):
    memory_store.append({
        "user": user_query,
        "assistant": response
    })


def get_memory_context():
    return "\n".join(
        f"User: {m['user']}\nAI: {m['assistant']}"
        for m in memory_store[-5:]
    )


# ============================
# QUERY NORMALIZATION
# ============================
def normalize_query(query: str):

    q = query.lower()

    if "apply" in q and "loan" in q:
        return query + " loan application process requirements documents"

    if "card" in q and "block" in q:
        return query + " credit card blocking freeze deactivate"

    if "card" in q and "activate" in q:
        return query + " activate credit card pin setup"

    return query


# ============================
# AGENT ROUTER
# ============================
def agent_router(query: str, context: str):

    prompt = f"""
You are an AI routing engine.

Choose ONE:
- vector_search
- hybrid_search
- direct_answer

Rules:
- factual/simple → vector_search
- complex/ambiguous → hybrid_search
- greeting → direct_answer

Return ONLY ONE WORD.

Context:
{context}

Query:
{query}
"""

    res = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "Routing engine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return res.choices[0].message.content.strip().lower()


# ============================
# MAIN ENGINE
# ============================
def retrieve(query: str):

    memory_context = get_memory_context()
    query = normalize_query(query)

    strategy = agent_router(query, memory_context)

    print(f"\n🚀 Strategy Used: {strategy}")

    # ---------------- ROUTING ----------------
    if strategy == "vector_search":
        docs = search_docs(query)

    elif strategy == "hybrid_search":
        docs = hybrid_search(query)

    else:
        answer = "Hello! I can help you with banking queries."
        save_to_memory(query, answer)
        return answer

    # ---------------- SAFETY ----------------
    if not docs:
        fallback = "I don't have enough information in the provided data."
        save_to_memory(query, fallback)
        return fallback

    # ---------------- FILTER ----------------
    if isinstance(docs, list):
        docs = [
            d for d in docs
            if isinstance(d, dict) and d.get("score", 0) >= 0.1
        ]

    # ---------------- CONTEXT ----------------
    context = "\n".join(
        d.get("content", str(d)) if isinstance(d, dict) else str(d)
        for d in docs[:3]
    )

    if not context.strip():
        context = "No relevant banking information found."

    # ---------------- LLM ----------------
    prompt = f"""
You are a BANKING CUSTOMER SUPPORT ASSISTANT.

Context:
{context}

User Question:
{query}

Instructions:
- Use context first
- Be concise and correct
- No hallucination

Final Answer:
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "Banking assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    answer = response.choices[0].message.content.strip()

    save_to_memory(query, answer)

    return answer


# ============================
# TEST MODE
# ============================
if __name__ == "__main__":

    print("🚀 Advanced AI Engine Started")

    while True:
        q = input("\nAsk: ")

        if q.lower() in ["exit", "quit"]:
            break

        print("\n🤖", retrieve(q))
