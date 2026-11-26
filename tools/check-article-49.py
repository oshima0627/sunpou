# -*- coding: utf-8 -*-
"""記事49の、最短辺と前後すき間・荷室の短い辺を独立に再計算する。

狭い足元は約190mm、広い足元は約320mm（シエンタ7人乗り、ターンチルト以外）。
最短辺は公表3辺の最小。荷室に入るは、電源の長い辺が荷室の短い辺以下。
買い物かごは 515×388×355 に、大きい順で割り当てる。
"""
import pathlib
import sys

# (名前, 幅mm, 奥行mm, 高さmm, 軸が分かっているか)
# EcoFlow は幅・奥行・高さの対応がページに無い。3数だけを入れる。
UNITS = [
    ("Anker Solix C300 DC", 124, 120, 200, True),
    ("Anker 522", 216, 144, 211, True),
    ("Jackery 240 New", 231, 153, 168.19, True),
    ("Anker Solix C300", 164, 161, 240, True),
    ("Anker 535", 292, 188, 251, True),
    ("EcoFlow DELTA 3", 398, 202, 284, False),
    ("EcoFlow DELTA 3 Plus", 398, 202, 284, False),
    ("Anker Solix C800", 371, 205, 250, True),
    ("Anker Solix C800 Plus", 371, 205, 250, True),
    ("Anker Solix C1000", 376, 205, 267, True),
    ("Anker Solix C1000 Gen 2", 384, 208, 244, True),
    ("EcoFlow DELTA 3 1000 Air", 220, 223, 263, False),
    ("Jackery 1000 New", 327, 224, 247, True),
    ("Anker 757", 463, 237, 288, True),
]

NARROW = 190
WIDE = 320
CARS = {
    "ヤリス": (630, 1000, 692),
    "フィット": (640, 1010, 870),
    "シエンタ": (840, 1265, 1055),
}
BASKET = (515, 388, 355)  # 長辺、高さ、短辺

ARTICLE = pathlib.Path("site/content/articles/portable-power-foot-gap-cargo-fit.md")


def shortest(u):
    return min(u[1], u[2], u[3])


def longest(u):
    return max(u[1], u[2], u[3])


def fits_sorted(box, dims):
    b = tuple(sorted(box, reverse=True))
    d = tuple(sorted(dims, reverse=True))
    return all(x <= y for x, y in zip(d, b))


def main():
    errors = []
    if len(UNITS) != 14:
        errors.append(f"機種数 {len(UNITS)}")

    narrow = [u for u in UNITS if shortest(u) <= NARROW]
    wide = [u for u in UNITS if shortest(u) <= WIDE]
    over = [u for u in UNITS if shortest(u) > WIDE]
    if len(narrow) != 5:
        errors.append(f"狭い {len(narrow)} {[u[0] for u in narrow]}")
    if len(wide) != 14:
        errors.append(f"広い {len(wide)}")
    if over:
        errors.append(f"320超 {over}")

    # 軸がある機種は最短辺が奥行
    for u in UNITS:
        if u[4] and shortest(u) != u[2]:
            errors.append(f"最短が奥行でない {u[0]} {shortest(u)} vs 奥行{u[2]}")

    expect_short = {
        "Anker Solix C300 DC": (120, 70, 200),
        "Anker 522": (144, 46, 176),
        "Jackery 240 New": (153, 37, 167),
        "Anker Solix C300": (161, 29, 159),
        "Anker 535": (188, 2, 132),
        "EcoFlow DELTA 3": (202, -12, 118),
        "Anker Solix C800": (205, -15, 115),
        "Anker Solix C1000 Gen 2": (208, -18, 112),
        "EcoFlow DELTA 3 1000 Air": (220, -30, 100),
        "Jackery 1000 New": (224, -34, 96),
        "Anker 757": (237, -47, 83),
    }
    by = {u[0]: u for u in UNITS}
    for name, (s, d190, d320) in expect_short.items():
        u = by[name]
        if shortest(u) != s:
            errors.append(f"最短 {name} {shortest(u)}")
        if NARROW - shortest(u) != d190:
            errors.append(f"190差 {name} {NARROW - shortest(u)}")
        if WIDE - shortest(u) != d320:
            errors.append(f"320差 {name} {WIDE - shortest(u)}")

    long757 = longest(by["Anker 757"])
    if long757 != 463:
        errors.append(f"757長い {long757}")
    if 630 - long757 != 167:
        errors.append("ヤリス差")
    if 640 - long757 != 177:
        errors.append("フィット差")
    if 840 - long757 != 377:
        errors.append("シエンタ差")
    if 515 - long757 != 52:
        errors.append("かご差")

    for u in UNITS:
        dims = (u[1], u[2], u[3])
        if longest(u) > 630:
            errors.append(f"ヤリスを超える {u[0]}")
        for car, box in CARS.items():
            if not fits_sorted(box, dims):
                errors.append(f"荷室 {car} {u[0]}")
        if not fits_sorted(BASKET, dims):
            errors.append(f"かご {u[0]}")

    # DELTA 3 は2番目に長い辺が284。どの軸が高さでも床の短い辺は284以下。
    d3 = by["EcoFlow DELTA 3"]
    ordered = tuple(sorted((d3[1], d3[2], d3[3]), reverse=True))
    if ordered != (398, 284, 202):
        errors.append(f"DELTA3順 {ordered}")

    text = ARTICLE.read_text(encoding="utf-8")
    for needle in (
        "5機種",
        "9機種",
        "14機種",
        "余り70mm",
        "余り2mm",
        "12mm出る",
        "167mm",
        "177mm",
        "377mm",
        "52mm",
        "168.19mm",
        "630mm",
        "約190mm",
        "約320mm",
        "未掲載",
        "未検証",
    ):
        if needle not in text:
            errors.append(f"本文に無い {needle}")

    if errors:
        print("NG")
        for e in errors:
            print(" -", e)
        return 1
    print("OK 14機種 狭い5 広い14 ヤリス差167 かご差52")
    return 0


if __name__ == "__main__":
    sys.exit(main())
