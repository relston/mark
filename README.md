# Mark
**Mark lets you seamlessly use markdown, images and links to interact with GPT4o**

Why Markdown + GPT? For a full rundown of the benefits and use cases, check out [Introducing 'Mark', a Markdown CLI tool for GPT4o](https://relston.github.io/markdown/gpt4o/cli/2024/06/07/introducing-mark.html)

## Key Features
- Interact with LLMs using Markdown
- Visual recognition of markdown image references via GPT4o
- Local and remote links are scraped for context
- GPT responses appended directly into Markdown files
- `stdin` and `stdout` support for piping

## Example
```markdown
Describe ![this image](https://www.animal.photos/mamm1/cat-tig1_files/bengal12.jpg) to me in one short sentence.

# GPT Response (model: gpt-4o-2024-05-13, system: default)
A Bengal tiger is walking on a sandy path with greenery in the background.

# User Response
List each section of content on [this page](https://en.wikipedia.org/wiki/Bengal_tiger)

# GPT Response (model: gpt-4o-2024-05-13, system: default)
## Sections of Content on the Bengal Tiger Wikipedia Page

1. **Taxonomy**
   - Genetic ancestry

2. **Characteristics**
   - Body weight and size

3. **Distribution and habitat**
   - India
   - Bangladesh
    ...
```

This allows you to carry on a conversation directly in the markdown file - or simply integrate the response back into the document you're working on. This is a powerful, flexible and natural way to interact with LLMs that unlocks countless use cases. `mark`'s focus on explicitly using Markdown as both a prompt and response medium for LLMs presents a unique approach. By blending interactive, version-controlled Markdown documents with LLM responses in a CLI tool offers an innovative workflow for those looking to integrate LLM interactions into their development and documentation processes.

# Install the Mark CLI
```bash
pipx install git+https://github.com/relston/mark.git
```
- *[Requires pipx](https://pipx.pypa.io/stable/installation/)*

Updating the CLI:
```bash
pipx upgrade mark
```

# Usage
By default, `mark` will read a markdown file, extract any context references, and send them to the LLM. The responses are then appended to the markdown file.
```bash
mark path/to/markdown.md
```
*Requires an OpenAI API key in the `OPENAI_API_KEY` environment variable*

Also supports `stdin` with `stdout` for piping GPT responses into other tools
```bash
cat path/to/markdown.md | mark 
# LLM response....
```

## Custom system prompts
The system prompts folder is located at `~/.mark/system_prompts` and it includes a `default.md` prompt. You can add any additional system prompts you'd like to use in this folder and use them with the `--system` flag.
```bash
# ~/.mark/system_prompts/custom.md
mark path/to/markdown.md --system custom
```

# Development
## Local Setup
```bash
poetry install
```
*[Requires poetry](https://python-poetry.org/docs/)*

## Run the CLI Tool locally
```bash
poetry run mark path/to/markdown.md
```

## Run the tests
```bash
poetry run python -m pytest
```
