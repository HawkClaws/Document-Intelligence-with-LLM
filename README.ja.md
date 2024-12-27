## 概要

このライブラリは、**様々な形式のテキストデータ（PDF、テキストファイル、文字列など）を入力とし、それを構造化されたMarkdown形式のテキストに変換する**ためのツールです。具体的には、入力テキストから**目次（TOC）を自動生成**し、その**目次に基づいて本文を抽出し、整形**します。

**このライブラリでできること**

-   **入力テキストから目次を自動生成**: 大規模言語モデル（LLM）を用いて、入力されたテキストデータから、適切な見出しレベルを持つ目次を自動的に生成します。
-   **目次に基づいた本文の抽出**: 生成された目次と元のテキストを照合し、目次の各見出しに対応する本文を抽出します。
-   **構造化されたMarkdown形式での出力**: 目次とそれに対応する本文を、構造化されたMarkdown形式のテキストとして出力します。これにより、人間が読みやすいだけでなく、RAG (Retrieval-Augmented Generation) のようなシステムで扱いやすい形式になります。
-   **多様な入力形式に対応**: PDFファイルだけでなく、テキストファイルや直接入力された文字列など、様々な形式のテキストデータを入力として扱うことができます。適切なテキスト抽出処理を追加することで、さらに多くのデータソース（例：Webページ、ドキュメントファイル）に対応可能です。

**処理の流れ**

```
入力データ (PDF, テキストファイル, 文字列など)  -->  テキスト抽出  -->  目次生成 (LLM使用)  -->  コンテンツ抽出 (目次と本文のマッチング)  -->  構造化されたMarkdown出力
```

**このライブラリを使うメリット**

-   **文書の構造化を自動化**: 手動で目次を作成したり、本文を整理したりする手間を省き、文書の構造化を自動化できます。
-   **可読性の向上**: 生成されたMarkdownは、人間にとって読みやすい形式です。
-   **機械可読性の向上**: 構造化されたMarkdownは、RAGなどのシステムで扱いやすく、情報検索や文書要約などのタスクに活用できます。
-   **多様な用途への応用**: 生成されたMarkdownは、ドキュメントの作成、Webページの作成、ナレッジベースの構築など、様々な用途に応用できます。

**要約すると、このライブラリは、非構造化テキストを、人間にも機械にも優しい、構造化されたMarkdownに変換するための強力なツールです。**

## 使用方法

**1. 必要なライブラリのインストール**

```bash
pip install litellm pdfminer.six python-dotenv
```

**2. 環境変数の設定 (オプション)**

複数のLLMを使用する場合、各モデルのAPIキーを環境変数に設定します。これは必須ではありませんが、設定しておくことを推奨します。

例：

```
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
ANYSCALE_API_KEY="YOUR_ANYSCALE_API_KEY"
```

`.env` ファイルを作成し、上記のようにキーを設定してプロジェクトのルートディレクトリに配置するか、システムの環境変数として設定してください。

**3. コードの使用例 (PDFを入力とする場合)**

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

# PDFからテキストを抽出する関数
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.detect_vertical = True  # 縦書きを認識する設定
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
pdf_file_path = "your_document.pdf"  # 処理したいPDFファイルのパス
extracted_text = extract_text_from_pdf(pdf_file_path)

if extracted_text:
    # 目次を生成 (ここではGeminiを使用)
    toc = create_toc(extracted_text, model="gemini/gemini-1.5-flash")

    # 目次に基づいてコンテンツを抽出
    toc_extractor = TocContentExtractor()
    structured_markdown = toc_extractor.extract_content_by_toc(toc, extracted_text)

    # 結果を出力
    print(structured_markdown)
else:
    print("PDFからテキストを抽出できませんでした。")
```

**4. コードの使用例 (テキストファイルを入力とする場合)**

```python
from create_toc import create_toc
from toc_content_extractor import TocContentExtractor

# テキストファイルからテキストを抽出する関数
def extract_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

# 使用例
text_file_path = "your_text_file.txt"  # 処理したいテキストファイルのパス
extracted_text = extract_text_from_file(text_file_path)

# 目次を生成 (ここではGPT-3.5を使用)
toc = create_toc(extracted_text, model="gpt-3.5-turbo")

# 目次に基づいてコンテンツを抽出
toc_extractor = TocContentExtractor()
structured_markdown = toc_extractor.extract_content_by_toc(toc, extracted_text)

# 結果を出力
print(structured_markdown)
```

**5. コードの使用例（文字列を直接入力する場合）**

```python
from create_toc import create_toc
from toc_content_extractor import TocContentExtractor

# 入力文字列
input_text = """
# はじめに

これはサンプルテキストです。

## 第1章

第1章の内容です。

### 1.1 節

節の内容です。

## 第2章

第2章の内容です。
"""

# 目次を生成 (ここではClaude 2を使用)
toc = create_toc(input_text, model="claude-2")

# 目次に基づいてコンテンツを抽出
toc_extractor = TocContentExtractor()
structured_markdown = toc_extractor.extract_content_by_toc(toc, input_text)

# 結果を出力
print(structured_markdown)
```

**カスタマイズ**

-   `create_toc.py` の `MARKDOWN_PROMPT_TEMPLATE` を変更することで、目次の生成方法（見出しレベル、フォーマットなど）をカスタマイズできます。
-   `toc_content_extractor.py` の `toc_search_min_length` と `toc_max_level` を変更することで、抽出する目次や本文の条件（最小文字列長、最大見出しレベル）を調整できます。

これらの例を参考に、用途に合わせてコードを修正し、様々な形式のテキストデータを構造化されたMarkdownに変換してみてください。
