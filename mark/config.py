from datetime import datetime
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
        self.log_folder = f"{self.config_dir}/logs"
        
        if not os.path.exists(self.system_prompts_dir):
            os.makedirs(self.system_prompts_dir)

        if not os.path.exists(self.default_system_prompt):
            default_config = read_text('templates', 'default_system_prompt.md')
            
            with open(os.path.expanduser(self.default_system_prompt), "w") as file:
                file.write(default_config)

        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

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
    
    def log(self, content):
        # Get current date and time as string
        dt_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        log_file = f"{self.log_folder}/{dt_string}.md"
        with open(log_file, "w") as file:
            file.write(content)

_config = None

def get_config():
    """
    TODO: This is causing tests/test_cli.py::TestCLI::test_command_custom_agent to fail because the config without custom is already created.
    """
    global _config
    if not _config:
        _config = Config()
    return _config
