# -*- coding: utf-8 -*-
"""記事41の余り・機種数を、表の一次寸法から独立に再計算する。"""
import pathlib
import sys

# 製品, 本体幅, 最小設置幅, 据付必要奥行
ROWS = [
    ("Panasonic NR-C37WS2", 600, 610, 600),
    ("Panasonic NR-F53HV2", 650, 660, 725),
    ("日立 R-HZC54Y", 650, 660, 699),
    ("三菱電機 MR-WZ55N", 650, 660, 709),
    ("Panasonic NR-F55WX3", 685, 695, 699),
    ("シャープ SJ-MF51R", 685, 695, 637),
    ("東芝 GR-A550FZ", 685, 695, 702),
    ("東芝 GR-W600FZS", 685, 695, 748),
    ("三菱電機 MR-WZ61N", 685, 695, 748),
    ("シャープ SJ-MF55R", 730, 740, 637),
    ("シャープ SJ-MF61R", 785, 795, 630),
]

# 最小設置幅が公表そのもの（本体幅+10の計算と一致はするが、出どころが公表）
PUBLISHED_MIN_W = {
    "シャープ SJ-MF51R": 695,
    "シャープ SJ-MF55R": 740,
    "シャープ SJ-MF61R": 795,
    "日立 R-HZC54Y": 660,
}


def main():
    errors = []
    both = []
    margin_both = []
    both_710 = []
    margin_710 = []
    depth_650 = []
    width_650 = []
    for name, body, min_w, depth in ROWS:
        if name in PUBLISHED_MIN_W:
            if min_w != PUBLISHED_MIN_W[name]:
                errors.append(f"{name}: 公表の最小設置幅が {PUBLISHED_MIN_W[name]} ではない")
        elif min_w != body + 10:
            errors.append(f"{name}: 最小設置幅 {min_w} != 本体幅+10")
        margin = min_w + 10
        if min_w <= 700 and depth <= 650:
            both.append(name)
        if margin <= 700 and depth <= 650:
            margin_both.append(name)
        if min_w <= 700 and depth <= 710:
            both_710.append(name)
        if margin <= 700 and depth <= 710:
            margin_710.append(name)
        if depth <= 650:
            depth_650.append(name)
        if min_w <= 650:
            width_650.append(name)
        # 記事の表と同じ余り
        expect = {
            "Panasonic NR-C37WS2": (40, 90, 50, 620, 80),
            "シャープ SJ-MF51R": (-45, 5, 13, 705, -5),
            "日立 R-HZC54Y": (-10, 40, -49, 670, 30),
        }
        if name in expect:
            got = (650 - min_w, 700 - min_w, 650 - depth, margin, 700 - margin)
            if got != expect[name]:
                errors.append(f"{name}: 余り {got} != {expect[name]}")

    checks = [
        (len(ROWS), 11, "機種数"),
        (len(both), 2, "幅700×奥行650"),
        (tuple(both), ("Panasonic NR-C37WS2", "シャープ SJ-MF51R"), "入る型番"),
        (len(margin_both), 1, "余裕込みで幅700×奥行650"),
        (margin_both, ["Panasonic NR-C37WS2"], "余裕込みの型番"),
        (len(both_710), 6, "幅700×奥行710"),
        (len(margin_710), 3, "余裕込みで幅700×奥行710"),
        (len(depth_650), 4, "奥行650以下"),
        (len(width_650), 1, "幅650以下"),
        (710 - 709, 1, "MR-WZ55Nの奥行710余り"),
    ]
    for got, want, label in checks:
        if got != want:
            errors.append(f"{label}: {got} != {want}")

    text = pathlib.Path("site/content/articles/fridge-niche-width-depth-fit.md").read_text(encoding="utf-8")
    for token in ("610", "620", "600", "40", "90", "50", "695", "705", "637", "5", "13",
                  "660", "670", "699", "-49", "740", "702", "2機種", "1機種"):
        if token not in text:
            errors.append(f"原稿に無い: {token}")

    if errors:
        print("\n".join(errors))
        return 1
    print("article-41 OK", len(ROWS), "models;", "700x650", both)
    return 0


if __name__ == "__main__":
    sys.exit(main())
