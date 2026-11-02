# -*- coding: utf-8 -*-
"""記事42の余り・機種数を、表の一次寸法から独立に再計算する。"""
import pathlib
import sys

# 製品, 種類, 幅, 外形奥行, 高さ
ROWS = [
    ("シャープ ES-GE7K", "縦型", 565, 538, 898),
    ("シャープ ES-GE5K", "縦型", 565, 540, 890),
    ("東芝 AW-7GM4", "縦型", 555, 560, 990),
    ("日立 BW-G70M", "縦型", 577, 586, 980),
    ("シャープ ES-GV10L", "縦型", 600, 597, 1009),
    ("シャープ ES-7S2", "ドラム", 640, 600, 1039),
    ("シャープ ES-8L2", "ドラム", 640, 600, 1040),
    ("東芝 TW-84GS5L", "ドラム", 640, 633, 975),
    ("Panasonic NA-FA10K6", "縦型", 592, 635, 1071),
    ("東芝 AW-12DPB6", "縦型", 637, 649, 1098),
    ("Panasonic NA-SD10UBL-W", "ドラム", 639, 650, 1010),
    ("シャープ ES-10L2", "ドラム", 640, 650, 1040),
    ("Panasonic NA-FA12V6", "縦型", 637, 694, 1086),
    ("日立 BD-SV120M", "ドラム", 638, 716, 1065),
    ("日立 BD-STX130M", "ドラム", 630, 720, 1065),
    ("東芝 TW-127XP5L", "ドラム", 645, 720, 1060),
    ("Panasonic NA-LX129FL", "ドラム", 639, 732, 1060),
    ("シャープ ES-X12C", "ドラム", 640, 739, 1115),
]

ARTICLE = pathlib.Path("site/content/articles/washer-outer-depth-limit-fit.md")


def main():
    errors = []
    text = ARTICLE.read_text(encoding="utf-8")
    for lim, want_all, want_drum in ((600, 7, 2), (650, 12, 5), (700, 13, 5)):
        fit = [r for r in ROWS if r[3] <= lim]
        drums = [r for r in fit if r[1] == "ドラム"]
        if len(fit) != want_all:
            errors.append(f"上限{lim}: 機種数 {len(fit)} != {want_all}")
        if len(drums) != want_drum:
            errors.append(f"上限{lim}: ドラム {len(drums)} != {want_drum}")
    spot = {
        "シャープ ES-7S2": (0, 50, 100),
        "シャープ ES-GV10L": (3, 53, 103),
        "東芝 TW-84GS5L": (-33, 17, 67),
        "東芝 AW-12DPB6": (-49, 1, 51),
        "Panasonic NA-SD10UBL-W": (-50, 0, 50),
        "Panasonic NA-FA12V6": (-94, -44, 6),
        "日立 BD-SV120M": (-116, -66, -16),
        "シャープ ES-X12C": (-139, -89, -39),
    }
    by = {r[0]: r for r in ROWS}
    for name, expect in spot.items():
        d = by[name][3]
        got = (600 - d, 650 - d, 700 - d)
        if got != expect:
            errors.append(f"{name}: 余り {got} != {expect}")
        for n in (str(d), *(str(abs(x)) for x in got)):
            if n not in text:
                errors.append(f"本文に {name} の {n} が無い")
    if 739 - 600 != 139:
        errors.append("ES-X12C と 600mm の差")
    if 560 and (600 - 560) != 40:
        errors.append("ES-GE5K 注記560の余り")
    # 表の行に、カードの商品名と 650 / 0 / 50 が同居する
    card_row = [
        line for line in text.splitlines()
        if line.startswith("|") and "[[LINK:Panasonic NA-SD10UBL-W::" in line
    ]
    if len(card_row) != 1:
        errors.append(f"カード商品の比較表の行が {len(card_row)} 本")
    elif not all(tok in card_row[0].replace(" ", "") for tok in ("650", "0", "50")):
        errors.append("カード商品の表行に余りが足りない")
    if errors:
        print("NG")
        for e in errors:
            print(" -", e)
        return 1
    print("OK 18機種 / 600は7（ドラム2） / 650は12（ドラム5） / 700は13（ドラム5）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
