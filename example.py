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

# Set environment variables (API keys)
# If using multiple models, set the API keys for each model in the environment variables
# Example:
# os.environ["GEMINI_API_KEY"] = "YOUR_OPENAI_API_KEY"
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
# os.environ["ANYSCALE_API_KEY"] = "YOUR_ANYSCALE_API_KEY"

def extract_text_from_pdf(pdf_path):
    """
    Function to extract text from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text (string).
    """
    with open(pdf_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        # Setting to recognize vertical writing as such.
        laparams.detect_vertical = True
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
pdf_file_path = "RAGの精度改善ハンドブック【第1回参加賞：2024年11月25日】.pdf"  # Replace with the actual PDF file path
extracted_text = extract_text_from_pdf(pdf_file_path)

if extracted_text:
    # Generate table of contents with Gemini
    print(f"extracted_text length: {len(extracted_text)}")
    toc_gemini = create_toc(extracted_text, model="gemini/gemini-1.5-flash")
    toc_content_extractor = TocContentExtractor()
    res = toc_content_extractor.extract_content_by_toc(toc_gemini, extracted_text)
    print(f"res length: {len(res)}")
    print(res)



else:
    print("Failed to extract text from the PDF.")