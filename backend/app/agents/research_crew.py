from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from tavily import TavilyClient

import crewai.llms.cache as _crewai_cache

_crewai_cache.mark_cache_breakpoint = lambda msg: msg


load_dotenv()



llm = LLM(
    model="groq/openai/gpt-oss-120b",
    temperature=0.2,
    max_tokens=1400,
    reasoning_effort="low",
)


tavily_client = TavilyClient()


class CompanySearchInput(BaseModel):
    query: str = Field(
        ...,
        description="A natural-language web search query."
    )


class CompanySearchTool(BaseTool):
    name: str = "company_web_search"

    description: str = (
        "Search the web for current information about a company. "
        "Use a focused natural-language search query. "
        "Examples: 'Zoho company products', "
        "'Zoho recent news', or "
        "'Zoho AI automation initiatives'."
    )

    args_schema: type[BaseModel] = CompanySearchInput

    def _run(self, query: str) -> str:
        response = tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=4,
            include_answer=True,
        )

        output = []

        if response.get("answer"):
            output.append(
                f"Summary: {response['answer']}"
            )

        for index, result in enumerate(
            response.get("results", []),
            start=1
        ):
            title = result.get("title", "Untitled")
            url = result.get("url", "")
            content = result.get("content", "")

            content = content[:1000]

            output.append(
                f"\nSource {index}:\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Content: {content}"
            )

        if not output:
            return "No useful search results were returned."

        return "\n".join(output)


search_tool = CompanySearchTool()


def build_research_crew(
    company_name: str,
    candidate_context: str = "",
) -> Crew:

 
    researcher = Agent(
        role="Senior Business Research Analyst",

        goal=(
            "Research the target company and collect accurate, "
            "relevant business intelligence that can be used "
            "for personalized B2B outreach."
        ),

        backstory=(
            "You are an experienced B2B business researcher. "
            "You investigate companies, their products, markets, "
            "recent developments, technology adoption, operational "
            "challenges, and potential AI or automation opportunities. "
            "You separate verified information from assumptions."
        ),

        tools=[search_tool],

        llm=llm,

        verbose=True,
    )

    research_task = Task(
        description=(
            f"Research the company: {company_name}.\n\n"

            "Use the company_web_search tool to investigate:\n"
            "1. What the company does.\n"
            "2. Main products or services.\n"
            "3. Target customers and markets.\n"
            "4. One or two recent company developments.\n"
            "5. Technology or digital transformation signals.\n"
            "6. Potential business challenges.\n"
            "7. Potential AI or automation opportunities.\n\n"

            "Use multiple focused searches when necessary.\n"
            "Do not invent facts.\n"
            "Clearly distinguish verified information from "
            "reasonable observations.\n"
            "Keep the final research concise and useful for the "
            "next analyst."
        ),

        expected_output=(
            "A concise company research report containing:\n"
            "- Company overview\n"
            "- Products/services\n"
            "- Target market\n"
            "- Recent developments\n"
            "- Technology signals\n"
            "- Business challenges\n"
            "- 2-3 realistic AI/automation opportunities\n"
            "- Relevant source URLs"
        ),

        agent=researcher,
    )


    analyst = Agent(
        role="AI Solutions Business Analyst",

        goal=(
            "Analyze company research and identify realistic "
            "AI and automation opportunities that could create "
            "measurable business value."
        ),

        backstory=(
            "You are an AI solutions consultant who translates "
            "business problems into practical AI and automation "
            "use cases. You avoid generic AI recommendations and "
            "focus on opportunities that are relevant to the "
            "company's actual operations."
        ),

        llm=llm,

        verbose=True,
    )

    analysis_task = Task(
        description=(
            f"Analyze the research for {company_name}.\n\n"

            "Identify:\n"
            "1. The most important business challenges.\n"
            "2. Potential inefficient or manual workflows.\n"
            "3. The strongest AI or automation opportunity.\n"
            "4. Why that opportunity is relevant to this company.\n"
            "5. The likely business value.\n"
            "6. One specific personalization hook that could be "
            "used in a B2B outreach email.\n\n"

            "Do not invent company facts. Base your analysis on "
            "the research provided by the previous agent."
        ),

        expected_output=(
            "A concise AI opportunity analysis containing:\n"
            "- Key business challenge\n"
            "- Recommended AI/automation use case\n"
            "- Why it fits the company\n"
            "- Expected business value\n"
            "- Personalized outreach angle"
        ),

        agent=analyst,

        context=[research_task],
    )


    writer = Agent(
        role="B2B Outreach Specialist",

        goal=(
            "Create concise, highly personalized B2B outreach "
            "messages based on verified company research and "
            "relevant AI opportunities."
        ),

        backstory=(
            "You are an experienced B2B sales copywriter who "
            "specializes in personalized technology outreach. "
            "Your writing is specific, professional, concise, "
            "and focused on business value rather than generic "
            "marketing language."
        ),

        llm=llm,

        verbose=True,
    )

    writer_task = Task(
        description=(
            f"Write a personalized cold outreach email for "
            f"{company_name}.\n\n"

            f"Candidate context:\n"
            f"{candidate_context or 'No additional candidate context provided.'}\n\n"

            "Use the company research and AI opportunity analysis "
            "from the previous agents.\n\n"

            "Requirements:\n"
            "- 100-130 words maximum.\n"
            "- Mention one specific company insight.\n"
            "- Focus on one realistic AI or automation opportunity.\n"
            "- Explain the potential business value briefly.\n"
            "- Include a low-pressure call to action.\n"
            "- Avoid generic marketing language.\n"
            "- Do not make unsupported claims.\n"
            "- Make the email sound human and professional."
        ),

        expected_output=(
            "A polished B2B outreach email containing:\n"
            "Subject: ...\n"
            "Body: ..."
        ),

        agent=writer,

        context=[research_task, analysis_task],
    )


    crew = Crew(
        agents=[
            researcher,
            analyst,
            writer,
        ],

        tasks=[
            research_task,
            analysis_task,
            writer_task,
        ],

        process=Process.sequential,

        verbose=True,
    )

    return crew