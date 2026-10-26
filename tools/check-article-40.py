# -*- coding: utf-8 -*-
"""記事40（/washer/vertical-opening-height/）の計算値を独立に出し直す。
データは一次（東芝特長ページ・仕様、シャープ仕様の代替テキスト、
日立特長ページと仕様JSON、パナソニックのデザインページと仕様）。取得 2026-10-25。
python3 tools/check-article-40.py"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

# 製品, 総外形高さ, 手前, 奥行, 幅, 槽底（約。Noneは使わない）
TOSHIBA = [
    ("AW-12DPB6", 1098, 891, 357, 441, 554),
    ("AW-10DPB6", 1033, 826, 357, 441, 489),
    ("AW-10DHB6", 1033, 826, 357, 441, 489),
    ("AW-9DPB6", 1033, 831, 324, 409, 500),
    ("AW-8DPB6", 1033, 831, 324, 409, 500),
    ("AW-9DHB6", 1033, 831, 324, 409, 500),
    ("AW-8DHB6", 1033, 831, 324, 409, 500),
]
print("東芝 | 総外形−手前 | 12kgとの差 | 開口")
base_front = TOSHIBA[0][2]
for name, total, front, depth, width, tub in TOSHIBA:
    print(f"{name} | {total - front} | {base_front - front} | {depth}×{width} 槽{tub}")
fronts = [r[2] for r in TOSHIBA]
print("手前の範囲", min(fronts), max(fronts), "幅", max(fronts) - min(fronts))
print("12−10 手前", 891 - 826, "総外形", 1098 - 1033, "槽底", 554 - 489)
print("9−10 手前", 831 - 826, "差の差", 207 - 202)
print("開口 奥行", 357 - 324, "幅", 441 - 409)

# 製品, ボディ, ホース込, 投入口
SHARP = [
    ("ES-SW11L", 992, 1055, 893),
    ("ES-SW10L", 962, 1025, 863),
    ("ES-GV8L", 964, 1018, 860),
    ("ES-GV10L", 952, 1009, 860),
    ("ES-PT11L", 1019, 1050, 858),
    ("ES-TX8L", 980, 1025, 850),
]
print("\nシャープ | ホース込−投入口 | ボディ−投入口")
opens = []
drops = []
for name, body, hose, open_h in SHARP:
    opens.append(open_h)
    drops.append(hose - open_h)
    print(f"{name} | {hose - open_h} | {body - open_h}")
print("投入口の範囲", min(opens), max(opens), "幅", max(opens) - min(opens))
print("差の範囲", min(drops), max(drops))
print("SW 投入口差", 893 - 863, "ホース差", 1055 - 1025)
print("GV ホース差", 1018 - 1009, "差の差", 158 - 149)

print("\n日立の換算")
for name, height, cm in (
    ("BW-X100M", 1000, 85),
    ("BW-X90M", 1000, 85),
    ("BW-V100M", 1000, 85),
    ("BW-V80M", 930, 78),
):
    mm = cm * 10
    print(f"{name} | {cm}cm={mm}mm | 差 {height - mm}")
print("外形差", 1000 - 930, "槽の深さ差", 55 * 10 - 48 * 10)

print("\nパナソニック")
print("幅", 437 - 402, "奥行", 340 - 309, "H6奥行", 334 - 309, "前面", 91 - 85)
print("JFA−K6", 1075 - 1071, "12−K6高さ", 1086 - 1071)
print("東芝幅−パナ幅", 441 - 437, "東芝奥行−パナ奥行", 357 - 340)
