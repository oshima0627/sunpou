# -*- coding: utf-8 -*-
"""記事47の、辺 − 薪の長さ を独立に再計算する。

40cm は DOD とキャプテンスタッグが書いた長さ。15cm はロゴス薪の公表長さ。
収まるは 辺 >= 薪。余り0を含む。板厚は引かない。
長い辺は横の2辺の大きい方。円は直径を両方に使う。
"""
import pathlib
import sys

# (名前, 長い辺mm, 短い辺mm)
PITS = [
    ("スノーピーク 焚火台S ST-031R", 285, 285),
    ("スノーピーク 焚火台M ST-033R", 350, 350),
    ("スノーピーク 焚火台L ST-032RS", 455, 455),
    ("スノーピーク 焚火台LL ST-034", 633, 633),
    ("ロゴス ピラミッドTAKIBI M 81064163", 360, 350),
    ("ロゴス ピラミッドTAKIBI L 81064162", 390, 385),
    ("ロゴス ピラミッドTAKIBI XL 81064161", 535, 525),
    ("ユニフレーム ファイアグリル 683040", 430, 430),
    ("コールマン ファイアーディスク 2000031235", 450, 450),
    ("コールマン ファイアーディスクソロ 2000037404", 300, 300),
    ("DOD ヒコタン Q2-013-BK", 400, 400),
    ("キャプテンスタッグ シェル ファイアピット UG-91", 400, 400),
    ("DOD ぺらもえファイヤー Q1-946-SL", 320, 140),
    ("DOD すけもえファイヤー Q3-998-SL", 505, 150),
    ("DOD すけもえファイヤー2 Q3-091-SL", 490, 150),
    ("キャプテンスタッグ ソロ ライトグリル UG-93", 415, 240),
]

ARTICLE = pathlib.Path("site/content/articles/fire-pit-wood-length-fit.md")


def cm(mm):
    x = mm / 10.0
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.1f}"


def bucket(wood):
    gt = eq = lt = 0
    for _, long, short in PITS:
        d = (long if wood[0] == "L" else short) - wood[1]
        if d > 0:
            gt += 1
        elif d == 0:
            eq += 1
        else:
            lt += 1
    return gt, eq, lt


def main():
    errors = []
    if len(PITS) != 16:
        errors.append(f"機種数 {len(PITS)}")
    text = ARTICLE.read_text(encoding="utf-8")

    # 40cm。長い辺 8正・2ゼロ・6出る。短い辺 5正・2ゼロ・9出る。
    if bucket(("L", 400)) != (8, 2, 6):
        errors.append(f"40長い {bucket(('L', 400))}")
    if bucket(("S", 400)) != (5, 2, 9):
        errors.append(f"40短い {bucket(('S', 400))}")
    # 15cm。長い辺は16機種とも正。短い辺は13正・2ゼロ・1出る。
    if bucket(("L", 150)) != (16, 0, 0):
        errors.append(f"15長い {bucket(('L', 150))}")
    if bucket(("S", 150)) != (13, 2, 1):
        errors.append(f"15短い {bucket(('S', 150))}")

    by = {n: (L, S) for n, L, S in PITS}
    expect = {
        "スノーピーク 焚火台S ST-031R": (-115, -115),
        "スノーピーク 焚火台M ST-033R": (-50, -50),
        "スノーピーク 焚火台L ST-032RS": (55, 55),
        "スノーピーク 焚火台LL ST-034": (233, 233),
        "ロゴス ピラミッドTAKIBI L 81064162": (-10, -15),
        "DOD ヒコタン Q2-013-BK": (0, 0),
        "キャプテンスタッグ シェル ファイアピット UG-91": (0, 0),
        "DOD ぺらもえファイヤー Q1-946-SL": (-80, -260),
        "DOD すけもえファイヤー Q3-998-SL": (105, -250),
        "DOD すけもえファイヤー2 Q3-091-SL": (90, -250),
        "キャプテンスタッグ ソロ ライトグリル UG-93": (15, -160),
        "コールマン ファイアーディスクソロ 2000037404": (-100, -100),
    }
    for name, (dl, ds) in expect.items():
        L, S = by[name]
        if (L - 400, S - 400) != (dl, ds):
            errors.append(f"{name} 40cm {(L - 400, S - 400)} != {(dl, ds)}")
        for label, mm in (("長い", L), ("短い", S)):
            token = cm(mm) + "cm"
            if token not in text.replace(" ", ""):
                errors.append(f"本文に辺が無い {name} {label} {token}")

    # ヒコタンの35cmとの余りは5cm（400-350）。
    if by["DOD ヒコタン Q2-013-BK"][0] - 350 != 50:
        errors.append("ヒコタンと35cm")

    # 板厚1.5mmを両側（3mm）引いても、Sは40cm未満、Lは40cm以上。
    if not (285 - 3 < 400 and 455 - 3 >= 400):
        errors.append("板厚を引いた判定")

    # 図の6本。長い辺から出る量。
    sticks = []
    for name, L, S in PITS:
        if L < 400:
            sticks.append((400 - L, name))
    sticks.sort(reverse=True)
    if [cm(d) for d, _ in sticks] != ["11.5", "10", "8", "5", "4", "1"]:
        errors.append(f"はみ出し順 {[cm(d) for d, _ in sticks]}")
    if len(sticks) != 6:
        errors.append(f"はみ出し機種 {len(sticks)}")

    for needle in ("7機種", "10機種", "6機種", "16機種", "11.5cm", "0cm", "5.5cm", "23.3cm"):
        if needle not in text.replace(" ", ""):
            errors.append(f"本文に無い {needle}")

    if errors:
        print("\n".join(errors))
        return 1
    print("ok 16機種 40cm長い 8/2/6 短い 5/2/9 15cm短い 13/2/1 はみ出し6")
    return 0


if __name__ == "__main__":
    sys.exit(main())
