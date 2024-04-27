from mark.writer import write_response
from IPython import embed

file_name = "dummy_file.txt"
message = "This is a test GPT response."
agent = "pytest"
model = "test_model"

expected_content = f"""
**GPT Response (model: {model}, agent: {agent})**
{message}

**User Response**
"""

def test_write_response(mock_file):    
    with mock_file(file_name, '') as mock_open:
        write_response(file_name=file_name, message=message, agent=agent, model=model)
        mock_open.assert_called_once_with(file_name, "a")
        mock_open().write.assert_called_once_with(expected_content)