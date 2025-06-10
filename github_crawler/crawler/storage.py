import json
from pathlib import Path
from datetime import datetime
import re

from github_crawler.core import settings


def load_input_data(path: str) -> dict:
    """Loads JSON data from json input file"""

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sanitize_filename(filename: str) -> str:
    """Cleans filename by replacing invalid characters with underscores."""

    return re.sub(r'[<>:"/\\|?*%]', "_", filename)


def save_output(
    keywords: list[str],
    search_type: str,
    results: list[dict[str, str]],
    output_dir: Path = settings.DEFAULT_OUTPUT_DIR,
) -> Path:
    """Saves scraping results to JSON file with timestamped filename.

    Args:
        keywords: Search terms
        search_type: GitHub search type: repositories, wikis, issues
        results: List of result dictionaries
        output_dir: Directory to save results (default from settings)

    Returns:
        Path to created output file
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = sanitize_filename(
        f"output_{timestamp}_{'_'.join(keywords)}_{search_type}.json"
    )
    output_path = output_dir / filename

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    return output_path
