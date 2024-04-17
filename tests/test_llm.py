import pytest
from unittest.mock import patch, MagicMock
from mark.llm import get_completion

# Sample data for testing
PROMPT = "Hello, world!"
SELECTED_AGENT = {"system": "I am a test system."}
EXPECTED_RESPONSE = "Hello, human!"

@pytest.fixture
def openai_mock():
    with patch('mark.llm.client') as mock:
        yield mock

def test_get_completion(openai_mock):
    # Prepare the mock return value simulating the structure of the OpenAI response
    completion_response = MagicMock(choices=[MagicMock(message=MagicMock(content=EXPECTED_RESPONSE))])

    # Configuring the mock to return our customized completion_response
    openai_mock.chat.completions.create.return_value = completion_response

    # Call the function
    response = get_completion(PROMPT, SELECTED_AGENT)

    # Assertions
    openai_mock.chat.completions.create.assert_called_once()  # Ensure our API was called
    assert response == EXPECTED_RESPONSE  # Validate the response
