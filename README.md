# GPT Agent

## Install
```bash
pipx install git+https://github.com/relston/agent_gpt.git
```

## Local Setup
https://python-poetry.org/docs/
```bash
poetry install
```

## Run the CLI Tool locally
```bash
poetry run agent_gpt thread.md
```

# Tasks
- add tests
- add agent management commands

# Design direction
This gets parsed and uploaded to gpt vision as context
```markdown
[img](path/to/img.png) 
```

Local links get pulled into the context as well
```markdown
[link](local/link/to/file.md) 
```

Later: introduce agent modifier settings to control the specifics of how the agent treats these.