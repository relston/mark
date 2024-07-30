import click
from mark import llm
from mark.llm_request import LLMRequest
from mark.markdown_file import MarkdownFile
from mark.config import get_config
from importlib.metadata import version, PackageNotFoundError

try:
    package_version = version("mark")
except PackageNotFoundError:
    package_version = "unknown"


@click.command()
@click.argument('file', type=click.File())
@click.option('--system', '-s', type=click.STRING, default='default', help='The system prompt to use')
@click.option('--generate-image', '-i', is_flag=True, default=False,
              help='EXPERIMENTAL: Generate an image using DALL-E.')
@click.version_option(version=package_version)
def command(file, system, generate_image):
    """
    Markdown powered LLM CLI - Multi-modal AI text generation tool

    In-document Thread Example:
    mark path/to/markdown.md

    stdin Example:
    echo "Hello, World!" | mark -
    """
    system_prompt = get_config().system_prompts().get(system, 'default')
    markdown_file = MarkdownFile(file)
    request = LLMRequest() \
        .with_prompt(markdown_file.content) \
        .with_system_message(system_prompt)

    [request.with_image(image) for image in markdown_file.images]
    [request.with_link(link) for link in markdown_file.links]

    if generate_image:
        response = llm.generate_image(request)
    else:
        response = llm.get_completion(request)

    response.with_system(system)

    if markdown_file.file_path:
        with open(markdown_file.file_path, "a") as file:
            file.write(response.to_markdown())
    else:
        click.echo(response.content)
