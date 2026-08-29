# -*- coding: utf-8 -*-
"""記事19（カセットコンロの選び方）の数値を、一次情報から再計算して突き合わせる。

データ源：
  コンロ11機種 … 岩谷産業 カセットこんろ 各製品ページ／`/function/` の商品スペック
                 https://www.iwatani.co.jp/jpn/consumer/products/cg/stove/
  土鍋18製品  … 銀峯陶器 公式オンラインショップ（docs/article-07-donabe-konro.md に収集済み）
  ボンベ      … イワタニカセットガス CB-250S-OR（250g）／ジュニア CB-JR-120S（120g）

使い方: python tools/check-konro-erabikata.py
記事に書いた数値は、すべてこのスクリプトが出した値と一致していること。
"""
import io
import re
import sys
import os

# ---- 一次情報：イワタニ カセットフー 11機種 -------------------------------
# (表示名, 型番, 最大発熱量kW, 使える鍋の原文, 幅mm, 奥行mm, 高さmm, 重量kg, ガス消費量g/h, 連続燃焼時間分)
KONRO = [
    ("ミニ",                "CB-JRC-MN",  1.86, "鍋の上面の内径が直径20cmまで（小さい鍋は直径11cm以上）", 279,   185,   85,  1.0, 135, 112),
    ("エコプレミアムIII",   "CB-EPR-3",   2.9,  "目安として土鍋10号まで",                                 334,   274,   89,  1.5, 210,  72),
    ("アモルフォ プレミアム", "CB-AMO-80N", 2.9,  "目安として9号土鍋まで（小さい鍋は鍋底が16cm以上）",       355,   310,   84,  2.2, 211,  72),
    ("スリム",              "CB-SL-1",    3.3,  "目安として9号土鍋まで",                                 328,   275,   84,  1.3, 236,  70),
    ("達人スリムβ",         "CB-BS-1",    3.3,  "目安として9号土鍋まで",                                 335,   275,   84,  1.3, 236,  70),
    ("雅SLIM",              "CB-WA-64",   3.3,  "9号土鍋まで（小さい鍋は鍋底が16cm以上）",                 358.5, 293,   73,  2.0, 236,  70),
    ("極",                  "CB-EX-2025", 3.3,  "目安として9号土鍋まで（小さい鍋は鍋底が16cm以上）",       391,   316,   90,  2.2, 236,  74),
    ("達人スリムV",         "CB-TS-5",    3.4,  "目安として9号土鍋まで",                                 335,   275,   84,  1.3, 245,  68),
    ("スマート",            "CB-SMT-1",   3.5,  "目安として9号土鍋まで",                                 334,   274,   93,  1.3, 254,  78),
    ("ウィンドシールド",    "CB-WS-1",    3.5,  "目安として9号土鍋まで",                                 334,   274,   93,  1.4, 254,  78),
    ("BO—",                 "CB-AH-41N",  4.1,  "目安として9号土鍋まで",                                 337,   300,   94,  1.7, 286,  55),
]

# ---- 一次情報：銀峯陶器の土鍋 18製品（号数, シリーズ, 幅cm(取手込), 口径cm, 高さcm, 容量L）
DONABE = [
    (5.5, "墨貫入",     20.0, 17.0,  9.0, 0.4),
    (6,   "菊花",       21.0, 18.5, 10.0, 0.8),
    (6,   "菊花 深型",  21.0, 19.0, 11.0, 0.9),
    (6,   "花三島",     21.0, 19.0, 11.0, 0.9),
    (6,   "墨貫入",     22.0, 18.5, 10.0, 0.6),
    (7,   "菊花",       24.0, 22.0, 12.5, 1.1),
    (7,   "花三島",     24.5, 22.0, 12.5, 1.5),
    (7,   "墨貫入",     26.5, 22.0, 12.0, 1.0),
    (8,   "菊花 深型",  27.0, 24.5, 14.0, 2.0),
    (8,   "菊花",       27.5, 24.0, 13.5, 1.9),
    (8,   "花三島",     27.5, 25.0, 14.0, 2.2),
    (8,   "墨貫入",     29.5, 25.0, 13.5, 1.5),
    (9,   "菊花 深型",  31.0, 28.5, 17.0, 3.0),
    (9,   "菊花",       31.5, 28.5, 15.5, 2.7),
    (9,   "花三島",     31.5, 28.0, 16.0, 3.2),
    (9,   "墨貫入",     32.5, 28.0, 15.0, 2.2),
    (10,  "花三島",     34.0, 31.0, 17.0, 4.0),
    (10,  "墨貫入",     36.0, 31.0, 16.0, 2.9),
]

BOMBE_G = 250          # イワタニカセットガス CB-250S-OR の内容量
BOMBE_JR_G = 120       # ジュニア CB-JR-120S
NOSUI_6 = 6            # 農水省「1人1週間6本」（記事17）

fails = []


def check(label, got, want, tol=1e-9):
    ok = abs(got - want) <= tol
    print(("  OK   " if ok else "  NG   ") + "%-52s got=%s want=%s" % (label, got, want))
    if not ok:
        fails.append(label)


def rank(vals):
    """同順位は平均順位。"""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(xs, ys):
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = sum((rx[i] - mx) ** 2 for i in range(n)) ** 0.5
    dy = sum((ry[i] - my) ** 2 for i in range(n)) ** 0.5
    return num / (dx * dy)


print("=" * 78)
print("1. 本体寸法・重量のレンジ")
print("=" * 78)
w = [k[4] for k in KONRO]
d = [k[5] for k in KONRO]
h = [k[6] for k in KONRO]
m = [k[7] for k in KONRO]
print("  幅   %.1f 〜 %.1f mm" % (min(w), max(w)))
print("  奥行 %.1f 〜 %.1f mm" % (min(d), max(d)))
print("  高さ %.1f 〜 %.1f mm" % (min(h), max(h)))
print("  重量 %.1f 〜 %.1f kg" % (min(m), max(m)))
check("幅の最小（ミニ）", min(w), 279)
check("幅の最大（極）", max(w), 391)
check("幅の倍率 最大/最小", round(max(w) / min(w), 2), 1.40)
check("高さの最小（雅SLIM）", min(h), 73)
check("高さの最大（BO—）", max(h), 94)
check("重量の倍率 最大/最小", round(max(m) / min(m), 1), 2.2)

# ミニを除いた10機種（＝号数で公表している機種）
big = [k for k in KONRO if k[1] != "CB-JRC-MN"]
bw = [k[4] for k in big]
print("  ミニを除く10機種の幅 %.1f 〜 %.1f mm" % (min(bw), max(bw)))
check("ミニ以外の幅の最小（スリム）", min(bw), 328)

print()
print("=" * 78)
print("2. 火力と連続燃焼時間は比例するか（記事18の見立ての検証）")
print("=" * 78)
kw = [k[2] for k in KONRO]
mins = [k[9] for k in KONRO]
gph = [k[8] for k in KONRO]
rho_kw_min = spearman(kw, mins)
rho_kw_gph = spearman(kw, gph)
rho_gph_min = spearman(gph, mins)
print("  火力 vs 燃焼時間     spearman = %+.3f" % rho_kw_min)
print("  火力 vs ガス消費量   spearman = %+.3f" % rho_kw_gph)
print("  ガス消費量 vs 燃焼時間 spearman = %+.3f" % rho_gph_min)

# ミニは別枠（ボンベが2種類ある）ので、ミニを除いた10機種でも見る
kw2 = [k[2] for k in big]
mins2 = [k[9] for k in big]
gph2 = [k[8] for k in big]
print("  ミニ除く10機種：火力 vs 燃焼時間     spearman = %+.3f" % spearman(kw2, mins2))
print("  ミニ除く10機種：火力 vs ガス消費量   spearman = %+.3f" % spearman(kw2, gph2))

# 反例：火力が上なのに燃焼時間も長い組み合わせ
gyaku = []
for a in KONRO:
    for b in KONRO:
        if a[2] > b[2] and a[9] > b[9]:
            gyaku.append((a[0], a[2], a[9], b[0], b[2], b[9]))
print("  「火力が上なのに燃焼時間も長い」組み合わせ: %d 組" % len(gyaku))
for g in gyaku[:8]:
    print("    %s(%.2fkW/%d分) > %s(%.2fkW/%d分)" % g)
check("反例が存在する（0組ではない）", 1 if gyaku else 0, 1)

print()
print("=" * 78)
print("3. 250g ÷ ガス消費量 と 実測の連続燃焼時間")
print("=" * 78)
print("  %-22s %8s %8s %8s %10s" % ("機種", "割り算", "実測", "差", "逆算g/h"))
for name, code, k, nabe, W, D, H, M, G, T in KONRO:
    warizan = BOMBE_G / G * 60.0
    gyaku_gph = BOMBE_G / (T / 60.0)
    print("  %-22s %7.1f分 %6d分 %+7.1f %9.1f" % (name, warizan, T, T - warizan, gyaku_gph))
    if T <= warizan:
        fails.append("%s: 実測が割り算より短い（記事18の観測と逆）" % name)
check("11機種すべてで 実測 > 250÷消費量", 0, len(fails))

# 同じ236g/h なのに 70分 と 74分
same236 = [(k[0], k[9]) for k in KONRO if k[8] == 236]
print("  236g/h の機種: %s" % ", ".join("%s %d分" % s for s in same236))
check("236g/h は4機種ある", len(same236), 4)
check("236g/h の燃焼時間は2種類（70分と74分）", len(set(s[1] for s in same236)), 2)

print()
print("=" * 78)
print("4. ミニの「内径20cmまで」を銀峯の号数に翻訳する")
print("=" * 78)
MINI_MAX_KOUKEI = 20.0   # 鍋の上面の内径 20cm まで（イワタニ公表）
MINI_MIN_KOUKEI = 11.0
noru = [row for row in DONABE if row[3] <= MINI_MAX_KOUKEI and row[3] >= MINI_MIN_KOUKEI]
noranai = [row for row in DONABE if row[3] > MINI_MAX_KOUKEI]
print("  乗る:   %s" % ", ".join("%s号 %s(口径%.1f)" % (str(r[0]), r[1], r[3]) for r in noru))
print("  乗らない最小: %s号 %s(口径%.1f)" % (noranai[0][0], noranai[0][1], noranai[0][3]) if noranai else "  なし")
max_gou_noru = max(r[0] for r in noru)
min_gou_noranai = min(r[0] for r in noranai)
check("ミニに乗る最大の号数は6号", max_gou_noru, 6)
check("乗らない最小の号数は7号", min_gou_noranai, 7)
check("6号は4製品すべて乗る", len([r for r in noru if r[0] == 6]), 4)
check("5.5号も乗る（口径17.0cm）", len([r for r in noru if r[0] == 5.5]), 1)

print()
print("=" * 78)
print("5. 卓上に要る幅は「コンロの幅」ではなく「鍋の幅」で決まる")
print("=" * 78)
gou9 = [r for r in DONABE if r[0] == 9]
gou10 = [r for r in DONABE if r[0] == 10]
w9 = [r[2] for r in gou9]
w10 = [r[2] for r in gou10]
print("  9号の幅(取手込) %.1f 〜 %.1f cm" % (min(w9), max(w9)))
print("  10号の幅(取手込) %.1f 〜 %.1f cm" % (min(w10), max(w10)))
check("9号の幅の最大は32.5cm（墨貫入）", max(w9), 32.5)
check("10号の幅の最大は36.0cm（墨貫入）", max(w10), 36.0)

print("  %-22s %8s %10s %12s" % ("機種(9号まで)", "本体幅", "9号最大幅", "卓上に要る幅"))
kyuugou = [k for k in KONRO if "9号" in k[3]]
for name, code, k, nabe, W, D, H, M, G, T in kyuugou:
    honntai_cm = W / 10.0
    need = max(honntai_cm, max(w9))
    yoyuu = honntai_cm - max(w9)
    print("  %-22s %6.1fcm %8.1fcm %10.1fcm  (余裕 %+.1fcm)" % (name, honntai_cm, max(w9), need, yoyuu))
check("「9号まで」を名乗るのは9機種", len(kyuugou), 9)
sl = [k for k in kyuugou if k[1] == "CB-SL-1"][0]
check("スリムの本体幅と9号最大幅の差は0.3cm", round(sl[4] / 10.0 - max(w9), 1), 0.3)
kiwami = [k for k in kyuugou if k[1] == "CB-EX-2025"][0]
check("極の本体幅と9号最大幅の差は6.6cm", round(kiwami[4] / 10.0 - max(w9), 1), 6.6)

# エコプレミアムIII（10号まで）と10号土鍋
epr = [k for k in KONRO if k[1] == "CB-EPR-3"][0]
print("  エコプレミアムIII 本体幅 %.1fcm / 10号の幅 %.1f〜%.1fcm" % (epr[4] / 10.0, min(w10), max(w10)))
check("10号 花三島は本体幅より0.6cm大きい", round(min(w10) - epr[4] / 10.0, 1), 0.6)
check("10号 墨貫入は本体幅より2.6cm大きい", round(max(w10) - epr[4] / 10.0, 1), 2.6)

print()
print("=" * 78)
print("6. ボンベ何本で何時間か（記事17・18との接続）")
print("=" * 78)
for name, code, k, nabe, W, D, H, M, G, T in KONRO:
    h6 = T * NOSUI_6 / 60.0
    print("  %-22s ボンベ1本 %3d分 / 6本で %.1f 時間" % (name, T, h6))
bo = [k for k in KONRO if k[1] == "CB-AH-41N"][0]
smt = [k for k in KONRO if k[1] == "CB-SMT-1"][0]
check("BO— の6本ぶんは5.5時間", round(bo[9] * NOSUI_6 / 60.0, 1), 5.5)
check("スマートの6本ぶんは7.8時間", round(smt[9] * NOSUI_6 / 60.0, 1), 7.8)
mini = KONRO[0]
check("ミニ（通常ボンベ）の6本ぶんは11.2時間", round(mini[9] * NOSUI_6 / 60.0, 1), 11.2)
check("ジュニアと通常の内容量比", round(BOMBE_JR_G / float(BOMBE_G), 2), 0.48)
check("ミニのジュニア/通常の燃焼時間比", round(56 / 112.0, 2), 0.50)

print()
print("=" * 78)
print("7. 記事本文との突き合わせ")
print("=" * 78)
ART = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "site", "content", "articles", "konro-erabikata.md")
if not os.path.exists(ART):
    print("  (記事がまだ無い。数値の検算のみ実施)")
else:
    body = io.open(ART, encoding="utf-8").read()
    # 早見表の各行が一次情報と一致するか
    for name, code, k, nabe, W, D, H, M, G, T in KONRO:
        # 早見表の行だけを見る（ガス消費量の欄がある行が早見表）。強調記号は落とす。
        rows = [ln.replace("*", "") for ln in body.split("\n")
                if code in ln and ln.strip().startswith("|") and "g/h" in ln]
        if not rows:
            fails.append("早見表に %s の行がない" % code)
            print("  NG   早見表に %s の行がない" % code)
            continue
        if len(rows) != 1:
            fails.append("早見表に %s の行が %d 本ある" % (code, len(rows)))
        row = rows[0]
        wtxt = ("%.1f" % W).rstrip("0").rstrip(".")
        for label, needle in [
            ("火力", ("%.2f" % k).rstrip("0").rstrip(".") + "kW"),
            ("幅", wtxt + "×"),
            ("奥行", "×%d×" % D),
            ("高さ", "×%dmm" % H),
            ("重量", "%.1fkg" % M),
            ("消費量", "%dg/h" % G),
            ("燃焼時間", "%d分" % T),
        ]:
            if needle not in row:
                fails.append("%s の行に %s(%s) が無い" % (code, label, needle))
                print("  NG   %s の行に %s(%s) が無い" % (code, label, needle))
    if not any(f.startswith(("早見表", "CB-")) for f in fails):
        print("  OK   早見表11行が一次情報と一致")

print()
print("=" * 78)
if fails:
    print("FAILED: %d 件" % len(fails))
    for f in fails:
        print("  - %s" % f)
    sys.exit(1)
print("ALL OK")
