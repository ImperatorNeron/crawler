from unittest.mock import MagicMock, patch
import pytest
from requests import RequestException
from github_crawler.core import settings
from github_crawler.crawler.fetcher import fetch_search_page, get_proxy_dict


def test_get_proxy_dict_results_with_valid_proxies_returns_chose_proxy_dict(
    common_proxy_dict,
):
    common_proxies = [
        "111.111.111.111:8080",
        "142.143.143.43:3333",
        "144.144.144.44:8888",
    ]
    expected = common_proxies[0]
    with patch("random.choice") as mock_choice:
        mock_choice.return_value = expected
        proxy = get_proxy_dict(common_proxies[0])
    assert proxy == common_proxy_dict


def test_get_proxy_dict_results_with_empty_proxies_list_returns_empty_dict():
    with pytest.raises(IndexError):
        assert get_proxy_dict([])


def test_fetch_search_page_results_with_valid_params_returns_html_text(
    sample_input_data,
    common_proxy_dict,
    mock_fetcher_deps,
):
    mock_get, mock_logger, mock_proxy_dict = mock_fetcher_deps
    expected_html = "<html>Test</html>"
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = expected_html

    result = fetch_search_page(
        keywords=sample_input_data["keywords"],
        search_type=sample_input_data["type"].capitalize(),
        proxies=sample_input_data["proxies"],
    )

    assert result == expected_html

    mock_get.assert_called_once_with(
        settings.BASE_URL,
        headers=settings.HEADERS,
        params={"q": "python testing", "type": sample_input_data["type"].capitalize()},
        proxies=common_proxy_dict,
        timeout=settings.TIMEOUT,
    )
    mock_proxy_dict.assert_called_once()
    mock_logger.info.assert_called_once()


@pytest.mark.parametrize(
    "attempts, expected_calls, should_succeed",
    [
        (3, 3, False),
        (2, 3, True),
        (1, 2, True),
        (0, 1, True),
    ],
)
def test_fetch_search_page_retry_behavior(
    sample_input_data,
    mock_fetcher_deps,
    attempts,
    expected_calls,
    should_succeed,
):
    mock_get, mock_logger, _ = mock_fetcher_deps
    expected_html = "<html>Success</html>"

    exceptions = [RequestException(f"Error {i}") for i in range(attempts)]
    responses = [*exceptions]
    if should_succeed:
        responses.append(MagicMock(status_code=200, text=expected_html))

    mock_get.side_effect = responses

    if should_succeed:
        result = fetch_search_page(
            keywords=sample_input_data["keywords"],
            search_type=sample_input_data["type"].capitalize(),
            proxies=sample_input_data["proxies"],
        )
        assert result == expected_html
        mock_logger.error.assert_not_called()
    else:
        with pytest.raises(RuntimeError):
            fetch_search_page(
                keywords=sample_input_data["keywords"],
                search_type=sample_input_data["type"].capitalize(),
                proxies=sample_input_data["proxies"],
            )
        mock_logger.error.assert_called_once()
    assert mock_get.call_count == expected_calls
