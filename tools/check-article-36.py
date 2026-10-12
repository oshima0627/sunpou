# -*- coding: utf-8 -*-
"""記事36（/washer/vertical-waterproof-pan-fit/）の計算値を独立に出し直す。
データはすべて一次（各社の仕様ページ・東芝カタログ2026-04・TOTO施工図）。取得 2026-10-12。
python3 tools/check-article-36.py"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

# 製品, 外形 幅, 外形 奥行, 外形 高さ, 防水パンの奥行内寸（条件）, 壁からパン前面内側（None=記載なし）
ROWS = [
    ("Panasonic NA-FA12V6", 637, 694, 1086, 540, 600),
    ("Panasonic NA-FA10K6", 592, 635, 1071, 540, 590),
    ("日立 BW-X120M", 640, 650, 1077, 530, None),
    ("日立 BW-V100M", 608, 610, 1000, 530, None),
    ("日立 BW-G70M", 577, 586, 980, 530, None),
    ("シャープ ES-SW11L", 600, 652, 1055, 540, None),
    ("シャープ ES-GV10L", 600, 597, 1009, 550, None),
    ("シャープ ES-GV8L", 565, 596, 1018, 510, None),
    ("シャープ ES-GE7K", 565, 538, 898, 507, None),
    ("シャープ ES-GE5K", 565, 540, 890, 535, None),
    ("東芝 AW-12DPB6", 637, 649, 1098, 550, 590),
    ("東芝 AW-9DPB6", 600, 621, 1033, 510, 580),
    ("東芝 AW-7DH6", 555, 567, 998, 540, 600),
    ("東芝 AW-10GM3", 622, 639, 1052, 570, None),
    ("東芝 AW-7GM4", 555, 560, 990, 540, None),
]
TOTO = {"640・740": 580, "800・900": 546}

print("製品 | 外形奥行 | 条件 | 外形奥行−条件")
for n, w, d, h, c, wall in ROWS:
    print(f"{n} | {d} | {c} | {d - c}")
conds = sorted({r[4] for r in ROWS})
diffs = [r[2] - r[4] for r in ROWS]
print("条件の範囲", min(conds), "〜", max(conds), "／差の範囲", min(diffs), "〜", max(diffs))
print("外形奥行の範囲", min(r[2] for r in ROWS), "〜", max(r[2] for r in ROWS))
print()
print("条件 | TOTO640・740(580)との差 | TOTO800・900(546)との差")
for c in conds:
    print(c, "|", f"{580 - c:+d}", "|", f"{546 - c:+d}")
short = [r[0] for r in ROWS if r[4] > 546]
print("546mmに届かない:", short)
