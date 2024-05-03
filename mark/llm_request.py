from IPython import embed
import base64

class LLMRequest:
    def __init__(self, body, images):
        """
        Can serialize itself into a payload that can be sent to the OpenAI API (potentially others in the future)
        """
        self.body = body
        self.images = images

    def to_payload(self):
        if self.images:
            content_segments = [{ 'type': 'text', 'text': self.body }]
            for image in self.images:
                content_segments.append({ 'type': 'image_url', 'image_url': { 'url': image.url } }) if image.url else None
            return content_segments
        return self.body


class Image:
    def __init__(self, path):
        self._path = path
        self.url = None

        if self._path.startswith("http"):
            self.url = self._path
        else:
            try:
                base64_image = self._base64_encode()
                self.url = f"data:image/jpeg;base64,{base64_image}"
            except (FileNotFoundError, IsADirectoryError) as e:
                print(f"Sorry, {e.filename} does not exist.")

    def _base64_encode(self):
        with open(self._path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image

def from_markdown_file(markdown_file):
    images = []
    for image_info in markdown_file.images:
        image = Image(image_info['image_path'])
        images.append(image)
    return LLMRequest(markdown_file.content, images)