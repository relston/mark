import click
from mark import llm, writer
from mark.llm_request import LLMRequest
from mark.markdown_file import MarkdownFile
from mark.config import Config

@click.command()
@click.argument('input', type=click.File())
@click.option('--system', type=click.STRING, default='default')
def command(input, system):
    """
    Command line tool that processes an input file with a specified agent to generate and record a response.
    """
    system_prompt = Config().system_prompts().get(system, 'default')
    markdown_file = MarkdownFile(input)
    request = LLMRequest() \
                .with_prompt(markdown_file.content) \
                .with_system_message(system_prompt)
    
    [request.with_image(image) for image in markdown_file.images]
    [request.with_link(link) for link in markdown_file.links]
    
    response = llm.get_completion(request, system_prompt)

    if markdown_file.file_path:
        writer.write_response(markdown_file.file_path, response, system)
    else:
        click.echo(response)
