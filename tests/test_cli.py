from mark.cli import command
from textwrap import dedent
from mark import config
import pytest
import os
import sys
import io
import llm
from unittest.mock import Mock

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
    def define_files(
            self,
            create_file,
            mock_llm_response,
            mock_web_page,
            mock_image_generation):
        config.reset()

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

        Local file link:
        [Anther Reference](./docs/another-reference.md)
        """)

        # and the files exists in the file system
        self.markdown_file = create_file(
            "test.md", self.mock_markdown_file_content)
        create_file("./images/sample.png", b"sample image data", binary=True)
        create_file(
            "../images/outside.png",
            b"outside image data",
            binary=True)
        create_file("./docs/another-reference.md", "Another reference content")

        # and the external url link returns this response
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Basic HTML Page</title>
        </head>
        <body>
            <h1>Welcome to My Page</h1>
            <a href="https://www.example.com">Visit Example.com</a>
        </body>
        </html>
        """
        mock_web_page('https://example.com/some-article', html_content)

        # and llm returning this response
        mock_llm_response.return_value = "Test completion"
        mock_image_generation.return_value = Mock(
            url='https://generated.image.url/image.png',
            revised_prompt='A revised mock image prompt'
        )

        self.default_system_prompt = dedent(
            """
            You are a helpful LLM agent that will receive user input in the form of a markdown file.
            The contents of the file will be used as context and the specific prompt from the use will be located at the end of the file.
            Your response to the users request should also be written in markdown format.

            RULES:
            - Do not echo back any of the input into your response to the user.
            - If using a heading in your response, start with a level 2 heading
            """
        )

        self.default_expected_context = dedent(
            """
            Link Text: External URL
            SRC: https://example.com/some-article
            Page Title: Basic HTML Page
            Page Content:


            Basic HTML Page

            Welcome to My Page
            ==================

            [Visit Example.com](https://www.example.com)


            ---
            Link Text: Anther Reference
            SRC: ./docs/another-reference.md
            Page Title: another-reference.md
            Page Content:
            Another reference content
            """
        )

        self.default_expected_system_message = self.default_expected_context + \
            self.default_system_prompt

        self.default_expected_llm_request = [
            {'role': 'system', 'content': self.default_expected_system_message},
            {'role': 'user', 'content': [
                {'type': 'text', 'text': self.mock_markdown_file_content},
                {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,c2FtcGxlIGltYWdlIGRhdGE='}},
                {'type': 'image_url', 'image_url': {'url': 'https://example.com/image.png'}},
                {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,b3V0c2lkZSBpbWFnZSBkYXRh'}},
            ]
            }
        ]
        self.default_expected_attachements = [
            llm.Attachment(path='./images/sample.png'),
            llm.Attachment(url='https://example.com/image.png'),
            llm.Attachment(path='../images/outside.png')
        ]

    def test_command_default(self, mock_llm_response):
        """Test CLI command without specifying an agent (default agent should be used)."""

        # Run the CLI command with only the markdown file
        command([str(self.markdown_file)], None, None, False)

        mock_llm_response.assert_called_once_with(
            self.mock_markdown_file_content, 
            system=self.default_expected_system_message,
            attachments=self.default_expected_attachements
        )

        # The markdown file will be updated with the response
        expected_markdown_file_content = self.mock_markdown_file_content + \
            dedent("""
            # GPT Response (model: gpt-4o, system: default)
            Test completion

            # User Response
            """)

        assert self.markdown_file.read_text() == expected_markdown_file_content

    def test_command_with_stdin(self, mock_llm_response, mock_stdout):
        byte_string = self.mock_markdown_file_content.encode('utf-8')
        input = io.TextIOWrapper(io.BytesIO(byte_string), encoding='utf-8')
        sys.stdin = input

        command(['-'], None, None, False)

        mock_llm_response.assert_called_once_with(
            self.mock_markdown_file_content, 
            system=self.default_expected_system_message,
            attachments=self.default_expected_attachements
        )

        mock_stdout.assert_called_once_with("Test completion")

    def test_command_custom_agent(self, create_file, mock_llm_response):
        # Define a custom agent
        create_file(
            self.config_path / 'system_prompts/custom.md',
            """You're a custom agent that ....."""
        )

        # Run the CLI command with the custom agent
        command([str(self.markdown_file), '--system=custom'], None, None, False)

        expected_system_message = self.default_expected_context + \
            "\nYou're a custom agent that ....."

        mock_llm_response.assert_called_once_with(
            self.mock_markdown_file_content, 
            system=expected_system_message,
            attachments=self.default_expected_attachements
        )

        # The markdown file will be updated indicating the custom agent
        expected_markdown_file_content = self.mock_markdown_file_content + \
            dedent("""
            # GPT Response (model: gpt-4o, system: custom)
            Test completion

            # User Response
            """)
        assert self.markdown_file.read_text() == expected_markdown_file_content

    def test_command_generate_image(self, mock_image_generation):
        """
        Test CLI command with the --generate-image option.
        """

        command([str(self.markdown_file), '--generate-image'], None, None, False)

        expected_prompt = self.default_expected_system_message + \
            "\n" + self.mock_markdown_file_content
        mock_image_generation.assert_called_once_with(
            expected_prompt, "dall-e-3")

        # The markdown file will be updated with the generated image URL
        expected_markdown_file_content = self.mock_markdown_file_content + \
            dedent("""
            # GPT Response (model: dall-e-3, system: default)
            A revised mock image prompt

            ![Generated Image](https://generated.image.url/image.png)

            # User Response
            """)

        assert self.markdown_file.read_text() == expected_markdown_file_content
