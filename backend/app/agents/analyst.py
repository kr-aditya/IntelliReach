from pydantic import BaseModel, Field
from crewai import Agent, LLM


# ============================================================
# Structured Analyst Output
# ============================================================

class SalesAnalysis(BaseModel):

    pain_points: list[str] = Field(
        description=(
            "Three realistic business or operational pain points "
            "inferred from the company research."
        )
    )

    strongest_opportunity: str = Field(
        description=(
            "The single strongest AI or automation opportunity "
            "for the company."
        )
    )

    business_value: str = Field(
        description=(
            "The potential business value of addressing the "
            "strongest opportunity."
        )
    )

    outreach_hook: str = Field(
        description=(
            "A concise personalized angle that can be used "
            "in a B2B outreach message."
        )
    )


# ============================================================
# Analyst LLM
# ============================================================

analyst_llm = LLM(
    model="groq/openai/gpt-oss-20b",
    temperature=0.1,
    max_tokens=350,
    reasoning_effort="low",
)


# ============================================================
# Analyst Agent Factory
# ============================================================

def create_analyst() -> Agent:

    return Agent(
        role="B2B Sales Intelligence Analyst",

        goal=(
            "Analyze structured company research and identify "
            "the most relevant business pain points, AI or "
            "automation opportunities, and sales angles."
        ),

        backstory=(
            "You are an experienced B2B sales intelligence analyst. "
            "You translate factual company research into practical "
            "sales insights. You distinguish evidence from assumptions, "
            "avoid exaggerated claims, and focus on realistic business "
            "opportunities."
        ),

        llm=analyst_llm,

        verbose=True,
    )