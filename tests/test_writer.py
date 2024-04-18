import pytest
from unittest.mock import mock_open, patch
from mark.writer import write_response
from IPython import embed

def test_write_response():
    # Define the details of the test case
    file_name = "dummy_file.txt"
    message = "This is a test GPT response."
    agent = "pytest"
    model = "test_model"

    # Expected content format
    expected_content = f"""
**GPT Response (model: {model}, agent: {agent})**
{message}

**User Response**
"""

    # Use patch to mock open function within the context of the write_response function
    with patch("builtins.open", mock_open()) as mocked_file:
        # Call the function under test
        write_response(file_name=file_name, message=message, agent=agent, model=model)

        # Ensure the mocked open function was called correctly
        mocked_file.assert_called_once_with(file_name, "a")  # Ensuring 'append' mode is used
        
        # Ensure write was called with the expected content
        mocked_file().write.assert_called_once_with(expected_content)