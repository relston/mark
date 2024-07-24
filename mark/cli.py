import click
from mark import llm
from mark.llm_request import LLMRequest
from mark.markdown_file import MarkdownFile
from mark.config import get_config


@click.command()
@click.argument('input', type=click.File())
@click.option('--system', '-s', type=click.STRING, default='default')
@click.option('--generate-image', '-i', is_flag=True, default=False,
              help='EXPERIMENTAL: Generate an image using DALL-E.')
def command(input, system, generate_image):
    """
    Command line tool that processes an input file with a specified agent to generate and record a response.
    """
    system_prompt = get_config().system_prompts().get(system, 'default')
    markdown_file = MarkdownFile(input)
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
