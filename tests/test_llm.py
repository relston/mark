import pytest
from unittest.mock import patch, MagicMock
from mark.llm import get_completion

SELECTED_AGENT = {'system': 'I am a test system.'}
EXPECTED_RESPONSE = 'Hello, human!'

@pytest.fixture
def openai_mock():
    with patch('mark.llm.client') as mock:
        yield mock

def test_get_completion(openai_mock, mock_llm_request):
    # Prepare the mock return value simulating the structure of the OpenAI response
    completion_response = MagicMock(choices=[MagicMock(message=MagicMock(content=EXPECTED_RESPONSE))])

    # Configuring the mock to return our customized completion_response
    openai_mock.chat.completions.create.return_value = completion_response

    response = get_completion(mock_llm_request, SELECTED_AGENT)
    
    # Assert that the OpenAI API was called with the expected arguments
    openai_mock.chat.completions.create.assert_called_once_with(
        model='gpt-4o-2024-05-13',
        messages=[
            {'role': 'system', 'content': SELECTED_AGENT['system']},
            {'role': 'user', 'content':  mock_llm_request.to_payload()}
        ]
    )

    # Assert that the response matches the expected response
    assert response == EXPECTED_RESPONSE
