from typing import Any

from langchain_community.utilities import GoogleSerperAPIWrapper


class SearchService:
    """
    Controlled web-search service for IntelliReach.

    The service performs a small number of predefined searches
    instead of allowing an AI agent to decide how many searches
    to execute.
    """

    def __init__(self) -> None:
        self.search = GoogleSerperAPIWrapper(
            k=5,
            gl="in",
            hl="en",
        )

    def search_company(self, company_name: str) -> dict[str, Any]:
        """
        Research a company using three focused Google searches.
        """

        queries = {
            "company_overview": (
                f"{company_name} company products services"
            ),
            "recent_developments": (
                f"{company_name} recent news developments"
            ),
            "technology_signals": (
                f"{company_name} technology AI automation"
            ),
        }

        results = {}

        for category, query in queries.items():
            results[category] = self._run_search(query)

        return results

    def _run_search(self, query: str) -> list[dict[str, str]]:
        """
        Execute one Serper search and normalize the results.
        """

        response = self.search.results(query)

        organic_results = response.get("organic", [])

        normalized_results = []

        for result in organic_results:
            normalized_results.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                }
            )

        return normalized_results