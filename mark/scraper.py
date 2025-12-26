import click
import asyncio
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
        click.echo(f"BrowserError while fetching {url}")
        return Page(url, body="BrowserError while fetching", title=None)
