import pytest
import os
from unittest.mock import patch
from langchain_core.documents import Document

@pytest.fixture
def mock_llm_response():
    with patch('mark.llm._call_model') as mock:
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