from app.rag.vector_store import VectorStore


def main():
    vector_store = VectorStore()

    count_before = vector_store.get_document_count()

    print("\n==============================")
    print("INTELLIREACH RAG RESET")
    print("==============================")

    print(
        f"\nStored chunks before reset: {count_before}"
    )

    vector_store.clear()

    count_after = vector_store.get_document_count()

    print(
        f"Stored chunks after reset: {count_after}"
    )

    print("\n✓ Knowledge base reset successfully.")


if __name__ == "__main__":
    main()