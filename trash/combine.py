import re
import unicodedata

def normalize_text(text):
    """テキストの正規化：全角/半角統一、半角カナを全角カナに変換"""
    text = unicodedata.normalize('NFKC', text)
    return text

def combine_text_with_toc(toc_path, text_path, output_path, ignore_kana=False):
    """
    見出しのみの目次（マークダウン）にテキストを埋め込む。
    検索を緩くするために、以下の変更を行いました。
    1. タイトルの部分一致で検索 (より厳密なマッチング)。
    2. 大文字小文字を区別しない。
    3. スペースを完全に無視する。
    4. 見出し記号(#)がない場合も考慮する。
    5. 全角/半角を区別しない (オプション)
    6. 半角カナを全角カナに変換 (オプション)

    Args:
        toc_path (str): 目次ファイルのパス (見出しのみ)
        text_path (str): テキストファイルのパス
        output_path (str): 出力ファイルのパス
        ignore_kana (bool): 全角/半角カナを区別しない場合はTrue
    """

    with open(toc_path, 'r', encoding='utf-8') as f_toc:
        toc_lines = [line.strip() for line in f_toc.readlines()]

    with open(text_path, 'r', encoding='utf-8') as f_text:
        text_content = f_text.read()

    output_lines = []
    remaining_text = text_content

    for i, toc_line in enumerate(toc_lines):
        output_lines.append(toc_line)
        print(f"処理中の目次行: {toc_line}")

        match_header = re.match(r'^(#*)\s*(.+)', toc_line)
        title = toc_line.strip()
        header_level = 0

        if match_header:
            header_level = len(match_header.group(1))
            title = match_header.group(2).strip()
            print(f"  見出しレベル: {'#' * header_level}, タイトル: {title}")
        else:
            print(f"  見出し記号なし、タイトル: {title}")

        normalized_title = normalize_text(title).replace(" ", "") if ignore_kana else title.replace(" ", "")

        found_match = False
        section_content = ""

        # 見出し記号がある場合
        if header_level > 0:
            header_pattern = rf"(^|\n)(#{{{header_level}}})\s*({re.escape(title)})(?:\n|$)"
            print(f"  検索パターン (見出しあり): {header_pattern}")
            matches = re.finditer(header_pattern, remaining_text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                matched_title_text = match.group(3)
                normalized_matched_title = normalize_text(matched_title_text).replace(" ", "") if ignore_kana else matched_title_text.replace(" ", "")
                if normalized_title in normalized_matched_title:
                    start_index = match.end()
                    next_header_pattern = r"(^|\n)(#+)\s"  # より低いレベルの見出しを検出
                    next_matches = re.finditer(next_header_pattern, remaining_text[start_index:], re.MULTILINE)
                    end_index = len(remaining_text)
                    for next_match in next_matches:
                        if next_match.start() > 0: # 空行の後の見出しを考慮
                            end_index = start_index + next_match.start()
                            break
                    section_content = remaining_text[start_index:end_index].strip()
                    remaining_text = remaining_text[end_index:] # 処理済みテキストを削除
                    found_match = True
                    print(f"  一致箇所が見つかりました (見出しあり): {match.group(0).strip()}")
                    break
        # 見出し記号がない場合
        else:
            header_pattern = rf"(^|\n)({re.escape(title)})(?:\n|$)"
            print(f"  検索パターン (見出しなし): {header_pattern}")
            matches = re.finditer(header_pattern, remaining_text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                matched_title_text = match.group(2)
                normalized_matched_title = normalize_text(matched_title_text).replace(" ", "") if ignore_kana else matched_title_text.replace(" ", "")
                if normalized_title in normalized_matched_title:
                    start_index = match.end()
                    next_block_pattern = r"(^|\n){2,}" # 2つ以上の連続する改行をブロックの区切りとする
                    next_matches = re.finditer(next_block_pattern, remaining_text[start_index:], re.MULTILINE)
                    end_index = len(remaining_text)
                    for next_match in next_matches:
                        end_index = start_index + next_match.start()
                        break
                    section_content = remaining_text[start_index:end_index].strip()
                    remaining_text = remaining_text[end_index:] # 処理済みテキストを削除
                    found_match = True
                    print(f"  一致箇所が見つかりました (見出しなし): {match.group(0).strip()}")
                    break

        if found_match:
            output_lines.append(section_content)
        else:
            print(f"  警告: 目次項目 '{title}' に対応するテキストが見つかりませんでした。")

    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write('\n'.join(output_lines))

if __name__ == "__main__":
    toc_file = 'toc.md'
    text_file = 'content.txt'
    output_file = 'combined.md'

    # サンプルファイルを作成（揺らぎを含む、スペースを大幅に変えてみる）
    with open(toc_file, 'w', encoding='utf-8') as f:
        f.write("# は じめ に\n")
        f.write("## セ ク シ ョ ン 1\n")
        f.write("### サ    ブ　セクショ ン1.1\n")
        f.write("## セ ク シ ョ ン ２\n")
        f.write("見出し記号なしの項目\n")

    with open(text_file, 'w', encoding='utf-8') as f:
        f.write("はじめに\n")
        f.write("はじめにのテキストです。\n\n")
        f.write("セクション1\n")
        f.write("セクション1のテキストです。\n")
        f.write("サブセクション1.1\n")
        f.write("サブセクション1.1のテキストです。\n\n")
        f.write("セクション２\n")
        f.write("セクション2のテキストです。\n")
        f.write("見出し記号なしの項目\n")
        f.write("これは見出し記号なしの項目のテキストです。\n")

    combine_text_with_toc(toc_file, text_file, output_file, ignore_kana=True) # 全角/半角カナを区別しない
    print(f"結合されたファイルが '{output_file}' に出力されました。")