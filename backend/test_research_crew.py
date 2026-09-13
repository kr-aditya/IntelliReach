from app.agents.research_crew import build_research_crew


crew = build_research_crew(
    company_name="Zoho",
    candidate_context=(
        "We provide AI automation and software engineering "
        "solutions for businesses."
    ),
)

result = crew.kickoff()


print("\n" + "=" * 70)
print("FINAL INTELLIREACH RESULT")
print("=" * 70)

print(result.raw)