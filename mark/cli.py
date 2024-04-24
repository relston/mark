import click
from mark import (
    agents,
    llm,
    llm_request,
    writer
) 

@click.command()
@click.argument('input', type=click.File("r"))
@click.option('--agent', type=click.STRING, default='default')
def command(input, agent):
    """
    Command line tool that processes an input file with a specified agent to generate and record a response.
    """
    file_name = input.name if input.name != '<stdin>' else None
    prompt = input.read()
    input.close()

    request = llm_request.parse_markdown_content(prompt)

    selected_agent = agents.list.get(agent, 'default')
    response = llm.get_completion(request, selected_agent)

    if file_name:
        writer.write_response(file_name, response, agent)
    else:
        click.echo(response)
