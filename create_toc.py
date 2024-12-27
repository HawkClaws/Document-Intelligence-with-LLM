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


import os
import io
import litellm
from litellm import completion


def create_toc(text, model):
    """
    指定されたモデルを使用してテキストから目次(TOC)を生成する関数。

    Args:
        text: 目次を生成する元のテキスト。
        model: 使用するモデル (例: "gemini/gemini-pro", "gpt-3.5-turbo", "claude-2")。

    Returns:
        生成された目次 (Markdown形式の文字列)。
        エラーが発生した場合はNoneを返す。
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

