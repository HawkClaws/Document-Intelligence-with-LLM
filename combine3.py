import re

# テスト用の目次とコンテンツ
toc = """# はじめに
## セクション1
### サブセクション1.1
## セクション2"""

content = """は じめ に
はじめにのテキストです。
セ ク シ ョ ン 1hogehoge
セクション1のテキストです。
セクション1のテキストの続きです。
サ    ブ　セクショ ン1.1
サブセクションのテキストです。
セ ク シ ョ ン ２hugahuga
セクション2のテキストです。
"""

# 期待される出力
expected = """# はじめに
はじめにのテキストです。
## セクション1
hogehogeセクション1のテキストです。
セクション1のテキストの続きです。
### サブセクション1.1
サブセクションのテキストです。
## セクション2
hugahugaセクション2のテキストです。"""

def normalize(text):
    """
    全角・半角やスペースを取り除いて正規化する関数。
    """
    return re.sub(r'[\s\u3000]+', '', text.lower())

def convert_toc_to_regex(toc):
    """
    TOC を正規表現形式に変換。
    """
    toc_lines = toc.splitlines()
    regex_patterns = []
    for line in toc_lines:
        normalized_line = normalize(line)
        pattern = re.sub(r'[#\s]+', r'.*', re.escape(normalized_line))
        regex_patterns.append((re.compile(pattern), line))
    return regex_patterns

def extract_content_by_toc(toc, content):
    """
    TOC を使って content から対応するセクションを抜き出す。
    """
    regex_patterns = convert_toc_to_regex(toc)
    result = []
    normalized_content = normalize(content)

    for i, (pattern, toc_line) in enumerate(regex_patterns):
        # 次の見出しまでの範囲を抽出
        next_pattern = regex_patterns[i + 1][0] if i + 1 < len(regex_patterns) else None

        # 現在のセクションに対応するテキストを検索
        if next_pattern:
            match = re.search(f'({pattern.pattern})(.*?)(?={next_pattern.pattern})', normalized_content, re.DOTALL)
        else:
            match = re.search(f'({pattern.pattern})(.*)', normalized_content, re.DOTALL)

        if match:
            extracted_text = match.group(2).strip()
            # 元の目次の形式を保持しつつ結果に追加
            result.append(toc_line)
            result.append(re.sub(r'\s+', '', extracted_text))

    return '\n'.join(result)

# 実行して結果を検証
merged_result = extract_content_by_toc(toc, content)
assert merged_result == expected, f"\nGot:\n{merged_result}\nExpected:\n{expected}"
print("Test passed. The merged content matches the expected output.")
