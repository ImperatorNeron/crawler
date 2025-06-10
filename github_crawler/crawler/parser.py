from bs4 import BeautifulSoup


def parse_search_results(html: str) -> list[dict[str, str]]:
    """Parse URLs from HTML"""

    # The same for Wikis, Repositories, Issues
    soup = BeautifulSoup(html, "html.parser")
    if results_block := soup.find("div", {"data-testid": "results-list"}):
        return [
            {"url": f"https://github.com{a['href']}"}
            for a in results_block.select("div.search-title a[href]")
        ]
    return []
