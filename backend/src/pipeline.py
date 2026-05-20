import time

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from chunking import chunk_documents
from embedding import get_embeddings

# 👇 SAFE SECRET LOADER (IMPORTANT FIX)
from config import get_secret


# =========================================================
# AZURE SEARCH CLIENT (SAFE INIT)
# =========================================================
search_client = SearchClient(
    endpoint=get_secret("AIsearch-endpoint"),
    index_name="bank-index",
    credential=AzureKeyCredential(get_secret("AIsearch-key"))
)


# =========================================================
# CONFIG
# =========================================================
EMBED_BATCH_SIZE = 5
UPLOAD_BATCH_SIZE = 50
RETRY = 3
DELAY_BETWEEN_BATCHES = 2


# =========================================================
# MAIN PIPELINE
# =========================================================
def upload_data():

    print("🚀 PIPELINE STARTED...\n")

    chunks = chunk_documents()

    print(f"📦 Total chunks: {len(chunks)}\n")

    documents = []

    # =====================================================
    # EMBEDDING LOOP
    # =====================================================
    for i in range(0, len(chunks), EMBED_BATCH_SIZE):

        batch = chunks[i:i + EMBED_BATCH_SIZE]

        print(f"⚙️ Processing {i} → {i+len(batch)} / {len(chunks)}")

        texts = [c["content"] for c in batch]

        embeddings = get_embeddings(texts)

        for chunk, embedding in zip(batch, embeddings):

            if not embedding:
                continue

            # flatten safety
            if isinstance(embedding[0], list):
                embedding = embedding[0]

            documents.append({
                "id": chunk["id"],
                "content": chunk["content"],
                "source": chunk["source"],
                "embedding": embedding
            })

        # =================================================
        # UPLOAD BATCH
        # =================================================
        if len(documents) >= UPLOAD_BATCH_SIZE:

            upload_with_retry(documents)
            documents = []

        time.sleep(DELAY_BETWEEN_BATCHES)

    # FINAL UPLOAD
    if documents:
        upload_with_retry(documents)

    print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY")


# =========================================================
# RETRY LOGIC
# =========================================================
def upload_with_retry(batch):

    for attempt in range(RETRY):

        try:
            search_client.upload_documents(batch)

            print(f"✅ Uploaded batch ({len(batch)} docs)")
            return

        except Exception as e:
            print(f"❌ Upload error (try {attempt+1}): {e}")
            time.sleep(2 ** attempt)

    print("❌ FAILED AFTER RETRIES")


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    upload_data()
