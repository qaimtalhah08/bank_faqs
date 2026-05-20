# ============================
# LLM Reranker (Key Vault Secured)
# ============================

import json
from openai import AzureOpenAI

# 👇 SAFE SECRET LOADER
from config import get_secret


# ============================
# AZURE CLIENT (LAZY SAFE INIT)
# ============================
client = AzureOpenAI(
    api_key=get_secret("openAI-key"),
    api_version="2024-02-01",
    azure_endpoint=get_secret("openAI-endpoint")
)

DEPLOYMENT_NAME = "gpt-4o"


# ============================
# RERANK FUNCTION
# ============================
def rerank(query, docs):

    if not docs:
        return []

    # ============================
    # FORMAT DOCS
    # ============================
    formatted_docs = "\n".join(
        f"{i+1}. {doc}"
        for i, doc in enumerate(docs)
    )

    # ============================
    # PROMPT
    # ============================
    prompt = f"""
You are a ranking system.

Task:
Rank documents by relevance.

RULES:
- Return ONLY JSON array
- Each item must be index number only
- No explanation

Query:
{query}

Documents:
{formatted_docs}

Output:
[2, 1, 3]
"""

    # ============================
    # LLM CALL
    # ============================
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a strict ranking engine. Return only JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()

    # ============================
    # PARSE
    # ============================
    try:
        order = json.loads(result)

        reranked = [
            docs[i - 1]
            for i in order
            if 0 < i <= len(docs)
        ]

        return reranked

    except Exception:
        return docs
