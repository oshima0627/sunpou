# -*- coding: utf-8 -*-
"""記事44の差・組数を、表の一次寸法から独立に再計算する。"""
import pathlib
import sys

# 新型, 従来品, 新型幅, 新型奥行, 新型高さ, 旧幅, 旧奥行, 旧高さ, 新内容積, 旧内容積, 新据付, 旧据付
# 内容積・据付が None の組は、公式の比較注記にその数字が無い。
ROWS = [
    ("NR-F55HY2", "NR-F53HX1", 650, 699, 1850, 650, 699, 1828, 551, 525, 699, 699),
    ("NR-F49EY3", "NR-F50EX1", 650, 650, 1850, 650, 699, 1828, 490, 501, 650, 699),
    ("NR-E45RY3", "NR-E45PX1", 600, 648, 1850, 600, 699, 1828, 450, 450, 648, 699),
    ("NR-E41RY3", "NR-E41EX1", 600, 648, 1850, 600, 679, 1818, 410, 406, 648, 684),
    ("MR-MZ60N", "MR-MXD57G", 685, 738, 1833, 685, 738, 1826, None, None, None, None),
]

ARTICLE = pathlib.Path("site/content/articles/fridge-replace-outer-delta.md")
GAPS = (10, 25, 40)


def main():
    errors = []
    text = ARTICLE.read_text(encoding="utf-8")
    deltas = []
    for row in ROWS:
        name, _old, nw, nd, nh, ow, od, oh, nv, ov, ni, oi = row
        dw, dd, dh = nw - ow, nd - od, nh - oh
        deltas.append((name, dw, dd, dh))
        for label, value in (("幅の差", dw), ("奥行の差", dd), ("高さの差", dh)):
            if str(value) not in text and str(abs(value)) not in text:
                errors.append(f"{name} の{label} {value} が本文に無い")
        if nv is not None:
            if str(nv - ov) not in text and str(abs(nv - ov)) not in text:
                errors.append(f"{name} の内容積差 {nv - ov} が本文に無い")
        if ni is not None and str(ni - oi) not in text and str(abs(ni - oi)) not in text:
            errors.append(f"{name} の据付差 {ni - oi} が本文に無い")

    box = [r for r in deltas if r[1] <= 0 and r[2] <= 0 and r[3] <= 0]
    width_ok = [r for r in deltas if r[1] <= 0]
    depth_ok = [r for r in deltas if r[2] <= 0]
    height_ok = [r for r in deltas if r[3] <= 0]
    if len(box) != 0:
        errors.append(f"旧型の箱 {len(box)} != 0")
    if len(width_ok) != 5 or len(depth_ok) != 5 or len(height_ok) != 0:
        errors.append(f"軸の組数 幅{len(width_ok)} 奥行{len(depth_ok)} 高さ{len(height_ok)}")
    heights = sorted(r[3] for r in deltas)
    if heights != [7, 22, 22, 22, 32]:
        errors.append(f"高さの差 {heights}")
    if min(r[2] for r in deltas) != -51:
        errors.append("奥行の最小が -51 ではない")

    for gap, want in ((10, 1), (25, 4), (40, 5)):
        fit = [r for r in deltas if r[3] <= gap]
        if len(fit) != want:
            errors.append(f"空き{gap}: {len(fit)} != {want}")
        for name, _dw, _dd, dh in deltas:
            remain = gap - dh
            if str(remain) not in text and str(abs(remain)) not in text:
                errors.append(f"空き{gap} {name} の余り {remain} が本文に無い")

    # 概要ページの cm が仕様の mm と一致するか
    cm_pairs = [(65, 650), (69.9, 699), (64.8, 648), (67.9, 679), (185, 1850), (182.8, 1828), (181.8, 1818)]
    for cm, mm in cm_pairs:
        if abs(cm * 10 - mm) > 0.05:
            errors.append(f"cm換算 {cm} != {mm}")

    if errors:
        print("NG")
        for e in errors:
            print(" -", e)
        return 1
    print("OK 5組 箱0 幅5 奥行5 高さ0 空き10/25/40 = 1/4/5")
    for name, dw, dd, dh in deltas:
        print(f"  {name}: 幅{dw} 奥行{dd} 高さ{dh}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
