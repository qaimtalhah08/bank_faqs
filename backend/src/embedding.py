import time
from openai import AzureOpenAI

# 👇 SAFE IMPORT (lazy secret access)
from config import get_secret


# =========================================================
# AZURE OPENAI CLIENT (SAFE INIT)
# =========================================================
client = AzureOpenAI(
    api_key=get_secret("openAI-key"),
    api_version="2024-02-01",
    azure_endpoint=get_secret("openAI-endpoint")
)

# IMPORTANT:
# Must match Azure deployment name
DEPLOYMENT_NAME = "embedding-model"


# =========================================================
# GET EMBEDDINGS (BATCH SAFE)
# =========================================================
def get_embeddings(texts, max_retries=3):
    """
    Generate embeddings for multiple texts (batch processing)
    """

    for attempt in range(max_retries):

        try:
            res = client.embeddings.create(
                model=DEPLOYMENT_NAME,
                input=texts
            )

            return [d.embedding for d in res.data]

        except Exception as e:
            print(f"❌ Embedding error (try {attempt+1}):", e)
            time.sleep(2)

    return [None] * len(texts)
