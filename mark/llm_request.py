from markdown import markdown
from bs4 import BeautifulSoup
from IPython import embed
import base64

"""
Take a string of markdown content and return an LLMRequest object
This has the original markdown content and a list of Image objects
found in the markdown content
"""

class LLMRequest:
    def __init__(self, body, images):
        self.body = body
        self.images = images

    def to_payload(self):
        if self.images:
            content_segments = [{ 'type': 'text', 'text': self.body }]
            for image in self.images:
                content_segments.append({ 'type': 'image_url', 'image_url': { 'url': image.url } })
            return content_segments
        return self.body


class Image:
    def __init__(self, path):
        self._path = path

    @property
    def url(self):
        if self._path.startswith("http"):
            return self._path 
        else:
            base64_image = self._base64_encode()
            return f"data:image/jpeg;base64,{base64_image}"

    def _base64_encode(self):
        with open(self._path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_image

def parse_markdown_content(markdown_content):
    html_content = markdown(markdown_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    images = [Image(img['src']) for img in soup.find_all('img')]
    return LLMRequest(markdown_content, images)