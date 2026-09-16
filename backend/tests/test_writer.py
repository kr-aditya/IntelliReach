import json

import crewai.llms.cache as _crewai_cache

# CrewAI/Groq compatibility workaround.
_crewai_cache.mark_cache_breakpoint = lambda msg: msg


from crewai import Task, Crew, Process

from app.agents.writer import (
    OutreachResult,
    create_writer,
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


sales_analysis = {
    "pain_points": [
        "Scaling complex payment infrastructure",
        "Managing operational complexity across financial products",
        "Maintaining efficient workflows as the product ecosystem grows",
    ],

    "strongest_opportunity": (
        "Automating repetitive operational workflows with AI."
    ),

    "business_value": (
        "AI-driven workflow automation could reduce repetitive "
        "manual work and help operational teams scale more efficiently."
    ),

    "outreach_hook": (
        "Explore how AI automation could streamline repetitive "
        "operational workflows as Razorpay expands its financial "
        "product ecosystem."
    ),
}


# ============================================================
# 1. Create Writer
# ============================================================

writer = create_writer()


# ============================================================
# 2. Build Writer Context
# ============================================================

writer_context = {
    "company_research": company_research,
    "sales_analysis": sales_analysis,
}


context_json = json.dumps(
    writer_context,
    indent=2,
)


# ============================================================
# 3. Create Writer Task
# ============================================================

writer_task = Task(

    description=(
        "Write a personalized B2B outreach message using the "
        "following company research and sales analysis.\n\n"

        "INPUT DATA:\n"
        f"{context_json}\n\n"

        "Requirements:\n"
        "1. Write one personalized outreach email.\n"
        "2. Keep the email approximately 100–120 words.\n"
        "3. Mention a specific company-related observation.\n"
        "4. Connect that observation to the strongest opportunity.\n"
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
        "Valid JSON containing one personalized outreach email "
        "and exactly three talking points."
    ),

    agent=writer,
)


# ============================================================
# 4. Create Crew
# ============================================================

crew = Crew(
    agents=[writer],
    tasks=[writer_task],
    process=Process.sequential,
    verbose=True,
)


# ============================================================
# 5. Run Writer
# ============================================================

result = crew.kickoff()


# ============================================================
# 6. Validate JSON
# ============================================================

raw_output = result.raw.strip()


print("\n" + "=" * 70)
print("RAW WRITER OUTPUT")
print("=" * 70)

print(raw_output)


try:

    writer_data = json.loads(raw_output)

    validated_result = OutreachResult.model_validate(
        writer_data
    )

except (json.JSONDecodeError, ValueError) as error:

    print("\n" + "=" * 70)
    print("WRITER VALIDATION FAILED")
    print("=" * 70)

    print(error)

    raise


# ============================================================
# 7. Display Final Result
# ============================================================

print("\n" + "=" * 70)
print("VALIDATED OUTREACH RESULT")
print("=" * 70)

print(
    validated_result.model_dump_json(
        indent=2
    )
)