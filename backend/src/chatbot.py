# =========================================================
# Chatbot Core (Production Ready + Key Vault Safe)
# =========================================================

from engine import retrieve
from prompt import build_prompt
from openai import AzureOpenAI

# 👇 Lazy secret loader (IMPORTANT FIX)
from config import get_secret

# =========================================================
# AZURE OPENAI CLIENT (SAFE INIT)
# =========================================================
client = AzureOpenAI(
    api_key=get_secret("openAI-key"),
    api_version="2024-02-01",
    azure_endpoint=get_secret("openAI-endpoint")
)

DEPLOYMENT_NAME = "gpt-4o"


# =========================================================
def chat(query: str):

    print(f"\n🔵 USER QUERY: {query}")

    # ---------------- SIMPLE RULE BASED ----------------
    if query.lower().strip() in ["hi", "hello", "hey"]:
        return {
            "answer": "Hello 👋 How can I help you?",
            "strategy": "rule_based"
        }

    # ---------------- RETRIEVE DOCS ----------------
    docs = retrieve(query)

    print("📦 RAW DOCS:", docs)

    # ---------------- NORMALIZE ----------------
    if isinstance(docs, str):
        docs = [docs]

    if not docs:
        return {
            "answer": "No relevant information found in banking knowledge base.",
            "strategy": "no_retrieval"
        }

    # ---------------- BUILD PROMPT ----------------
    prompt = build_prompt(query, docs)

    print("🧠 PROMPT SENT TO LLM:\n", prompt)

    # ---------------- LLM CALL ----------------
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a banking AI assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ LLM ERROR:", e)

        return {
            "answer": "System error while generating response.",
            "strategy": "llm_error"
        }

    # ---------------- RETURN ----------------
    return {
        "answer": answer,
        "strategy": "vector/hybrid"
    }


# =========================================================
# LOCAL TEST
# =========================================================
if __name__ == "__main__":

    print("🚀 Chatbot Test Mode Started")

    while True:
        q = input("\nAsk: ")

        if q.lower() in ["exit", "quit"]:
            break

        result = chat(q)

        print("\n🤖 RESPONSE:")
        print(result)
