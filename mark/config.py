import os
from importlib.resources import read_text

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36'

# Initialize and setup
class Config:
    DEFAULT_SYSTEM_PROMPT_TEMPLATE_PATH = 'templates/default_system_prompt.md'

    def __init__(self):
        self.config_dir = os.getenv('MARK_CONFIG_PATH', os.path.expanduser("~/.mark"))
        self.system_prompts_dir = f"/{self.config_dir}/system_prompts"
        self.default_system_prompt = f"{self.system_prompts_dir}/default.md"
        
        if not os.path.exists(self.system_prompts_dir):
            os.makedirs(self.system_prompts_dir)

        if not os.path.exists(self.default_system_prompt):
            default_config = read_text('templates', 'default_system_prompt.md')
            
            with open(os.path.expanduser(self.default_system_prompt), "w") as file:
                file.write(default_config)

        if not os.environ.get("USER_AGENT"):
            os.environ["USER_AGENT"] = DEFAULT_USER_AGENT

    def system_prompts(self):
        system_prompts = {}
        for filename in os.listdir(self.system_prompts_dir):
            filepath = os.path.join(self.system_prompts_dir, filename)
            with open(filepath, "r") as file:
                system_prompt_name = os.path.splitext(filename)[0]
                system_prompts[system_prompt_name] = file.read()
        return system_prompts

