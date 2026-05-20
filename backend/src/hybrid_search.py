from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential

from embedding import get_embeddings

# 👇 SAFE SECRET LOADER
from config import get_secret


# =========================================================
# SEARCH CLIENT (SAFE INIT)
# =========================================================
search_client = SearchClient(
    endpoint=get_secret("AIsearch-endpoint"),
    index_name="bank-index",
    credential=AzureKeyCredential(get_secret("AIsearch-key"))
)


# =========================================================
# HYBRID SEARCH
# =========================================================
def hybrid_search(query: str):

    # ============================
    # 1. EMBEDDING
    # ============================
    vector = get_embeddings([query])

    if not vector:
        return []

    vector = vector[0]  # flatten

    # ============================
    # 2. SEARCH
    # ============================
    results = search_client.search(
        search_text=query,
        vector_queries=[
            VectorizedQuery(
                vector=vector,
                k_nearest_neighbors=5,
                fields="embedding"
            )
        ],
        top=5
    )

    # ============================
    # 3. FORMAT RESULTS
    # ============================
    docs = []

    for r in results:
        docs.append({
            "content": r.get("content"),
            "score": r.get("@search.score", 0)
        })

    return docs
