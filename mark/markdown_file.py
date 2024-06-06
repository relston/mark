import os
import re
from langchain_core.utils.image import image_to_data_url
from langchain_core.documents import Document
from io import TextIOWrapper
from textwrap import dedent

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
            cls.from_reference_folder(self.file_dir) \
                    .with_src(src) \
                    .with_text(text)
            for text, src in matches    
        ]
    
    # def _resolve_file_dir(self, file_wrapper):
    #     if hasattr(file_wrapper, 'name'):
    #         return os.path.dirname(file_wrapper.name) if file_wrapper.name != '<stdin>' else None
    #     return os.getcwd()

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
            self.uri = os.path.normpath(os.path.join(self.reference_folder, self.src))

class Image(PageReference):
    # Regular expression to find Markdown image syntax with alt text
    REGX_PATTERN = r'!\[(.*?)\]\((.*?)\)'

    @property
    def url(self):
        if self.is_web_reference():
            return self.uri
        else:
            try:
                return image_to_data_url(self.uri)
            except (FileNotFoundError, IsADirectoryError) as e:
                print(f"Sorry, {e.filename} does not exist.")
        
class Link(PageReference):
    # Regular expression to find Markdown link syntax
    # it will match `[text](url)` but not `![text](url)`
    REGX_PATTERN = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'

    def __init__(self, reference_folder, src=None):
        super().__init__(reference_folder, src)
        self._document = None
    
    def __str__(self):
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
            self._document = self._get_document(self.uri)    
            self._document.metadata['link text'] = self.link_text
        return self._document
    
    def _get_document(self, uri):
        if self.is_web_reference():
            return self._request_page_content(uri)    
        else:
            try:
                with open(uri, 'r') as file:
                    file_content = file.read()
                    file_document = Document(page_content=file_content, metadata={'title': os.path.basename(uri)})
                    return file_document
            except (FileNotFoundError, IsADirectoryError) as e:
                print(f"Sorry, {e.filename} does not exist.")
    
    def _request_page_content(self, uri):
        # Only used if the link is a web reference
        from langchain_community.document_loaders import WebBaseLoader

        web_document, *_ = WebBaseLoader(uri).load()
        return web_document
        