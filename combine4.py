import re
import unicodedata

# テスト用の目次とコンテンツ
toc = """# はじめに
## セクション1
## サブセクション1.1
## セクション2
## サブセクション3.1"""

content = """は じめ に
はじめにのテキストです。
セ ク シ ョ ン 1hogehoge
セクション①のテキストです。
セクション①のテキストの続きです。
ｻ    ブ　セクショ ン1.1
サブセクションのテキストです。
セ ク シ ョ ン ２hugahuga
セクショントゥーのテキストです。
セクション３
セクションスリーのテキーストですー。
"""

# 期待される出力
expected = """# はじめに
はじめにのテキストです。
## セクション1
hogehogeセクション1のテキストです。セクション1のテキストの続きです。
## サブセクション1.1
サブセクションのテキストです。
## セクション2
hugahugaセクショントゥーのテキストです。
## サブセクション3.1
セクションスリーのテキーストですー。
"""

def normalize(text):
    """
    全角・半角の違いを無視して正規化する関数。
    """
    # 文字列を正規化形式「NFKC」に変換
    text = unicodedata.normalize('NFKC', text)
    # スペースを取り除く
    return re.sub(r'[\s\u3000]+', '', text.lower())

def convert_toc_to_regex(toc):
    """
    TOC を正規表現形式に変換。
    """

    normalized_line = normalize(toc)
    pattern = re.sub(r'[#\s]+', r'.*', re.escape(normalized_line))
    return re.compile(pattern).pattern

def extract_content_by_toc(toc_text:str, content:str):
    """
    TOC を使って content から対応するセクションを抜き出す。
    """
    # regex_patterns = convert_toc_to_regex(toc)
    result = []
    normalized_content = normalize(content)
    search_start = 0  # 検索の開始位置を管理

    toc_list = toc_text.splitlines()
    for i, toc_line in enumerate(toc_list):
        # 次の見出しまでの範囲を抽出
        next_toc_line = None
        if i + 1 < len(toc_list):
            next_toc_line = toc_list[i + 1]


        # 現在のセクションに対応するテキストを検索
        if next_toc_line:
            matches = list(re.finditer(f'({convert_toc_to_regex(toc_line)})(.*?)(?={convert_toc_to_regex(next_toc_line)})', normalized_content[search_start:], re.DOTALL))
        else:
            matches = list(re.finditer(f'({convert_toc_to_regex(toc_line)})(.*)', normalized_content[search_start:], re.DOTALL))

        # マッチしたもののうち、最長の内容を選択
        longest_match = max(matches, key=lambda m: len(m.group(2)), default=None)

        if longest_match:
            extracted_text = longest_match.group(2).strip()
            # 元の目次の形式を保持しつつ結果に追加
            result.append(toc_line)
            result.append(re.sub(r'\\s+', '', extracted_text))
            # 検索開始位置を更新（ヒットした最後の位置の次から検索を開始）
            search_start += longest_match.end()

    return '\n'.join(result)


# 実行して結果を検証
merged_result = extract_content_by_toc(toc, content)
print(merged_result)
assert merged_result == expected, f"\nGot:\n{merged_result}\nExpected:\n{expected}"
print("Test passed. The merged content matches the expected output.")
