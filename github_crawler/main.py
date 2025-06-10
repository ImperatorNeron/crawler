from pathlib import Path
import time
from github_crawler.core import settings
from github_crawler.core.search_type import SearchType
from github_crawler.crawler.fetcher import fetch_search_page
from github_crawler.crawler.parser import parse_search_results
from github_crawler.crawler.storage import load_input_data, save_output
import logging

from github_crawler.core.logger_settings import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
start_time = time.perf_counter()


def crawl_github(
    keywords: list[str], proxies: list[str], search_type: SearchType
) -> list[dict[str, str]]:
    """Starts the functions of receiving the landing page and parsing the result

    Args:
        keywords: Search terms
        search_type: GitHub search type: repositories, wikis, issues
        proxies: List of proxy servers

    Returns:
        List of result dictionaries
    """

    logger.info("Start fetching page...")
    html = fetch_search_page(keywords, search_type.value, proxies)
    logger.info("Start parsing data...")
    parsed_search_results = parse_search_results(html)
    return parsed_search_results


def run_from_json(
    input_path: str, output_dir: Path = settings.DEFAULT_OUTPUT_DIR
) -> None:
    """The main function that calls the functions of opening
    a file with source data, collecting and saving results.

    Args:
        input_path: Path to input JSON file
        output_dir: Directory to save results (default from settings)
    """

    logger.info("Crawler started...")
    logger.info(f"Start read input data from {input_path}")
    data = load_input_data(input_path)

    results = crawl_github(
        keywords=data["keywords"],
        proxies=data["proxies"],
        search_type=SearchType[data["type"].upper()],
    )

    output_path = save_output(
        keywords=data["keywords"],
        search_type=data["type"],
        results=results,
        output_dir=output_dir,
    )

    logger.info(f"Saved to {output_path}")
    logger.info(f"Execution time: {time.perf_counter() - start_time:.2f} sec")
