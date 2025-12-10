import pytest
import os
from unittest.mock import patch
import llm


@pytest.fixture(autouse=True)
def mock_openai_key():
    os.environ['OPENAI_API_KEY'] = 'test_key'


@pytest.fixture(autouse=True)
def mock_cwd(tmp_path):
    with patch('os.getcwd') as mock:
        mock.return_value = tmp_path
        yield mock


@pytest.fixture
def mock_stdout():
    with patch('click.echo') as mock:
        yield mock


@pytest.fixture
def mock_llm_response():
    with patch('llm.models._Model.prompt') as mock:
        yield mock


@pytest.fixture
def mock_llm_get_model():
    get_model_method = llm.get_model

    with patch('llm.get_model') as mock:
        mock.side_effect = get_model_method
        yield mock


@pytest.fixture
def mock_image_generation():
    with patch('mark.llm._call_generate_image') as mock:
        yield mock


@pytest.fixture
def create_file(tmp_path):
    def _create_file(file_path, content, binary=False):
        file = tmp_path / file_path
        file.parent.mkdir(parents=True, exist_ok=True)
        if binary:
            file.write_bytes(content)
        else:
            file.write_text(content, encoding="utf-8")
        return file
    return _create_file


@pytest.fixture
def mock_web_page():
    """Mock crawl4ai's _crawl() function to return test data"""
    from types import SimpleNamespace
    from unittest.mock import AsyncMock, patch
    
    url_to_result = {}

    def _mock(url, markdown_content, title=None):
        """Helper to set up mock data for a URL.
        
        Args:
            url: The URL to mock
            markdown_content: The markdown content to return (for Page.body)
            title: The title to return in metadata
        """
        # Create a mock crawl4ai result structure
        mock_markdown = SimpleNamespace(raw_markdown=markdown_content)
        mock_metadata = {'title': title} if title else {}
        
        mock_result = SimpleNamespace(
            markdown=mock_markdown,
            metadata=mock_metadata,
            url=url,
            status_code=200,
            success=True
        )
        url_to_result[url] = mock_result

    async def mock_crawl(url):
        """Mock _crawl() async function"""
        if url in url_to_result:
            return url_to_result[url]
        # Default fallback
        mock_markdown = SimpleNamespace(raw_markdown="")
        return SimpleNamespace(
            markdown=mock_markdown,
            metadata={},
            url=url,
            status_code=200,
            success=True
        )

    with patch('mark.scraper._crawl', new_callable=AsyncMock, side_effect=mock_crawl, create=True):
        yield _mock
