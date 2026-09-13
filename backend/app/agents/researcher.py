from pydantic import BaseModel, Field
from crewai import Agent, LLM


class CompanyResearch(BaseModel):
    company_name: str = Field(
        description="The researched company name."
    )

    overview: str = Field(
        description="A concise description of what the company does."
    )

    products_services: list[str] = Field(
        description="The company's main products or services."
    )

    target_market: str = Field(
        description="The company's primary customers or markets."
    )

    recent_developments: list[str] = Field(
        description="Important recent company developments."
    )

    technology_signals: list[str] = Field(
        description="Relevant technology, AI, or digital transformation signals."
    )

    potential_challenges: list[str] = Field(
        description="Potential business or operational challenges supported by the research."
    )

    ai_opportunities: list[str] = Field(
        description="Realistic AI or automation opportunities."
    )

    sources: list[str] = Field(
        description="URLs of the most relevant research sources."
    )


researcher_llm = LLM(
    model="groq/openai/gpt-oss-20b",
    temperature=0.1,
    max_tokens=500,
    reasoning_effort="low",
)


def create_researcher() -> Agent:
    return Agent(
        role="Company Research Analyst",

        goal=(
            "Analyze verified web research and extract concise, "
            "accurate company intelligence for B2B outreach."
        ),

        backstory=(
            "You are a careful B2B research analyst. "
            "You extract facts from provided search results, "
            "avoid unsupported claims, and identify useful "
            "business and technology signals."
        ),

        llm=researcher_llm,

        verbose=True,
    )