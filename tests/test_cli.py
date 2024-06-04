from mark.cli import command
from textwrap import dedent
import pytest
import os

"""
These tests are meant to act as 'functional-lite'. Maximizing code coverage for 
each of the main use cases of the CLI command and minimizing the number of 
basic unit tests needed for each individual module.

We just mock out the files and the OpenAI API calls, and then test the CLI
"""

class TestCLI:
    @pytest.fixture(autouse=True)
    def use_tmp_config_path(self, tmp_path):
        # MARK_CONFIG_PATH defaults to ~/.mark 
        # for all tests we use a temporary directory
        self.config_path = tmp_path / 'config'
        os.environ['MARK_CONFIG_PATH'] = str(self.config_path)

    @pytest.fixture(autouse=True)
    def define_files(self, create_file, mock_llm_response, mock_web_page):
        # Given a markdown file with the following content
        self.mock_markdown_file_content = dedent("""
        A Markdown file with various images and links
                                            
        Local image:
        ![Local Image](./images/sample.png)

        Remote image:
        ![Remote Image](https://example.com/image.png)

        Relative image outside directory:
        ![Outside Image](../images/outside.png)

        External url link:
        [External URL](https://example.com/some-article)
        """)

        mock_web_page("https://example.com/some-article", "Example link title", "Content of the external url link")

        # and the files exists in the file system
        self.markdown_file = create_file("test.md", self.mock_markdown_file_content)
        create_file("./images/sample.png", b"sample image data", binary=True)
        create_file("../images/outside.png", b"outside image data", binary=True)

        # and llm returning this response
        mock_llm_response.return_value = "Test completion"

    def test_command_default(self, mock_llm_response):
        """Test CLI command without specifying an agent (default agent should be used)."""

        # Run the CLI command with only the markdown file
        command([str(self.markdown_file)], None, None, False)

        expected_system_message = dedent(
            """
            Link Text: External URL
            Title: Example link title
            URL: https://example.com/some-article
            Page Content:
            Content of the external url link
            
            You are a helpful LLM agent that always returns your response in Markdown format."""
        )
        
        # The llm will be called with the following request
        expected_llm_request = [
            {'role': 'system', 'content': expected_system_message}, 
            {'role': 'user', 'content': [
                    {'type': 'text', 'text': self.mock_markdown_file_content}, 
                    {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,c2FtcGxlIGltYWdlIGRhdGE='}}, 
                    {'type': 'image_url', 'image_url': {'url': 'https://example.com/image.png'}}, 
                    {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,b3V0c2lkZSBpbWFnZSBkYXRh'}},
                ]
            }
        ]
        mock_llm_response.assert_called_once_with(expected_llm_request, 'gpt-4o-2024-05-13')
        
        # The markdown file will be updated with the response
        expected_markdown_file_content = self.mock_markdown_file_content + dedent(
            """
            **GPT Response (model: gpt-4o-2024-05-13, agent: default)**
            Test completion

            **User Response**
            """
        )
        assert self.markdown_file.read_text() == expected_markdown_file_content
        
    def test_command_custom_agent(self, create_file, mock_llm_response):
        # Define a custom agent
        create_file(
            self.config_path / 'agents/custom.yaml', 
            """system: >
                You're a custom agent that ....."""
        )

        # Run the CLI command with the custom agent
        command([str(self.markdown_file), '--agent=custom'], None, None, False)

        expected_system_message = dedent(
            """
            Link Text: External URL
            Title: Example link title
            URL: https://example.com/some-article
            Page Content:
            Content of the external url link
            
            You're a custom agent that ....."""
        )

        # The llm will be called with the following request
        expected_llm_request = [
            {'role': 'system', 'content': expected_system_message}, 
            {'role': 'user', 'content': [
                    {'type': 'text', 'text': self.mock_markdown_file_content}, 
                    {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,c2FtcGxlIGltYWdlIGRhdGE='}}, 
                    {'type': 'image_url', 'image_url': {'url': 'https://example.com/image.png'}}, 
                    {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,b3V0c2lkZSBpbWFnZSBkYXRh'}},
                ]
            }
        ]
        mock_llm_response.assert_called_once_with(expected_llm_request, 'gpt-4o-2024-05-13')
        
        # The markdown file will be updated indicating the custom agent
        expected_markdown_file_content = self.mock_markdown_file_content + dedent(
            """
            **GPT Response (model: gpt-4o-2024-05-13, agent: custom)**
            Test completion

            **User Response**
            """
        )
        assert self.markdown_file.read_text() == expected_markdown_file_content
