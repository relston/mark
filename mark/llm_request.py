from textwrap import dedent

class LLMRequest:
    def __init__(self):
        """
        Can serialize itself into a payload that can be sent to the OpenAI API (potentially others in the future)
        """
        self.system_message = None
        self.prompt = None
        self.images = []
        self.links = []

    def with_system_message(self, system_message):
        self.system_message = system_message
        return self

    def with_prompt(self, prompt):
        self.prompt = prompt
        return self
    
    def with_image(self, image):
        self.images.append(image)
        return self
    
    def with_link(self, document):
        self.links.append(document)
        return self
    
    def system_content(self):
        system_content = ""
        
        if self.links:
            link_content_block = "---".join([str(link) for link in self.links])
            system_content += link_content_block

        if self.system_message:
            system_content += "\n" + self.system_message
        
        return system_content

    def to_payload(self):
        system_message = {"role": "system", "content": self.system_content()}
        
        if self.images:
            user_content = [{ 'type': 'text', 'text': self.prompt }]
            for image in self.images:
                if image.url:
                    user_content.append({ 'type': 'image_url', 'image_url': { 'url': image.url } })
        else:
            user_content = self.prompt

        user_message = {"role": "user", "content": user_content}
        return [system_message, user_message]

    def to_log(self):
        return dedent("""
        # System message
        ---
        """) \
        + self.system_content() \
        + dedent("""
        ---
        # User Message
        ---
        """) \
        + self.prompt \
        + dedent("""
        ---
        # Images
        ---
        """) \
        + "\n".join([image.url for image in self.images])