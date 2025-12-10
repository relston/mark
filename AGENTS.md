# AGENTS.md

**Mark** is a CLI tool that processes markdown files, extracts images and links, sends them to LLMs, and appends responses back to the markdown file.

## Core Flow

1. [`mark/cli.py`](mark/cli.py) - Entry point, processes markdown file
2. [`mark/markdown_file.py`](mark/markdown_file.py) - Parses markdown, extracts images/links
3. [`mark/scraper.py`](mark/scraper.py) - Scrapes web links (if any)
4. [`mark/llm_request.py`](mark/llm_request.py) - Builds LLM request (builder pattern)
5. [`mark/llm.py`](mark/llm.py) - Calls LLM API via `llm` library
6. [`mark/llm_response.py`](mark/llm_response.py) - Formats response as markdown
7. Response appended to file (or stdout)

## Key Modules

- **`MarkdownFile`**: Extracts images (`![alt](src)`) and links (`[text](url)`) from markdown
- **`LLMRequest`**: Builder for combining prompt, system message, images, and link content
- **`llm.get_completion()`**: Gets text completion from LLM
- **`llm.generate_image()`**: Generates images via DALL-E
- **`Config`**: Manages system prompts in `~/.mark/system_prompts/`

## Environment

- `OPENAI_API_KEY`: Required
- `OPENAI_API_BASE_URL`: Optional override for API endpoint
