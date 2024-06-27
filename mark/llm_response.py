from textwrap import dedent


class LLMResponse(object):
    RESPONSE_TEMPLATE = dedent(
        """
        # GPT Response (model: {model}, system: {system})
        {content}

        # User Response
        """
    )

    def __init__(self, content, model):
        self.model = model
        self.content = content
        self.system = 'default'

    def with_system(self, system):
        self.system = system
        return self

    def to_markdown(self):
        content = self.content
        return self.RESPONSE_TEMPLATE.format(
            model=self.model, system=self.system, content=content)


class LLMImageResponse(LLMResponse):
    def __init__(self, image_url, model, revised_prompt=None):
        super().__init__(image_url, model)
        self.revised_prompt = revised_prompt

    def to_markdown(self):
        content = f"![Generated Image]({self.content})"

        if self.revised_prompt:
            content = f"{self.revised_prompt}\n\n{content}"

        return self.RESPONSE_TEMPLATE.format(
            model=self.model, system=self.system, content=content)
