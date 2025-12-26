import asyncio
from mark import scraper
from unittest.mock import patch


def test_page_scrape(mock_web_page):
    # Expected markdown output format (matching what the test expects)
    expected_markdown = '\n\nBasic HTML Page\n\nWelcome to My Page\n' + \
        '==================\n\n[Visit Example.com](https://www.example.com)\n\n'
    
    # Mock crawl4ai to return the expected markdown and title
    mock_web_page(
        'https://supercool.com',
        markdown_content=expected_markdown,
        title='Basic HTML Page'
    )

    page = scraper.get('https://supercool.com')

    assert page.title == 'Basic HTML Page'
    assert page.url == 'https://supercool.com'
    assert page.body == expected_markdown


def test_timeout_error_handling():
    # Mock the async crawl function to raise TimeoutError
    with patch('mark.scraper._crawl', side_effect=asyncio.TimeoutError, create=True):
        page = scraper.get('https://timeout-test.com')

        assert page.body == 'Timeout while fetching page'
        assert page.title is None, "Expected no title when a TimeoutError occurs"
        assert page.url == 'https://timeout-test.com', "URL should be correct even when timeout occurs"
