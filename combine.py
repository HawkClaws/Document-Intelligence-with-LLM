import re

def combine_text_with_toc(toc_path, text_path, output_path):
    """
    見出しのみの目次（マークダウン）にテキストを埋め込む。

    Args:
        toc_path (str): 目次ファイルのパス (見出しのみ)
        text_path (str): テキストファイルのパス
        output_path (str): 出力ファイルのパス
    """

    with open(toc_path, 'r', encoding='utf-8') as f_toc:
        toc_lines = [line.strip() for line in f_toc.readlines()]

    with open(text_path, 'r', encoding='utf-8') as f_text:
        text_content = f_text.read()

    output_lines = []

    for i, toc_line in enumerate(toc_lines):
        output_lines.append(toc_line)
        print(f"処理中の目次行: {toc_line}")  # デバッグ用

        match_header = re.match(r'^(#+)\s+(.+)', toc_line)

        if match_header:
            header_level = match_header.group(1)
            title = match_header.group(2).strip()
            print(f"  見出しレベル: {header_level}, タイトル: {title}")  # デバッグ用

            header_pattern = rf"(^|\n){header_level}\s*{re.escape(title)}\s*(\n|$)"
            print(f"  検索パターン: {header_pattern}")  # デバッグ用
            match = re.search(header_pattern, text_content, re.MULTILINE)

            if match:
                print(f"  一致箇所が見つかりました: {match.group(0)}")  # デバッグ用
                start_index = match.end()

                next_section_start = len(text_content)
                for j in range(i + 1, len(toc_lines)):
                    next_toc_line = toc_lines[j]
                    next_match_header = re.match(r'^(#+)\s+(.+)', next_toc_line)
                    if next_match_header:
                        next_header_level = next_match_header.group(1)
                        next_title = next_match_header.group(2).strip()
                        next_header_pattern = rf"(^|\n){next_header_level}\s*{re.escape(next_title)}\s*(\n|$)"
                        next_match = re.search(next_header_pattern, text_content, re.MULTILINE)
                        if next_match:
                            next_section_start = next_match.start()
                            break
                section_content = text_content[start_index:next_section_start].strip()
                output_lines.append(section_content)
            else:
                print(f"  警告: 目次項目 '{title}' に対応するテキストが見つかりませんでした。")

    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write('\n'.join(output_lines))

if __name__ == "__main__":
    toc_file = 'toc.md'
    text_file = 'content.txt'
    output_file = 'combined.md'

    # サンプルファイルを作成
    with open(toc_file, 'w', encoding='utf-8') as f:
        f.write("# はじめに\n")
        f.write("## セクション1\n")
        f.write("### サブセクション1.1\n")
        f.write("## セクション2\n")

    with open(text_file, 'w', encoding='utf-8') as f:
        f.write("はじ めに\n")
        f.write("はじめにのテキストです。\n\n")
        f.write("セクション1のテキストです。\n\n")
        f.write("サブセクション1.1のテキストです。\n\n")
        f.write("セクション2のテキストです。\n")

    combine_text_with_toc(toc_file, text_file, output_file)
    print(f"結合されたファイルが '{output_file}' に出力されました。")