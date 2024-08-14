import os
import click
import openai
from mark.config import get_config
from mark.llm_response import LLMResponse, LLMImageResponse

# TODO: Move this config logic to the config class
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

    response_text = _call_completion(
        llm_request.to_payload(), llm_request.model)

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
    response = client.images.generate(
        prompt=prompt,
        model=model,
        size="1024x1024",
        n=1
    )

    return response.data[0]


@handle_openai_errors
def _call_completion(messages, model):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    return chat_completion.choices[0].message.content
