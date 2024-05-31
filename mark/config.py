import os
import yaml

# Initialize and setup
class Config:
    def __init__(self):
        self.config_dir = os.getenv('MARK_CONFIG_PATH', os.path.expanduser("~/.mark"))
        self.agents_dir = f"/{self.config_dir}/agents"
        self.default_agent = f"{self.agents_dir}/default.yaml"
        
        if not os.path.exists(self.agents_dir):
            os.makedirs(self.agents_dir)

        if not os.path.exists(self.default_agent):
            with open(os.path.expanduser( self.default_agent), "w") as file:
                file.write("""system: >
            You are a helpful LLM agent that always returns your response in Markdown format.""")

    def agents(self):
        agents = {}
        for filename in os.listdir(self.agents_dir):
            filepath = os.path.join(self.agents_dir, filename)
            with open(filepath, "r") as file:
                agent_name = os.path.splitext(filename)[0]
                agents[agent_name] = yaml.safe_load(file)
        return agents

