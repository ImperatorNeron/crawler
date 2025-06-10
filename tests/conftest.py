from unittest.mock import patch
import pytest


@pytest.fixture
def sample_input_data():
    return {
        "keywords": ["python", "testing"],
        "proxies": ["111.111.111.111:8080", "185.85.85.185:8080"],
        "type": "repositories",
    }


@pytest.fixture
def common_proxy_dict():
    proxy = "111.111.111.111:8080"
    return {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }


@pytest.fixture
def mock_fetcher_deps(common_proxy_dict):
    with (
        patch("requests.get") as mock_get,
        patch("github_crawler.crawler.fetcher.logger") as mock_logger,
        patch(
            "github_crawler.crawler.fetcher.get_proxy_dict",
            return_value=common_proxy_dict,
        ) as mock_proxy_dict,
    ):
        yield mock_get, mock_logger, mock_proxy_dict


@pytest.fixture
def mock_crawl_deps():
    """Combined fixture for crawl_github dependencies"""
    with (
        patch("github_crawler.main.logger") as mock_logger,
        patch("github_crawler.main.fetch_search_page") as mock_fetcher,
        patch("github_crawler.main.parse_search_results") as mock_parser,
    ):
        yield mock_logger, mock_fetcher, mock_parser


@pytest.fixture
def tmp_input_file(tmp_path):
    def _create_file(content):
        file_path = tmp_path / "input.json"
        file_path.write_text(content)
        return str(file_path)

    return _create_file
