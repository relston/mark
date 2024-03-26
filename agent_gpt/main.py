import os
import yaml
from openai import OpenAI
import click

open_ai_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=open_ai_key)

# Initialize and setup
AGENTS_FOLDER = os.path.expanduser("~/.gpt/agents")
DEFAULT_AGENT = f"{AGENTS_FOLDER}/default.yaml"

if not os.path.exists(AGENTS_FOLDER):
    os.makedirs(AGENTS_FOLDER)
    print(f"Created {AGENTS_FOLDER} folder.")

if not os.path.exists(DEFAULT_AGENT):
    with open(os.path.expanduser( DEFAULT_AGENT), "w") as file:
        file.write("""system: >
    You are a helpful LLM agent that always returns your response in Markdown format.""")
    print(f"Created {DEFAULT_AGENT} file.")


# Loading Agents in AGENTS_FOLDER
agents = {}
for filename in os.listdir(os.path.expanduser("~/.gpt/agents")):
    with open(os.path.expanduser(f"~/.gpt/agents/{filename}"), "r") as file:
        agent_name = os.path.splitext(filename)[0]        
        agents[agent_name] = yaml.safe_load(file)

# Create request 
def get_completion(prompt, selected_agent):
    messages = []
    system_message = {
        "role": "system",
        "content": selected_agent['system']
    }
    messages.append(system_message)
    messages.append({ "role": "user", "content": prompt})

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-turbo-preview",
    )
    return chat_completion.choices[0].message.content

def write_response(file_name, message):
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
    This is a command line tool that processes a file and uses an agent to generate a response.
    """
    file_name = input.name
    if file_name == '<stdin>':
        file_name = None
    prompt = input.read()
    input.close()
    selected_agent = agents[agent]
    response = get_completion(prompt, selected_agent)
    if file_name:
        write_response(file_name, response)
    else:
        click.echo(response)
    
if __name__ == '__main__':
    cli()