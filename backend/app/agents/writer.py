from pydantic import BaseModel, Field
from crewai import Agent, LLM


# ============================================================
# Structured Writer Output
# ============================================================

class OutreachResult(BaseModel):

    email: str = Field(
        description=(
            "A personalized B2B outreach email of approximately "
            "100 to 120 words."
        )
    )

    talking_points: list[str] = Field(
        description=(
            "Exactly three concise talking points for a sales call."
        )
    )


# ============================================================
# Writer LLM
# ============================================================

writer_llm = LLM(
    model="groq/openai/gpt-oss-20b",
    temperature=0.3,
    max_tokens=400,
    reasoning_effort="low",
)


# ============================================================
# Writer Agent Factory
# ============================================================

def create_writer() -> Agent:

    return Agent(
        role="B2B Outreach Copywriter",

        goal=(
            "Transform company research and sales intelligence "
            "into concise, credible, and highly personalized "
            "B2B outreach communication."
        ),

        backstory=(
            "You are an experienced B2B technology sales copywriter. "
            "You write concise outreach that demonstrates genuine "
            "understanding of the prospect's business. "
            "You avoid generic sales language, exaggerated claims, "
            "unsupported statistics, and unnecessary buzzwords."
        ),

        llm=writer_llm,

        verbose=True,
    )