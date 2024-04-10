import click
from agent_gpt import agents
from agent_gpt import llm
from agent_gpt import  writer

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
    print('Something happening here')

    selected_agent = agents.list.get(agent, 'default')
    response = llm.get_completion(prompt, selected_agent)

    if file_name:
        writer.write_response(file_name, response, agent)
    else:
        click.echo(response)
