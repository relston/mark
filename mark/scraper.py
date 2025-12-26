import click
import asyncio
import sys
from crawl4ai import AsyncWebCrawler, BrowserConfig


class Document:
    """Simple document class to replace langchain Document."""
    def __init__(self, page_content='', metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}


class Page(object):
    def __init__(
            self,
            url,
            body: str = None,
            title: str = None):
        self.url = url
        self.body = body
        self.title = title

    def with_title(self, title: str):
        self.title = title
        return self

    def to_document(self):
        return Document(
            page_content=self.body,
            metadata={'title': self.title, 'url': self.url}
        )


async def _crawl(url: str):
    """Async helper to crawl a URL using crawl4ai."""
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        return await crawler.arun(url)


def _check_browsers_installed():
    """Check if Playwright browsers are installed."""
    try:
        # Try both playwright and patchright (crawl4ai uses patchright)
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            try:
                from patchright.sync_api import sync_playwright
            except ImportError:
                return False
        
        with sync_playwright() as p:
            browser = p.chromium
            browser_path = browser.executable_path
            if browser_path:
                from pathlib import Path
                return Path(browser_path).exists()
    except Exception:
        pass
    return False


def get(url: str) -> Page:
    """Fetch and process a URL, returning a Page instance."""
    try:
        result = asyncio.run(_crawl(url))
        
        # Extract markdown content
        markdown_content = result.markdown.raw_markdown if result.markdown else ""
        
        # Extract title from metadata
        title = result.metadata.get('title') if result.metadata else None
        
        # Create Page instance
        page = Page(url, body=markdown_content, title=title)
        
        return page
        
    except asyncio.TimeoutError:
        click.echo(f"Timeout while fetching {url}")
        return Page(url, body="Timeout while fetching page", title=None)
    except Exception as exc:
        # Check if this is a browser installation error
        error_msg = str(exc)
        if "Executable doesn't exist" in error_msg or "BrowserType.launch" in str(type(exc).__name__):
            click.echo(f"Browser not found while fetching {url}", err=True)
            click.echo("Playwright browsers need to be installed. Run:", err=True)
            click.echo("  mark-setup-browsers", err=True)
            click.echo("Or manually:", err=True)
            click.echo("  playwright install chromium", err=True)
            return Page(url, body="BrowserError while fetching", title=None)
        
        click.echo(f"BrowserError while fetching {url}")
        return Page(url, body="BrowserError while fetching", title=None)
