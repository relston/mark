import os

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
