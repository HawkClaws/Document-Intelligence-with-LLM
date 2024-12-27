from litellm import completion


MARKDOWN_PROMPT_TEMPLATE = """
## Instructions

Please structure the provided text for chunking in RAG (Retrieval-Augmented Generation) by following these guidelines:

1. Generate a table of contents in Markdown format.
2. Use only the following heading notations: #, ##, ###, ####, #####, ######.
3. Integrate related items (e.g., QA) into appropriate hierarchies. For example, if a question is ###, its answer should be ####.
4. Use the exact wording from the input text for the table of contents. Do not change, replace, or omit any text.
5. Exclude list elements from the table of contents.
6. Do not include the body text in the output.

## Text

{text}

"""

def create_toc(text, model):
    """
    Generates a table of contents (TOC) from the given text using the specified model.

    Args:
        text: The original text to generate the TOC from.
        model: The model to use (e.g., "gemini/gemini-pro", "gpt-3.5-turbo", "claude-2").

    Returns:
        The generated TOC in Markdown format (string).
        Returns None if an error occurs.
    """
    try:
        prompt = MARKDOWN_PROMPT_TEMPLATE.format(text=text)
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during completion with model {model}: {e}")
        return None
