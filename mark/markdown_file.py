import os
import re
from langchain_core.documents import Document
from io import TextIOWrapper
from textwrap import dedent
import click
from mark import scraper
import base64
import mimetypes

"""
MarkdownFile
Parses the markdown and extracts image elements from the file, resolving the paths of local images.
"""


class MarkdownFile:
    def __init__(self, file_wrapper: TextIOWrapper):
        """
        Initializes the MarkdownFile object with a TextIOWrapper, usually obtained from opening a file.
        """
        self.file_path = None
        self.file_dir = None
        if hasattr(file_wrapper, 'name') and file_wrapper.name != '<stdin>':
            self.file_path = file_wrapper.name
            self.file_dir = os.path.dirname(file_wrapper.name)
        else:
            self.file_dir = os.getcwd()
        self.file_content = file_wrapper.read()
        self._images = None
        self._links = None

    @property
    def content(self):
        """
        Returns the content of the markdown file as a string.
        """
        return self.file_content

    @property
    def images(self):
        if not self._images:
            self._images = self._parse_elements(Image)
        return self._images

    @property
    def links(self):
        if not self._links:
            self._links = self._parse_elements(Link)
        return self._links

    def _parse_elements(self, cls):
        matches = re.findall(cls.REGX_PATTERN, self.file_content)
        return [
            cls.from_reference_folder(self.file_dir)
            .with_src(src)
            .with_text(text)
            for text, src in matches
        ]


class PageReference:
    @classmethod
    def from_reference_folder(cls, folder):
        return cls(folder)

    def __init__(self, reference_folder, src=None):
        self.reference_folder = reference_folder
        self.src = src
        self.uri = None
        if src:
            self._resolve_uri()

    def with_src(self, src):
        self.src = src
        self._resolve_uri()
        return self

    def with_text(self, text):
        self.link_text = text
        return self

    def is_web_reference(self):
        return self.src.startswith("http")

    def _resolve_uri(self):
        if self.is_web_reference():
            self.uri = self.src
        else:
            self.uri = os.path.normpath(
                os.path.join(
                    self.reference_folder,
                    self.src))


class Image(PageReference):
    # Regular expression to find Markdown image syntax with alt text
    REGX_PATTERN = r'!\[(.*?)\]\((.*?)\)'

    @property
    def url(self):
        if self.is_web_reference():
            return self.uri
        else:
            try:
                return Image.image_to_data_url(self.uri)
            except (FileNotFoundError, IsADirectoryError):
                click.echo(f"Image Reference {self.src} not found. Skipping")
                return ''

    @classmethod
    def encode_image(cls, image_path: str) -> str:
        """Get base64 string from image URI.

        Args:
            image_path: The path to the image.

        Returns:
            The base64 string of the image.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @classmethod
    def image_to_data_url(cls, image_path: str) -> str:
        """Get data URL from image URI.

        Args:
            image_path: The path to the image.

        Returns:
            The data URL of the image.
        """
        encoding = cls.encode_image(image_path)
        mime_type = mimetypes.guess_type(image_path)[0]
        return f"data:{mime_type};base64,{encoding}"


class Link(PageReference):
    # Regular expression to find Markdown link syntax
    # it will match `[text](url)` but not `![text](url)`
    REGX_PATTERN = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'

    def __init__(self, reference_folder, src=None):
        super().__init__(reference_folder, src)
        self._document = None

    def __str__(self):
        if not self.document:
            return f"\nNo document found for: {self.src}\n"

        serialized_document = dedent(f"""
        Link Text: {self.link_text}
        SRC: {self.src}
        Page Title: {self.document.metadata['title']}
        Page Content:
        """)
        serialized_document += self.document.page_content + "\n"
        return serialized_document

    @property
    def document(self):
        if not self._document:
            try:
                self._document = self._get_document(self.uri)
                self._document.metadata['link text'] = self.link_text
            except (FileNotFoundError, IsADirectoryError):
                click.echo(f"Link Reference {self.src} not found. Skipping")
                return
        return self._document

    def _get_document(self, uri):
        if self.is_web_reference():
            return scraper.get(uri).to_document()
        else:
            with open(uri, 'r') as file:
                file_content = file.read()
                file_document = Document(
                    page_content=file_content, metadata={
                        'title': os.path.basename(uri)})
                return file_document
