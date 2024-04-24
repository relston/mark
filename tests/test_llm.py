import pytest
from unittest.mock import patch, MagicMock, mock_open
from mark.llm import get_completion
from mark.llm_request import parse_markdown_content

PROMPT = 'Hello, check out the picture of this ![world](./world.jpg)!'
SELECTED_AGENT = {'system': 'I am a test system.'}
EXPECTED_RESPONSE = 'Hello, human!'

@pytest.fixture
def mock_file():
    mocked_open_function = mock_open(read_data=b'world image content')
    with patch('builtins.open', mocked_open_function):
        yield

@pytest.fixture
def openai_mock():
    with patch('mark.llm.client') as mock:
        yield mock

def test_get_completion(openai_mock, mock_file):
    # Prepare the mock return value simulating the structure of the OpenAI response
    completion_response = MagicMock(choices=[MagicMock(message=MagicMock(content=EXPECTED_RESPONSE))])

    llm_request = parse_markdown_content(PROMPT)

    # Configuring the mock to return our customized completion_response
    openai_mock.chat.completions.create.return_value = completion_response

    response = get_completion(llm_request, SELECTED_AGENT)

    # Assert that the OpenAI API was called with the expected arguments
    openai_mock.chat.completions.create.assert_called_once_with(
        model='gpt-4-turbo',
        messages=[
            {'role': 'system', 'content': SELECTED_AGENT['system']},
            {'role': 'user', 'content':  [
                    {'type': 'text', 'text': PROMPT}, 
                    {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,d29ybGQgaW1hZ2UgY29udGVudA=='}}
                ]
            }
        ]
    )

    # Assert that the response matches the expected response
    assert response == EXPECTED_RESPONSE
