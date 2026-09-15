from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_DIR = BASE_DIR / "chroma_db"


class VectorStore:
    """
    Persistent ChromaDB vector store for IntelliReach.

    Uploaded company documents are stored as document chunks
    inside the intellireach_documents collection.
    """

    COLLECTION_NAME = "intellireach_documents"

    def __init__(self) -> None:
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = Chroma(
            collection_name=self.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=str(CHROMA_DIR),
        )

    def add_documents(self, documents) -> None:
        """
        Add document chunks to ChromaDB.
        """

        if not documents:
            raise ValueError(
                "No document chunks were provided."
            )

        self.vector_store.add_documents(documents)

    def get_retriever(self):
        """
        Return the retriever used by the RAG layer.

        We intentionally retrieve more chunks than the old
        configuration so that short factual questions have
        a better chance of finding the relevant chunk.
        """

        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 8,
            },
        )

    def get_document_count(self) -> int:
        """
        Return the number of stored chunks.
        """

        return self.vector_store._collection.count()

    def similarity_search(
        self,
        query: str,
        k: int = 8,
    ):
        """
        Run a direct similarity search.

        Useful for debugging retrieval independently
        from the LLM.
        """

        return self.vector_store.similarity_search(
            query,
            k=k,
        )

    def clear(self) -> None:
        """
        Delete all documents from the current Chroma collection.

        This is primarily useful during development/testing.
        """

        self.vector_store.delete_collection()

        self.vector_store = Chroma(
            collection_name=self.COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=str(CHROMA_DIR),
        )