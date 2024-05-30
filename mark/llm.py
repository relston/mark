import os
from openai import OpenAI

OPEN_AI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = "gpt-4o-2024-05-13"

client = OpenAI(api_key=OPEN_AI_API_KEY)

def get_completion(llm_request, selected_agent):
    """
    Get completion from the OpenAI model for the given prompt and agent.
    """
    system_message = {"role": "system", "content": selected_agent['system']}
    user_message = {"role": "user", "content": llm_request.to_payload()}
    messages = [system_message, user_message]

    return _call_model(messages, MODEL)
    
def _call_model(messages, model):
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    return chat_completion.choices[0].message.content