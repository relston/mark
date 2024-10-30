## Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [0.8.2] - 2024-08-13
#### Fixed
- Slightly improved errors raise when scraping pages on low memory hardware

### [0.8.1] - 2024-08-13
#### Changed
- Bump langchain from 0.2.14 to 0.2.15
- Bump httpx from 0.27.0 to 0.27.2
- Bump openai from 1.42.0 to 1.43.0
- Bump ipython from 8.26.0 to 8.27.0
- Bump langchain-community from 0.2.4 to 0.2.12
- Bump openai from 1.41.1 to 1.42.0
- Bump openai from 1.14.2 to 1.41.1
- Bump langchain from 0.2.1 to 0.2.14
- Bump markdownify from 0.12.1 to 0.13.1
- Bump pyyaml from 6.0.1 to 6.0.2
- Bump langchain-community from 0.2.1 to 0.2.4
- Bump ipython from 8.21.0 to 8.26.0
- Bump flake8 from 7.1.0 to 7.1.1
- Bump pytest from 6.2.5 to 8.3.

### [0.8.0] - 2024-08-13
#### Added
- Support for `--model` option to allow for selecting a specific OpenAI model

### [0.7.3] - 2024-07-24
#### Added
- Support for `--version` option in the CLI

### [0.7.2] - 2024-07-24
#### Added
- Aliases for cli options `--system` (`-s`) and `--generate-images` (`-i`)

### [0.7.1] - 2024-06-28
#### Fixed
- Gracefully handle timeouts when fetching urls

### [0.7.0] - 2024-06-27
#### Changed
- Updated the scraping logic to render pages as clean markdown which exposes the LLM to urls on the page.

### [0.6.3] - 2024-06-20
#### Fixed
- Gracefully handle broken links in markdown files.

### [0.6.2] - 2024-06-20
#### Added
- Cleaner OpenAI error handling for common issues

### [0.6.1] - 2024-06-20
#### Removed
- Response log for image generation

### [0.6.0] - 2024-06-20
#### Added
- Ability to override the OpenAI endpoint with OPENAI_API_BASE_URL env var

### [0.5.0] - 2024-06-18
#### Added
- Adding experimental support for DALL-E image generation

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
