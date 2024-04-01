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
- segment code into separate modules
    - cli.py
    - openai.py
    - agents.py
- add tests
- add agent management commands


## Testing
Establish a testing strategy early, including:
- Unit tests for individual functions.

## Dependency Management
Minimize external dependencies to reduce potential conflicts and ease installation. When necessary, ensure your tool works with specific versions of dependencies to avoid compatibility issues.

## Package Structure
A typical Python package structure includes:

```
mypackage/
|-- mypackage/
|   |-- __init__.py
|   |-- module1.py
|   |-- module2.py
|   `-- subpackage/
|       |-- __init__.py
|       `-- submodule1.py
|-- tests/
|   |-- __init__.py
|   |-- test_module1.py
|   `-- test_module2.py
|-- README.md
|-- LICENSE
`-- pyproject.toml (optional, but recommended)
```

- **`mypackage/` (top level)**: This directory contains your package source code. The name of this directory is the name of your package.
- **`__init__.py`**: These files are required to make Python treat the directories as containing packages; this is done to prevent directories with a common name, such as `string`, from unintentionally hiding valid modules that occur later on the module search path.
- **Module files**: Files like `module1.py` and `module2.py` are individual modules that contain your code.
- **`subpackage/`**: A package can contain one or more subpackages for better organization.
- **`tests/`**: Contains unit tests that can be run to test the functionality in your package.
- **`README.md`**: A Markdown file containing an overview of your package, any necessary documentation for users, and installation instructions.
- **`LICENSE`**: The license file specifies the terms under which your package is made available.
- **`pyproject.toml`**: A file introduced in PEP 518 that contains build system requirements. It is recommended for specifying your project’s build requirements.
