import os
import asyncio
from rag.text_pipeline import ingest_text_folder
from rag.ocr_pipeline import ingest_ocr_folder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

async def initialize_vector_store():
    if os.path.exists(DB_DIR) and len(os.listdir(DB_DIR)) > 0:
        print("✅ Vector database already exists. Skipping initialization.")
        return

    print("🚀 Initializing Vector Database...")

    text_path = os.path.join(KNOWLEDGE_DIR, "text")
    if os.path.exists(text_path):
        await ingest_text_folder(text_path)

    ocr_path = os.path.join(KNOWLEDGE_DIR, "ocr")
    if os.path.exists(ocr_path):
        await ingest_ocr_folder(ocr_path)

    print("✨ Knowledge base successfully indexed.")

if __name__ == "__main__":
    asyncio.run(initialize_vector_store())