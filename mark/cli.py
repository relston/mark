import click
from mark import (
    agents,
    llm,
    llm_request,
    writer
) 
from mark.markdown_file import MarkdownFile

@click.command()
@click.argument('input', type=click.File("r"))
@click.option('--agent', type=click.STRING, default='default')
def command(input, agent):
    """
    Command line tool that processes an input file with a specified agent to generate and record a response.
    """
    selected_agent = agents.list.get(agent, 'default')
    markdown_file = MarkdownFile(input)
    request = llm_request.from_markdown_file(markdown_file)
    response = llm.get_completion(request, selected_agent)

    if markdown_file.file_path:
        writer.write_response(markdown_file.file_path, response, agent)
    else:
        click.echo(response)
