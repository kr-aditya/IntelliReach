from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

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

@router.post("/research",
    summary="Research a company and generate outreach",
)
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

@router.post("/ingest",
    summary="Upload and ingest a company document",
)
async def ingest_document(
    file: UploadFile = File(...)
):

    allowed_extensions = {
        ".pdf",
        ".txt",
    }

    file_extension = (
        Path(file.filename or "")
        .suffix
        .lower()
    )

    if file_extension not in allowed_extensions:

        raise HTTPException(
            status_code=422,
            detail=(
                "Unsupported file type. "
                "Only PDF and TXT files are allowed."
            ),
        )


    try:

        file_bytes = await file.read()

        max_file_size = 10 * 1024 * 1024

        if len(file_bytes) > max_file_size:

         raise HTTPException(
          status_code=413,
          detail=(
            "File is too large. "
            "Maximum supported size is 10 MB."
        ),
    )

        if not file_bytes:

            raise HTTPException(
                status_code=422,
                detail="Uploaded file is empty.",
            )


        with NamedTemporaryFile(
            suffix=file_extension,
            delete=False,
        ) as temp_file:

            temp_file.write(
                file_bytes
            )

            temp_path = temp_file.name


        try:

            service = DocumentIngestionService()

            chunk_count = service.ingest_file(
                temp_path
            )

        finally:

            Path(temp_path).unlink(
                missing_ok=True
            )


        return {
            "status": "success",
            "message": (
                "Document ingested successfully."
            ),
            "filename": file.filename,
            "chunks_stored": chunk_count,
        }


    except HTTPException:

        raise


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

@router.post("/ask",
    summary="Ask the company knowledge base",
)
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