# ============================
# Simple embedding cache
# ============================

embedding_cache = {}


def get_cached_embedding(text, embed_func):
    """
    Prevent duplicate API calls
    """

    if text in embedding_cache:
        return embedding_cache[text]

    emb = embed_func(text)
    embedding_cache[text] = emb

    return emb
