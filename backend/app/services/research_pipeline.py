import json
from typing import Any

import crewai.llms.cache as _crewai_cache

# CrewAI/Groq compatibility workaround.
_crewai_cache.mark_cache_breakpoint = lambda msg: msg


from crewai import Crew, Process, Task

from app.agents.researcher import (
    CompanyResearch,
    create_researcher,
)

from app.agents.analyst import (
    SalesAnalysis,
    create_analyst,
)

from app.agents.writer import (
    OutreachResult,
    create_writer,
)

from app.services.search_service import SearchService


class ResearchPipeline:
    """
    Orchestrates the complete IntelliReach research workflow.

    Flow:
        Company Name
            ↓
        Serper Search
            ↓
        Researcher
            ↓
        CompanyResearch
            ↓
        Analyst
            ↓
        SalesAnalysis
            ↓
        Writer
            ↓
        OutreachResult
    """

    def __init__(self) -> None:

        self.search_service = SearchService()

        self.researcher = create_researcher()
        self.analyst = create_analyst()
        self.writer = create_writer()


    # ========================================================
    # Public Pipeline
    # ========================================================

    def run(self, company_name: str) -> dict[str, Any]:
        """
        Run the complete IntelliReach pipeline.
        """

        company_name = company_name.strip()

        if not company_name:
            raise ValueError(
                "Company name cannot be empty."
            )

        # ----------------------------------------------------
        # 1. Search
        # ----------------------------------------------------

        search_results = (
            self.search_service.search_company(
                company_name
            )
        )

        research_context = (
            self._build_research_context(
                search_results
            )
        )

        # ----------------------------------------------------
        # 2. Researcher
        # ----------------------------------------------------

        company_research = (
            self._run_researcher(
                company_name,
                research_context,
            )
        )

        # ----------------------------------------------------
        # 3. Analyst
        # ----------------------------------------------------

        sales_analysis = (
            self._run_analyst(
                company_research
            )
        )

        # ----------------------------------------------------
        # 4. Writer
        # ----------------------------------------------------

        outreach_result = (
            self._run_writer(
                company_research,
                sales_analysis,
            )
        )

        # ----------------------------------------------------
        # 5. Final result
        # ----------------------------------------------------

        return {
            "company_research": (
                company_research.model_dump()
            ),

            "sales_analysis": (
                sales_analysis.model_dump()
            ),

            "outreach": (
                outreach_result.model_dump()
            ),
        }


    # ========================================================
    # Researcher
    # ========================================================

    def _run_researcher(
        self,
        company_name: str,
        research_context: str,
    ) -> CompanyResearch:
        """
        Run the Researcher agent and validate its output.
        """

        task = Task(

            description=(
                f"Research and analyze the company: "
                f"{company_name}.\n\n"

                "You have been given Google search results "
                "below.\n\n"

                "SEARCH RESULTS:\n"
                f"{research_context}\n\n"

                "Extract only information supported by "
                "these results.\n"

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
                "Valid JSON matching the exact structure "
                "specified in the task."
            ),

            agent=self.researcher,
        )

        crew = Crew(
            agents=[self.researcher],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        raw_output = result.raw.strip()

        try:

            data = json.loads(raw_output)

            return CompanyResearch.model_validate(
                data
            )

        except (json.JSONDecodeError, ValueError) as error:

            raise ValueError(
                f"Researcher produced invalid output: {error}"
            ) from error


    # ========================================================
    # Analyst
    # ========================================================

    def _run_analyst(
        self,
        company_research: CompanyResearch,
    ) -> SalesAnalysis:
        """
        Run the Analyst agent and validate its output.
        """

        research_json = json.dumps(
            company_research.model_dump(),
            indent=2,
        )

        task = Task(

            description=(
                "Analyze the following structured company "
                "research.\n\n"

                "COMPANY RESEARCH:\n"
                f"{research_json}\n\n"

                "Identify useful B2B sales intelligence.\n\n"

                "Requirements:\n"
                "1. Identify exactly 3 realistic pain points.\n"
                "2. Identify the single strongest AI or "
                "automation opportunity.\n"
                "3. Explain the potential business value.\n"
                "4. Create one concise personalized "
                "outreach hook.\n\n"

                "Base your reasoning on the provided research.\n"
                "Do not invent company facts.\n"
                "Do not claim unsupported statistics.\n"
                "Avoid generic statements.\n\n"

                "Return ONLY valid JSON.\n"
                "Do not use Markdown.\n"
                "Do not wrap the JSON in ```.\n\n"

                "Use exactly this JSON structure:\n"
                "{\n"
                '  "pain_points": ["string", "string", "string"],\n'
                '  "strongest_opportunity": "string",\n'
                '  "business_value": "string",\n'
                '  "outreach_hook": "string"\n'
                "}\n\n"

                "Keep the output concise."
            ),

            expected_output=(
                "Valid JSON containing exactly three pain "
                "points, one strongest opportunity, business "
                "value, and one outreach hook."
            ),

            agent=self.analyst,
        )

        crew = Crew(
            agents=[self.analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        raw_output = result.raw.strip()

        try:

            data = json.loads(raw_output)

            return SalesAnalysis.model_validate(
                data
            )

        except (json.JSONDecodeError, ValueError) as error:

            raise ValueError(
                f"Analyst produced invalid output: {error}"
            ) from error


    # ========================================================
    # Writer
    # ========================================================

    def _run_writer(
        self,
        company_research: CompanyResearch,
        sales_analysis: SalesAnalysis,
    ) -> OutreachResult:
        """
        Run the Writer agent and validate its output.
        """

        writer_context = {
            "company_research": (
                company_research.model_dump()
            ),

            "sales_analysis": (
                sales_analysis.model_dump()
            ),
        }

        context_json = json.dumps(
            writer_context,
            indent=2,
        )

        task = Task(

            description=(
                "Write a personalized B2B outreach message "
                "using the following company research and "
                "sales analysis.\n\n"

                "INPUT DATA:\n"
                f"{context_json}\n\n"

                "Requirements:\n"
                "1. Write one personalized outreach email.\n"
                "2. Keep the email approximately 100–120 words.\n"
                "3. Mention a specific company-related observation.\n"
                "4. Connect that observation to the strongest "
                "opportunity.\n"
                "5. Keep the tone professional and conversational.\n"
                "6. Include a simple, natural call to action.\n"
                "7. Provide exactly 3 sales call talking points.\n\n"

                "Do not invent company facts.\n"
                "Do not invent statistics or ROI numbers.\n"
                "Do not use excessive buzzwords.\n"
                "Do not make the email sound like mass marketing.\n"
                "Do not mention that AI generated the message.\n\n"

                "Return ONLY valid JSON.\n"
                "Do not use Markdown.\n"
                "Do not wrap the JSON in ```.\n\n"

                "Use exactly this JSON structure:\n"
                "{\n"
                '  "email": "string",\n'
                '  "talking_points": ["string", "string", "string"]\n'
                "}\n\n"

                "Keep the talking points concise."
            ),

            expected_output=(
                "Valid JSON containing one personalized "
                "outreach email and exactly three talking points."
            ),

            agent=self.writer,
        )

        crew = Crew(
            agents=[self.writer],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        raw_output = result.raw.strip()

        try:

            data = json.loads(raw_output)

            return OutreachResult.model_validate(
                data
            )

        except (json.JSONDecodeError, ValueError) as error:

            raise ValueError(
                f"Writer produced invalid output: {error}"
            ) from error


    # ========================================================
    # Search Context Builder
    # ========================================================

    def _build_research_context(
        self,
        search_results: dict[str, list[dict[str, str]]],
    ) -> str:
        """
        Convert normalized search results into compact
        context for the Researcher.
        """

        context_parts = []

        for category, results in search_results.items():

            context_parts.append(
                f"### {category.upper()}"
            )

            for result in results[:3]:

                context_parts.append(
                    f"Title: {result['title']}\n"
                    f"URL: {result['url']}\n"
                    f"Snippet: {result['snippet']}\n"
                )

        return "\n".join(context_parts)