from mark import llm

def write_response(file_name, message, agent='default', model=llm.MODEL):
    """
    Append the GPT response to the given file.
    """
    with open(file_name, "a") as file:
        content = f"""
**GPT Response (model: {model}, agent: {agent})**
{message}

**User Response**
"""
        file.write(content)
