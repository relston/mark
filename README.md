# GPT Agent

## Tasks
- Choose a cli library

## Setup
https://python-poetry.org/docs/
```bash
poetry install
```

## Run the CLI Tool locally
```bash
poetry run python -m agent_gpt thread.md
```

### If Your CLI Tool is an Installed Command

If you've set up your package such that installing it creates a command-line executable (common with `Click` or when using `entry_points` in `setup.py`), you would run the tool using the command name you defined. For example:

```bash
your_command_name [arguments]
```

# Notes
## Choice of Libraries
Several excellent libraries can help you create CLI tools in Python. The most popular ones include:

- **Typer**: https://github.com/tiangolo/typer
- **Argparse**: A module that allows for easy parsing of command-line options, arguments, and sub-commands. It is included in Python’s standard library.
- **Click**: A package for creating beautiful command-line interfaces in a composable way with as little code as necessary. It’s very user-friendly and flexible.
    https://click.palletsprojects.com/en/8.0.x/api/
    https://github.com/pallets/click/tree/main/examples/inouts
- **Fire**: A library for automatically generating command-line interfaces (CLIs) from Python objects. It’s particularly useful for quickly creating CLIs for existing codebases.
- **Docopt**: Enables you to create CLI applications by merely defining the interface documentation in a specific format that `docopt` uses to create a parser.

Choosing the right library depends on your specific needs, such as simplicity, customization, and the complexity of commands you plan to support.

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

## `pyproject.toml`

PEP 518 has introduced the `pyproject.toml` file, which allows for the specification of build system requirements. Dependencies can be specified using the `[project]` table and the `dependencies` key. An example of defining dependencies in `pyproject.toml`:

```toml
[project]
name = "mypackage"
version = "0.1"
description = "A sample Python package"
authors = [{name = "Author Name", email = "author@example.com"}]
dependencies = [
    "numpy>=1.18.1",
    "pandas>=1.0",
    "requests",
    # Other dependencies
]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

- **Modern Standard**: Introduced in [PEP 518](https://www.python.org/dev/peps/pep-0518/) and enhanced by subsequent PEPs like [PEP 517](https://www.python.org/dev/peps/pep-0517/) and [PEP 621](https://www.python.org/dev/peps/pep-0621/), it aims to standardize project metadata and dependencies.
- **Declarative Style**: As a TOML (Tom's Obvious, Minimal Language) file, it represents data in a clear, fixed format. This reduces complexity and makes the build behavior more predictable.
- **Supports Multiple Tools**: Designed to specify not only project dependencies but also which build system should be used (e.g., `setuptools`, `poetry`, `flit`). This makes it more flexible and forward-compatible.
- **Centralizes Configuration**: It can also include other project metadata and configuration options, aiming to replace multiple configuration files with a single, standardized file.


