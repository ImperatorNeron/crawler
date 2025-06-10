from unittest.mock import patch
import pytest

from github_crawler.core.search_type import SearchType
from github_crawler.main import crawl_github, run_from_json


def test_crawl_github_valid_inputs_returns_expected_results(mock_crawl_deps):
    mock_logger, mock_fetcher, mock_parser = mock_crawl_deps
    mock_fetcher.return_value = "<html>Very simple</html>"
    mock_parser.return_value = [{"url": "https://repo1"}, {"url": "https://repo2"}]

    results = crawl_github(
        keywords=["test"],
        proxies=["111.111.111.111:8080"],
        search_type=SearchType.REPOSITORIES,
    )

    mock_logger.info.assert_called()
    mock_fetcher.assert_called_once_with(
        ["test"],
        "repositories",
        ["111.111.111.111:8080"],
    )
    mock_parser.assert_called_once_with("<html>Very simple</html>")
    assert results == [{"url": "https://repo1"}, {"url": "https://repo2"}]


def test_crawl_github_empty_results_returns_empty_list(mock_crawl_deps):
    mock_logger, mock_fetcher, mock_parser = mock_crawl_deps
    mock_fetcher.return_value = "<html>Very simple</html>"
    mock_parser.return_value = []

    results = crawl_github(
        keywords=["empty"],
        proxies=["111.111.111.111:8080"],
        search_type=SearchType.ISSUES,
    )

    assert results == []
    mock_logger.info.call_count == 2


def test_crawl_github_fetch_error_raises_exception(mock_crawl_deps):
    _, mock_fetcher, _ = mock_crawl_deps
    mock_fetcher.side_effect = Exception("Simple error")

    with pytest.raises(Exception):
        crawl_github(["test"], [], SearchType.REPOSITORIES)


@patch("github_crawler.main.crawl_github")
@patch("github_crawler.main.save_output")
@patch("github_crawler.main.load_input_data")
def test_run_from_json_valid_inputs_saves_output(
    mock_load,
    mock_save,
    mock_crawl,
    tmp_path,
    sample_input_data,
):
    mock_load.return_value = sample_input_data
    mock_crawl.return_value = [{"url": "https://repo1"}]

    run_from_json("input.json", output_dir=tmp_path)

    mock_load.assert_called_once_with("input.json")
    mock_crawl.assert_called_once_with(
        keywords=["python", "testing"],
        search_type=SearchType.REPOSITORIES,
        proxies=["111.111.111.111:8080", "185.85.85.185:8080"],
    )
    mock_save.assert_called_once_with(
        keywords=["python", "testing"],
        search_type="repositories",
        results=[{"url": "https://repo1"}],
        output_dir=tmp_path,
    )


@patch("github_crawler.main.load_input_data")
def test_run_from_json_invalid_type_raises_KeyError(mock_load, sample_input_data):
    mock_load.return_value = {**sample_input_data, "type": "invalid"}

    with pytest.raises(KeyError):
        run_from_json("invalid_input.json")


@patch("github_crawler.main.load_input_data")
def test_run_from_json_missing_keys_raises_KeyError(mock_load):
    mock_load.return_value = {"keywords": ["test"]}

    with pytest.raises(KeyError):
        run_from_json("invalid_input.json")
