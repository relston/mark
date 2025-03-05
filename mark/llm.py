import os
import click
import llm
from llm.default_plugins.openai_models import openai, Chat, AsyncChat
from mark.config import get_config
from mark.llm_request import LLMRequest
from mark.llm_response import LLMResponse, LLMImageResponse

# TODO: Remove this. Only needed to support image generation.
# Should differ to llm model registration
OPENAI_BASE_URL = os.getenv('OPENAI_API_BASE_URL', openai.base_url)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    click.echo(
        "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    exit(1)

client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


def handle_openai_errors(func):
    def error_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except openai.APIConnectionError as e:
            click.echo(f"{OPENAI_BASE_URL} could not be reached")
            click.echo(e.__cause__)
            exit(1)
        except openai.RateLimitError:
            click.echo("RateLimitError was received; we should back off a bit.")
            exit(1)
        except openai.BadRequestError as e:
            click.echo("BadRequestError was received")
            click.echo(e.message)
            exit(1)
        except openai.APIStatusError as e:
            click.echo("Another non-200-range status code was received")
            click.echo(e.status_code)
            click.echo(e.response)
            exit(1)

    return error_handler


def get_completion(llm_request):
    """
    Get completion from the OpenAI model for the given prompt and agent.
    """
    get_config().log(llm_request.to_log())

    response_text = _llm_call_completion(llm_request)

    return LLMResponse(response_text, llm_request.model)


def generate_image(llm_request):
    get_config().log(llm_request.to_log())

    response = _call_generate_image(
        llm_request.to_flat_prompt(),
        llm_request.model)

    return LLMImageResponse(
        response.url,
        llm_request.model,
        response.revised_prompt)


@handle_openai_errors
def _call_generate_image(prompt, model):
    # TODO: Can I manually register the dall-e-3 using the llm api?
    response = client.images.generate(
        prompt=prompt,
        model=model,
        size="1024x1024",
        n=1
    )

    return response.data[0]


@handle_openai_errors
def _llm_call_completion(llm_request: LLMRequest) -> str:
    model = llm.get_model(llm_request.model)
    if isinstance(model, (Chat, AsyncChat)) and model.api_base == None:
        # Backwards compatible with the older override
        model.api_base = OPENAI_BASE_URL

    attachment = []
    for image in llm_request.images:
        if image.is_web_reference():
            attachment.append(llm.Attachment(url=image.src))
        else:
            attachment.append(llm.Attachment(path=image.src))

    # llm.Attachment(path="pelican.jpg"),
    # llm.Attachment(url="https://static.simonwillison.net/static/2024/pelicans.jpg"),
    # llm.Attachment(content=b"binary image content here")
    return model.prompt(
        llm_request.prompt,
        system=llm_request.system_content(),
        attachments=attachment,
        stream=False # we do not support streaming
    )
