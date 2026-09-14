import json

from app.services.research_pipeline import ResearchPipeline


# ============================================================
# Configuration
# ============================================================

company_name = "Razorpay"


# ============================================================
# Create Pipeline
# ============================================================

pipeline = ResearchPipeline()


# ============================================================
# Run Complete Pipeline
# ============================================================

result = pipeline.run(company_name)


# ============================================================
# Display Result
# ============================================================

print("\n" + "=" * 80)
print("INTELLIREACH PIPELINE RESULT")
print("=" * 80)

print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False,
    )
)