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
    A Markdown file with various images and links
                                        
    Local image:
    ![Local Image](./images/sample.png)

    Remote image:
    ![Remote Image](https://example.com/image.png)

    Relative image outside directory:
    ![Outside Image](../images/outside.png)

    External url link:
    [External URL](https://example.com)

    Local link:
    [Local Link](./local.md)

    Relative link outside directory:
    [Outside Link](../outside.md)
    """)

    # and the files exists in the file system
    markdown_file = create_file("test.md", mock_markdown_file_content)
    create_file("./images/sample.png", b"sample image data", binary=True)
    create_file("../images/outside.png", b"outside image data", binary=True)

    # and llm returning this response
    mock_llm_response.return_value = "Test completion"
    
    command([str(markdown_file)], None, None, False)

    # The llm will be called with the following request
    expected_llm_request = [
        {'role': 'system', 'content': 'You are a helpful LLM agent that always returns your response in Markdown format.'}, 
        {'role': 'user', 'content': [
                {'type': 'text', 'text': mock_markdown_file_content}, 
                {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,c2FtcGxlIGltYWdlIGRhdGE='}}, 
                {'type': 'image_url', 'image_url': {'url': 'https://example.com/image.png'}}, 
                {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,b3V0c2lkZSBpbWFnZSBkYXRh'}}
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
    