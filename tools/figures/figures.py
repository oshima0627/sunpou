# -*- coding: utf-8 -*-
"""図版の中身。1関数 = 1スライド = 1枚の PNG。

各関数は **図に書いた数値トークンの集合** を返す。build.py がそれを元の SVG と
突き合わせて、**手で打ち直したときの転記ミスを機械で捕まえる**
（元の SVG に無い数字が出たら、根拠のない数字か打ち間違い）。

⚠️ **ここに無い図は、まだ SVG 由来の PNG のまま。** 移行は1枚ずつ進める。
   `tools/svg-to-png.py` が焼いたものが残っているので、サイトは常に完全な状態を保つ。
"""
from pptx.enum.text import PP_ALIGN

from deck import (BAND, BG, HILI, INK, INNER, M, MUTE, NAVY, NAVY2, PALE, PALE2,
                  RULE, W, WHITE)


# ---------------------------------------------------------------- 脚立：設置奥行

SECCHI = [
    # 製品名, しまうとき(cm), 広げたとき(cm), 倍率
    ("長谷川 SE-3a",         18.0,  31,  1.7),
    ("長谷川 SE-8a",         18.0,  66,  3.7),
    ("長谷川 RHB-18a",       17.0, 108,  6.4),
    ("長谷川 EFA-11",         9.6, 104, 10.8),
    ("アルインコ PRT-360FX", 17.2, 250, 14.5),
]


def kyatatsu_secchi_eyecatch(f):
    f.header("広げると、奥行が最大14.5倍になります",
             "濃い色がしまうとき、薄い色が広げたとき。メーカー公表の寸法から計算",
             key="14.5", key_label="いちばん差が大きい", key_unit="倍")

    scale = 640 / 250.0
    x0, barh = 386, 38
    top_i = max(range(len(SECCHI)), key=lambda i: SECCHI[i][3])
    ys = f.rows(len(SECCHI), top=186, rh=72, highlight=top_i)

    for (name, shut, opened, ratio), y in zip(SECCHI, ys):
        by = y + (72 - 8 - barh) / 2
        ow, sw = opened * scale, shut * scale
        f.bar(x0, by, ow, barh, PALE2, PALE, NAVY, 2, radius=0.22)
        f.bar(x0, by, sw, barh, NAVY2, NAVY, None, radius=0.30)
        f.text(74, y + 12, 280, 26, name, 19, INK, bold=True)
        f.text(74, y + 38, 280, 22, f"{shut:g}cm → {opened}cm", 15, MUTE)
        f.text(x0 + ow + 16, by, 130, barh, f"{ratio}倍", 24, NAVY, bold=True)

    f.footer("薄くしまえるものほど、広げたときの差が大きくなります。")


def kyatatsu_secchi(f):
    """RHB-18a を上から見た図。幅は変わらず奥行だけが伸びることを面で見せる。"""
    f.header("広げても幅は変わりません",
             "長谷川工業 RHB-18a を上から見た図。伸びるのは奥行だけ",
             key="6.4", key_label="奥行だけが", key_unit="倍")

    scale = 2.6                      # 1cm = 2.6px
    wcm, shut, opened = 62, 17, 108
    bw = wcm * scale
    top = 212
    sh_h, op_h = shut * scale, opened * scale

    # しまうとき（後ろに「広げるとここまで」の破線を敷いて、伸びしろを面で見せる）
    # ⚠️ 寸法の行は**図の上**に置く。下に置くと破線の内側に入って重なる（2026-09-01 に実際に重なった）
    f.text(120, top - 54, 300, 24, "しまうとき", 19, INK, bold=True)
    f.text(120, top - 28, 300, 22, f"幅 {wcm}cm × 奥行 {shut}cm", 16, MUTE)
    f.ghost(120, top, bw, op_h)
    f.bar(120, top, bw, sh_h, NAVY2, NAVY, None, radius=0.10)
    f.text(120, top + op_h + 14, 320, 22, "破線まで広がります", 15, NAVY, bold=True)

    # 広げたとき
    f.text(430, top - 54, 300, 24, "広げたとき", 19, INK, bold=True)
    f.text(430, top - 28, 300, 22, f"幅 {wcm}cm × 奥行 {opened}cm", 16, MUTE)
    f.bar(430, top, bw, op_h, PALE2, PALE, NAVY, 2, radius=0.04)

    # 右の説明
    px, py = 700, 224
    f.rect(px - 20, py - 26, 436, 142, BAND, radius=0.06)
    f.text(px, py, 400, 26, "奥行だけが伸びます", 21, INK, bold=True)
    f.text(px, py + 32, 400, 24, f"{shut}cm → {opened}cm（6.4倍）", 17, NAVY, bold=True)
    f.text(px, py + 62, 400, 24, f"幅は {wcm}cm のまま変わりません", 17, MUTE)

    card = f.rect(px - 20, py + 142, 436, 122, WHITE, PALE, 2, radius=0.06)
    f.shadow(card, blur=14, dist=3, alpha=0.10)
    f.text(px, py + 162, 400, 24, "いちばん差が大きいのは", 16, MUTE)
    f.text(px, py + 190, 400, 26, "アルインコ PRT-360FX", 20, INK, bold=True)
    f.text(px, py + 220, 400, 24, "17.2cm → 250cm（14.5倍）", 17, NAVY, bold=True)

    f.footer("しまう場所と広げる場所は、別々に測ってください。",
             "薄くしまえることと、狭い場所で使えることは別の話です。")


ORDER = [
    "kyatatsu-secchi-eyecatch",
    "kyatatsu-secchi",
]

FIGURES = {
    "kyatatsu-secchi-eyecatch": kyatatsu_secchi_eyecatch,
    "kyatatsu-secchi": kyatatsu_secchi,
}
