from app.services.search_service import SearchService
from dotenv import load_dotenv

load_dotenv()

search_service = SearchService()


results = search_service.search_company("Razorpay")


print("\n" + "=" * 70)
print("INTELLIREACH SEARCH SERVICE TEST")
print("=" * 70)


for category, search_results in results.items():

    print(f"\n\n### {category.upper()}")

    for index, result in enumerate(
        search_results,
        start=1,
    ):
        print(f"\n[{index}] {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}")