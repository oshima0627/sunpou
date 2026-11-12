# -*- coding: utf-8 -*-
"""記事45の、天板高 − 座面高 を独立に再計算する。

帯は 25 以上 30 以下。コールマン公式の例（座面40cmなら天板65cmと70cm）が
差25cmと30cmなので、両端を含む。
座面15段 × 天板9段 = 135通り。
"""
import pathlib
import sys

SEATS = [
    ("レイチェア LOW", 27),
    ("レイチェア LOW FLAT", 24),
    ("レイチェア MID", 38),
    ("レイチェア MID FLAT", 36),
    ("レイチェア HIGH", 43),
    ("レイチェア HIGH FLAT", 42),
    ("ヒーリング", 41),
    ("スゴイッス 焚き火", 18),
    ("スゴイッス ロー", 32),
    ("スゴイッス 星空", 36),
    ("スゴイッス ミドル", 37),
    ("スゴイッス ディナー", 38),
    ("スゴイッス ハイ", 42),
    ("バックアシスト", 43),
    ("ローチェア30", 30),
]

TABLES = [
    ("バタフライ70", 70),
    ("バタフライ60", 60),
    ("バタフライ41", 41),
    ("オサマリー82", 82),
    ("オサマリー64", 64),
    ("オサマリー56", 56),
    ("オサマリー38", 38),
    ("2FD70", 70),
    ("2FD50", 50),
]

COLEMAN_SEATS = SEATS[:7]
COLEMAN_TABLES = TABLES[:3]

ARTICLE = pathlib.Path("site/content/articles/camp-chair-seat-table-gap.md")


def in_band(table, seat):
    return 25 <= table - seat <= 30


def main():
    errors = []
    if len(SEATS) != 15 or len(TABLES) != 9:
        errors.append(f"段数 {len(SEATS)}×{len(TABLES)}")
    pairs = [(sn, s, tn, t, t - s) for sn, s in SEATS for tn, t in TABLES]
    if len(pairs) != 135:
        errors.append(f"通り数 {len(pairs)}")
    ins = [p for p in pairs if in_band(p[3], p[1])]
    if len(ins) != 20:
        errors.append(f"帯に入る {len(ins)} != 20")
    neg = [p for p in pairs if p[4] < 0]
    eq = [p for p in pairs if p[4] == 0]
    low = [p for p in pairs if 1 <= p[4] <= 24]
    high = [p for p in pairs if p[4] >= 31]
    if (len(neg), len(eq), len(low), len(high)) != (9, 3, 57, 46):
        errors.append(f"分布 neg={len(neg)} eq={len(eq)} low={len(low)} high={len(high)}")
    if len(neg) + len(eq) + len(low) + len(ins) + len(high) != 135:
        errors.append("分布の合計が135ではない")

    own = [(sn, s, tn, t, t - s) for sn, s in COLEMAN_SEATS for tn, t in COLEMAN_TABLES]
    if len(own) != 21:
        errors.append(f"コールマン同士 {len(own)}")
    own_in = [p for p in own if in_band(p[3], p[1])]
    if len(own_in) != 3:
        errors.append(f"コールマン同士で入る {len(own_in)}")
    if any(p[3] != 70 for p in own_in):
        errors.append("コールマン同士で入るのに天板70以外がある")

    # カテゴリページの端
    ends = [(40, 65, 25), (40, 70, 30), (30, 30, 0), (30, 35, 5), (30, 40, 10)]
    for seat, table, diff in ends:
        if table - seat != diff:
            errors.append(f"端 {seat} {table}")

    # バタフライのローを40cmにしても、15段では帯に入らない
    if any(in_band(40, s) for _, s in SEATS):
        errors.append("天板40cmで帯に入る段がある")
    if 41 - 18 != 23 or 40 - 18 != 22:
        errors.append("焚き火18cmとの差")

    # 境界の1cm
    if 56 - 32 != 24:
        errors.append("スゴイッスローとオサマリー56")
    if 64 - 42 != 22:
        errors.append("スゴイッスハイとオサマリー64")
    if 70 - 38 != 32:
        errors.append("MIDと天板70")

    text = ARTICLE.read_text(encoding="utf-8") if ARTICLE.exists() else ""
    needles = [
        "135通り",
        "20通り",
        "21通り",
        "3通り",
        "差は27cm",
        "差は29cm",
        "差は26cm",
        "差は24cm",
        "差は22cm",
        "差は14cm",
        "差は11cm",
        "差は10cm",
        "差は0cm",
        "9通り",
        "0通り",
        "5通り",
        "2通り",
        "1通り",
        "未掲載",
        "未検証",
        "直リンクは載せていません",
    ]
    for n in needles:
        if n not in text:
            errors.append(f"本文に無い: {n}")
    for sn, s, tn, t, d in ins:
        if str(d) not in text:
            errors.append(f"入る差が本文に無い: {sn} {tn} {d}")

    if errors:
        print("NG")
        for e in errors:
            print(" -", e)
        return 1
    print("OK", len(pairs), "pairs / in", len(ins), "/ coleman", len(own_in))
    return 0


if __name__ == "__main__":
    sys.exit(main())
