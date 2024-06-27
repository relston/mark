import pytest
import os
from unittest.mock import patch
from langchain_core.documents import Document


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
    with patch('mark.llm._call_completion') as mock:
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
    url_to_content = {}

    def _mock(url, title, page_content):
        content = Document(page_content, metadata={'title': title})
        url_to_content[url] = content

    with patch('mark.markdown_file.Link._request_page_content') as mock:
        def side_effect(url):
            return url_to_content[url]
        mock.side_effect = side_effect
        yield _mock
