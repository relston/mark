import os
import yaml

# Initialize and setup
CONFIG_DIR = os.getenv('MARK_CONFIG_PATH', os.path.expanduser("~/.mark"))
AGENTS_DIR = f"/{CONFIG_DIR}/agents"
DEFAULT_AGENT = f"{AGENTS_DIR}/default.yaml"

if not os.path.exists(AGENTS_DIR):
    os.makedirs(AGENTS_DIR)
    print(f"Created {AGENTS_DIR} folder.")

if not os.path.exists(DEFAULT_AGENT):
    with open(os.path.expanduser( DEFAULT_AGENT), "w") as file:
        file.write("""system: >
    You are a helpful LLM agent that always returns your response in Markdown format.""")
    print(f"Created {DEFAULT_AGENT} file.")


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

list = load_agents()
