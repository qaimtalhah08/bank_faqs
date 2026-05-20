# ============================
# Split documents into chunks (AZURE SAFE VERSION)
# ============================

import os
import re
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Folder where your .txt files are stored
FOLDER_PATH = "./data/clean_data"

# Text splitter configuration
# chunk_size = size of each text part
# chunk_overlap = overlap between chunks for better context
splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100
)


def chunk_documents(folder_path=FOLDER_PATH):

    # List to store all chunks
    all_chunks = []

    # Loop through all files in folder
    for file in os.listdir(folder_path):

        # Only process .txt files
        if not file.endswith(".txt"):
            continue

        # Full file path
        path = os.path.join(folder_path, file)

        # Read file content
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()

            # Skip empty files
            if not text:
                continue

            # Split text into chunks
            chunks = splitter.split_text(text)

            # 🔥 CLEAN FILE NAME (remove .txt + unsafe chars)
            clean_file = re.sub(r'[^a-zA-Z0-9_-]', '',
                                file.replace(".txt", ""))

            # Process each chunk
            for i, chunk in enumerate(chunks):

                # 🔥 CREATE STABLE HASH (first 20 chars only)
                # This ensures unique + consistent ID
                chunk_hash = hashlib.md5(
                    chunk[:20].encode("utf-8")
                ).hexdigest()[:8]

                # Final Azure-safe document ID
                doc_id = f"{clean_file}_{i}_{chunk_hash}"

                all_chunks.append({
                    "id": doc_id,          # Unique safe ID
                    "content": chunk,      # Chunk text
                    "source": file         # Original file name
                })

    # Debug info
    print("📁 Files processed:", len(os.listdir(folder_path)))
    print("📦 Total chunks:", len(all_chunks))

    return all_chunks
