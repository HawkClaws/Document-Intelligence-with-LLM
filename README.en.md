## Overview

This library is a tool designed to **transform text data from various formats (PDF, text files, strings, etc.) into structured Markdown text.** Specifically, it **automatically generates a Table of Contents (TOC)** from the input text and then **extracts and formats the main content based on that TOC.**

**What this library can do:**

-   **Automatic TOC Generation:** Uses a Large Language Model (LLM) to automatically generate a TOC with appropriate heading levels from the input text data.
-   **Content Extraction Based on TOC:** Matches the generated TOC with the original text to extract the corresponding content for each heading in the TOC.
-   **Output in Structured Markdown Format:** Outputs the TOC and its corresponding content as structured Markdown text. This makes it easy to read for humans and easy to process for systems like RAG (Retrieval-Augmented Generation).
-   **Support for Various Input Formats:**  Handles not only PDF files but also text files, directly input strings, and more. With appropriate text extraction processing, it can support even more data sources (e.g., web pages, document files).

**Process Flow**

```
Input Data (PDF, text file, string, etc.)  -->  Text Extraction  -->  TOC Generation (using LLM)  -->  Content Extraction (matching TOC and content)  -->  Structured Markdown Output
```

**Benefits of using this library:**

-   **Automated Document Structuring:** Eliminates the manual effort of creating a TOC and organizing content, automating the document structuring process.
-   **Improved Readability:** The generated Markdown is in a format that is easy for humans to read.
-   **Improved Machine Readability:** The structured Markdown is easy to process for systems like RAG, making it useful for tasks like information retrieval and document summarization.
-   **Application to Various Use Cases:** The generated Markdown can be applied to various use cases, such as document creation, web page creation, and knowledge base construction.

**In summary, this library is a powerful tool for converting unstructured text into structured Markdown that is friendly to both humans and machines.**

## Usage Guide

**1. Install Required Libraries**

```bash
pip install litellm pdfminer.six python-dotenv
```

**2. Set Environment Variables (Optional)**

If you are using multiple LLMs, set the API keys for each model in the environment variables. This is not required, but it is recommended.

Example:

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
ANYSCALE_API_KEY="YOUR_ANYSCALE_API_KEY"
```

Create a `.env` file, set the keys as shown above, and place it in the root directory of your project, or set them as system environment variables.

**3. Example Code (Using a PDF as Input)**

```python
import os
import io

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from create_toc import create_toc
from toc_content_extractor import TocContentExtractor

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.detect_vertical = True  # Setting to recognize vertical writing
        output_string = io.StringIO()
        converter = TextConverter(rsrcmgr, output_string, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, converter)

        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

        text = output_string.getvalue()
        converter.close()
        output_string.close()
        return text

# Example usage
pdf_file_path = "your_document.pdf"  # Path to the PDF file you want to process
extracted_text = extract_text_from_pdf(pdf_file_path)

if extracted_text:
    # Generate TOC (using Gemini here)
    toc = create_toc(extracted_text, model="gemini/gemini-1.5-flash")

    # Extract content based on the TOC
    toc_extractor = TocContentExtractor()
    structured_markdown = toc_extractor.extract_content_by_toc(toc, extracted_text)

    # Output the result
    print(structured_markdown)
else:
    print("Failed to extract text from the PDF.")
```

**4. Example Code (Using a Text File as Input)**

```python
from create_toc import create_toc
from toc_content_extractor import TocContentExtractor

# Function to extract text from a text file
def extract_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

# Example usage
text_file_path = "your_text_file.txt"  # Path to the text file you want to process
extracted_text = extract_text_from_file(text_file_path)

# Generate TOC (using GPT-3.5 here)
toc = create_toc(extracted_text, model="gpt-3.5-turbo")

# Extract content based on the TOC
toc_extractor = TocContentExtractor()
structured_markdown = toc_extractor.extract_content_by_toc(toc, extracted_text)

# Output the result
print(structured_markdown)
```

**5. Example Code (Using a String as Direct Input)**

```python
from create_toc import create_toc
from toc_content_extractor import TocContentExtractor

# Input string
input_text = """
# Introduction

This is a sample text.

## Chapter 1

This is the content of Chapter 1.

### 1.1 Section

This is the content of the section.

## Chapter 2

This is the content of Chapter 2.
"""

# Generate TOC (using Claude 2 here)
toc = create_toc(input_text, model="claude-2")

# Extract content based on the TOC
toc_extractor = TocContentExtractor()
structured_markdown = toc_extractor.extract_content_by_toc(toc, input_text)

# Output the result
print(structured_markdown)
```

**Customization**

-   You can customize how the TOC is generated (heading levels, format, etc.) by modifying the `MARKDOWN_PROMPT_TEMPLATE` in `create_toc.py`.
-   You can adjust the conditions for extracting TOC and content (minimum string length, maximum heading level) by changing `toc_search_min_length` and `toc_max_level` in `toc_content_extractor.py`.

Using these examples as a reference, modify the code to suit your needs and convert text data from various formats into structured Markdown.
