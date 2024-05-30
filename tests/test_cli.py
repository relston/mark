from click.testing import CliRunner
from mark.cli import command
from textwrap import dedent

"""
These tests are meant to act as 'functional-lite'. Maximizing code coverage for 
each of the main use cases of the CLI command and minimizing the number of 
basic unit tests needed for each individual module.

We just mock out the files and the OpenAI API calls, and then test the CLI
"""

def test_command_default(create_file, mock_llm_response):
    """Test CLI command without specifying an agent (default agent should be used)."""

    # Given a markdown file with the following content
    mock_markdown_file_content = dedent("""
    Describe these images in vivid detail

    ![So horrifying](https://example.com/image.jpg)

    ![So beautiful](./image2.jpg)

    ***GPT Response (model: test_model, agent: pytest)**
    Oh god, I can't even look at that first image. It's so horrifying. The second one is so beautiful though.

    ***User Response**
    I know, right? I can't believe how different they are.
    """)

    # and the files exists in the file system
    markdown_file = create_file("test.md", mock_markdown_file_content)
    create_file("image2.jpg", b"This is an image", binary=True)

    # and llm returning this response
    mock_llm_response.return_value = "Test completion"
    
    command([str(markdown_file)], None, None, False)

    # The llm will be called with the following request
    expected_llm_request = [
        {'role': 'system', 'content': 'You are a helpful LLM agent that always returns your response in Markdown format.'}, 
        {'role': 'user', 'content': [
                {'type': 'text', 'text': mock_markdown_file_content}, 
                {'type': 'image_url', 'image_url': {'url': 'https://example.com/image.jpg'}}, 
                {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,VGhpcyBpcyBhbiBpbWFnZQ=='}}
            ]
        }
    ]
    mock_llm_response.assert_called_once_with(expected_llm_request, 'gpt-4o-2024-05-13')
    
    # The markdown file will be updated with the response
    new_markdown_file_content = markdown_file.read_text()
    expected_markdown_file_content = mock_markdown_file_content + dedent(
        """
        **GPT Response (model: gpt-4o-2024-05-13, agent: default)**
        Test completion

        **User Response**
        """
    )
    assert new_markdown_file_content == expected_markdown_file_content
