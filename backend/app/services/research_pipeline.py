import json
from typing import Any

import crewai.llms.cache as _crewai_cache

# Workaround for the current CrewAI/Groq cache_breakpoint issue.
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from crewai import Crew, Process, Task

from app.agents.analyst import SalesAnalysis, create_analyst
from app.agents.researcher import CompanyResearch, create_researcher
from app.agents.writer import OutreachResult, create_writer
from app.services.search_service import SearchService
from app.utils.json_parser import parse_llm_json


class ResearchPipeline:
    """
    End-to-end IntelliReach research pipeline.

    Flow:
        1. Search the company using controlled Serper queries.
        2. Researcher extracts structured company intelligence.
        3. Analyst identifies sales pain points and opportunities.
        4. Writer generates personalized outreach.
    """

    def __init__(self) -> None:
        self.search_service = SearchService()

        self.researcher = create_researcher()
        self.analyst = create_analyst()
        self.writer = create_writer()

    def run(self, company_name: str) -> dict[str, Any]:
        """
        Run the complete research pipeline for a company.
        """

        company_name = company_name.strip()

        if not company_name:
            raise ValueError("Company name cannot be empty.")

        # ---------------------------------------------------------
        # Step 1: Controlled web research
        # ---------------------------------------------------------

        search_results = self.search_service.search_company(
            company_name
        )

        research_context = self._build_research_context(
            company_name,
            search_results,
        )

        # ---------------------------------------------------------
        # Step 2: Company research
        # ---------------------------------------------------------

        company_research = self._run_researcher(
            company_name,
            research_context,
        )

        # ---------------------------------------------------------
        # Step 3: Sales analysis
        # ---------------------------------------------------------

        sales_analysis = self._run_analyst(
            company_research,
        )

        # ---------------------------------------------------------
        # Step 4: Personalized outreach
        # ---------------------------------------------------------

        outreach_result = self._run_writer(
            company_research,
            sales_analysis,
        )

        # ---------------------------------------------------------
        # Final structured response
        # ---------------------------------------------------------

        return {
            "company_research": company_research.model_dump(),
            "sales_analysis": sales_analysis.model_dump(),
            "outreach": outreach_result.model_dump(),
        }

    # =============================================================
    # RESEARCHER
    # =============================================================

    def _run_researcher(
        self,
        company_name: str,
        research_context: str,
    ) -> CompanyResearch:
        """
        Ask the researcher agent to convert web research
        into structured company intelligence.

        If the LLM returns malformed JSON, retry once.
        """

        researcher_task = Task(
            description=f"""
You are researching the following company:

COMPANY:
{company_name}

VERIFIED WEB RESEARCH:
{research_context}

Analyze the provided research and return structured company intelligence.

You must return ONLY valid JSON.

The JSON must follow this exact structure:

{{
    "company_name": "string",
    "overview": "string",
    "products_services": [
        "string"
    ],
    "target_market": "string",
    "recent_developments": [
        "string"
    ],
    "technology_signals": [
        "string"
    ],
    "potential_challenges": [
        "string"
    ],
    "ai_opportunities": [
        "string"
    ],
    "sources": [
        "string"
    ]
}}

STRICT RULES:

1. Use only information supported by the supplied web research.
2. Do not invent facts.
3. Keep every field concise.
4. Do not repeat information.
5. Return no more than 3 products/services.
6. Return no more than 3 recent developments.
7. Return no more than 3 technology signals.
8. Return no more than 3 potential challenges.
9. Return no more than 3 AI opportunities.
10. Return no more than 5 sources.
11. Return ONLY JSON.
12. Do not use markdown.
13. Do not use ```json fences.
14. Make sure every string has properly closed quotation marks.
15. Escape quotation marks inside strings.
16. Do not include explanations before or after the JSON.
""",
            expected_output="Only valid JSON matching the requested structure.",
            agent=self.researcher,
        )

        crew = Crew(
            agents=[self.researcher],
            tasks=[researcher_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        raw_output = result.raw

        # ---------------------------------------------------------
        # First parsing attempt
        # ---------------------------------------------------------

        try:
            parsed_output = parse_llm_json(raw_output)

        except ValueError as first_error:
            print(
                "\nResearcher returned malformed JSON."
                "\nRetrying researcher once."
                f"\nFirst parsing error: {first_error}\n"
            )

            # -----------------------------------------------------
            # Controlled retry
            # -----------------------------------------------------

            retry_task = Task(
                description=f"""
The previous researcher response could not be parsed as valid JSON.

You must produce the company research again.

COMPANY:
{company_name}

VERIFIED WEB RESEARCH:
{research_context}

Return ONLY valid JSON using this exact structure:

{{
    "company_name": "string",
    "overview": "string",
    "products_services": [
        "string"
    ],
    "target_market": "string",
    "recent_developments": [
        "string"
    ],
    "technology_signals": [
        "string"
    ],
    "potential_challenges": [
        "string"
    ],
    "ai_opportunities": [
        "string"
    ],
    "sources": [
        "string"
    ]
}}

STRICT JSON RULES:

1. Return ONLY JSON.
2. Do not use markdown.
3. Do not use ``` fences.
4. Every string must have properly closed quotation marks.
5. Escape quotation marks inside strings.
6. Do not include any explanation.
7. Keep every field concise.
8. Do not repeat information.
9. Maximum 3 products/services.
10. Maximum 3 recent developments.
11. Maximum 3 technology signals.
12. Maximum 3 potential challenges.
13. Maximum 3 AI opportunities.
14. Maximum 5 sources.
15. The response must be directly parseable by Python json.loads().
""",
                expected_output="Only valid JSON.",
                agent=self.researcher,
            )

            retry_crew = Crew(
                agents=[self.researcher],
                tasks=[retry_task],
                process=Process.sequential,
                verbose=True,
            )

            retry_result = retry_crew.kickoff()

            parsed_output = parse_llm_json(
                retry_result.raw
            )

        return CompanyResearch.model_validate(
            parsed_output
        )

    # =============================================================
    # ANALYST
    # =============================================================

    def _run_analyst(
        self,
        company_research: CompanyResearch,
    ) -> SalesAnalysis:
        """
        Analyze structured company research and identify
        sales pain points and opportunities.
        """

        research_json = json.dumps(
            company_research.model_dump(),
            indent=2,
        )

        analyst_task = Task(
            description=f"""
Analyze the following structured company research.

COMPANY RESEARCH:
{research_json}

Identify realistic business pain points, the strongest AI or
automation opportunity, the potential business value, and a
personalized outreach hook.

Return ONLY valid JSON.

Use this exact structure:

{{
    "pain_points": [
        "string",
        "string",
        "string"
    ],
    "strongest_opportunity": "string",
    "business_value": "string",
    "outreach_hook": "string"
}}

STRICT RULES:

1. Return exactly 3 pain points.
2. Base the analysis on the supplied company research.
3. Distinguish evidence from assumptions.
4. Do not invent statistics.
5. Do not exaggerate potential business outcomes.
6. Keep the output concise.
7. Return ONLY JSON.
8. Do not use markdown.
9. Do not use ``` fences.
""",
            expected_output="Only valid JSON matching the requested structure.",
            agent=self.analyst,
        )

        crew = Crew(
            agents=[self.analyst],
            tasks=[analyst_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        parsed_output = parse_llm_json(
            result.raw
        )

        return SalesAnalysis.model_validate(
            parsed_output
        )

    # =============================================================
    # WRITER
    # =============================================================

    def _run_writer(
        self,
        company_research: CompanyResearch,
        sales_analysis: SalesAnalysis,
    ) -> OutreachResult:
        """
        Generate personalized outreach based on the
        company research and sales analysis.
        """

        research_json = json.dumps(
            company_research.model_dump(),
            indent=2,
        )

        analysis_json = json.dumps(
            sales_analysis.model_dump(),
            indent=2,
        )

        writer_task = Task(
            description=f"""
Write personalized B2B outreach based on the following
company research and sales analysis.

COMPANY RESEARCH:
{research_json}

SALES ANALYSIS:
{analysis_json}

Return ONLY valid JSON.

Use this exact structure:

{{
    "email": "string",
    "talking_points": [
        "string",
        "string",
        "string"
    ]
}}

STRICT RULES:

1. Write an email of approximately 100 to 120 words.
2. Make the email specifically relevant to the company.
3. Use the identified pain points and strongest opportunity.
4. Avoid generic sales language.
5. Avoid exaggerated claims.
6. Do not invent statistics.
7. Do not use unsupported facts.
8. Return exactly 3 talking points.
9. Keep talking points concise.
10. Return ONLY JSON.
11. Do not use markdown.
12. Do not use ``` fences.
""",
            expected_output="Only valid JSON matching the requested structure.",
            agent=self.writer,
        )

        crew = Crew(
            agents=[self.writer],
            tasks=[writer_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        parsed_output = parse_llm_json(
            result.raw
        )

        return OutreachResult.model_validate(
            parsed_output
        )

    # =============================================================
    # SEARCH CONTEXT
    # =============================================================

    def _build_research_context(
        self,
        company_name: str,
        search_results: dict[str, list[dict[str, str]]],
    ) -> str:
        """
        Convert Serper results into a compact context
        for the researcher agent.
        """

        context_parts = [
            f"COMPANY: {company_name}",
        ]

        for category, results in search_results.items():
            context_parts.append(
                f"\n=== {category.upper()} ==="
            )

            # Keep only the first 3 results from each
            # controlled search category.
            for index, result in enumerate(
                results[:3],
                start=1,
            ):
                title = result.get(
                    "title",
                    "",
                )

                url = result.get(
                    "url",
                    "",
                )

                snippet = result.get(
                    "snippet",
                    "",
                )

                context_parts.append(
                    f"""
Result {index}
Title: {title}
URL: {url}
Snippet: {snippet}
"""
                )

        return "\n".join(context_parts)