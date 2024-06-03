import click
from mark import (
    llm,
    llm_request,
    writer
) 
from mark.llm_request import LLMRequest
from mark.markdown_file import MarkdownFile
from mark.config import Config

@click.command()
@click.argument('input', type=click.File("r"))
@click.option('--agent', type=click.STRING, default='default')
def command(input, agent):
    """
    Command line tool that processes an input file with a specified agent to generate and record a response.
    """
    selected_agent = Config().agents().get(agent, 'default')
    markdown_file = MarkdownFile(input)
    request = LLMRequest() \
                .with_prompt(markdown_file.content) \
                .with_system_message(selected_agent['system'])
    
    for image in markdown_file.images:
        request.with_image(image['image_path'])
    
    response = llm.get_completion(request, selected_agent)

    if markdown_file.file_path:
        writer.write_response(markdown_file.file_path, response, agent)
    else:
        click.echo(response)
