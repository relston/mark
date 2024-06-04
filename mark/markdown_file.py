import os
import re
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.utils.image import image_to_data_url
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
        self.file = file_wrapper
        self.file_path = file_wrapper.name if file_wrapper.name != '<stdin>' else None
        self.file_dir = os.path.dirname(self.file_path)
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
            self._images = self._parse_images()
        return self._images
        
    @property
    def links(self):
        if not self._links:
            self._links = self._parse_links()
        return self._links

    def _parse_images(self):
        """
        Parses the markdown file to find all images (local and remote),
        capturing their alt text, source path/URL, and resolving relative paths.
        Returns a list of dictionaries with keys 'alt', 'src', and 'resolved_path'.
        """
        images_info = []

        # Find all matches of the pattern in the line
        matches = re.findall(Image.REGX_PATTERN, self.file_content)
        # For each match, create a dictionary with alt, src, and resolved path keys
        for alt_text, src in matches:
            if src.startswith("http"):
                images_info.append(Image(src, src, alt_text))
            else:
                resolved_path = os.path.normpath(os.path.join(self.file_dir, src))
                images_info.append(Image(src, resolved_path, alt_text))

        return images_info

    def _parse_links(self):
        """
        Parses the markdown file to find all links, capturing their text and URL.
        Returns a list of dictionaries with keys 'text' and 'url'.
        """
        links_info = []

        # Find all matches of the pattern in the document
        matches = re.findall(Link.REGX_PATTERN, self.file_content)
        # For each match, create a dictionary with text and URL keys
        for text, src in matches:
            if src.startswith("http"):
                links_info.append(Link(src, text))
            else:
                resolved_path = os.path.normpath(os.path.join(self.file_dir, src))
                links_info.append(Link(resolved_path, text))

        return links_info    

class Image:
    # Regular expression to find Markdown image syntax with alt text
    REGX_PATTERN = r'!\[(.*?)\]\((.*?)\)'

    def __init__(self, src, path, link_text=None):
        self._path = path
        self.src = src
        self.url = None
        self.link_text = link_text

        if self._path.startswith("http"):
            self.url = self._path
        else:
            try:
                self.url = image_to_data_url(self._path)
            except (FileNotFoundError, IsADirectoryError) as e:
                print(f"Sorry, {e.filename} does not exist.")
        
class Link:
    # Regular expression to find Markdown link syntax
    # it will match `[text](url)` but not `![text](url)`
    REGX_PATTERN = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'

    def __init__(self, src, text):
        self.text = text
        self.src = src
        self._document = None

    def __str__(self):
        serialized_web_document = dedent(f"""
        Link Text: {self.text}
        Title: {self.document.metadata['title']}
        URL: {self.src}
        Page Content:
        """)
        serialized_web_document += self.document.page_content
        return serialized_web_document

    @property
    def document(self):
        if not self._document:
            self._document = self._request_page_content(self.src)    
            self._document.metadata['link text'] = self.text
        return self._document
    
    def _request_page_content(self, src):
        web_document, *_ = WebBaseLoader(src).load()
        return web_document
        

