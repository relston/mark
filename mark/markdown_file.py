from io import TextIOWrapper
import re
import os

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

    @property
    def content(self):
        """
        Returns the content of the markdown file as a string.
        """
        return self.file_content

    @property
    def images(self):
        """
        Parses the markdown file to find all images (local and remote),
        capturing their alt text, source path/URL, and resolving relative paths.
        Returns a list of dictionaries with keys 'alt', 'src', and 'resolved_path'.
        """
        # Regular expression to find Markdown image syntax with alt text
        img_pattern = r'!\[(.*?)\]\((.*?)\)'
        images_info = []

        # Find all matches of the pattern in the line
        matches = re.findall(img_pattern, self.file_content)
        # For each match, create a dictionary with alt, src, and resolved path keys
        for alt_text, src in matches:
            if src.startswith("http"):
                images_info.append({'alt': alt_text, 'src': src, 'image_path': src})
            else:
                resolved_path = os.path.normpath(os.path.join(self.file_dir, src))
                images_info.append({'alt': alt_text, 'src': src, 'image_path': resolved_path})

        return images_info
    
    @property
    def links(self):
        """
        Parses the markdown file to find all links, capturing their text and URL.
        Returns a list of dictionaries with keys 'text' and 'url'.
        """
        # Regular expression to find Markdown link syntax
        # it will match `[text](url)` but not `![text](url)`
        link_pattern = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'
        links_info = []

        # Find all matches of the pattern in the line
        matches = re.findall(link_pattern, self.file_content)
        # For each match, create a dictionary with text and URL keys
        for text, url in matches:
            if url.startswith("http"):
                links_info.append({'text': text, 'url': url})
            else:
                resolved_path = os.path.normpath(os.path.join(self.file_dir, url))
                links_info.append({'text': text, 'url': resolved_path})

        return links_info

