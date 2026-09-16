import json

# CrewAI/Groq compatibility workaround
import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crewai import Task, Crew, Process

from app.agents.researcher import (
    CompanyResearch,
    create_researcher,
)

from app.services.search_service import SearchService


# ============================================================
# Configuration
# ============================================================

company_name = "Razorpay"


# ============================================================
# 1. Search the company
# ============================================================

search_service = SearchService()

search_results = search_service.search_company(
    company_name
)


# ============================================================
# 2. Build compact research context
# ============================================================

research_context_parts = []

for category, results in search_results.items():

    research_context_parts.append(
        f"### {category.upper()}"
    )

    for result in results[:3]:

        research_context_parts.append(
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Snippet: {result['snippet']}\n"
        )


research_context = "\n".join(
    research_context_parts
)


# ============================================================
# 3. Create Researcher
# ============================================================

researcher = create_researcher()


# ============================================================
# 4. Research Task
# ============================================================

research_task = Task(
    description=(
        f"Research and analyze the company: {company_name}.\n\n"

        "You have been given Google search results below.\n\n"

        "SEARCH RESULTS:\n"
        f"{research_context}\n\n"

        "Extract only information supported by these results.\n"
        "Do not invent facts.\n\n"

        "Return ONLY valid JSON.\n"
        "Do not use Markdown.\n"
        "Do not wrap the JSON in ```.\n\n"

        "Use exactly this JSON structure:\n"
        "{\n"
        '  "company_name": "string",\n'
        '  "overview": "string",\n'
        '  "products_services": ["string"],\n'
        '  "target_market": "string",\n'
        '  "recent_developments": ["string"],\n'
        '  "technology_signals": ["string"],\n'
        '  "potential_challenges": ["string"],\n'
        '  "ai_opportunities": ["string"],\n'
        '  "sources": ["string"]\n'
        "}\n\n"

        "Keep every field concise."
    ),

    expected_output=(
        "Valid JSON matching the exact structure specified "
        "in the task description."
    ),

    agent=researcher,
)


# ============================================================
# 5. Run CrewAI
# ============================================================

crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True,
)


result = crew.kickoff()


# ============================================================
# 6. Validate the JSON ourselves
# ============================================================

raw_output = result.raw.strip()

print("\n" + "=" * 70)
print("RAW RESEARCH OUTPUT")
print("=" * 70)

print(raw_output)


try:

    research_data = json.loads(raw_output)

    validated_research = CompanyResearch.model_validate(
        research_data
    )

except (json.JSONDecodeError, ValueError) as error:

    print("\n" + "=" * 70)
    print("STRUCTURED OUTPUT VALIDATION FAILED")
    print("=" * 70)

    print(error)

    raise


# ============================================================
# 7. Display validated result
# ============================================================

print("\n" + "=" * 70)
print("VALIDATED COMPANY RESEARCH")
print("=" * 70)

print(
    validated_research.model_dump_json(
        indent=2
    )
)