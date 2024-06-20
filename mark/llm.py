import os
import click
import openai
from mark.config import get_config
from mark.llm_response import LLMResponse, LLMImageResponse

MODEL = "gpt-4o-2024-05-13"
DALL_E_MODEL = "dall-e-3"

# TODO: Move this config logic to the config class
OPENAI_BASE_URL  = os.getenv('OPENAI_API_BASE_URL', openai.base_url )
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    click.echo("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    exit(1)

client = openai.OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

def get_completion(llm_request):
    """
    Get completion from the OpenAI model for the given prompt and agent.
    """

    get_config().log(llm_request.to_log())

    response_text = _call_model(llm_request.to_payload(), MODEL)
    
    return LLMResponse(response_text, MODEL)

def generate_image(llm_request):
    get_config().log(llm_request.to_log())
    
    response = client.images.generate(
        prompt=llm_request.to_flat_prompt(),
        model=DALL_E_MODEL,
        size="1024x1024",
        n=1
    )

    revised_prompt = response.data[0].revised_prompt
    image_url = response.data[0].url
    return LLMImageResponse(image_url, DALL_E_MODEL, revised_prompt)
    
def _call_model(messages, model):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    return chat_completion.choices[0].message.content