import pytest
from unittest.mock import patch, MagicMock
from mark.llm import get_completion

SELECTED_AGENT = {'system': 'I am a test system.'}
EXPECTED_RESPONSE = 'Hello, human!'

def test_get_completion(mock_llm_response, mock_llm_request):
    
    # Configuring the mock to return our customized completion_response
    mock_llm_response.return_value = EXPECTED_RESPONSE

    response = get_completion(mock_llm_request, SELECTED_AGENT)
    
    # Assert that the OpenAI API was called with the expected arguments
    mock_llm_response.assert_called_once_with(
        [
            {'role': 'system', 'content': SELECTED_AGENT['system']},
            {'role': 'user', 'content':  mock_llm_request.to_payload()}
        ],
        'gpt-4o-2024-05-13'
    )

    # Assert that the response matches the expected response
    assert response == EXPECTED_RESPONSE
