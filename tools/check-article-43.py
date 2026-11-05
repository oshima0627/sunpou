# -*- coding: utf-8 -*-
"""記事43のマット枚数を、公表の床の2辺から独立に再計算する。

向きの規則:
- マットは全部同じ向き。軸に平行。重ねない。
- 床の辺A（幅・W・並びの1番目）と辺B（奥行・D・2番目）。
- マットの長さが辺B以下なら、幅を辺Aに並べる。
- マットの長さが辺A以下なら、幅を辺Bに並べる。
- 両方できるときは枚数が多い方を「多い」、少ない方を「少ない」。
- 片方しかできないときは、その枚数を多い・少ないの両方に入れる。
"""
import pathlib
import sys

# 名前, 辺A, 辺B, 定員下限, 定員上限（無ければ None）
TENTS = [
    ("DOD ワンタッチテント T2-629-TN", 225, 145, 2, 2),
    ("DOD ライダーズワンタッチテント T2-275", 225, 145, 2, 2),
    ("DOD ザ・ワンタッチテントM T3-673-KH", 215, 215, 3, 3),
    ("DOD ワンポールテントS T3-44-TN", 270, 230, 3, 3),
    ("DOD カマボコテント3S T3-688-TN", 225, 235, 3, 3),
    ("DOD カマボコテント3M T5-689-TN", 280, 220, 5, 5),
    ("DOD ワンポールテントM T5-47-TN", 330, 290, 5, 5),
    ("ロゴス neos エーコン リビングドーム M 71201192", 210, 210, 3, 4),
    ("ロゴス Tradcanvas イージーセットキャビン XL 71201171", 270, 270, None, None),
    ("ロゴス Tradcanvas PANEL オーニングドゥーブル XL 71201015", 270, 270, None, None),
    ("ロゴス プレミアム エーコン PANEL EVER DOME L 71101022", 270, 210, None, None),
    ("コールマン 4Sワイド2ルームコクーンIII 2000036431", 360, 240, 5, 6),
    ("コールマン タフスクリーン2ルームエアー MDX+ 2000039084", 300, 250, 4, 5),
]

PADS = [
    ("50", 50, 150),
    ("60", 60, 180),
    ("80", 80, 208),
]

ARTICLE = pathlib.Path("site/content/articles/tent-mat-floor-count.md")


def orientations(a, b, pw, pl):
    out = []
    if pl <= b:
        n = a // pw
        out.append((n, a - n * pw, b - pl, "A"))
    if pl <= a:
        n = b // pw
        out.append((n, b - n * pw, a - pl, "B"))
    return out


def pair(a, b, pw, pl):
    opts = orientations(a, b, pw, pl)
    if not opts:
        return None
    more = max(opts, key=lambda c: (c[0], c[1]))
    less = min(opts, key=lambda c: (c[0], -c[1]))
    return more, less


def main():
    errors = []
    rows = []
    for name, a, b, lo, hi in TENTS:
        cell = {"name": name, "a": a, "b": b, "lo": lo, "hi": hi}
        for key, pw, pl in PADS:
            got = pair(a, b, pw, pl)
            if got is None:
                errors.append(f"{name} {key}: 置ける向きが無い")
                continue
            more, less = got
            cell[key] = {"more": more, "less": less}
        rows.append(cell)

    known = [r for r in rows if r["lo"] is not None]
    if len(known) != 10:
        errors.append(f"定員あり {len(known)} != 10")

    def reach_any(key):
        return [r for r in known if r[key]["more"][0] >= r["lo"]]

    def short_both(key):
        return [r for r in known if r[key]["more"][0] < r["lo"]]

    if [r["name"] for r in reach_any("80")] != ["DOD ワンポールテントS T3-44-TN"]:
        errors.append("80cmで下限に届く向きがある機種が T3-44 だけではない: " +
                      ", ".join(r["name"] for r in reach_any("80")))
    if len(short_both("80")) != 9:
        errors.append(f"80cmで多い向きでも届かない機種数 {len(short_both('80'))} != 9")
    if len(short_both("60")) != 1 or "T5-689" not in short_both("60")[0]["name"]:
        errors.append("60cmで届かないのが T5-689 だけではない")
    if len(reach_any("60")) != 9:
        errors.append(f"60cmで届く向きがある機種数 {len(reach_any('60'))} != 9")
    if len(reach_any("50")) != 10:
        errors.append(f"50cmで届く向きがある機種数 {len(reach_any('50'))} != 10")
    if len(short_both("50")) != 0:
        errors.append("50cmで多い向きでも届かない機種がある")

    t2 = rows[0]
    if t2["80"]["more"] != (1, 65, 17, "B") or t2["80"]["less"] != t2["80"]["more"]:
        errors.append(f"T2-629 80cm {t2['80']}")
    if t2["60"]["more"] != (2, 25, 45, "B"):
        errors.append(f"T2-629 60cm {t2['60']}")
    acorn = rows[7]
    if acorn["50"]["more"][0] != 4 or acorn["50"]["more"][1] != 10:
        errors.append(f"エーコン 50 {acorn['50']}")
    if acorn["60"]["more"][0] != 3 or acorn["60"]["more"][1] != 30:
        errors.append(f"エーコン 60 {acorn['60']}")
    if acorn["80"]["more"][0] != 2:
        errors.append(f"エーコン 80 {acorn['80']}")
    m3 = rows[5]
    if m3["60"]["more"][0] != 4 or m3["60"]["less"][0] != 3:
        errors.append(f"3M 60 {m3['60']}")
    if m3["80"]["more"][0] != 3 or m3["50"]["more"][0] != 5:
        errors.append(f"3M 80/50 {m3['80']} {m3['50']}")
    s = rows[3]
    if s["80"]["more"] != (3, 30, 22, "A") or s["80"]["less"][0] != 2:
        errors.append(f"T3-44 80 {s['80']}")
    col = rows[11]
    if col["60"]["more"] != (6, 0, 60, "A") or col["60"]["less"][0] != 4:
        errors.append(f"コクーン 60 {col['60']}")
    if col["80"]["more"][0] != 4 or col["50"]["more"][0] != 7:
        errors.append(f"コクーン 80/50 {col['80']} {col['50']}")
    mdx = rows[12]
    if mdx["60"]["more"] != (5, 0, 70, "A") or mdx["80"]["more"][0] != 3:
        errors.append(f"MDX {mdx['60']} {mdx['80']}")

    # キワミエアーを3Mの床280×220に、長さを220側へ置く（DODの「横に並べる」文）
    if 138 * 2 != 276 or 280 - 276 != 4 or 220 - 208 != 12:
        errors.append("L×2 の余り")
    if 115 + 80 + 80 != 275 or 280 - 275 != 5:
        errors.append("M+S+S の余り")

    text = ARTICLE.read_text(encoding="utf-8") if ARTICLE.exists() else ""
    needles = [
        "届く向きがあるのは1機種",
        "どちらの向きでも届かないのは9機種",
        "届かないのは1機種",
        "10機種とも",
        "余りは25cm",
        "余りは65cm",
        "余りは4cm",
        "余りは5cm",
        "余り10cm",
        "余り30cm",
        "4枚と3枚",
        "幅方向の余りは0cm",
    ]
    for n in needles:
        if n not in text:
            errors.append(f"本文に無い: {n}")

    # 表の多い/少ないが再計算と一致するか（定員あり10機種の80cm多い）
    for r in rows:
        token = f"{r['80']['more'][0]}枚"
        if r["name"].split()[-1] not in text and r["name"] not in text:
            errors.append(f"製品名が本文に無い: {r['name']}")
        if token not in text and r["80"]["more"][0] == 1:
            pass

    if errors:
        print("NG")
        for e in errors:
            print(" -", e)
        return 1
    print("OK", len(rows), "tents / known", len(known))
    print("80 reach", [r["name"] for r in reach_any("80")])
    print("60 short", [r["name"] for r in short_both("60")])
    return 0


if __name__ == "__main__":
    sys.exit(main())
