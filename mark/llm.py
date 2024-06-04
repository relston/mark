import os
import click
from openai import OpenAI

OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = "gpt-4o-2024-05-13"

if not OPEN_AI_API_KEY:
    click.echo("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    exit(1)

client = OpenAI(api_key=OPEN_AI_API_KEY)

def get_completion(llm_request, selected_agent):
    """
    Get completion from the OpenAI model for the given prompt and agent.
    """

    return _call_model(llm_request.to_payload(), MODEL)
    
def _call_model(messages, model):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    return chat_completion.choices[0].message.content