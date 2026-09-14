from pydantic import BaseModel


class HealthResponse(BaseModel):

    status: str
    service: str


class ResearchResponse(BaseModel):

    status: str
    company_name: str
    result: dict


class IngestResponse(BaseModel):

    status: str
    message: str
    chunks_stored: int


class AskResponse(BaseModel):

    status: str
    question: str
    result: dict