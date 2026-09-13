from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper


load_dotenv()


search = GoogleSerperAPIWrapper(
    k=5,
    gl="in",
    hl="en",
)


query = "Razorpay company products services"


results = search.results(query)


print("\n" + "=" * 70)
print("SERPER SEARCH TEST")
print("=" * 70)

for index, result in enumerate(
    results.get("organic", []),
    start=1,
):
    print(f"\n[{index}] {result.get('title')}")
    print(f"URL: {result.get('link')}")
    print(f"Snippet: {result.get('snippet')}")