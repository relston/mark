# Migration Plan: Replace pyppeteer with crawl4ai

## Overview
Replace the current `mark/scraper.py` implementation that uses `pyppeteer` and `markdownify` with `crawl4ai`, while maintaining backward compatibility with the existing public API (`Document`, `Page`, `get(url)`).

## Current State Analysis

### Public API (Must Preserve)
- `Document` class: `page_content`, `metadata` dict
- `Page` class: `url`, `body`, `title`, `with_title()`, `to_document()` (`.soup` attribute will be removed)
- `get(url: str) -> Page`: Synchronous function that fetches and processes a URL

### Current Dependencies
- `pyppeteer`: Browser automation (to be removed)
- `markdownify`: HTML to markdown conversion (to be removed)
- `beautifulsoup4`: HTML parsing (to be removed - crawl4ai provides markdown directly)

### Current Error Handling
- `BrowserError` → returns page with body "BrowserError while fetching"
- `TimeoutError` → returns page with body "Timeout while fetching page"

### Test Requirements
- `test_page_scrape`: Verifies title, URL, and markdown body content
- `test_timeout_error_handling`: Verifies timeout error message format
- Mock fixture `mock_web_page` patches `get_rendered_html`

## Tasks

## Phase 1: Research and Setup
Set up crawl4ai and understand its API surface

- [x] a) Research crawl4ai API: understand `AsyncWebCrawler`, `BrowserConfig`, response structure (`markdown`, `html`, `metadata`)
- [x] b) Add crawl4ai dependency to `pyproject.toml` (check latest stable version)
- [x] c) Add playwright as optional dependency if needed by crawl4ai
- [x] d) Run `poetry install` and verify crawl4ai imports successfully
- [x] e) Test crawl4ai manually with a simple URL to understand output format

### Phase 1 Findings

**crawl4ai API Structure:**
- `AsyncWebCrawler(config=BrowserConfig(headless=True))` - async context manager
- `crawler.arun(url)` returns `CrawlResultContainer`
- Response structure:
  - `result.markdown.raw_markdown` - markdown string (use this for `Page.body`)
  - `result.metadata` - dict with `{'title': str, 'description': ..., 'keywords': ..., 'author': ...}` (use `metadata['title']` for `Page.title`)
  - `result.url` - the URL that was crawled
  - `result.status_code` - HTTP status code
  - `result.success` - boolean indicating success
- **Note**: crawl4ai provides clean markdown directly, so BeautifulSoup is not needed

**Dependencies:**
- crawl4ai 0.7.8 requires `patchright` (playwright fork) which is automatically installed
- Playwright browsers need to be installed: `playwright install chromium` (or `crawl4ai-setup`)
- Note: pyppeteer conflicts with crawl4ai (pyee version conflict) - will be removed in Phase 4

**BrowserConfig:**
- Supports `headless=True` for headless mode
- Many other options available but minimal config works fine

## Phase 2: Test Updates (TDD Approach)
Update tests to work with crawl4ai mocking strategy

- [x] a) Update `conftest.py` fixture `mock_web_page` to mock crawl4ai's `_crawl()` function instead of `get_rendered_html()`
- [x] b) Ensure mock returns structure matching crawl4ai response: `markdown.raw_markdown`, `metadata` (no need to mock HTML since we're not using BeautifulSoup)
- [x] c) Update `test_timeout_error_handling` to mock `asyncio.TimeoutError` from crawl4ai context
- [x] d) Run tests and verify they fail with expected errors (TDD red phase)

### Phase 2 Results

**Test Updates Completed:**
- Updated `mock_web_page` fixture to mock `mark.scraper._crawl()` (using `create=True` since function doesn't exist yet)
- Mock returns crawl4ai result structure: `SimpleNamespace` with `markdown.raw_markdown` and `metadata['title']`
- Updated `test_page_scrape` to use new mock API: `mock_web_page(url, markdown_content, title)`
- Updated `test_timeout_error_handling` to patch `_crawl` with `asyncio.TimeoutError`

**TDD Red Phase Verified:**
- Tests fail as expected because `scraper.get()` still uses old implementation (`get_rendered_html()`)
- Mocks are correctly set up for Phase 3 implementation
- Ready to proceed to Phase 3 where `_crawl()` will be implemented and tests should pass

## Phase 3: Implementation
Replace scraper implementation while maintaining public API

- [ ] a) Remove `pyppeteer`, `markdownify`, and `beautifulsoup4` imports from `scraper.py`
- [ ] b) Add crawl4ai imports: `AsyncWebCrawler`, `BrowserConfig` (and any other needed)
- [ ] c) Update `Page` class: remove `soup` parameter and attribute (tests don't use it)
- [ ] d) Keep `Document` class unchanged
- [ ] e) Create async helper `_crawl(url: str)` that uses `AsyncWebCrawler` with appropriate `BrowserConfig`
- [ ] f) Update `get(url: str)` to call `asyncio.run(_crawl(url))` and convert crawl4ai response to `Page` instance
- [ ] g) Map crawl4ai's `markdown.raw_markdown` to `Page.body`
- [ ] h) Extract title from crawl4ai `metadata['title']`, set on `Page`
- [ ] i) Implement error handling: catch `asyncio.TimeoutError` and return page with "Timeout while fetching page"
- [ ] j) Implement error handling: catch other exceptions and return page with "BrowserError while fetching"
- [ ] k) Remove helper functions: `get_rendered_html()`, `_render_page()`, `_clean_soup_from_html()`, `_markdown_from_soup()`

## Phase 4: Cleanup and Verification
Remove old dependencies and verify everything works

- [ ] a) Remove `pyppeteer` from `pyproject.toml` dependencies
- [ ] b) Remove `markdownify` from `pyproject.toml` dependencies
- [ ] c) Remove `beautifulsoup4` from `pyproject.toml` dependencies
- [ ] d) Run `poetry lock` to update lock file
- [ ] e) Run all tests: `poetry run pytest tests/test_scraper.py -v`
- [ ] f) Run full test suite: `poetry run pytest`
- [ ] g) Test manually with a real URL to verify end-to-end functionality
- [ ] h) Verify that `markdown_file.py` integration still works (test with a markdown file containing web links)

## Phase 5: Documentation and CI Updates
Update documentation and CI if needed

- [ ] a) Check if README mentions pyppeteer or browser requirements, update if needed
- [ ] b) Update CI workflow if crawl4ai requires browser setup (`crawl4ai-setup` command)
- [ ] c) Document any new runtime requirements (e.g., playwright browsers) in README if applicable

## Phase 6: Optional Enhancements
Future improvements that can be done post-migration

- [ ] a) Consider exposing async `aget(url)` method for concurrent scraping
- [ ] b) Add retry logic with exponential backoff
- [ ] c) Add configuration options (timeout, headless mode) via CLI or config
- [ ] d) Consider using crawl4ai's caching features for development

## Notes

### Key Design Decisions
1. **Maintain sync API**: Use `asyncio.run()` inside `get()` to keep the public API synchronous, avoiding changes to `markdown_file.py`
2. **Remove BeautifulSoup**: crawl4ai provides clean markdown directly via `markdown.raw_markdown`, so BeautifulSoup is unnecessary
3. **Remove `.soup` attribute**: Tests don't use it, and crawl4ai's markdown output eliminates the need for HTML parsing
4. **Error message compatibility**: Maintain exact error strings to avoid test changes
5. **Minimal changes**: Only modify `scraper.py` and test fixtures, no changes to callers

### Potential Challenges
- Crawl4ai's markdown format might differ from markdownify - may need to verify/test output format (tests will catch this)
- Browser setup in CI environments (playwright browsers need to be installed)
- Timeout handling might need adjustment based on crawl4ai's timeout model
- Removing `.soup` attribute is safe since tests don't assert on it
