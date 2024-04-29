import pytest
from unittest.mock import MagicMock, mock_open, patch

@pytest.fixture
def mock_file():
    def _mock_file(path, content):
        m = mock_open(read_data=content)
        m.return_value.name = path
        return patch('builtins.open', m)
    
    return _mock_file



mock_markdown_file_content = """
Describe these images in vivid detail

![So horrifying](https://example.com/image.jpg)

![So beautiful](./image2.jpg)

***GPT Response (model: test_model, agent: pytest)**
Oh god, I can't even look at that first image. It's so horrifying. The second one is so beautiful though.

***User Response**
I know, right? I can't believe how different they are.
"""

@pytest.fixture
def mock_markdown_file():
    md_file = MagicMock()
    md_file.file_path = 'path/to/docs/markdown.md'
    md_file.content = mock_markdown_file_content
    md_file.images = [
        {
            'alt': 'So horrifying',
            'src': 'https://example.com/image.jpg',
            'image_path': 'https://example.com/image.jpg',
        },
        {
            'alt': 'So beautiful',
            'src': './image2.jpg',
            'image_path': './image2.jpg'
        }
    ]
    return md_file

@pytest.fixture
def mock_llm_request():
    llm_request = MagicMock()
    llm_request.to_payload.return_value = [
        {'type': 'text', 'text': mock_markdown_file_content},
        {'type': 'image_url', 'image_url': {'url': 'https://example.com/image.jpg'}},
        {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,d29ybGQgaW1hZ2UgY29udGVudA=='}}
    ]
    return llm_request