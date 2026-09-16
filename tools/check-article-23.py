# -*- coding: utf-8 -*-
"""記事23「スーツケース40Lは何泊？」の検算。

各社が公表する「容量 ↔ 泊数」の目安を、取得した原文のまま並べ、
(1) 容量ごとに各社が何泊と言うか（早見表）
(2) 帯の境目から「1泊あたり何L」か
を独立に計算する。記事の表はこの出力と突き合わせる。

出典は docs/article-23-liter-nanpaku.md にある（2026-09-16 取得）。
"""
import io
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------- 社ごとの目安（原文の値）

# 容量帯 → 泊数。(下限L, 上限L, 泊の下限, 泊の上限, 原文)
ACE = [
    (0, 29, 1, 2, "-29L (1-2泊)"),
    (30, 49, 2, 3, "30-49L (2-3泊)"),
    (50, 59, 3, 5, "50-59L (3-5泊)"),
    (60, 79, 5, 7, "60-79L (5-7泊)"),
    (80, 99, 7, 10, "80-99L (7-10泊)"),
    (100, 999, 10, None, "100L- (10泊-)"),
]
LEGEND = [
    (0, 26, 0, 1, "日帰り～1泊 26L以下"),
    (27, 41, 1, 2, "1泊～2泊 27~41L"),
    (42, 59, 3, 5, "3泊～5泊 42~59L"),
    (60, 79, 5, 7, "5泊～7泊 60~79L"),
    (80, 99, 7, None, "7泊以上 80~99L"),
    (100, 999, 10, None, "10泊以上 100L~"),
]
# サムソナイト：「1泊＝10リットル」＋ 帯（4～6泊 50-70リットル台／1週間以上 80リットル以上／
# 小型 40リットル以下＝短期旅行・出張／機内持込＝1～3泊）
SAMSONITE_PER_NIGHT = 10.0
# 無印良品（読みもの）：泊数 → 容量
MUJI = [
    (1, 1, 20, 30, "1泊なら20～30L"),
    (2, 2, 30, 40, "2泊なら30～40L"),
    (3, 3, 40, 50, "3泊なら40～50L"),
    (4, None, 40, 60, "4泊以上 40～60L"),
]
# 製品ごと：(容量L, 泊の下限, 泊の上限, 原文)
NITORI = [
    (33, 1, 2, "1～2泊の短期旅行や出張に最適"),
    (38, 1, 2, "出張や1～2泊の短期旅行"),
    (40, 2, 3, "2～3泊程度の短期旅行やビジネス出張"),
    (60, 4, 6, "4～6泊程度の中長期旅行や出張"),
]
RIMOWA = [
    (36, 3, 4, "3～4日のご旅行に理想的"),      # Essential キャビン（「日」表記）
    (37, 3, 4, "3～4泊のご旅行に最適"),        # Hybrid キャビン
    (46, 4, 5, "4～5泊の旅行に最適"),          # Essential Sleeve キャビン プラス
    (60, 7, 7, "1 週間の旅行に理想的"),        # Essential チェックイン M
    (85, 14, 15, "14～15日のご旅行に理想的"),  # Essential チェックイン L
    (101, 14, None, "2週間以上のご旅行に理想的"),  # Essential トランク プラス
]
MUJI_PRODUCTS = [  # ブランドページ「選べるサイズ」
    (19, 1, 2), (35, 2, 3), (62, 5, 6), (87, 7, 8), (104, 9, 10),
]


def fmt(lo, hi):
    if hi is None:
        return f"{lo}泊以上"
    if lo == hi:
        return f"{lo}泊"
    return f"{lo}〜{hi}泊"


def band(table, liters):
    for lo, hi, nlo, nhi, _ in table:
        if lo <= liters <= hi:
            return fmt(nlo, nhi)
    return "—"


def muji_guide(liters):
    hits = [fmt(nlo, nhi) for nlo, nhi, llo, lhi, _ in MUJI if llo <= liters <= lhi]
    return " / ".join(hits) if hits else "—"


def nearest(products, liters, tol=2):
    hits = [(cap, fmt(nlo, nhi)) for cap, nlo, nhi, *_ in products if abs(cap - liters) <= tol]
    return " / ".join(f"{cap}L:{n}" for cap, n in hits) if hits else "—"


# ---------------------------------------------------------------- (1) 早見表
out = []
out.append("## 早見表（容量 → 各社の泊数）")
out.append("| L | ace | Legend Walker | Samsonite(10L/泊) | 無印(読みもの) | 無印(製品±2L) | ニトリ(製品±2L) | RIMOWA(製品±2L) |")
for L in (20, 30, 36, 40, 45, 50, 60, 70, 75, 85, 100):
    out.append(f"| {L} | {band(ACE, L)} | {band(LEGEND, L)} | {L / SAMSONITE_PER_NIGHT:g}泊 | "
               f"{muji_guide(L)} | {nearest(MUJI_PRODUCTS, L)} | {nearest(NITORI, L)} | {nearest(RIMOWA, L)} |")

# ---------------------------------------------------------------- (2) 1泊あたり何L
out.append("")
out.append("## 1泊あたりの容量（帯の境目・製品の値から）")
out.append("式: L/泊 = 容量 ÷ 泊数。帯は「帯の下限 ÷ 泊の下限」と「帯の上限 ÷ 泊の上限」で幅を出す")


def per_night_band(name, table):
    rows = []
    for lo, hi, nlo, nhi, src in table:
        if nlo == 0 or nhi is None:
            continue
        a = lo / nlo
        b = hi / nhi
        rows.append(f"| {name} | {src} | {min(a, b):.1f}〜{max(a, b):.1f} |")
    return rows


out.append("| 社 | 帯 | L/泊 |")
out += per_night_band("ace", ACE)
out += per_night_band("Legend Walker", LEGEND)
for nlo, nhi, llo, lhi, src in MUJI:
    if nhi is None:
        continue
    out.append(f"| 無印良品 | {src} | {llo / nlo:.1f}〜{lhi / nhi:.1f} |")
for cap, nlo, nhi, src in NITORI:
    out.append(f"| ニトリ {cap}L | {src} | {cap / nhi:.1f}〜{cap / nlo:.1f} |")
for cap, nlo, nhi, src in RIMOWA:
    hi = cap / nlo
    lo = cap / nhi if nhi else None
    out.append(f"| RIMOWA {cap}L | {src} | {'' if lo is None else f'{lo:.1f}〜'}{hi:.1f}{'' if lo is not None else ' 以下'} |")

# ---------------------------------------------------------------- (3) 記事で使う要点
out.append("")
out.append("## 記事の要点（この出力から転記する）")
r40 = {"ace": band(ACE, 40), "LW": band(LEGEND, 40), "Sams": f"{40 / SAMSONITE_PER_NIGHT:g}泊",
       "MUJI": muji_guide(40), "Nitori": nearest(NITORI, 40, 0), "RIMOWA": nearest(RIMOWA, 40, 4)}
out.append(f"40L: {r40}")
r60 = {"ace": band(ACE, 60), "LW": band(LEGEND, 60), "Sams": f"{60 / SAMSONITE_PER_NIGHT:g}泊",
       "MUJI": nearest(MUJI_PRODUCTS, 60, 2), "Nitori": nearest(NITORI, 60, 0), "RIMOWA": nearest(RIMOWA, 60, 0)}
out.append(f"60L: {r60}")
r100 = {"ace": band(ACE, 100), "LW": band(LEGEND, 100), "Sams": f"{100 / SAMSONITE_PER_NIGHT:g}泊",
        "MUJI": nearest(MUJI_PRODUCTS, 100, 4), "RIMOWA": nearest(RIMOWA, 100, 1)}
out.append(f"100L: {r100}")
# 境目の点を結ぶ直線（ace: 50L=3泊, 100L=10泊 / LW: 42L=3泊, 100L=10泊）
for name, p1, p2 in (("ace", (3, 50), (10, 100)), ("Legend Walker", (3, 42), (10, 100))):
    slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
    icpt = p1[1] - slope * p1[0]
    out.append(f"{name}: 帯の境目 {p1[1]}L={p1[0]}泊 と {p2[1]}L={p2[0]}泊 を結ぶと "
               f"傾き {slope:.1f}L/泊, 切片 {icpt:.1f}L")
out.append("無印良品: 1泊 20〜30L → 2泊 30〜40L → 3泊 40〜50L: 1泊増えるごとに +10L, 切片 10〜20L")
out.append(f"サムソナイト: 1泊＝{SAMSONITE_PER_NIGHT:g}L, 切片 0L")

text = "\n".join(out)
print(text)
io.open("docs/article-23-check-output.md", "w", encoding="utf-8").write(text + "\n")


# ---------------------------------------------------------------- (4) 当てはめ：容量 ≈ 10L×泊数 ＋ 10〜20L
# 無印良品の読みもの（1泊 20〜30L → 1泊増えるごとに +10L）をそのまま式にしたもの。
# 他社の帯がこの式の範囲に入るかを見る。判定は「社の帯の上下限が、式の上下限の内側か」。
def fit(nlo, nhi):
    return 10 * nlo + 10, 10 * nhi + 20


rows = []
for name, table in (("ace", ACE), ("Legend Walker", LEGEND)):
    for lo, hi, nlo, nhi, src in table:
        if nlo == 0 or nhi is None:
            continue
        flo, fhi = fit(nlo, nhi)
        ok = flo <= lo and hi <= fhi
        rows.append(f"| {name} | {src} | {flo}〜{fhi}L | {'○' if ok else '×'} |")
for cap, nlo, nhi, src in NITORI:
    flo, fhi = fit(nlo, nhi)
    rows.append(f"| ニトリ {cap}L | {fmt(nlo, nhi)} | {flo}〜{fhi}L | {'○' if flo <= cap <= fhi else '×'} |")
for cap, nlo, nhi, src in RIMOWA:
    if nhi is None:
        continue
    flo, fhi = fit(nlo, nhi)
    rows.append(f"| RIMOWA {cap}L | {src} | {flo}〜{fhi}L | {'○' if flo <= cap <= fhi else '×'} |")
for cap, nlo, nhi in MUJI_PRODUCTS:
    flo, fhi = fit(nlo, nhi)
    rows.append(f"| 無印良品 {cap}L | {fmt(nlo, nhi)} | {flo}〜{fhi}L | {'○' if flo <= cap <= fhi else '×'} |")
# サムソナイトの帯：4～6泊 50-70リットル台（=50〜79）, 1週間以上 80L以上
for lo, hi, nlo, nhi, src in ((50, 79, 4, 6, "4～6泊 50-70リットル台"),):
    flo, fhi = fit(nlo, nhi)
    rows.append(f"| Samsonite | {src} | {flo}〜{fhi}L | {'○' if flo <= lo and hi <= fhi else '×'} |")

extra = ["", "## 当てはめ：容量 ≈ 10L×泊数 ＋ 10〜20L（無印良品の読みものを式にしたもの）",
         "| 社 | 目安 | 式の範囲 | 入るか |"] + rows
print("\n".join(extra))
io.open("docs/article-23-check-output.md", "a", encoding="utf-8").write("\n".join(extra) + "\n")
