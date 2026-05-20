import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

VAULT_URL = "https://bank-vault.vault.azure.net/"

credential = DefaultAzureCredential()

client = SecretClient(
    vault_url=VAULT_URL,
    credential=credential
)

# =========================
# LAZY LOADING (IMPORTANT FIX)
# =========================


def get_secret(name: str):
    return client.get_secret(name).value


# =========================
# OPTIONAL CACHED LOADING
# =========================
OPENAI_KEY = None
OPENAI_ENDPOINT = None
SEARCH_KEY = None
SEARCH_ENDPOINT = None


def load_secrets():
    global OPENAI_KEY, OPENAI_ENDPOINT, SEARCH_KEY, SEARCH_ENDPOINT

    OPENAI_KEY = get_secret("openAI-key")
    OPENAI_ENDPOINT = get_secret("openAI-endpoint")
    SEARCH_KEY = get_secret("AIsearch-key")
    SEARCH_ENDPOINT = get_secret("AIsearch-endpoint")
