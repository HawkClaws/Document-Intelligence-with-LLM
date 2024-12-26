import re

def merge_toc_content(toc, content):
    # TOC の見出しとレベルを抽出
    toc_lines = [line for line in toc.splitlines() if line.strip()]
    toc_entries = []
    for line in toc_lines:
        match = re.match(r"(#+)\s*(.+)", line)
        if match:
            level = len(match.group(1))
            # タイトル内の空白を単一スペースに正規化
            title = ' '.join(match.group(2).split())
            toc_entries.append((level, title))

    # コンテンツをパース
    content_dict = {}
    lines = [line.rstrip() for line in content.splitlines()]
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:  # 空行をスキップ
            i += 1
            continue
            
        # 見出し行の処理
        heading = line
        text = None
        
        # 次の行がある場合、それをテキストとして扱う
        if i + 1 < len(lines):
            text = lines[i + 1].strip()
            i += 2
        else:
            i += 1
            
        # 見出しをキーとして、対応するテキストを格納
        if text:
            content_dict[heading] = text

    # 結合
    result = []
    for level, title in toc_entries:
        # 見出しから空白を削除したものでマッチング
        normalized_title = ''.join(title.split())
        result.append('#' * level + ' ' + normalized_title)
        
        # コンテンツ辞書から対応するテキストを探す
        for content_heading, content_text in content_dict.items():
            if ''.join(content_heading.split()) == normalized_title:
                result.append(content_text)
                break

    return '\n'.join(result)

# テストデータ
toc = """# は じめ に
## セ ク シ ョ ン 1
### サ    ブ　セクショ ン1.1
## セ ク シ ョ ン ２
"""

content = """はじめに
はじめにのテキストです。
セクション1
セクション1のテキストです。
サブセクション1.1
サブセクション1.1のテキストです。
セクション２
セクション2のテキストです。
"""

# 実行して結果を確認
result = merge_toc_content(toc, content)
print(result)