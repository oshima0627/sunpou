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
                  RULE, W, WARN, WARNB, WHITE)


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


# ---------------------------------------------------------------- クーラーボックス

def coolerbox_500ml_eyecatch(f):
    """内寸22×39cm に丸型ボトルを並べると 5列×3行 = 15本。余りが出るのが要点。"""
    f.header("500mlは何本入る？",
             "容量Lではなく「内寸」で決まります。同じ20Lでも15本と18本",
             key="15", key_label="20Lに丸型なら", key_unit="本")

    sc = 9.6                                   # 1cm = 9.6px
    W_cm, D_cm, dia = 39, 22, 6.85             # 内寸39×22cm、丸型68.5φ
    bx, by = 560, 214
    bw, bh = W_cm * sc, D_cm * sc
    cols, rows_n = 5, 3
    d = dia * sc

    f.rect(bx, by, bw, bh, BAND, PALE, 2)      # 内寸の床面（灰色の部分が「余り」）
    for r in range(rows_n):
        for c in range(cols):
            f.oval(bx + c * d, by + r * d, d, d, PALE2, NAVY, 2)

    f.text(bx, by - 30, 400, 24, f"内寸 {D_cm} × {W_cm}cm ／ 丸型 68.5φ", 16, MUTE)
    f.text(bx, by + bh + 14, 460, 24, "灰色は割り切れずに捨てられる余り", 15, MUTE)

    px = 72
    f.text(px, 210, 420, 26, "床に並ぶ数で決まります", 21, INK, bold=True)
    f.rich(px, 262, 420, 60, [("5列 × 3行 ＝ ", 26, INK, True), ("15", 46, NAVY, True), ("本", 24, NAVY, True)])
    f.rect(px, 330, 420, 96, BAND, radius=0.06)
    f.text(px + 18, 350, 380, 24, "同じ20Lでも 15本 と 18本", 18, INK, bold=True)
    f.text(px + 18, 382, 380, 22, "容量Lは中身の広さを表していません", 15, MUTE)

    f.footer("容量Lではなく、内寸の掛け算で決まります。")


def coolerbox_2l_eyecatch(f):
    """2Lは全高306mm。内寸の深さ255mmでは51mmはみ出す。"""
    f.header("2Lペットボトルは立てて入る？",
             "10〜25Lには、まず立ちません",
             key="51", key_label="はみ出す", key_unit="mm")

    base = 520                                  # 床の位置
    depth, bottle = 255, 306                    # mm。1px = 1mm で描く
    bxx = 470
    f.rect(bxx - 20, base - depth, 240, depth, BAND, PALE, 2)
    f.text(bxx - 20, base - depth - 28, 300, 24, f"内寸の深さ {depth}mm", 16, MUTE)

    f.bar(bxx + 40, base - bottle, 96, bottle, PALE2, PALE, NAVY, 2, radius=0.06)
    f.text(bxx + 40, base + 14, 320, 24, f"2Lボトル 全高 {bottle}mm", 16, MUTE)

    # はみ出している分
    f.rect(bxx + 40, base - bottle, 96, bottle - depth, WARNB, WARN, 2)
    f.text(bxx + 150, base - bottle + 6, 300, 30, f"{bottle - depth}mm はみ出す", 24, WARN, bold=True)

    px = 800
    f.rect(px - 20, 214, 336, 120, BAND, radius=0.06)
    f.text(px, 236, 300, 26, "1.5L も同じ高さです", 20, INK, bold=True)
    f.text(px, 268, 300, 24, "容量が減った分、細くなる", 16, MUTE)
    f.text(px, 296, 300, 24, "だけで背は変わりません", 16, MUTE)

    f.footer("10〜25Lのクーラーボックスには、まず立ちません。")


def coleman_fukasa_eyecatch(f):
    """同じ26Lクラスでも内寸の深さが 350mm と 235mm。2Lが立つかが分かれる。"""
    f.header("同じ26Lクラス。深さが1.5倍ちがう",
             "内寸を横から見た図。橙は2Lペットボトル（全高306mm）",
             key="1.5", key_label="深さの差が", key_unit="倍")

    base = 500
    sc = 0.86                                    # 1mm
    for x, cap, depth, verdict, ok in (
            (150, "コールマン 28QT（約26L）", 350, "2Lが立つ", True),
            (640, "ダイワ PV-REX 2800（28L）", 235, "2Lは立たない", False)):
        h = depth * sc
        f.text(x, 190, 400, 24, cap, 17, INK, bold=True)
        f.rect(x, base - h, 260, h, BAND, PALE, 2)
        f.bar(x + 70, base - 306 * sc, 84, 306 * sc, WARNB, WARNB, WARN, 2, radius=0.06)
        f.text(x, base + 16, 400, 26, f"深さ {depth}mm ／ {verdict}", 19,
               NAVY if ok else WARN, bold=True)

    f.text(150, base - 306 * sc - 30, 400, 24, "2Lの高さ 306mm", 15, WARN, bold=True)
    f.footer("同じ容量表示でも、深さは1.5倍ちがいます。")


def coolerbox_nagasa_eyecatch(f):
    """80Lと60Lで長辺は同じ85cm。違うのは深さ。"""
    f.header("80L と 60L。長さは同じ 85cm",
             "ダイワ トランクマスター の内寸を横から見た図",
             key="85", key_label="長辺はどちらも", key_unit="cm")

    sc = 5.4
    x = 150
    for y, cap, depth in ((210, "80L　トランクマスターHD III 8000", 31.5),
                          (390, "60L　トランクマスターHD II 6000", 23.5)):
        h = depth * sc
        f.text(x, y - 30, 500, 24, cap, 17, INK, bold=True)
        f.rect(x, y, 85 * sc, h, BAND, PALE, 2)
        f.text(x + 85 * sc + 20, y + 4, 260, 26, "長辺 85cm", 21, NAVY, bold=True)
        f.text(x + 85 * sc + 20, y + 36, 260, 24, f"深さ {depth}cm", 17, MUTE)

    f.footer("容量が増えても長さは同じ。増えるのは深さです。")

def coolerbox_yoryo_eyecatch(f):
    """外寸で測ると46Lの箱なのに、中身に使えるのは13.4L。"""
    f.header("「20L」は何の20L？",
             "外寸の体積のうち、中身に使えるのは 28.9〜40.0%",
             key="13.4", key_label="46Lの箱で使えるのは", key_unit="L")

    sc = 9.0
    ox, oy = 96, 214
    ow, oh = 45.0 * sc, 30.8 * sc
    iw, ih = 30.2 * sc, 18.2 * sc
    f.rect(ox, oy, ow, oh, BAND, PALE, 2)
    f.rect(ox + (ow - iw) / 2, oy + (oh - ih) / 2, iw, ih, PALE2, NAVY, 3)
    f.text(ox, oy - 30, 500, 24, "アイリスオーヤマ HUGEL 15L を上から見た床面", 16, MUTE)
    f.text(ox, oy + oh + 14, 560, 24, "外寸 45.0 × 30.8cm ／ 内寸 30.2 × 18.2cm", 15, MUTE)

    px = 620
    f.text(px, 214, 400, 24, "外寸で測ると", 17, MUTE)
    f.rich(px, 248, 400, 56, [("46", 48, INK, True), (" L の箱", 24, INK, True)])
    f.text(px, 320, 400, 24, "中身に使えるのは", 17, MUTE)
    f.rich(px, 354, 400, 56, [("13.4", 48, NAVY, True), (" L", 24, NAVY, True)])
    f.rect(px, 418, 420, 62, BAND, radius=0.08)
    f.text(px + 18, 436, 380, 26, "公表容量は 15L", 19, INK, bold=True)

    f.footer("外寸で測った体積のうち、中に入るのは 28.9〜40.0% です。")


def coolerbox_horeizai_eyecatch(f):
    """同じ箱・同じ保冷剤1枚でも、置き方で6本と18本に分かれる。"""
    f.header("保冷剤を入れると 500ml は何本減る？",
             "ダイワ S2000（20L）内寸 22 × 39cm ／ 500ml角型 ／ 保冷剤なしなら18本",
             key="6", key_label="寝かせると", key_unit="本")

    for x, cap, n, bad in ((110, "床に寝かせる", 6, True), (660, "壁に立てかける", 18, False)):
        f.rect(x - 26, 196, 470, 300, WARNB if bad else BAND, WARN if bad else PALE, 2, radius=0.04)
        f.text(x, 218, 420, 28, cap, 21, INK, bold=True)
        f.rich(x, 270, 420, 90, [(str(n), 76, WARN if bad else NAVY, True),
                                 ("本", 30, WARN if bad else NAVY, True)])
        f.text(x, 390, 420, 26,
               "保冷剤が床を占めます" if bad else "本数は減りません", 17, MUTE)
        f.text(x, 430, 420, 26,
               "並べられる列が減ります" if bad else "壁に立てれば床が空きます", 17, MUTE)

    f.footer("同じ箱・同じ保冷剤でも、置き方で 6本 と 18本 に分かれます。",
             "メーカー公表の内寸と保冷剤11製品の公表寸法から計算（実測ではありません）")


def horeizai_maisuu_eyecatch(f):
    """500mlの本数を減らさずに入る保冷剤の枚数。製品で7倍ちがう。"""
    f.header("保冷剤は何枚まで入るか",
             "氷点下パックM（196×138×厚26mm）／ 500ml角型を減らさない枚数",
             key="7", key_label="いちばん多くて", key_unit="枚")

    data = [("ダイワ S1000X（10L）", 1), ("アイリスオーヤマ HUGEL 15L", 1),
            ("ダイワ S1500（15L）", 2), ("ダイワ S2000（20L）", 2),
            ("ロゴス ハイパーL（20L）", 3), ("アイリスオーヤマ HUGEL 20L", 4),
            ("コールマン 28QT（約26L）", 4), ("ダイワ S2500（25L）", 6),
            ("アイリスオーヤマ HUGEL 40L", 7)]
    top, rh, x0, unit = 176, 40, 470, 84
    ys = f.rows(len(data), top=top, rh=rh, highlight=len(data) - 1)
    for (name, n), y in zip(data, ys):
        f.text(74, y + 4, 380, 24, name, 16, INK, bold=True)
        for k in range(n):
            f.bar(x0 + k * (unit + 6), y + 6, unit, 20, PALE2, PALE, NAVY, 2, radius=0.30)
        f.text(x0 + n * (unit + 6) + 8, y + 4, 90, 24, f"{n}枚", 17, NAVY, bold=True)

    f.footer("同じ「入る」でも、製品で1枚と7枚に分かれます。")


def coolerbox_daiwa_shimano_eyecatch(f):
    """KEEP と COOL は名前が違うだけで、同じ JIS の簡便法。"""
    f.header("ダイワ「KEEP」と シマノ「COOL」",
             "名前は違っても、同じ物差しでした",
             key="同じ", key_label="測り方は", key_unit="")

    for x, brand, series, rng in ((110, "ダイワ クールラインα3", "KEEP", "26 〜 90"),
                                  (640, "シマノ フィクセル", "COOL", "32 〜 140")):
        f.rect(x - 26, 196, 450, 150, BAND, PALE, 2, radius=0.05)
        f.rich(x, 226, 400, 50, [(series, 34, NAVY, True), (f"  {rng}", 26, INK, True)])
        f.text(x, 292, 400, 26, brand, 18, MUTE)

    f.rect(90, 378, 1020, 152, WHITE, PALE, 2, radius=0.04)
    f.text(120, 404, 900, 28, "どちらも JIS S 2048：2006 の簡便法", 22, INK, bold=True)
    f.text(120, 444, 940, 26, "外気40℃ ／ 本体容量の25%の角氷 ／ 氷が溶け切るまでの時間に換算", 17, MUTE)
    f.text(120, 480, 940, 26, "両社とも「目安であり保証値ではない」と明記しています", 17, MUTE)

    f.footer("名前が違うだけで、中身は同じ物差しです。",
             "両社の公表資料で確認しました（実測ではありません）")

# ---------------------------------------------------------------- カセットコンロ

def konro_erabikata_eyecatch(f):
    """「9号まで」を名乗っても本体幅は32.8〜39.1cm。土鍋との差が機種で違う。"""
    f.header("同じ「9号まで」でも幅が違う",
             "横棒は本体幅。破線は9号土鍋でいちばん幅のある墨貫入（32.5cm）",
             key="6.6", key_label="土鍋との差は最大", key_unit="cm")

    data = [("スリム", 32.8), ("スマート／ウィンドシールド", 33.4),
            ("達人スリムV／達人スリムβ", 33.5), ("BO", 33.7),
            ("アモルフォプレミアム", 35.5), ("雅SLIM", 35.85), ("極", 39.1)]
    # ⚠️ **0 から描く。** 途中で軸を切ると差が誇張される（このサイトは数字の扱いが売り）
    x0, sc, top, rh = 330, 17.2, 176, 50
    ys = f.rows(len(data), top=top, rh=rh, highlight=len(data) - 1)
    nabe = x0 + 32.5 * sc
    for (name, w), y in zip(data, ys):
        f.bar(x0, y + 8, w * sc, 26, PALE2, PALE, NAVY, 2, radius=0.30)
        f.text(74, y + 8, 250, 26, name, 15, INK, bold=True)
        f.text(x0 + w * sc + 12, y + 8, 110, 26, f"{w}cm", 16, NAVY, bold=True)
    f.ghost(nabe, top - 6, 1, len(data) * rh - 6, WARN)
    f.text(nabe - 130, top + len(data) * rh - 2, 260, 24, "9号土鍋 32.5cm", 15, WARN, bold=True)

    f.footer("「9号まで」は号数の目安で、寸法ではありません。")


def konro_jikan_eyecatch(f):
    """ボンベ1本の連続燃焼時間は55〜78分。割り算では出ない。"""
    f.header("ボンベ1本は55〜78分",
             "濃い部分が「250g ÷ ガス消費量」。薄い部分まで伸びると公表の連続燃焼時間",
             key="78", key_label="いちばん長くて", key_unit="分")

    data = [("BO", "286g/h ／ ＋3分", 55), ("スマート／ウィンドシールド", "254g/h ／ ＋19分", 78),
            ("達人スリムV", "245g/h ／ ＋7分", 68), ("スリム ほか2機種", "236g/h ／ ＋6分", 70),
            ("エコプレミアムIII", "210g/h ／ ＋1分", 72), ("ミニ", "135g/h ／ ＋1分", 112)]
    x0, sc, top, rh = 420, 5.6, 176, 58
    hot = max(range(len(data)), key=lambda i: data[i][2])
    ys = f.rows(len(data), top=top, rh=rh, highlight=hot)
    for (name, spec, mins), y in zip(data, ys):
        f.bar(x0, y + 10, mins * sc, 28, PALE2, PALE, NAVY, 2, radius=0.30)
        f.text(74, y + 4, 330, 24, name, 16, INK, bold=True)
        f.text(74, y + 28, 330, 22, spec, 14, MUTE)
        f.text(x0 + mins * sc + 12, y + 10, 100, 28, f"{mins}分", 18, NAVY, bold=True)

    f.footer("火力が強い機種ほど、早く使い切ります。")


def konro_bombe_eyecatch(f):
    """農水省の「1人6本」に届くのは、10℃で全部まかなうときだけ。"""
    f.header("6本に届くのは「全部まかなう」とき",
             "1人・1週間あたり ／ 気温10℃での計算",
             key="5.8", key_label="全部まかなっても", key_unit="本")

    data = [("食事＋カップ麺＋飲み物＋お湯", "全部まかなう", 5.8),
            ("食事＋飲み物＋お湯", "カップ麺なし", 4.5),
            ("食事＋飲み物", "お湯を沸かさない", 3.2),
            ("食事だけ", "1日3回のレトルト", 2.5)]
    x0, sc, top, rh = 430, 95.0, 200, 76
    ys = f.rows(len(data), top=top, rh=rh, highlight=0)
    goal = x0 + 6 * sc
    for (name, note, n), y in zip(data, ys):
        f.bar(x0, y + 16, n * sc, 34, PALE2, PALE, NAVY, 2, radius=0.30)
        f.text(74, y + 12, 350, 24, name, 16, INK, bold=True)
        f.text(74, y + 38, 350, 22, note, 14, MUTE)
        f.text(x0 + n * sc + 12, y + 16, 100, 34, f"{n}本", 19, NAVY, bold=True)
    f.ghost(goal, top - 8, 1, len(data) * rh - 4, WARN)
    f.text(goal - 200, top - 34, 260, 24, "農林水産省の目安 6本", 16, WARN, bold=True)

    f.footer("「1人6本」はカップ麺まで含めた全部の想定でした。",
             "農水省とイワタニの公表値からの計算です（実測ではありません）")


def konro_donabe_eyecatch(f):
    """号数は幅を決めていない。同じ号数でもシリーズで幅が違う。"""
    f.header("土鍋の「号数」は幅を決めていません",
             "銀峯陶器の公表寸法。同じ号数でもシリーズで幅が違う（幅は取手込み）",
             key="33.4", key_label="コンロの本体幅", key_unit="cm")

    data = [("6号", 21, 22), ("7号", 24, 26.5), ("8号", 27, 29.5),
            ("9号", 31, 32.5), ("10号", 34, 36)]
    x0, sc, top, rh = 300, 22.0, 186, 66
    base = 18.0
    ys = f.rows(len(data), top=top, rh=rh, highlight=3)
    konro = x0 + (33.4 - base) * sc
    for (name, lo, hi), y in zip(data, ys):
        f.bar(x0 + (lo - base) * sc, y + 14, (hi - lo) * sc, 30, PALE2, PALE, NAVY, 2, radius=0.30)
        f.text(74, y + 14, 180, 30, name, 20, INK, bold=True)
        f.text(x0 + (hi - base) * sc + 14, y + 14, 180, 30, f"{lo}〜{hi}cm", 17, NAVY, bold=True)
    f.ghost(konro, top - 8, 1, len(data) * rh - 8, WARN)
    f.text(konro - 60, top - 34, 420, 24, "カセットコンロの本体幅 33.4cm", 16, WARN, bold=True)

    f.footer("同じ号数でも、シリーズで幅が違います。")

# ---------------------------------------------------------------- 脚立・踏み台

def kyatatsu_takasa_eyecatch(f):
    """型番に180が付いても天板高さは1.80m〜1.68m。立てる高さは1.40m。"""
    f.header("同じ「180」でも天板の高さが違う",
             "型番に180が付く4シリーズのメーカー公表値",
             key="1.40", key_label="実際に立てるのは", key_unit="m")

    data = [("アルインコ BSA-180A", "専用脚立", 1.80, False),
            ("ピカ SEC-S180", "専用脚立", 1.80, False),
            ("長谷川工業 RHB-18a", "はしご兼用脚立", 1.70, False),
            ("ピカ MCX-180", "はしご兼用脚立", 1.68, False),
            ("RHB-18a に立てる高さ", "天板には乗れません", 1.40, True)]
    x0, sc, top, rh = 400, 340.0, 176, 68
    ys = f.rows(len(data), top=top, rh=rh, highlight=4)
    for (name, note, m, hot), y in zip(data, ys):
        f.bar(x0, y + 16, m * sc, 30, WARNB if hot else PALE2, WARNB if hot else PALE,
              WARN if hot else NAVY, 2, radius=0.30)
        f.text(74, y + 10, 320, 24, name, 16, INK, bold=True)
        f.text(74, y + 36, 320, 22, note, 14, MUTE)
        f.text(x0 + m * sc + 12, y + 16, 110, 30, f"{m:.2f}m", 18,
               WARN if hot else NAVY, bold=True)

    f.footer("専用脚立は型番＝天板高さ。はしご兼用脚立は型番より9〜12cm低い値でした。")


def kyatatsu_omosa_eyecatch(f):
    """足を置ける高さが同じでも、重さは1.7kgと6.3kg。"""
    f.header("同じ高さに立つのに 1.7kg と 6.3kg",
             "足を置ける高さが0.5〜0.6mの5製品",
             key="6.3", key_label="いちばん重いもの", key_unit="kg")

    data = [("アルインコ CCA-60K", "踏台 ／ 0.56m", 1.7),
            ("長谷川工業 SE-6a", "踏台 ／ 0.56m", 1.8),
            ("長谷川工業 EFA-05", "踏台（上わく付き）／ 0.51m", 3.5),
            ("長谷川工業 RHB-09a", "はしご兼用脚立 ／ 0.50m", 3.6),
            ("長谷川工業 SWH-09", "強力型脚立 ／ 0.60m", 6.3)]
    x0, sc, top, rh = 430, 92.0, 176, 68
    ys = f.rows(len(data), top=top, rh=rh, highlight=4)
    for (name, note, kg), y in zip(data, ys):
        f.bar(x0, y + 16, kg * sc, 30, PALE2, PALE, NAVY, 2, radius=0.30)
        f.text(74, y + 10, 350, 24, name, 16, INK, bold=True)
        f.text(74, y + 36, 350, 22, note, 14, MUTE)
        f.text(x0 + kg * sc + 12, y + 16, 110, 30, f"{kg}kg", 18, NAVY, bold=True)

    f.footer("踏台は天板高さ、脚立は使用最大高さでそろえています。")


def kyatatsu_kaidan_eyecatch(f):
    """伸縮脚は21〜45cm。階段で必要な69cmに届かない。"""
    f.header("伸縮脚は21〜45cm。階段には届きません",
             "3社5シリーズの公表値",
             key="69", key_label="階段で必要な高低差", key_unit="cm")

    data = [("長谷川工業 RZS", "脚軽伸縮タイプ／専用脚立", 21, False),
            ("長谷川工業 RYZB", "はしご兼用伸縮脚立", 31, False),
            ("ピカ スタッピー SXJ", "四脚アジャスト式", 31, False),
            ("アルインコ PRT-FX", "伸縮脚付専用脚立", 44, False),
            ("ピカ かるノビ SCL", "階段用／前後の脚の長さが違う", 45, False),
            ("階段で必要な高低差", "踏面15cm・蹴上げ23cm・3段ぶん", 69, True)]
    x0, sc, top, rh = 430, 8.6, 176, 62
    ys = f.rows(len(data), top=top, rh=rh, highlight=5)
    for (name, note, cm, hot), y in zip(data, ys):
        f.bar(x0, y + 14, cm * sc, 28, WARNB if hot else PALE2, WARNB if hot else PALE,
              WARN if hot else NAVY, 2, radius=0.30)
        f.text(74, y + 8, 350, 24, name, 16, INK, bold=True)
        f.text(74, y + 32, 350, 22, note, 14, MUTE)
        f.text(x0 + cm * sc + 12, y + 14, 110, 28, f"{cm}cm", 18,
               WARN if hot else NAVY, bold=True)

    f.footer("前脚と後脚は3段離れます。1段で済ませるには踏面が28cm近く必要でした。")


def kyatatsu_fumidai_eyecatch(f):
    """「踏台」の天板は0.30mから1.61mまで。上わくが付くと80cmを超えても踏台。"""
    f.header("「踏台」の天板は0.30mから1.61mまで",
             "メーカーが呼び分けている天板高さの範囲",
             key="1.61", key_label="踏台なのに最大", key_unit="m")

    data = [("踏台（上わくなし）", 0.30, 0.79), ("踏台（上わく付き）", 0.51, 1.61),
            ("脚立", 0.51, 2.70)]
    x0, sc, top, rh = 380, 260.0, 200, 84
    ys = f.rows(len(data), top=top, rh=rh, highlight=1)
    for (name, lo, hi), y in zip(data, ys):
        f.bar(x0 + lo * sc, y + 20, (hi - lo) * sc, 34, PALE2, PALE, NAVY, 2, radius=0.30)
        f.text(74, y + 14, 300, 24, name, 17, INK, bold=True)
        f.text(74, y + 40, 300, 22, f"{lo:.2f} 〜 {hi:.2f}m", 15, MUTE)
    line = x0 + 0.80 * sc
    f.ghost(line, top - 10, 1, len(data) * rh - 10, WARN)
    f.text(line - 90, top - 36, 300, 24, "天板高さ 80cm", 16, WARN, bold=True)
    for v, lab in ((0, "0"), (1, "1m"), (2, "2m")):
        f.text(x0 + v * sc - 20, top + len(data) * rh - 4, 60, 22, lab, 14, MUTE)

    f.footer("上わくが付くと、80cmを超えても「踏台」と呼ばれていました。")


def kyatatsu_erabikata_eyecatch(f):
    """届きたい高さ − 身長 ＝ 必要な足場。0.8m に立つ3つの選び方。"""
    f.header("届きたい高さ − 身長 ＝ 必要な足場",
             "長谷川工業の「身長＋天板高さ＝作業高さ」を逆に使う（身長160cm基準）",
             key="0.8", key_label="2.4mに届くには", key_unit="m")

    for x, lab, val in ((150, "届きたい高さ", "2.4m"), (500, "身長", "1.6m"),
                        (860, "必要な足場", "0.8m")):
        f.rect(x - 24, 186, 260, 108, BAND if x < 800 else HILI, PALE, 2, radius=0.06)
        f.text(x, 204, 220, 24, lab, 16, MUTE)
        f.text(x, 238, 220, 44, val, 34, NAVY, bold=True)
    f.text(422, 218, 60, 44, "−", 30, MUTE, bold=True)
    f.text(786, 218, 60, 44, "＝", 30, MUTE, bold=True)

    f.text(72, 320, 500, 26, "0.8m に足を置ける3つの選び方", 20, INK, bold=True)
    for x, kind, model, spec, note in (
            (96, "踏台", "アルインコ CCA-80K", "0.79m ／ 2.5kg", "いちばん軽く、短くしまえる"),
            (456, "踏台（上わく付き）", "アルインコ TBF-4", "0.77m ／ 3.8kg", "手すりが天板の60cm上"),
            (816, "はしご兼用脚立", "長谷川工業 RHB-12a", "0.80m ／ 4.5kg", "天板には乗れない")):
        f.rect(x - 22, 356, 320, 150, WHITE, PALE, 2, radius=0.05)
        f.text(x, 376, 290, 24, kind, 16, MUTE)
        f.text(x, 404, 290, 26, model, 17, INK, bold=True)
        f.text(x, 436, 290, 26, spec, 18, NAVY, bold=True)
        f.text(x, 470, 290, 24, note, 14, MUTE)

    f.footer("脚立の「足を置ける高さ」は天板高さではなく、使用最大高さです。")

ORDER = [
    "kyatatsu-secchi-eyecatch",
    "kyatatsu-secchi",
    "coolerbox-500ml-eyecatch",
    "coolerbox-2l-eyecatch",
    "coleman-fukasa-eyecatch",
    "coolerbox-nagasa-eyecatch",
    "coolerbox-yoryo-eyecatch",
    "coolerbox-horeizai-eyecatch",
    "horeizai-maisuu-eyecatch",
    "coolerbox-daiwa-shimano-eyecatch",
    "konro-erabikata-eyecatch",
    "konro-jikan-eyecatch",
    "konro-bombe-eyecatch",
    "konro-donabe-eyecatch",
    "kyatatsu-takasa-eyecatch",
    "kyatatsu-omosa-eyecatch",
    "kyatatsu-kaidan-eyecatch",
    "kyatatsu-fumidai-eyecatch",
    "kyatatsu-erabikata-eyecatch",
]

FIGURES = {
    "kyatatsu-secchi-eyecatch": kyatatsu_secchi_eyecatch,
    "kyatatsu-secchi": kyatatsu_secchi,
    "coolerbox-500ml-eyecatch": coolerbox_500ml_eyecatch,
    "coolerbox-2l-eyecatch": coolerbox_2l_eyecatch,
    "coleman-fukasa-eyecatch": coleman_fukasa_eyecatch,
    "coolerbox-nagasa-eyecatch": coolerbox_nagasa_eyecatch,
    "coolerbox-yoryo-eyecatch": coolerbox_yoryo_eyecatch,
    "coolerbox-horeizai-eyecatch": coolerbox_horeizai_eyecatch,
    "horeizai-maisuu-eyecatch": horeizai_maisuu_eyecatch,
    "coolerbox-daiwa-shimano-eyecatch": coolerbox_daiwa_shimano_eyecatch,
    "konro-erabikata-eyecatch": konro_erabikata_eyecatch,
    "konro-jikan-eyecatch": konro_jikan_eyecatch,
    "konro-bombe-eyecatch": konro_bombe_eyecatch,
    "konro-donabe-eyecatch": konro_donabe_eyecatch,
    "kyatatsu-takasa-eyecatch": kyatatsu_takasa_eyecatch,
    "kyatatsu-omosa-eyecatch": kyatatsu_omosa_eyecatch,
    "kyatatsu-kaidan-eyecatch": kyatatsu_kaidan_eyecatch,
    "kyatatsu-fumidai-eyecatch": kyatatsu_fumidai_eyecatch,
    "kyatatsu-erabikata-eyecatch": kyatatsu_erabikata_eyecatch,
}
