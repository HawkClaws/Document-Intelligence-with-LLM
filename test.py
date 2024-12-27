from toc_content_extractor import TocContentExtractor

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
    matcher = TocContentExtractor()
    merged_result = matcher.extract_content_by_toc(toc, content)
    print(merged_result)
    assert merged_result == expected, f"\nGot:\n{merged_result}\nExpected:\n{expected}"
    print("Test passed. The merged content matches the expected output.")
