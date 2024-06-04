import click
from mark import llm, writer
from mark.llm_request import LLMRequest
from mark.markdown_file import MarkdownFile
from mark.config import Config

@click.command()
@click.argument('input', type=click.File())
@click.option('--agent', type=click.STRING, default='default')
def command(input, agent):
    """
    Command line tool that processes an input file with a specified agent to generate and record a response.
    """

    # from IPython import embed; embed()
    selected_agent = Config().agents().get(agent, 'default')
    markdown_file = MarkdownFile(input)
    request = LLMRequest() \
                .with_prompt(markdown_file.content) \
                .with_system_message(selected_agent['system'])
    
    [request.with_image(image) for image in markdown_file.images]
    [request.with_link(link) for link in markdown_file.links]
    
    response = llm.get_completion(request, selected_agent)

    if markdown_file.file_path:
        writer.write_response(markdown_file.file_path, response, agent)
    else:
        click.echo(response)
