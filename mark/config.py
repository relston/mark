import os
from importlib.resources import read_text

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

    def system_prompts(self):
        system_prompts = {}
        for filename in os.listdir(self.system_prompts_dir):
            filepath = os.path.join(self.system_prompts_dir, filename)
            with open(filepath, "r") as file:
                system_prompt_name = os.path.splitext(filename)[0]
                system_prompts[system_prompt_name] = file.read()
        return system_prompts

