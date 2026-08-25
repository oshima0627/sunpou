# -*- coding: utf-8 -*-
"""X（旧Twitter）の文字数を数える。投稿する前に必ずこれで確認する。

数え方（twitter-text の weighted counting）:
  - コードポイントが U+0000〜U+10FF と一部の記号レンジ → 1
  - それ以外（日本語を含む）                           → 2
  - URL は長さに関係なく 23
上限は 280（無料アカウント）。

使い方:
    python tools/x-count.py drafts.txt      # ファイルを読む（推奨）
    python tools/x-count.py                 # 標準入力

複数の投稿を1ファイルに入れるときは、行頭の `---` で区切る。

⚠️ Windows のシェル経由で日本語を渡すと文字化けして数値が狂う。
   **必ずファイルに書いてから渡すこと。**（実際に printf 経由で 462 と誤検出した）

検算: 2026-08-25 の固定ポストで 272/280（残り8）。Xの表示と一致することを確認済み。
"""
import re, sys, io

sys.stdout.reconfigure(encoding="utf-8")

LIMIT = 280
URL_WEIGHT = 23
# weight 1 のレンジ。これ以外は 2。
LIGHT = [(0x0000, 0x10FF), (0x2000, 0x200D), (0x2010, 0x201F), (0x2032, 0x2037)]
URL_RE = re.compile(r"https?://\S+")


def weight(ch):
    c = ord(ch)
    return 1 if any(a <= c <= b for a, b in LIGHT) else 2


def count(text):
    n = 0
    last = 0
    for m in URL_RE.finditer(text):
        n += sum(weight(c) for c in text[last:m.start()])
        n += URL_WEIGHT
        last = m.end()
    n += sum(weight(c) for c in text[last:])
    return n


def main():
    if len(sys.argv) > 1:
        raw = io.open(sys.argv[1], encoding="utf-8").read()
    else:
        sys.stdin.reconfigure(encoding="utf-8")
        raw = sys.stdin.read()

    # 行頭 # はコメント。数えない。
    raw = "\n".join(l for l in raw.split("\n") if not l.startswith("#"))
    posts = [p.strip("\n") for p in re.split(r"^---$", raw, flags=re.M)]
    ng = 0
    for i, p in enumerate([x for x in posts if x.strip()], 1):
        n = count(p)
        head = p.split("\n")[0][:34]
        if n <= LIMIT:
            print(f"[{i}] OK  {n:3d}/{LIMIT}  残り{LIMIT - n:3d}   {head}")
        else:
            ng += 1
            over = n - LIMIT
            print(f"[{i}] NG! {n:3d}/{LIMIT}  {over}オーバー（日本語で約{-(-over // 2)}字削る）   {head}")
    sys.exit(1 if ng else 0)


if __name__ == "__main__":
    main()
