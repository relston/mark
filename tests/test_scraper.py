import pyppeteer
from mark import scraper
from unittest.mock import patch


def test_page_scrape(mock_web_page):
    html_content = """
        <!DOCTYPE html>
    <html>
    <head>
        <title>Basic HTML Page</title>
    </head>
    <body>
        <h1>Welcome to My Page</h1>
        <a href="https://www.example.com">Visit Example.com</a>
    </body>
    </html>
    """

    mock_web_page('https://supercool.com', html_content)

    page = scraper.get('https://supercool.com')

    assert page.title == 'Basic HTML Page'
    assert page.url == 'https://supercool.com'
    assert page.body == '\n\nBasic HTML Page\n\nWelcome to My Page\n' + \
        '==================\n\n[Visit Example.com](https://www.example.com)\n\n'


def test_timeout_error_handling():
    with patch('mark.scraper._render_page', side_effect=pyppeteer.errors.TimeoutError):
        page = scraper.get('https://timeout-test.com')

        assert page.body == 'Timeout while fetching page'
        assert page.title is None, "Expected no title when a TimeoutError occurs"
        assert page.url == 'https://timeout-test.com', "URL should be correct even when timeout occurs"
