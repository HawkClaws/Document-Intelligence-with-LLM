# PDF to Markdown Converter using LangChain and LLMs

This project provides a Python script to convert PDF documents into Markdown format using the capabilities of Large Language Models (LLMs) such as Google Gemini or OpenAI's GPT models. It leverages the [LangChain](https://www.langchain.com/) framework for efficient text processing and model interaction.

## Features

*   **PDF Text Extraction:** Extracts text from PDF files page by page using `pdfminer.six`.
*   **Intelligent Chunking:** Splits the extracted text into smaller chunks using `RecursiveCharacterTextSplitter` to ensure optimal processing by LLMs.
*   **LLM-Powered Conversion:** Uses either Google Gemini (e.g., `gemini-1.5-flash`) or OpenAI GPT (e.g., `gpt-4o-mini`) to generate Markdown, taking advantage of their natural language understanding and generation capabilities.
*   **Customizable Markdown Formatting:** Employs a prompt template to guide the LLM in producing Markdown with:
    *   Appropriate headings (#, ##, etc.)
    *   Bulleted or numbered lists
    *   Bold/italic emphasis
    *   Code blocks
    *   Tables
*   **Flexible LLM Provider:** You can select between Google or OpenAI models by setting the `llm_provider` variable and the corresponding API key environment variable.
*   **Environment Variable Configuration:** Uses environment variables (`GOOGLE_API_KEY` or `OPENAI_API_KEY`) for secure API key management.

## Requirements

*   Python 3.7+
*   `langchain-core`
*   `langchain-google-genai`
*   `langchain-openai`
*   `pdfminer.six`

## Installation

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Set up environment variables:**
    *   **For Google Gemini:**
        ```bash
        export GOOGLE_API_KEY="your_google_api_key"
        ```
    *   **For OpenAI GPT:**
        ```bash
        export OPENAI_API_KEY="your_openai_api_key"
        ```

2. **Place your PDF file:** Put the PDF you want to convert in the same directory as the script and name it `test.pdf` or change the `pdf_path` variable in the `main` function.

3. **Run the script:**

    ```bash
    python pdf_to_markdown.py
    ```

4. **Output:** The converted Markdown will be printed to the console, separated by page, and also saved to a file named `output.md`.

## Configuration

*   **LLM Provider:** Change the `llm_provider` variable in the `main` function to either `"google"` or `"openai"` to switch between LLMs.
*   **Model:** You can specify the model (e.g., `"gemini-1.5-flash"`, `"gpt-4o-mini"`) within the `ChatGoogleGenerativeAI` or `ChatOpenAI` instantiation.
*   **Temperature:** Adjust the `temperature` parameter (e.g., `0.5` for Google, `0.7` for OpenAI) when creating the LLM instance to control the creativity of the output (lower values are more deterministic, higher values are more creative).
*   **Chunk Size and Overlap:** You can modify the `CHUNK_SIZE` and `CHUNK_OVERLAP` constants at the beginning of the script to adjust how the text is split for processing by the LLM.
*   **Markdown Prompt:** Customize the `MARKDOWN_PROMPT_TEMPLATE` string to fine-tune the instructions given to the LLM for Markdown generation.

## Example Prompt (MARKDOWN_PROMPT_TEMPLATE)

```
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
```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
