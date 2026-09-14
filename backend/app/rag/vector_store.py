from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# ============================================================
# Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# Vector Store
# ============================================================

class VectorStore:

    def __init__(self) -> None:

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = Chroma(
            collection_name="intellireach_documents",
            embedding_function=self.embeddings,
            persist_directory=str(CHROMA_DIR),
        )


    # ========================================================
    # Add Documents
    # ========================================================

    def add_documents(self, documents):

        self.vector_store.add_documents(
            documents
        )


    # ========================================================
    # Retriever
    # ========================================================

    def get_retriever(self):

        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 4
            },
        )