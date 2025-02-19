import click
from click_default_group import DefaultGroup
from click.testing import CliRunner
from mark import llm
from llm.cli import cli as llm_cli
from mark.llm_request import LLMRequest
from mark.markdown_file import MarkdownFile
from mark.config import get_config
from importlib.metadata import version, PackageNotFoundError

try:
    package_version = version("mark")
except PackageNotFoundError:
    package_version = "unknown"

DEFAULT_MODEL = "gpt-4o"
DALL_E_MODEL = "dall-e-3"


@click.group(
    cls=DefaultGroup,
    default="down",
    default_if_no_args=True,
)
@click.version_option(version=package_version)
def mark_cli():
    """Markdown powered LLM CLI - Multi-modal AI text generation tool"""


@mark_cli.command(name="down")
@click.argument('file', type=click.File())
@click.option('--system', '-s', type=click.STRING,
              default='default', help='The system prompt to use')
@click.option('--model', '-m', type=click.STRING, help='The llm model')
@click.option('--generate-image', '-i', is_flag=True, default=False,
              help='EXPERIMENTAL: Generate an image using DALL-E.')
def down(file, system, model, generate_image):
    """
    Default: Process markdown file or stdin

    In-document Thread Example:
    mark path/to/markdown.md

    stdin Example:
    echo "Hello, World!" | mark -
    """
    system_prompt = get_config().system_prompts().get(system, 'default')
    markdown_file = MarkdownFile(file)

    if not model:
        model = DALL_E_MODEL if generate_image else DEFAULT_MODEL

    request = LLMRequest(model) \
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


@mark_cli.command("models")
def models_command():
    """List available llm models"""
    runner = CliRunner()
    result = runner.invoke(llm_cli, ["models"])
    if result.exception:
        raise click.ClickException(str(result.exception))
    click.echo(result.output)


if __name__ == "__main__":
    mark_cli()
