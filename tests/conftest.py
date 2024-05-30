import pytest
from unittest.mock import patch

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