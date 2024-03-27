import os
import click
import yaml
from openai import OpenAI

# Constants
OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
AGENTS_DIR = os.path.expanduser("~/.gpt/agents")

client = OpenAI(api_key=OPEN_AI_API_KEY)

# Loading agents
def load_agents():
    """Load agents from the designated agents directory."""
    agents = {}
    for filename in os.listdir(AGENTS_DIR):
        filepath = os.path.join(AGENTS_DIR, filename)
        with open(filepath, "r") as file:
            agent_name = os.path.splitext(filename)[0]
            agents[agent_name] = yaml.safe_load(file)
    return agents

agents = load_agents()

def get_completion(prompt, selected_agent):
    """
    Get completion from the OpenAI model for the given prompt and agent.
    """
    messages = [
        {"role": "system", "content": selected_agent['system']},
        {"role": "user", "content": prompt}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-turbo-preview",
    )
    return chat_completion.choices[0].message.content

def write_response(file_name, message):
    """
    Append the GPT response to the given file.
    """
    with open(file_name, "a") as file:
        content = f"""
**GPT Response (model: gpt-4-turbo-preview)**
{message}

**User Response**
"""
        file.write(content)

@click.command()
@click.argument('input', type=click.File("r"))
@click.option('--agent', type=click.STRING, default='default')
def cli(input, agent):
    """
    Command line tool that processes an input file with a specified agent to generate and record a response.
    """
    file_name = input.name if input.name != '<stdin>' else None
    prompt = input.read()
    input.close()

    selected_agent = agents.get(agent, 'default')
    response = get_completion(prompt, selected_agent)

    if file_name:
        write_response(file_name, response)
    else:
        click.echo(response)

if __name__ == '__main__':
    cli()
