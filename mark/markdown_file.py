from io import TextIOWrapper
import re
import os

class MarkdownFile:
    def __init__(self, file_wrapper: TextIOWrapper):
        """
        Initializes the MarkdownFile object with a TextIOWrapper, usually obtained from opening a file.
        """
        self.file = file_wrapper
        self.file_path = file_wrapper.name
        self.file_dir = os.path.dirname(self.file_path)

    def images(self):
        """
        Parses the markdown file to find all images (local and remote),
        capturing their alt text, source path/URL, and resolving relative paths.
        Returns a list of dictionaries with keys 'alt', 'src', and 'resolved_path'.
        """
        # Move to the beginning of the file if previously read
        self.file.seek(0)
        
        # Regular expression to find Markdown image syntax with alt text
        img_pattern = r'!\[(.*?)\]\((.*?)\)'
        images_info = []

        # Read through each line of the file
        for line in self.file:
            # Find all matches of the pattern in the line
            matches = re.findall(img_pattern, line)
            # For each match, create a dictionary with alt, src, and resolved path keys
            for alt_text, src in matches:
                if src.startswith("http"):
                    images_info.append({'alt': alt_text, 'src': src, 'image_path': src})
                else:
                    resolved_path = os.path.normpath(os.path.join(self.file_dir, src))
                    images_info.append({'alt': alt_text, 'src': src, 'image_path': resolved_path})

        return images_info
