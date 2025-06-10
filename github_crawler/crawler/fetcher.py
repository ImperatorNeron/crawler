import random
import requests
import logging

from github_crawler.core import settings

logger = logging.getLogger(__name__)


def get_proxy_dict(proxies: list[str]) -> dict[str, str]:
    """Returns random proxy from list"""

    proxy = random.choice(proxies)
    return {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }


def fetch_search_page(
    keywords: list[str],
    search_type: str,
    proxies: list[str],
    timeout: int = settings.TIMEOUT,
):
    """Fetches GitHub search page with retry logic.

    Args:
        keywords: Search terms
        search_type: GitHub search type: repositories, wikis, issues
        proxies: List of proxy servers
        timeout: Request timeout in seconds

    Returns:
        HTML content of the page

    Raises:
        RuntimeError: After all retry attempts fail
    """

    params = {"q": " ".join(keywords), "type": search_type}
    proxy_dict = get_proxy_dict(proxies)
    logger.info(f"Proxy selected: {proxy_dict}")

    for attempt in range(settings.MAX_RETRIES):
        try:
            response = requests.get(
                settings.BASE_URL,
                headers=settings.HEADERS,
                params=params,
                proxies=proxy_dict,
                timeout=timeout,
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            if attempt == settings.MAX_RETRIES - 1:
                logger.error(f"Request failed on attempt {attempt + 1}: {str(e)}")
                raise RuntimeError(
                    f"Request failed after {settings.MAX_RETRIES} attempts: {e}"
                )
