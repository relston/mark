# Mark
A CLI tool for interacting with LLMs using markdown files.

## Install
```bash
pipx install git+https://github.com/relston/mark.git
```

## Local Setup
https://python-poetry.org/docs/
```bash
poetry install
```

## Run the CLI Tool locally
```bash
poetry run mark thread.md
```

## Run the tests
```bash
poetry run python -m pytest
poetry run python -m pytest tests/test_llm.py
```

# TODO
- Add support for url's in the markdown

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

# Inspiration
https://github.com/simonw/llm/
https://github.com/relston/gpt-cli