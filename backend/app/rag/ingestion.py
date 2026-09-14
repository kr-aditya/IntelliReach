from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from app.rag.vector_store import VectorStore


class DocumentIngestionService:

    def __init__(self) -> None:

        self.vector_store = VectorStore()

        self.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=120,
            )
        )


    def ingest_file(
        self,
        file_path: str,
    ) -> int:

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                f"File not found: {file_path}"
            )


        # ----------------------------------------------------
        # Load document
        # ----------------------------------------------------

        if path.suffix.lower() == ".pdf":

            loader = PyPDFLoader(
                str(path)
            )

        elif path.suffix.lower() == ".txt":

            loader = TextLoader(
                str(path),
                encoding="utf-8",
            )

        else:

            raise ValueError(
                "Unsupported file type. "
                "Currently supported: PDF and TXT."
            )


        documents = loader.load()


        # ----------------------------------------------------
        # Split document
        # ----------------------------------------------------

        chunks = self.text_splitter.split_documents(
            documents
        )


        # ----------------------------------------------------
        # Store chunks
        # ----------------------------------------------------

        self.vector_store.add_documents(
            chunks
        )


        return len(chunks)