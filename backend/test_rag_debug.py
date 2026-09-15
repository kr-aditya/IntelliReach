from app.rag.vector_store import VectorStore


def main():
    vector_store = VectorStore()

    count = vector_store.get_document_count()

    print("\n==============================")
    print("INTELLIREACH RAG DEBUG")
    print("==============================")

    print(f"\nStored chunks: {count}")

    if count == 0:
        print("\n❌ ChromaDB is empty.")
        return

    question = "What is the name of the candidate?"

    print(f"\nQuestion: {question}")

    documents = vector_store.similarity_search(
        question,
        k=4,
    )

    print(
        f"\nRetrieved documents: {len(documents)}"
    )

    for index, document in enumerate(
        documents,
        start=1,
    ):
        print(
            f"\n--- Document {index} ---"
        )

        print(
            document.page_content[:1000]
        )

        print(
            "\nMetadata:",
            document.metadata,
        )


if __name__ == "__main__":
    main()