import os
import time
from typing import List

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

# Constants for Text Splitting and Rate Limiting
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 200

# Markdown conversion prompt template
MARKDOWN_PROMPT_TEMPLATE = """
**Instructions:**

*   Use headings (#, ##, ###, etc.) that appropriately represent the content of the text.
*   Use bulleted or numbered lists to organize information effectively.
*   Emphasize important terms or phrases using **bold** or *italics*.
*   Use code blocks (```) to represent code as needed.
*   Use tables (|) to organize information.
*   Remove unnecessary line breaks or extra spaces.
*   Follow standard Markdown syntax.

**Text:**
{text}
"""

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    """
    Extracts text from a PDF file page by page.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A list of strings, where each string represents the text content of a page.
    """
    all_texts = []
    for page_layout in extract_pages(pdf_path):
        page_text = "".join(
            element.get_text()
            for element in page_layout
            if isinstance(element, LTTextContainer)
        )
        all_texts.append(page_text)
    return all_texts

def create_markdown_chain(llm: Runnable) -> Runnable:
    """
    Creates a LangChain chain for converting text to Markdown.

    Args:
      llm: The language model runnable to use (e.g., ChatGoogleGenerativeAI, ChatOpenAI).

    Returns:
      A LangChain chain (Runnable).
    """
    prompt = PromptTemplate.from_template(MARKDOWN_PROMPT_TEMPLATE)
    return (
        {"text": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

def convert_to_markdown(text: str, llm: Runnable) -> str:
    """
    Converts a text to Markdown format using LangChain and a specified LLM.

    Args:
        text: The text to convert.
        llm: The language model runnable instance.

    Returns:
        The text converted to Markdown format.
    """
    chain = create_markdown_chain(llm)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, add_start_index=True
    )

    docs = text_splitter.split_documents([Document(page_content=text)])
    markdown_text = ""
    for doc in docs:
        markdown_text += chain.invoke(doc.page_content) + "\n"
    return markdown_text

def save_markdown_to_file(markdown_texts: List[str], output_filename: str = "output.md"):
    """Saves the generated Markdown to a file."""
    with open(output_filename, "w", encoding="utf-8") as f:
        for page in markdown_texts:
            f.write(page)
            f.write("\n")

def main():
    """Main function to run the PDF to Markdown conversion."""
    pdf_path = "test.pdf"  # Specify the path to your PDF

    # Configure LLM provider and API key
    llm_provider = "google"  # Or "openai"
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    # Gemini
    if llm_provider == "google" and not google_api_key:
        raise ValueError(
            "The environment variable 'GOOGLE_API_KEY' is not set. "
            "Please set it to use the Google Gemini model."
        )
    # GPT
    elif llm_provider == "openai" and not openai_api_key:
        raise ValueError(
            "The environment variable 'OPENAI_API_KEY' is not set. "
            "Please set it to use the OpenAI model."
        )

    # Create the LLM instance based on the selected provider
    if llm_provider == "google":
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_api_key, convert_system_message_to_human=True, temperature=0.5) 
    elif llm_provider == "openai":
        llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o-mini", temperature=0.7)
    else:
        raise ValueError(f"Invalid LLM provider: {llm_provider}")

    extracted_texts = extract_text_from_pdf(pdf_path)

    markdown_output = []
    for text in extracted_texts:
        markdown_text = convert_to_markdown(text, llm)
        markdown_output.append(markdown_text)

    for i, page in enumerate(markdown_output):
        print(f"--- Page {i+1} ---")
        print(page)

    save_markdown_to_file(markdown_output)
    print(f"Markdown file saved to 'output.md'.")

if __name__ == "__main__":
    main()