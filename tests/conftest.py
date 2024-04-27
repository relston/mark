import pytest
from unittest.mock import mock_open, patch

@pytest.fixture
def mock_file():
    def _mock_file(path, content):
        m = mock_open(read_data=content)
        m.return_value.name = path
        return patch('builtins.open', m)
    
    return _mock_file