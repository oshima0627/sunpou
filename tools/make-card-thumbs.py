#!/usr/bin/env python3
"""記事一覧カード用のサムネイルを作る（site/public/img/card/）。

一覧（トップ・カテゴリ）のカードは 240px 幅で表示するのに、1200×630 のアイキャッチ原寸
（1枚約100〜180KB）を読んでいた。ここでは 600×315（2x 表示まで足りる幅）の WebP と JPEG を作る。

- 原本: site/public/img/*-photo-eyecatch.jpg（**触らない**。OG画像・記事ヒーローで使う）
- 出力: site/public/img/card/<同じ名前>.webp / .jpg（コミットして配信する）
- 使われ方: site/img-cards.mjs がビルド後に一覧の <img> を <picture> へ差し替える。
  サムネが無い画像は原寸のままにして警告を出す（ビルドは落とさない）。

使い方（新しい記事を足したら実行してコミット）:
    python tools/make-card-thumbs.py          # 無いものだけ作る
    python tools/make-card-thumbs.py --force  # 全部作り直す
要: Pillow
"""
import sys
from pathlib import Path
from PIL import Image

SRC = Path(__file__).resolve().parent.parent / "site" / "public" / "img"
DST = SRC / "card"
W, H = 600, 315
WEBP_Q, JPEG_Q = 80, 78

force = "--force" in sys.argv
DST.mkdir(exist_ok=True)
made = 0
for src in sorted(SRC.glob("*-photo-eyecatch.jpg")):
    webp, jpg = DST / (src.stem + ".webp"), DST / src.name
    if not force and webp.exists() and jpg.exists():
        continue
    im = Image.open(src).convert("RGB")
    if im.size != (1200, 630):
        print(f"skip（1200x630 ではない）: {src.name} {im.size}")
        continue
    im = im.resize((W, H), Image.LANCZOS)
    im.save(webp, "WEBP", quality=WEBP_Q, method=6)
    im.save(jpg, "JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    made += 1
print(f"made {made} thumbnails -> {DST}")
