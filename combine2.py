import re
import unicodedata

def normalize_text(text):
    # NFKC正規化（全角→半角、文字の正規化）
    text = unicodedata.normalize('NFKC', text)
    # 空白文字を削除
    text = re.sub(r'\s+', '', text)
    # 英字を削除（数字は保持）
    text = re.sub(r'[a-zA-Z]', '', text)
    # 記号を削除
    text = re.sub(r'[!"#$%&\'()*+,-./:;<=>?@\[\]^_`{|}~]', '', text)
    return text

def merge_toc_content(toc, content):
    # TOCの見出しとレベルを抽出
    toc_entries = []
    for line in toc.splitlines():
        if not line.strip():
            continue
        match = re.match(r'(#+)\s*(.+)', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            normalized_title = normalize_text(title)
            print(f"\nTOCエントリー: '{title}'")
            print(f"正規化後: '{normalized_title}'")
            toc_entries.append((level, title, normalized_title))

    # コンテンツの解析
    content_dict = {}
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
            
        normalized_line = normalize_text(line)
        print(f"\n検査中の行: '{line}'")
        print(f"正規化後: '{normalized_line}'")
        
        for level, title, normalized_title in toc_entries:
            if normalized_line == normalized_title:
                print(f"マッチ成功: '{title}'")
                if i + 1 < len(lines):
                    content_dict[normalized_title] = lines[i + 1].strip()
                break
        i += 1

    # 結果の構築
    result = []
    for level, title, normalized_title in toc_entries:
        result.append('#' * level + ' ' + title)
        if normalized_title in content_dict:
            result.append(content_dict[normalized_title])
    
    return '\n'.join(result)

# テスト実行
if __name__ == "__main__":
    toc = """# はじめに
## セクション1
### サブセクション1.1
## セクション2"""

    content = """は じめ に
はじめにのテキストです。
セ ク シ ョ ン 1hogehoge
セクション1のテキストです。
サ    ブ　セクショ ン1.1
サブセクション1.1のテキストです。
セ ク シ ョ ン ２hugahuga
セクション2のテキストです。
"""

    print("=== 処理開始 ===")
    result = merge_toc_content(toc, content)
    print("\n=== 最終出力 ===")
    print(result)

    expected = """# はじめに
はじめにのテキストです。
## セクション1
セクション1のテキストです。
### サブセクション1.1
サブセクション1.1のテキストです。
## セクション2
セクション2のテキストです。"""

    print("\n=== 期待値との比較 ===")
    if result != expected:
        print("不一致があります。差分:")
        result_lines = result.splitlines()
        expected_lines = expected.splitlines()
        for i, (r, e) in enumerate(zip(result_lines, expected_lines)):
            if r != e:
                print(f"行 {i+1}:")
                print(f"実際: '{r}'")
                print(f"期待: '{e}'")
    else:
        print("期待値と完全に一致しました。")