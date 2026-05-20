from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# 👇 SAFE SECRET LOADER
from config import get_secret


# =========================================================
# SEARCH CLIENT (SAFE INIT)
# =========================================================
client = SearchClient(
    endpoint=get_secret("AIsearch-endpoint"),
    index_name="bank-index",
    credential=AzureKeyCredential(get_secret("AIsearch-key"))
)


# =========================================================
# SIMPLE SEARCH
# =========================================================
def search_docs(query: str):

    results = client.search(
        search_text=query,
        top=5
    )

    docs = []

    for r in results:
        docs.append(r.get("content"))

    return docs
