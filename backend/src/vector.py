from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from chunking import chunk_documents

# 👇 SAFE KEY VAULT ACCESS
from config import get_secret


# ============================
# AZURE OPENAI CLIENT
# ============================
client = AzureOpenAI(
    api_key=get_secret("openAI-key"),
    api_version="2024-02-01",
    azure_endpoint=get_secret("openAI-endpoint")
)

DEPLOYMENT_NAME = "embedding-model"


# ============================
# EMBEDDING FUNCTION
# ============================
def get_embedding(text: str):

    try:
        response = client.embeddings.create(
            model=DEPLOYMENT_NAME,
            input=text
        )

        return response.data[0].embedding

    except Exception as e:
        print("❌ Embedding error:", e)
        return None


# ============================
# SEARCH CLIENT
# ============================
search_client = SearchClient(
    endpoint=get_secret("AIsearch-endpoint"),
    index_name="bank-index",
    credential=AzureKeyCredential(get_secret("AIsearch-key"))
)


# ============================
# LOAD DATA
# ============================
texts = chunk_documents()
documents = []

print(f"📦 Total chunks: {len(texts)}")


# ============================
# BUILD VECTOR STORE
# ============================
for i, text in enumerate(texts):

    embedding = get_embedding(text)

    if embedding is None:
        continue

    documents.append({
        "id": str(i),
        "content": text,
        "embedding": embedding
    })


# ============================
# UPLOAD TO AZURE SEARCH
# ============================
try:
    result = search_client.upload_documents(documents)

    print(f"✅ Upload successful: {len(documents)} documents indexed")

except Exception as e:
    print("❌ Upload error:", e)
