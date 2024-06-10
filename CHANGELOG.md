## Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [0.4.0] - 2024-06-06
#### Added
- Requests are now logged to `~/.mark/logs/`

### [0.3.6] - 2024-06-06
#### Fixed
- USER_AGENT warning

### [0.3.5] - 2024-06-06
#### Added
- Included additional files in the project for `templates/default_system_prompt.md`.

#### Changed
- Updated default system prompt and refactored into the templates directory.

### [0.3.4] - 2024-06-04
#### Added
- Returned a pretty error if no `OPENAI_API_KEY` is found.

### [0.3.3] - 2024-06-04
#### Fixed
- Fixed stdin use case.

### [0.3.2] - 2024-06-04
#### Added
- Added local file references to page links.

### [0.3.1] - 2024-06-04
#### Added
- Utilized LangChain image utilities for local image encoding.

### [0.3.0] - 2024-06-04
#### Added
- Bumped version.
- Added new dependencies: `langchain ^0.2.1` and `langchain-community ^0.2.1`.

### [0.2.3] - 2024-05-29
#### Changed
- Updated model.

### [0.2.2] - 2024-05-03
#### Fixed
- Fixed issue handling malformed image tags.

### [0.2.1] - 2024-04-29
#### Fixed
- Fixed pathing issue with images.

### [0.2.0] - 2024-04-23
#### Added
- Added parsing support for images in markdown text.
- Added new dependencies: `beautifulsoup4 ^4.12.3` and `markdown ^3.6`.

### [0.1.0] - 2024-03-25
#### Added
- Initial setup with dependencies: `python ^3.8`, `PyYAML 5.4.1`, `ipython 8.21.0`, `openai 1.14.2`.
- Replace `typer` with `click` for CLI tool.
- Setup CLI interface with entry point `agent_gpt.__main__:cli`.
- Added development dependencies: `pytest ^6.2.5`.
