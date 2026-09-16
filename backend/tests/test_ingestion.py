from app.rag.ingestion import (
    DocumentIngestionService,
)


# ============================================================
# Configuration
# ============================================================

FILE_PATH = "sample_company.txt"


# ============================================================
# Ingestion
# ============================================================

service = DocumentIngestionService()

chunk_count = service.ingest_file(
    FILE_PATH
)


# ============================================================
# Result
# ============================================================

print("\n" + "=" * 70)
print("DOCUMENT INGESTION COMPLETE")
print("=" * 70)

print(
    f"Chunks stored: {chunk_count}"
)