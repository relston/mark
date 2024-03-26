import os
import sys
import yaml
from IPython import embed
from openai import OpenAI
import os
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


# Detecting input file and agent
input_file = None
selected_agent = None
def detect_file(param):
    global input_file  # Add this line to access the global variable
    if os.path.exists(param):
        input_file = param

def detect_agent(param):
    global selected_agent  # Add this line to access the global variable
    if param in agents:
        selected_agent = agents[param]

if len(sys.argv) > 1:
    params = sys.argv.copy()
    params.pop(0)
    for param in params:
        detect_file(param)
        detect_agent(param)

if selected_agent is None:
    selected_agent = agents['default']

if input_file is None:
    if not sys.stdin.isatty():
        data = sys.stdin.read()
    else:
        # this is a usecase I have not considered yet but it seems reasonable 
        data = input("Enter data: ")
        print("Data entered:", data)
else:
    with open(input_file, "r") as file:
        data = file.read()

# Create request 
messages = []
system_message = {
    "role": "system",
    "content": selected_agent['system']
}
messages.append(system_message)
messages.append({ "role": "user", "content": data})

chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-4-turbo-preview",
)
# embed()   
# If this is a file I need to append this message to the file
# print(chat_completion.choices[0].message.content)
# I might also need my own parsing format for understanding the various chunks of the chain. Give OpenAI the context it needs to do it's best work.
# If this is a file I need to append this message to the file
if input_file:
    with open(input_file, "a") as file:
        message = chat_completion.choices[0].message.content
        content = f"""
**GPT Response (model: gpt-4-turbo-preview)**
{message}

**User Response**
"""
        file.write(content)