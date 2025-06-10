import pytest
from github_crawler.crawler.parser import parse_search_results


VALID_HTML = """
    <div data-testid="results-list" class="Box-sc-g0xbh4-0 gZKkEq">
        <div class="Box-sc-g0xbh4-0 MHoGG search-title"><a class="prc-Link-Link-85e08"
            href="/farnodes/DevOps-Internship/issues/25">Issue1</a>
        </div>
        <div class="Box-sc-g0xbh4-0 MHoGG search-title"><a class="prc-Link-Link-85e08"
            href="/farnodes/DevOps-Internship/issues/26">Issue2</a>
        </div>
    </div>  
"""

INVALID_HTML = "<div>Hi from tests. Hope you fine:)< div>"

NO_LINKS_HTML = """
    <div data-testid="results-list">
        <div class="search-title">No links here</div>
    </div>
"""

OUTSIDE_BLOCK_HTML = """
    <div data-testid="results-list"></div>
    <div class="search-title">
        <a href="/invalid">Invalid link</a>
    </div>
"""

MIXED_CONTENT_HTML = """
    <div data-testid="results-list">
        <div class="wrong-class">
            <a href="/invalid">Invalid</a>
        </div>
        <div class="search-title">
            <a href="/valid">Valid</a>
        </div>
    </div>
"""


@pytest.mark.parametrize(
    "html, expected",
    [
        (
            VALID_HTML,
            [
                {"url": "https://github.com/farnodes/DevOps-Internship/issues/25"},
                {"url": "https://github.com/farnodes/DevOps-Internship/issues/26"},
            ],
        ),
        ("", []),
        (INVALID_HTML, []),
        (NO_LINKS_HTML, []),
        (OUTSIDE_BLOCK_HTML, []),
        (MIXED_CONTENT_HTML, [{"url": "https://github.com/valid"}]),
    ],
)
def test_parse_search_results_cases(html, expected):
    assert parse_search_results(html) == expected
