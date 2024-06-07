# Mark
**Mark lets you seamlessly use markdown, images and links to interact with GPT**

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

# Why Markdown + LLMs?
Markdown provides a powerful, flexible, and efficient medium to interact with LLMs. It's simplicity, combined with the richness of its features and compatibility with modern development tools, makes it uniquely suitable for optimizing the effectiveness of LLM interactions.

- **Semantic Structuring**:
    - Markdown's semantic elements like headers, blockquotes, and emphasis can help structure prompts in a way that guides the LLM through the task, emphasizing key parts and delineating sections logically. This can lead to more accurate understanding and processing by the LLM.
    - Also the simple formatting notation allows one to easily create prompts with structure that communicates a lot to the LLM while minimizing the input token count
    - Markdown allows you to insert code blocks seamlessly within text. This is incredibly useful for creating and sharing code snippets or requests for code generation, maintenance, or documentation. The LLM can analyze the code context provided with the prose to give better responses.

- **Explicit Relevant Context**:
    - Most RAG systems rely on embedding models to guess which context is relevant to the prompt based on semantic search from a prepared database of content. By using markdown files, the context of the link references is explicit and can be easily manipulated on the fly to provide the most relevant context documents to the LLM.

- **Visual Context**:
    - Images referenced in Markdown files is a natural way to provide visual context to the LLM.

- **Extensibility & Custom Syntax**:
    - Markdown can be extended with custom syntax, allowing for the inclusion of specialized elements such as task lists, diagrams (e.g., Mermaid.js for flowcharts), and more. This can provide additional context and directives to LLMs trained to parse such custom syntax.    
    - llms can provide responses structured as tables and lists, which are easily rendered in markdown

- **Collaboration & Versioning**:
    - Markdown's compatibility with version control systems like Git allows for efficient collaboration, auditing, and version tracking.

- **Integration with Other Tools**:
    - Modern IDEs and text editors provide excellent support for Markdown, including syntax highlighting, preview panes, and dictation tools. This can enhance the authoring experience and make it easier to interact with LLMs.
    - Markdown can be integrated with a variety of other tools and services, such as static site generators (e.g., Jekyll, Hugo), which can provide preview capabilities for iterating on LLM interactions.
    - Markdown files can be easily converted to other formats (PDF, HTML, DOCX) using tools like Pandoc. This ensures that any work done in Markdown for interacting with LLMs can be repurposed in multiple venues.

