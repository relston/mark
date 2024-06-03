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
        self.images.append(image)
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
