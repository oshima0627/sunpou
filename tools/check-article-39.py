# -*- coding: utf-8 -*-
"""記事39（/washer/lixil-panasonic-pan-inner-depth/）の計算値を独立に出し直す。
データは一次（LIXIL取付説明書の各部寸法表、PF-6464AC/FW1参考図面、
パナソニック設置ページの外寸・内寸）。取得 2026-10-22。
python3 tools/check-article-39.py"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

# 製品, 外形幅, 外形奥行, 外形高さ, 内寸幅, 内寸奥行, 縁の出（LIXILのみ。Noneは未掲載）
PANS = [
    ("LIXIL PF-6464AC", 640, 640, 55, 618, 618, 11),
    ("LIXIL PF-7464AC", 740, 640, 55, 718, 618, 11),
    ("LIXIL PF-8064AC", 800, 640, 82, 744, 584, 28),
    ("LIXIL PF-9064", 900, 640, 82, 820, 560, 40),
    ("LIXIL PF-9375", 930, 750, 82, 870, 690, 30),
    ("Panasonic GB724", 640, 640, 55, 590, 590, None),
    ("Panasonic GB745", 740, 640, 55, 690, 590, None),
    ("Panasonic GB73", 800, 640, 55, 744, 584, None),
    ("Panasonic GB731", 900, 640, 50, 850, 590, None),
    ("Panasonic GB605J", 640, 640, 50, 596, 596, None),
]
CONDS = (540, 550, 570)
WIDTH = 590

print("製品 | 縁の検算 | 奥行−540 | −550 | −570 | 幅−590")
for name, ow, od, oh, iw, idp, e in PANS:
    rim_w = (ow - iw) / 2
    rim_d = (od - idp) / 2
    if e is None:
        rim = "未掲載"
    else:
        ok = rim_w == e and rim_d == e
        rim = f"{rim_w:g} {'OK' if ok else 'NG'}"
    diffs = [idp - c for c in CONDS]
    print(f"{name} | {rim} | {diffs[0]} | {diffs[1]} | {diffs[2]} | {iw - WIDTH}")

pairs = [
    ("640", "LIXIL PF-6464AC", "Panasonic GB724"),
    ("740", "LIXIL PF-7464AC", "Panasonic GB745"),
    ("800", "LIXIL PF-8064AC", "Panasonic GB73"),
    ("900", "LIXIL PF-9064", "Panasonic GB731"),
]
by = {r[0]: r for r in PANS}
print("\n呼び名 | LIXIL内寸奥行 | Panasonic内寸奥行 | 差 | 高さ差")
for label, a, b in pairs:
    da, db = by[a][5], by[b][5]
    ha, hb = by[a][3], by[b][3]
    print(f"{label} | {da} | {db} | {da - db} | {ha - hb}")

print("\nLIXIL 640→900 の内寸奥行差", 618 - 560)
print("Panasonic 640→800 の内寸奥行差", 590 - 584)

# PF-6464 参考図面
print("\nPF-6464 参考図面")
for label, n in (("各部寸法表", 618), ("参考値600", 600), ("参考値587", 587)):
    print(f"{label} | {n} | 618との差 {618 - n} | 590との差 {n - 590}")
print("20+600+20", 20 + 600 + 20)
