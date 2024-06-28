from datetime import datetime
import os
from importlib.resources import read_text


class Config:
    DEFAULT_SYSTEM_PROMPT_TEMPLATE_PATH = 'templates/default_system_prompt.md'

    def __init__(self):
        self.config_dir = os.getenv(
            'MARK_CONFIG_PATH',
            os.path.expanduser("~/.mark"))
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


def reset():
    """
    Reset the config object.
    """
    global _config
    _config = None


def get_config():
    """
    Return memoized config object.
    """
    global _config
    if not _config:
        _config = Config()
    return _config
