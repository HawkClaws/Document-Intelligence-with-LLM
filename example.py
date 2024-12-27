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

# 環境変数を設定 (APIキー)
# 複数のモデルを使用する場合は、それぞれのAPIキーを環境変数に設定してください
# 例:
# os.environ["GEMINI_API_KEY"] = "YOUR_OPENAI_API_KEY"
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
# os.environ["ANYSCALE_API_KEY"] = "YOUR_ANYSCALE_API_KEY"


def extract_text_from_pdf(pdf_path):
    """
    PDFファイルからテキストを抽出する関数。

    Args:
        pdf_path: PDFファイルへのパス。

    Returns:
        抽出されたテキスト (文字列)。
    """
    with open(pdf_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        # 縦書きをそれとして判定してもらうための設定。
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


# 使用例
pdf_file_path = "RAGの精度改善ハンドブック【第1回参加賞：2024年11月25日】.pdf"  # 実際のPDFファイルパスに置き換えてください
extracted_text = extract_text_from_pdf(pdf_file_path)

if extracted_text:
    # Geminiで目次生成
    print(f"extracted_text length: {len(extracted_text)}")
    toc_gemini = create_toc(extracted_text, model="gemini/gemini-1.5-flash")
    toc_content_extractor = TocContentExtractor()
    res = toc_content_extractor.extract_content_by_toc(toc_gemini, extracted_text)
    print(f"res length: {len(res)}")
    print(res)



else:
    print("Failed to extract text from the PDF.")