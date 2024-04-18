from mark import llm
from IPython import embed

RESPONSE_TEMPLATE = """
**GPT Response (model: {model}, agent: {agent})**
{message}

**User Response**
"""

def write_response(file_name, message, agent='default', model=llm.MODEL):
    """
    Append the GPT response to the given file.
    """
    content = RESPONSE_TEMPLATE.format(model=model, agent=agent, message=message)
    with open(file_name, "a") as file:
        # embed()
        file.write(content)
