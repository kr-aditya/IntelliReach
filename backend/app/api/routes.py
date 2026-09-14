from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.ingestion import DocumentIngestionService
from app.rag.qa_service import RAGService
from app.services.research_pipeline import ResearchPipeline


router = APIRouter()


# ============================================================
# Request Models
# ============================================================

class ResearchRequest(BaseModel):

    company_name: str = Field(
        min_length=1,
        max_length=100,
        description="Name of the company to research.",
    )


class AskRequest(BaseModel):

    question: str = Field(
        min_length=1,
        max_length=500,
        description="Question to ask the knowledge base.",
    )


class IngestRequest(BaseModel):

    file_path: str = Field(
        min_length=1,
        description="Path to the document to ingest.",
    )


# ============================================================
# Health Check
# ============================================================

@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "IntelliReach",
    }


# ============================================================
# Company Research
# ============================================================

@router.post("/research")
def research_company(
    request: ResearchRequest,
):

    try:

        pipeline = ResearchPipeline()

        result = pipeline.run(
            request.company_name
        )

        return {
            "status": "success",
            "company_name": request.company_name,
            "result": result,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception as error:

        print(
            f"Research endpoint error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred while "
                "researching the company."
            ),
        ) from error


# ============================================================
# Document Ingestion
# ============================================================

@router.post("/ingest")
def ingest_document(
    request: IngestRequest,
):

    try:

        service = DocumentIngestionService()

        chunk_count = service.ingest_file(
            request.file_path
        )

        return {
            "status": "success",
            "message": "Document ingested successfully.",
            "chunks_stored": chunk_count,
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except ValueError as error:

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception as error:

        print(
            f"Ingestion endpoint error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred while "
                "ingesting the document."
            ),
        ) from error


# ============================================================
# RAG Question Answering
# ============================================================

@router.post("/ask")
def ask_knowledge_base(
    request: AskRequest,
):

    try:

        service = RAGService()

        result = service.ask(
            request.question
        )

        return {
            "status": "success",
            "question": request.question,
            "result": result.model_dump(),
        }

    except ValueError as error:

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception as error:

        print(
            f"RAG endpoint error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred while "
                "answering the question."
            ),
        ) from error