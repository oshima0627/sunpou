# -*- coding: utf-8 -*-
"""記事46の上がり・余り・組数を、表の一次寸法から独立に再計算する。"""
import pathlib
import sys

ARTICLE = pathlib.Path("site/content/articles/washer-pedestal-raise-shelf-fit.md")

# 製品, 閉じた全高, 小さい上がり, 大きい上がり
SMALL = [
    ("TW-84GS5L", 975, 15),
    ("TW-127XP5L", 1060, 15),
    ("NA-LX129FL", 1060, 20),
    ("NA-FA10K6", 1071, 20),
    ("NA-FA12V6", 1086, 20),
]
LARGE = [
    ("TW-84GS5L", 975, 77),
    ("NA-LX129FL", 1060, 40),
    ("NA-FA10K6", 1071, 40),
    ("BD-SV120M", 1065, 50),
    ("NA-FA12V6", 1086, 40),
    ("TW-127XP5L", 1060, 77),
]
SHELVES = (1100, 1200, 1300)


def remain(height, add, shelf):
    return shelf - (height + add)


def main():
    errors = []
    text = ARTICLE.read_text(encoding="utf-8")

    def need(value, label):
        if str(value) not in text:
            errors.append(f"{label} {value} が本文に無い")

    small_fit = 0
    for name, height, add in SMALL:
        summed = height + add
        need(summed, f"{name} 小")
        for shelf in SHELVES:
            need(remain(height, add, shelf), f"{name} 小{shelf}")
        if summed <= 1100:
            small_fit += 1
    if small_fit != 4:
        errors.append(f"小さい上がりで1100に入るのは {small_fit} != 4")
    if (1086 + 20) - 1100 != 6:
        errors.append("FA12 の不足が 6 ではない")

    large_fit = 0
    for name, height, add in LARGE:
        summed = height + add
        need(summed, f"{name} 大")
        for shelf in SHELVES:
            need(remain(height, add, shelf), f"{name} 大{shelf}")
        if summed <= 1100:
            large_fit += 1
    if large_fit != 2:
        errors.append(f"大きい上がりで1100に入るのは {large_fit} != 2")

    if 1038 + 300 != 1338:
        errors.append("LX 必要高さ")
    if 1338 + 20 != 1358 or 1338 + 40 != 1378:
        errors.append("LX かさ上げ後")
    if 1338 - 1300 != 38:
        errors.append("1300までの不足")
    if 1060 - 1038 != 22 or 1338 - 1060 != 278:
        errors.append("ホースと上方の差")
    for value in (1338, 1358, 1378, 38, 22, 278):
        need(value, "LX")

    if 1065 + 215 != 1280:
        errors.append("日立 1280")
    if 1100 - 1280 != -180 or 1200 - 1280 != -80 or 1300 - 1280 != 20:
        errors.append("日立の棚下余り")
    if 215 - 15 != 200 or 62 - 58 != 4:
        errors.append("幅の差")
    for value in (1280, -180, -80, 20, 200, 4, 58, 62):
        need(value, "その他")

    if errors:
        print("NG")
        for err in errors:
            print(" -", err)
        return 1
    print("OK 小4/5 大2/6 LX1338 日立1280")
    return 0


if __name__ == "__main__":
    sys.exit(main())
