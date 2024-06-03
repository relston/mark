import base64

class LLMRequest:
    def __init__(self):
        """
        Can serialize itself into a payload that can be sent to the OpenAI API (potentially others in the future)
        """
        self.system_message = None
        self.prompt = None
        self.images = []

    def with_system_message(self, system_message):
        self.system_message = system_message
        return self

    def with_prompt(self, prompt):
        self.prompt = prompt
        return self
    
    def with_image(self, image):
        self.images.append(Image(image))
        return self

    def to_payload(self):
        system_message = {"role": "system", "content": self.system_message}
        
        if self.images:
            user_content = [{ 'type': 'text', 'text': self.prompt }]
            for image in self.images:
                user_content.append({ 'type': 'image_url', 'image_url': { 'url': image.url } }) if image.url else None
        else:
            user_content = self.prompt

        user_message = {"role": "user", "content": user_content}
        return [system_message, user_message]


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