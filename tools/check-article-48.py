# -*- coding: utf-8 -*-
"""記事48の脚外寸と内寸640mmの余りを、一次寸法から独立に再計算する。"""
import pathlib
import sys

ARTICLE = pathlib.Path("site/content/articles/washer-drum-foot-inner-640.md")
INNER = 640

# 幅, 奥行 or None, 幅条件 or None, 奥行条件
ROWS = [
    ("LX129", 584, 514, 590, 540),
    ("LX125", 584, 514, 590, 540),
    ("LX123", 584, 514, 590, 540),
    ("SX", 584, 510, 590, 540),
    ("SD", 584, 510, 590, 540),
    ("ES7", 569, 483, None, 540),
    ("ESX", 572, 501, None, 540),
    ("ES8", 580, None, None, 540),
    ("ES10", 580, None, None, 540),
    ("TOSH", 578, 512, 580, 520),
    ("HIT", 576, 539, None, 540),
]


def main():
    errors = []
    text = ARTICLE.read_text(encoding="utf-8")

    def need(value, label):
        if str(value) not in text:
            errors.append(f"{label} {value} が本文に無い")

    width_fit = 0
    depth_rows = 0
    depth_fit = 0
    width_rem = []
    depth_rem = []
    for name, w, d, cw, cd in ROWS:
        wr = INNER - w
        width_rem.append(wr)
        need(wr, f"{name} 幅余り")
        if wr >= 0:
            width_fit += 1
        if d is not None:
            dr = INNER - d
            depth_rem.append(dr)
            depth_rows += 1
            need(dr, f"{name} 奥行余り")
            if dr >= 0:
                depth_fit += 1
        if cw is not None:
            need(cw - w, f"{name} 条件-幅")
        if cd is not None and d is not None:
            need(cd - d, f"{name} 条件-奥行")

    if width_fit != 11 or len(ROWS) != 11:
        errors.append(f"幅の行数 {len(ROWS)} 入り {width_fit}")
    if depth_rows != 9 or depth_fit != 9:
        errors.append(f"奥行の行 {depth_rows} 入り {depth_fit}")
    if min(width_rem) != 56 or max(width_rem) != 71:
        errors.append(f"幅余り {min(width_rem)}..{max(width_rem)}")
    if min(depth_rem) != 101 or max(depth_rem) != 157:
        errors.append(f"奥行余り {min(depth_rem)}..{max(depth_rem)}")

    expect = {
        "pana幅差": 590 - 584,
        "lx奥行差": 540 - 514,
        "sx奥行差": 540 - 510,
        "条件50": 640 - 590,
        "東芝幅差": 580 - 578,
        "東芝奥行差": 520 - 512,
        "ES7差": 540 - 483,
        "ESX差": 540 - 501,
        "日立差": 540 - 539,
        "台枠和": 12 + 576 + 12,
        "cm脚幅": int(round(57.8 * 10)),
        "cm脚奥": int(round(51.2 * 10)),
        "58cm": int(58 * 10),
        "52cm": int(52 * 10),
        "57cm": int(57 * 10),
        "54cm": int(54 * 10),
        "S差": 547 - 540,
        "S余り": 640 - 547,
        "R余り": 640 - 510,
    }
    for label, value in expect.items():
        if value != int(value):
            errors.append(f"{label} が整数でない")
        need(int(value), label)

    if 57.8 * 10 != 578 or 51.2 * 10 != 512:
        errors.append("cm換算")

    for token in ("56mm", "60mm", "62mm", "64mm", "68mm", "71mm", "101mm", "157mm"):
        if token not in text.replace(" ", "").replace("　", ""):
            errors.append(f"単位つき {token} が無い")

    if errors:
        print("NG")
        for e in errors:
            print(" -", e)
        return 1
    print("OK", len(ROWS), "rows", "width", min(width_rem), max(width_rem), "depth", min(depth_rem), max(depth_rem))
    return 0


if __name__ == "__main__":
    sys.exit(main())
