import json

import crewai.llms.cache as _crewai_cache

# CrewAI/Groq compatibility workaround.
# Prevents CrewAI from injecting unsupported cache metadata.
_crewai_cache.mark_cache_breakpoint = lambda msg: msg


from crewai import Task, Crew, Process

from app.agents.analyst import (
    SalesAnalysis,
    create_analyst,
)


# ============================================================
# Configuration
# ============================================================

company_research = {
    "company_name": "Razorpay",

    "overview": (
        "Razorpay is a financial technology company providing "
        "payment and business banking solutions."
    ),

    "products_services": [
        "Payment gateway",
        "Payment processing",
        "Business banking solutions",
    ],

    "target_market": (
        "Businesses ranging from startups to larger enterprises."
    ),

    "recent_developments": [
        "Expansion of financial technology products",
        "Growth of its broader business payments ecosystem",
    ],

    "technology_signals": [
        "Large-scale digital payment infrastructure",
        "Use of technology to automate financial workflows",
    ],

    "potential_challenges": [
        "Scaling complex payment infrastructure",
        "Managing operational complexity across financial products",
    ],

    "ai_opportunities": [
        "Automation of repetitive operational workflows",
        "AI-assisted fraud and risk analysis",
    ],

    "sources": [
        "https://example.com/source-1",
        "https://example.com/source-2",
    ],
}


# ============================================================
# 1. Create Analyst
# ============================================================

analyst = create_analyst()


# ============================================================
# 2. Create Analyst Task
# ============================================================

research_json = json.dumps(
    company_research,
    indent=2,
)


analysis_task = Task(

    description=(
        "Analyze the following structured company research.\n\n"

        "COMPANY RESEARCH:\n"
        f"{research_json}\n\n"

        "Your job is to identify useful B2B sales intelligence.\n\n"

        "Requirements:\n"
        "1. Identify exactly 3 realistic pain points.\n"
        "2. Identify the single strongest AI or automation opportunity.\n"
        "3. Explain the potential business value of that opportunity.\n"
        "4. Create one concise personalized outreach hook.\n\n"

        "Base your reasoning on the provided research.\n"
        "Do not invent company facts.\n"
        "Do not claim specific ROI numbers unless they are supported.\n"
        "Avoid generic statements that could apply to every company.\n\n"

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
        "Valid JSON containing exactly three pain points, "
        "one strongest opportunity, business value, and "
        "one outreach hook."
    ),

    agent=analyst,
)


# ============================================================
# 3. Create Crew
# ============================================================

crew = Crew(
    agents=[analyst],
    tasks=[analysis_task],
    process=Process.sequential,
    verbose=True,
)


# ============================================================
# 4. Run Analyst
# ============================================================

result = crew.kickoff()


# ============================================================
# 5. Validate JSON
# ============================================================

raw_output = result.raw.strip()


print("\n" + "=" * 70)
print("RAW ANALYST OUTPUT")
print("=" * 70)

print(raw_output)


try:

    analysis_data = json.loads(raw_output)

    validated_analysis = SalesAnalysis.model_validate(
        analysis_data
    )

except (json.JSONDecodeError, ValueError) as error:

    print("\n" + "=" * 70)
    print("ANALYST VALIDATION FAILED")
    print("=" * 70)

    print(error)

    raise


# ============================================================
# 6. Display Validated Analysis
# ============================================================

print("\n" + "=" * 70)
print("VALIDATED SALES ANALYSIS")
print("=" * 70)

print(
    validated_analysis.model_dump_json(
        indent=2
    )
)