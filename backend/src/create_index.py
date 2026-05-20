from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)

from azure.core.credentials import AzureKeyCredential

# 👇 SAFE IMPORT (lazy loading)
from config import get_secret

INDEX_NAME = "bank-index"


# =========================================================
# SEARCH CLIENT (SAFE INIT)
# =========================================================
client = SearchIndexClient(
    endpoint=get_secret("AIsearch-endpoint"),
    credential=AzureKeyCredential(get_secret("AIsearch-key"))
)


# =========================================================
# CREATE INDEX
# =========================================================
def create_index():

    index = SearchIndex(
        name=INDEX_NAME,

        fields=[

            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True
            ),

            SearchableField(
                name="content",
                type=SearchFieldDataType.String
            ),

            SearchableField(
                name="source",
                type=SearchFieldDataType.String
            ),

            SearchField(
                name="embedding",
                type=SearchFieldDataType.Collection(
                    SearchFieldDataType.Single
                ),
                searchable=True,
                vector_search_dimensions=1536,
                vector_search_profile_name="vec-profile"
            )
        ],

        vector_search=VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(name="hnsw")
            ],

            profiles=[
                VectorSearchProfile(
                    name="vec-profile",
                    algorithm_configuration_name="hnsw"
                )
            ]
        )
    )

    client.create_or_update_index(index)

    print("✅ Index created successfully")


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    create_index()
