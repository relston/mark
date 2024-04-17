import os
from openai import OpenAI

# Constants
OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = "gpt-4-turbo-preview"

client = OpenAI(api_key=OPEN_AI_API_KEY)

def get_completion(prompt, selected_agent):
    """
    Get completion from the OpenAI model for the given prompt and agent.
    """
    messages = [
        {"role": "system", "content": selected_agent['system']},
        {"role": "user", "content": prompt}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=MODEL,
    )

    return chat_completion.choices[0].message.content
