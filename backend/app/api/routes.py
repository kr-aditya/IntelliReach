from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.research_pipeline import ResearchPipeline


router = APIRouter()


# ============================================================
# Request Model
# ============================================================

class ResearchRequest(BaseModel):

    company_name: str = Field(
        min_length=1,
        max_length=100,
        description="Name of the company to research.",
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
# Research Endpoint
# ============================================================

@router.post("/research")
def research_company(request: ResearchRequest):

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

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred while "
                "researching the company."
            ),
        ) from error