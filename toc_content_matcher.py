from collections import Counter
import re
import unicodedata


class TocContentMatcher:
    def __init__(self, toc_search_min_length: int = 6, toc_max_level: int = 3):
        self.toc_search_min_length = toc_search_min_length
        self.toc_max_level = toc_max_level

    def find_closest_match(self, matches, N):
        """matchesの中から長さNに最も近いものを返す。"""
        if not matches:
            return None

        closest_match = min(matches, key=lambda m: abs(len(m.group(1)) - N))
        return closest_match

    def normalize(self, text):
        """
        全角・半角の違いを無視して正規化する関数。
        """
        # 文字列を正規化形式「NFKC」に変換
        text = unicodedata.normalize("NFKC", text)
        # スペースを取り除く
        return re.sub(r"[\s\u3000]+", "", text.lower())

    def generate_filtered_toc(self, toc_list, toc_max_level):
        """
        Markdownテキストから目次を生成し、指定されたレベル以下の階層のみにフィルタリングし、
        重複と短い文字列を除去する関数。

        Args:
            markdown_text: Markdown形式のテキスト。
            toc_max_level: フィルタリングする最大ヘッダーレベル (デフォルトは2, ## まで)。
            # toc_search_min_length: 除去する最小文字列の長さ (デフォルトは4)。

        Returns:
            指定されたレベル以下の階層の目次リスト (文字列リスト)。空リストを返す場合もあります。
        """

        # レベル判定とフィルタリング
        filtered_toc = []
        for item in toc_list:
            if bool(re.match(r"^#{1,6}\s", item)) == False:
                continue
            item = item.strip()
            level = len(item) - len(item.lstrip("# ")) - 1  # '#'の数でレベルを判断
            if level <= toc_max_level:
                filtered_toc.append(item)

        # 重複と短い文字列を除去
        # filtered_array = [item.strip() for item in filtered_toc if len(item.strip()) > self.toc_search_min_length]
        counts = Counter(filtered_toc)
        return [item for item in filtered_toc if counts[item] == 1]

    def convert_toc_to_regex(self, toc):
        """
        TOC を正規表現形式に変換。
        """
        normalized_line = self.normalize(toc)
        pattern = re.sub(r"[#\s]+", r".*", re.escape(normalized_line))
        return re.compile(pattern).pattern

    def extract_content_by_toc(self, toc_text: str, content: str):
        """
        TOC を使って content から対応するセクションを抜き出す。
        """
        result = []
        normalized_content = self.normalize(content)
        search_start = 0  # 検索の開始位置を管理

        toc_list = toc_text.splitlines()
        toc_list = self.generate_filtered_toc(toc_list, self.toc_max_level)
        for i, toc_line in enumerate(toc_list):
            # 次の見出しまでの範囲を抽出
            next_toc_line = None
            if i + 1 < len(toc_list):
                next_toc_line = toc_list[i + 1]

                # 現在のセクションに対応するテキストを検索
                next_toc_line_temp = next_toc_line.lstrip("#").lstrip(" ")
            toc_line_temp = toc_line.lstrip("#").lstrip(" ")

            while True:
                target_text = normalized_content[search_start:]
                if next_toc_line:
                    regex_patterns = f"({self.convert_toc_to_regex(toc_line_temp)})(.*?)(?={self.convert_toc_to_regex(next_toc_line_temp)})"
                    regex_patterns = (
                        f"(.*?)(?={self.convert_toc_to_regex(next_toc_line_temp)})"
                    )
                else:
                    regex_patterns = f"({self.convert_toc_to_regex(toc_line_temp)})(.*)"
                    regex_patterns = f"(.*)"
                matches = list(re.finditer(regex_patterns, target_text, re.DOTALL))
                if len(matches) > 0:
                    break
                else:
                    if i == 0:
                        toc_line_temp = toc_line_temp[1:-1]
                        next_toc_line_temp = next_toc_line_temp[1:-1]
                    elif i == len(toc_list) - 1:
                        toc_line_temp = toc_line_temp[1:-1]
                    else:
                        next_toc_line_temp = next_toc_line_temp[1:-1]

                    if (
                        len(toc_line_temp) < self.toc_search_min_length
                        or len(next_toc_line_temp) < self.toc_search_min_length
                    ):
                        print(f"match failed :{next_toc_line}")
                        break

            # マッチしたもののうち、最長の内容を選択
            # longest_match = self.find_closest_match(matches, N=1000)
            # longest_match = max(matches, key=lambda m: len(m.group(1)), default=None)

            # if longest_match:
            if len(matches) > 0:
                longest_match = matches[0]

                extracted_text = longest_match.group(1).strip()
                print(f"match success :{next_toc_line} length:{len(extracted_text)}")
                # 元の目次の形式を保持しつつ結果に追加
                result.append(toc_line)
                result.append(re.sub(r"\\s+", "", extracted_text))
                # 検索開始位置を更新（ヒットした最後の位置の次から検索を開始）
                search_start += longest_match.end()
            print(search_start)
        return "\n".join(result)


if __name__ == "__main__":
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
はじめにはじめにのテキストです。
## セクション1
セクション1hogehogeセクション1のテキストです。セクション1のテキストの続きです。
## サブセクション1.1
サブセクション1.1サブセクションのテキストです。
## セクション2
セクション2hugahugaセクショントゥーのテキストです。
## サブセクション3.1
セクション3セクションスリーのテキーストですー。"""

    # クラスのインスタンスを作成し、メソッドを呼び出して結果を検証
    matcher = TocContentMatcher()
    merged_result = matcher.extract_content_by_toc(toc, content)
    print(merged_result)
    assert merged_result == expected, f"\nGot:\n{merged_result}\nExpected:\n{expected}"
    print("Test passed. The merged content matches the expected output.")
