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

    base = 500                                  # 床の位置
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
             "足を置ける高さ0.5〜0.6m（伸縮脚付きは除く）",
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

# ---------------------------------------------------------------- 本文の図版

def _plan(f, x, y, wcm, dcm, sc, dia, cols, rows_n, label, sub):
    """上から見た床面に丸型ボトルを敷き詰める図。灰色の残りが「余り」。"""
    bw, bh = wcm * sc, dcm * sc
    d = dia * sc
    f.text(x, y - 30, 520, 24, label, 16, INK, bold=True)
    f.rect(x, y, bw, bh, BAND, PALE, 2)
    for r in range(rows_n):
        for c in range(cols):
            f.oval(x + c * d, y + r * d, d, d, PALE2, NAVY, 2)
    f.text(x, y + bh + 16, 520, 24, sub, 15, MUTE)
    return bh


def bottle_height_chart(f):
    """ボトルの全高と、クーラーボックスの深さの関係。"""
    f.header("1.5L も 2L とほぼ同じ高さ",
             "棒がボトルの全高、線がクーラーボックスの内寸の深さ",
             key="310", key_label="立つのは深さ", key_unit="mm")

    x0, sc, top, rh = 480, 1.55, 186, 58
    data = [("ダイワ10L・20L", 220), ("ダイワ15L", 230), ("ロゴス・アイリス", 243),
            ("ダイワ25L", 255), ("アイリス40L", 310)]
    ys = f.rows(len(data), top=top, rh=rh, highlight=4)
    for (name, mm), y in zip(data, ys):
        ok = mm >= 306
        f.bar(x0, y + 12, mm * sc, 28, PALE2 if ok else BAND, PALE if ok else BAND,
              NAVY if ok else MUTE, 2, radius=0.30)
        f.text(74, y + 12, 380, 28, f"{name}　内寸の深さ {mm}mm", 16, INK, bold=True)
        f.text(x0 + mm * sc + 12, y + 12, 160, 28, "2Lが立つ" if ok else "立たない",
               16, NAVY if ok else MUTE, bold=True)
    line = x0 + 306 * sc
    f.ghost(line, top - 8, 1, len(data) * rh - 8, WARN)
    f.text(line - 40, top - 34, 320, 24, "2Lの全高 306mm", 16, WARN, bold=True)

    f.footer("1.5L（305〜307.5mm）は 2L（305〜306mm）とほぼ同じ高さです。",
             "出典：ボトル＝料材開発／深さ＝各メーカー公式の内寸")


def coolerbox_floorplan(f):
    """床面積が同じ858cm²でも、割り切れ方で15本と12本に分かれる。"""
    f.header("床面積が同じでも本数は違う",
             "どちらも 858cm² ／ 丸型ボトル 胴径 68.5mm ／ 灰色は割り切れない余り",
             key="12", key_label="ロゴスは", key_unit="本")

    sc, dia = 7.4, 6.85
    _plan(f, 80, 230, 39, 22, sc, dia, 5, 3,
          "ダイワ S2000（20L）　内寸 22 × 39cm", "39 ÷ 6.85 ＝ 5.7 → 5列 ／ 22 ÷ 6.85 ＝ 3.2 → 3行")
    _plan(f, 620, 230, 33, 26, sc, dia, 4, 3,
          "ロゴス ハイパー氷点下クーラーL（20L）　内寸 33 × 26cm",
          "33 ÷ 6.85 ＝ 4.8 → 4列 ／ 26 ÷ 6.85 ＝ 3.8 → 3行")
    # 合計行は左右で同じ高さに置く（床の奥行が違うので、低いほうに合わせる）
    f.rich(80, 480, 400, 44, [("5列 × 3行 ＝ ", 22, INK, True), ("15", 34, NAVY, True), ("本", 20, NAVY, True)])
    f.rich(620, 480, 400, 44, [("4列 × 3行 ＝ ", 22, INK, True), ("12", 34, NAVY, True), ("本", 20, NAVY, True)])

    f.footer("広さではなく、胴径で割り切れるかで決まります。")


def coolerbox_daiwa_shimano_yuka(f):
    """公表容量20Lと22L。どちらも15本。"""
    f.header("公表容量は 20L と 22L。どちらも 15本",
             "ボトルはシマノ公表の前提 Φ66 × 全高207mm ／ 灰色は使えない余り",
             key="15", key_label="どちらも", key_unit="本")

    sc, dia = 7.2, 6.6
    _plan(f, 80, 230, 39, 22, sc, dia, 5, 3,
          "ダイワ クールラインα3 2000（20L）　内寸 22 × 39cm",
          "メーカーの公表は18本（前提にしたボトルが違う）")
    f.rich(80, 452, 400, 44, [("3列 × 5行 ＝ ", 22, INK, True), ("15", 34, NAVY, True), ("本", 20, NAVY, True)])
    _plan(f, 620, 230, 39.1, 21.1, sc, dia, 5, 3,
          "シマノ フィクセル 22L　内寸（底部）21.1 × 39.1cm",
          "本数の公表なし。内寸は「底部」の値を使った")
    f.rich(620, 452, 400, 44, [("3列 × 5行 ＝ ", 22, INK, True), ("15", 34, NAVY, True), ("本", 20, NAVY, True)])

    f.footer("公表容量が違っても、入る本数は同じでした。")


def coolerbox_horeizai_oki(f):
    """同じ箱・同じ1枚でも、置き方で6本と18本。"""
    f.header("同じ箱・同じ1枚。置き方だけで違う",
             "ダイワ S2000（20L）内寸 22 × 39cm ／ 500ml角型 胴径60mm",
             key="6", key_label="寝かせると", key_unit="本")

    sc = 7.4
    for x, cap, pack, n, note, bad in (
            (80, "氷点下パックL（25.5 × 16.4 × 厚2.5cm）を床に寝かせる", (25.5, 16.4), 6,
             "残る帯は 22 − 16.4 ＝ 5.6cm。胴径6cmに足りず丸ごと死ぬ", True),
            (620, "氷点下パックM（19.6 × 13.8 × 厚2.6cm）を壁に立てかける", (19.6, 2.6), 18,
             "床の余り 4cm と 3cm に、厚さ2.6cmがそのまま収まる", False)):
        bw, bh = 39 * sc, 22 * sc
        f.text(x, 200, 520, 24, cap, 15, INK, bold=True)
        f.rect(x, 230, bw, bh, BAND, PALE, 2)
        f.rect(x, 230, pack[0] * sc, pack[1] * sc, WARNB if bad else PALE, WARN if bad else NAVY, 2)
        cols, rows_n = (3, 2) if bad else (6, 3)
        oy = 230 + pack[1] * sc + 4 if bad else 230
        for r in range(rows_n):
            for c in range(cols):
                f.oval(x + c * 6 * sc, oy + r * 6 * sc, 6 * sc, 6 * sc, PALE2, NAVY, 2)
        f.rich(x, 230 + bh + 16, 400, 40,
               [(str(n), 32, WARN if bad else NAVY, True), ("本", 20, WARN if bad else NAVY, True)])
        f.text(x, 230 + bh + 58, 520, 24, note, 14, MUTE)

    f.footer("面積ではなく、残った帯が胴径で割り切れるかで決まります。")


def coolerbox_nagasa_diagonal(f):
    """斜めに置くと長辺より長いものが入る。"""
    f.header("斜めに置くと、長辺より長いものが入る",
             "シマノ スペーザ 350（内寸 25.2 × 59.2 × 深さ 23.0cm）を上から見た床",
             key="68.3", key_label="立体の対角線", key_unit="cm")

    sc = 6.4
    x, y = 100, 230
    bw, bh = 59.2 * sc, 25.2 * sc
    f.rect(x, y, bw, bh, BAND, PALE, 2)
    f.ghost(x, y, bw, bh, NAVY)

    px = 640
    f.rect(px - 20, 210, 480, 120, BAND, radius=0.06)
    f.text(px, 230, 440, 26, "床の対角線", 18, MUTE)
    f.text(px, 264, 440, 34, "√(25.2² ＋ 59.2²) ＝ 64.3", 21, NAVY, bold=True)
    f.rect(px - 20, 346, 480, 120, WHITE, PALE, 2, radius=0.06)
    f.text(px, 366, 440, 26, "立体の対角線", 18, MUTE)
    f.text(px, 400, 440, 34, "√(25.2² ＋ 59.2² ＋ 23.0²) ＝ 68.3", 20, NAVY, bold=True)

    f.footer("角の丸みや水栓の出っ張りは計算に入っていません。")


def coolerbox_yoryo_danmen(f):
    """どちらも15L。外寸が小さいほうが中は広い。"""
    f.header("どちらも15L。中の広さは違う",
             "上から見た床面 ／ 灰色の外枠＝外寸、青い内枠＝内寸（メーカー公表値）",
             key="6.3", key_label="断熱で片側", key_unit="cm")

    sc = 6.4
    for x, cap, ow, od, iw, idp, note in (
            (100, "アイリスオーヤマ HUGEL 15L（真空断熱パネル）", 45.0, 30.8, 30.2, 18.2,
             "長辺で片側7.4cm ／ 短辺で片側6.3cm"),
            (640, "ダイワ クールラインα3 S1500（発泡スチロール）", 47.5, 25.0, 36.0, 17.0,
             "長辺で片側5.75cm ／ 短辺で片側4.0cm")):
        f.text(x, 200, 520, 24, cap, 15, INK, bold=True)
        f.rect(x, 230, ow * sc, od * sc, BAND, PALE, 2)
        f.rect(x + (ow - iw) * sc / 2, 230 + (od - idp) * sc / 2, iw * sc, idp * sc, PALE2, NAVY, 3)
        f.text(x, 230 + od * sc + 18, 480, 26, f"外寸 {ow} × {od}cm", 18, INK, bold=True)
        f.text(x, 230 + od * sc + 46, 480, 26, f"→ 内寸 {iw} × {idp}cm", 18, NAVY, bold=True)
        f.text(x, 230 + od * sc + 74, 480, 24, f"外寸と内寸の差は {note}", 14, MUTE)

    f.footer("外寸が大きくても、断熱が厚ければ中は狭くなります。")

def coolerbox_erabikata_eyecatch(f):
    """入れたいものから内寸を逆に引く。容量Lは何が入るかを教えない。"""
    f.header("入れたいものから内寸を逆に引く",
             "容量Lは「何が入るか」を教えてくれない",
             key="33", key_label="内寸を並べた", key_unit="製品")

    data = [("500ml ペットボトル", "全高 207mm", "内寸の辺 ÷ 胴径", "同じ20Lでも 15〜18本"),
            ("2L ペットボトル", "全高 306mm", "内寸の深さ", "306mm以上は 33製品中9つ"),
            ("保冷剤", "厚さ 25〜35mm", "深さの余り", "25mm未満なら床を食う"),
            ("大きい魚", "まっすぐ入る長さ", "内寸の長辺", "80cm以上は 3製品"),
            ("持ち運び", "空のときの重さ", "自重", "1.5kg 〜 13.2kg")]
    ys = f.rows(len(data), top=178, rh=72)
    for (want, spec, key_, ans), y in zip(data, ys):
        f.text(74, y + 10, 300, 24, want, 17, INK, bold=True)
        f.text(74, y + 36, 300, 22, spec, 14, MUTE)
        f.text(392, y + 18, 50, 28, "→", 20, NAVY, bold=True)
        f.text(456, y + 10, 300, 24, key_, 17, NAVY, bold=True)
        f.text(790, y + 18, 340, 28, ans, 17, INK, bold=True)

    f.footer("容量Lではなく、入れたいものから内寸を決めます。")


def konro_donabe_haba(f):
    """「10号まで」の機種より、10号土鍋のほうが幅がある。"""
    f.header("「10号まで」でも土鍋のほうが広い",
             "上から見た図 ／ 灰色＝コンロ本体、橙＝土鍋（口径31cm＋取手）",
             key="1.3", key_label="左右にはみ出す", key_unit="cm")

    sc = 7.2
    kx, ky = 110, 240
    kw, kh = 33.4 * sc, 27.4 * sc
    f.rect(kx, ky, kw, kh, BAND, PALE, 2)
    pw = 36 * sc
    f.oval(kx + (kw - pw) / 2, ky + (kh - pw / 1.35) / 2, pw, pw / 1.35, WARNB, WARN, 3)

    px = 640
    f.text(px, 214, 460, 26, "イワタニ エコプレミアムIII", 18, INK, bold=True)
    f.text(px, 244, 460, 26, "本体 33.4 × 27.4cm", 18, NAVY, bold=True)
    f.text(px, 296, 460, 26, "墨貫入 10号", 18, INK, bold=True)
    f.text(px, 326, 460, 26, "幅（取手込）36cm", 18, WARN, bold=True)
    f.rect(px - 20, 366, 480, 66, WARNB, WARN, 2, radius=0.06)
    f.text(px, 386, 440, 26, "左右に 1.3cm ずつはみ出す", 19, WARN, bold=True)
    f.text(px, 452, 480, 24, "はみ出しても五徳に乗れば使えます。", 15, MUTE)
    f.text(px, 480, 480, 24, "効くのは「卓上で必要な幅」のほうです。", 15, MUTE)

    f.footer("号数ではなく、取手込みの幅で決まります。")


def kyatatsu_takasa(f):
    """「180」の脚立で足を置けるのは1.40m。型番より40cm低い。"""
    f.header("「180」でも足を置けるのは 1.40m",
             "長谷川工業 RHB-18a ／ 横から見た図 ／ 踏ざんは省略",
             key="40", key_label="型番より低い", key_unit="cm")

    sc = 148.0
    x, base = 150, 520
    f.bar(x, base - 1.70 * sc, 200, 1.70 * sc, PALE2, PALE, NAVY, 2, radius=0.03)
    f.rect(x - 20, base - 1.40 * sc, 240, 4, WARN)

    px = 500
    for y, big, note, warn in (
            (200, "型番の数字 180", "開いた状態の高さではありません", False),
            (272, "天板の高さ 1.70m", "乗ることは禁止されています", False),
            (344, "使用最大高さ 1.40m", "足を置けるのはここまで", True)):
        f.rect(px - 20, y - 16, 500, 62, WARNB if warn else BAND, WARN if warn else None,
               2, radius=0.06)
        f.text(px, y - 4, 460, 26, big, 20, WARN if warn else INK, bold=True)
        f.text(px, y + 24, 460, 24, note, 15, MUTE)

    f.text(px, 434, 500, 26, "型番の数字より 40cm 低い", 19, NAVY, bold=True)
    f.text(px, 464, 500, 24, "RHB は5サイズすべてこの差でした", 15, MUTE)
    f.text(px, 492, 520, 24, "BSA-A と SEC-S の仕様表にはこの欄がありません", 15, MUTE)

    f.footer("型番の数字は、足を置ける高さではありません。")


def kyatatsu_omosa(f):
    """0.8m前後に立つ6製品。2.5kgから7.6kgまで3.0倍。"""
    f.header("0.8m前後に立つのに 2.5kg と 7.6kg",
             "踏台は天板高さ、脚立は使用最大高さでそろえています",
             key="3.0", key_label="重さの差は", key_unit="倍")

    data = [("アルインコ CCA-80K", "踏台 ／ 0.79m", 2.5), ("長谷川 SE-8a", "踏台 ／ 0.79m", 2.6),
            ("アルインコ TBF-4", "踏台（上わく付き）／ 0.77m", 3.8),
            ("長谷川 EFA-08", "踏台（上わく付き）／ 0.79m", 4.4),
            ("長谷川 RHB-12a", "はしご兼用脚立 ／ 0.80m", 4.5),
            ("長谷川 SWH-12", "強力型脚立 ／ 0.90m", 7.6)]
    x0, sc, top, rh = 430, 78.0, 176, 62
    ys = f.rows(len(data), top=top, rh=rh, highlight=5)
    for (name, note, kg), y in zip(data, ys):
        f.bar(x0, y + 14, kg * sc, 28, PALE2, PALE, NAVY, 2, radius=0.30)
        f.text(74, y + 8, 350, 24, name, 16, INK, bold=True)
        f.text(74, y + 32, 350, 22, note, 14, MUTE)
        f.text(x0 + kg * sc + 12, y + 14, 110, 28, f"{kg}kg", 18, NAVY, bold=True)

    f.footer("いちばん軽い2.5kgと、いちばん重い7.6kgで3.0倍の差があります。")


def kyatatsu_kaidan(f):
    """階段では前脚と後脚が3段離れ、必要な高低差は69cm。伸縮脚は31cm。"""
    f.header("階段では前脚と後脚が3段離れます",
             "踏面15cm・蹴上げ23cm（住宅の法定の限界値）／ 脚立の設置奥行 55.2cm",
             key="38", key_label="足りない分", key_unit="cm")

    sc = 3.2
    x, base = 110, 480
    for i in range(4):
        f.rect(x + i * 15 * sc, base - (i + 1) * 23 * sc, 15 * sc + 2, 23 * sc + 2, BAND, PALE, 2)
    f.rect(x - 14, base - 69 * sc, 5, 69 * sc, WARN)
    f.text(x - 6, base - 69 * sc - 32, 200, 26, "69cm", 19, WARN, bold=True)
    f.rect(x + 230, base - 31 * sc, 5, 31 * sc, NAVY)
    f.text(x + 242, base - 31 * sc - 32, 200, 26, "31cm", 19, NAVY, bold=True)

    px = 560
    f.rect(px - 20, 196, 500, 78, WARNB, WARN, 2, radius=0.06)
    f.text(px, 214, 460, 26, "必要な高低差 69cm", 20, WARN, bold=True)
    f.text(px, 244, 460, 24, "3段離れる × 蹴上げ23cm", 15, MUTE)
    f.rect(px - 20, 292, 500, 78, BAND, radius=0.06)
    f.text(px, 310, 460, 26, "伸縮脚で調整できるのは 31cm", 20, INK, bold=True)
    f.text(px, 340, 460, 24, "ピカ スタッピー SXJ-90A の公表値", 15, MUTE)
    f.text(px, 400, 460, 30, "38cm 足りません", 24, WARN, bold=True)
    f.text(px, 440, 520, 24, "踏面が広い階段でも2段離れるので、", 15, MUTE)
    f.text(px, 468, 520, 24, "必要なのは32cm以上でした", 15, MUTE)

    f.footer("伸縮脚では、住宅の階段の高低差に届きません。")


def kyatatsu_fumidai(f):
    """天板は0.79mと0.81mでほぼ同じ。足を置ける高さは0.79mと0.50mに分かれる。"""
    f.header("天板は同じでも足場の高さが違う",
             "横から見た図 ／ 同じ0.8m前後の2製品を並べています",
             key="0.50", key_label="脚立で立てるのは", key_unit="m")

    sc = 185.0
    base = 500
    x = 150
    f.bar(x, base - 0.79 * sc, 170, 0.79 * sc, PALE2, PALE, NAVY, 2, radius=0.03)
    f.ghost(x + 20, base - 1.40 * sc, 130, (1.40 - 0.79) * sc, NAVY)
    f.text(x, base - 1.40 * sc - 32, 300, 26, "全高 1.40m", 17, MUTE)
    f.text(x + 190, base - 1.06 * sc, 250, 26, "上わく ＋61cm", 17, NAVY, bold=True)
    f.text(x + 190, base - 0.79 * sc, 250, 26, "天板 0.79m", 17, INK, bold=True)
    f.text(x, base + 10, 320, 24, "踏台（上わく付き）", 16, INK, bold=True)
    f.text(x, base + 32, 320, 22, "長谷川工業 EFA-08", 15, MUTE)

    x = 700
    f.bar(x, base - 0.81 * sc, 170, 0.81 * sc, BAND, BAND, MUTE, 2, radius=0.03)
    f.bar(x, base - 0.50 * sc, 170, 0.50 * sc, PALE2, PALE, NAVY, 2, radius=0.03)
    f.text(x + 190, base - 0.81 * sc, 250, 26, "天板 0.81m", 17, MUTE, bold=True)
    f.text(x + 190, base - 0.50 * sc, 250, 26, "使用最大 0.50m", 17, NAVY, bold=True)
    f.text(x, base + 10, 320, 24, "はしご兼用脚立", 16, INK, bold=True)
    f.text(x, base + 32, 320, 22, "長谷川工業 RHB-09a", 15, MUTE)

    f.footer("天板は0.79mと0.81m。足を置ける高さは0.79mと0.50mに分かれます。")

def coolerbox_omosa_eyecatch(f):
    """自重は満載重量の一部。軽さで選んでも満載では逆転する。

    ⚠️ 元の SVG が無い（新規に起こした図）ので、build の数値照合は効かない。
    値は `site/content/articles/coolerbox-omosa.md` の表から取っている。
    """
    f.header("中身を入れると何kgになる？",
             "濃い色が自重（メーカー公表）、薄い色まで伸びると満載の上限",
             key="91", key_label="80Lは満載で", key_unit="kg")

    # 自重の軽い順。**並べ替えると満載の順序がそろわない**のがこの図の言いたいこと
    data = [("ロゴス ハイパー氷点下クーラーL", "20L", 1.5, 21.5),
            ("ダイワ クールラインα3 S1000X", "10L", 2.1, 12.1),
            ("ダイワ クールラインα3 S2000", "20L", 3.7, 23.7),
            ("コールマン 50QT", "約47L", 6.3, 53.3),
            ("コールマン 62QT", "約58L", 6.3, 64.3),
            ("ダイワ トランクマスターHD III 8000", "80L", 11.0, 91.0)]
    x0, sc, top, rh = 470, 6.1, 182, 62
    ys = f.rows(len(data), top=top, rh=rh, highlight=len(data) - 1)
    for (name, cap, own, full), y in zip(data, ys):
        f.bar(x0, y + 14, full * sc, 28, PALE2, PALE, NAVY, 2, radius=0.30)
        f.bar(x0, y + 14, own * sc, 28, NAVY2, NAVY, None, radius=0.40)
        f.text(74, y + 8, 380, 24, name, 16, INK, bold=True)
        f.text(74, y + 32, 380, 22, f"{cap} ／ 自重 {own}kg", 14, MUTE)
        f.text(x0 + full * sc + 12, y + 14, 120, 28, f"{full}kg", 18, NAVY, bold=True)

    f.footer("自重がいちばん軽い1.5kgの製品が、満載では21.5kgになります。")

# ---------------------------------------------------------------- 土鍋：号数と人数

# 銀峯陶器の公表値（18製品）。号数ごとの容量のはばと、目安人数のはば。
NINZUU = [
    # 号数, 容量の下限(ℓ), 容量の上限(ℓ), 目安人数のはば
    ("6号", 0.6, 0.9, "1人前"),
    ("7号", 1.0, 1.5, "1〜2人前"),
    ("8号", 1.5, 2.2, "1〜3人前"),
    ("9号", 2.2, 3.2, "2〜5人前"),
    ("10号", 2.9, 4.0, "3〜6人前"),
]


def donabe_ninzuu_eyecatch(f):
    """号数は口径を決めるが、容量は決めない。号数ごとの容量のはばを面で見せる。"""
    f.header("同じ9号でも、容量は1.45倍ちがう",
             "銀峯陶器18製品の公表値。濃い色が下限、薄い色までが号数ごとのはば",
             key="1.45", key_label="9号のなかで", key_unit="倍")

    x0, sc, top, rh = 250, 128.0, 190, 70
    ys = f.rows(len(NINZUU), top=top, rh=rh, highlight=3)
    for (name, lo, hi, ppl), y in zip(NINZUU, ys):
        f.bar(x0, y + 16, hi * sc, 32, PALE2, PALE, NAVY, 2, radius=0.22)
        f.bar(x0, y + 16, lo * sc, 32, NAVY2, NAVY, None, radius=0.30)
        f.text(74, y + 16, 160, 32, name, 21, INK, bold=True)
        # ⚠️ ラベルは棒の右端に追従させず、列を固定する（号数で長さが変わるとガタつく）
        f.text(800, y + 16, 170, 32, f"{lo}〜{hi}ℓ", 18, NAVY, bold=True)
        f.text(980, y + 16, 200, 32, ppl, 17, MUTE)

    f.footer("号数が決めているのは口径だけで、容量と人数は決めていません。",
             note="メーカー公表値です（実測ではありません）")


def donabe_ninzuu(f):
    """同じ9号の4製品。口径はほぼ同じで、深さと容量と人数が違う。"""
    f.header("同じ9号で、2〜3人前 と 4〜5人前",
             "銀峯陶器の公表値。口径の差は0.5cmしかありません",
             key="1.45", key_label="容量の差", key_unit="倍")

    data = [("墨貫入 9号", 28, 15, 2.2, "2〜3人前"),
            ("菊花 9号", 28.5, 15.5, 2.7, "3〜4人前"),
            ("菊花 深型 9号", 28.5, 17, 3.0, "4〜5人前"),
            ("花三島 9号", 28, 16, 3.2, "4〜5人前")]
    x0, sc, top, rh = 420, 105.0, 200, 78
    ys = f.rows(len(data), top=top, rh=rh, highlight=0)
    for (name, dia, h, cap, ppl), y in zip(data, ys):
        f.bar(x0, y + 18, cap * sc, 34, PALE2, PALE, NAVY, 2, radius=0.28)
        f.text(74, y + 10, 330, 26, name, 19, INK, bold=True)
        f.text(74, y + 38, 330, 22, f"口径{dia:g}cm ／ 高さ{h:g}cm", 15, MUTE)
        f.text(x0 + cap * sc + 14, y + 18, 110, 34, f"{cap}ℓ", 20, NAVY, bold=True)
        f.text(1000, y + 18, 170, 34, ppl, 18, WARN, bold=True)

    f.footer("口径が同じでも、深さが違えば入る量が変わります。")


# ---------------------------------------------------------------- スーツケース：40Lは何泊

# 社, 泊の下限, 泊の上限, 右に出す注記。40L の目安（製品ごとの公表しかない社は 36〜40L の製品）
NANPAKU = [
    ("Legend Walker", 1, 2, "27〜41Lの帯"),
    ("ace",           2, 3, "30〜49Lの帯"),
    ("ニトリ",        2, 3, "40L製品"),
    ("無印良品",      2, 3, "36L製品"),
    ("RIMOWA",        3, 4, "36〜37L製品"),
    ("サムソナイト",  4, 4, "1泊＝10Lで計算"),
]


def liter_nanpaku_eyecatch(f):
    """同じ40Lで、社ごとの泊数の目安がどれだけ開くか。横棒の左端が最短、右端が最長。"""
    f.header("同じ40Lで、1〜2泊 から 4泊",
             "6社の公表目安を横に並べたもの。棒の左端が最短、右端が最長の泊数",
             key="2", key_label="40Lの目安の開き", key_unit="倍")

    x0, sc, top, rh = 330, 150.0, 200, 58
    # 目盛り（1〜5泊）
    for n in range(1, 6):
        f.text(x0 + n * sc - 40, 170, 80, 22, f"{n}泊", 15, MUTE, align=PP_ALIGN.CENTER)
    ys = f.rows(len(NANPAKU), top=top, rh=rh, highlight=None)
    for (name, lo, hi, note), y in zip(NANPAKU, ys):
        w = max((hi - lo) * sc, 14)
        x = x0 + lo * sc - (7 if hi == lo else 0)
        c1, c2 = (NAVY2, NAVY) if name in ("Legend Walker", "サムソナイト") else (PALE2, PALE)
        f.bar(x, y + 11, w, 28, c1, c2, NAVY, 2, radius=0.3)
        f.text(74, y + 11, 240, 28, name, 20, INK, bold=True)
        label = f"{lo}泊" if lo == hi else f"{lo}〜{hi}泊"
        f.text(x + w + 12, y + 11, 90, 28, label, 18, NAVY, bold=True)
        f.text(x + w + 104, y + 13, 190, 24, note, 14, MUTE)

    f.footer("泊数は容量から決まらず、社ごとの目安です。60L以上は各社4〜7泊に収まります。",
             note="メーカー公表の目安です（実測ではありません）")


# ---------------------------------------------------------------- ベビーゲート

BABY_GATE = [
    # 製品短縮名, 本体レンジ表記, 最大(追加込み), 開口100での読み
    ("日本育児（本体）",   "67〜91",  91,  "本体では届かない"),
    ("日本育児＋ワイドS",  "91〜115", 115, "ワイドパネルS側"),
    ("カトージ LDK-STYLEⅡ","〜95",   95,  "最大95で外れる"),
    ("リッチェル＋拡張1",  "91〜104", 104, "拡張1本側"),
]


def baby_gate_opening_width_fit_eyecatch(f):
    """開口100cmは本体レンジを超え、カトージ最大95で外れる。"""
    f.header("開口100cmは、本体では届かない",
             "公表の取付幅レンジに当てると、カトージは外れ、日本育児はワイドS側",
             key="95", key_label="カトージの最大", key_unit="cm")

    x0, sc, top, rh = 360, 6.0, 186, 70
    # 目盛り
    for n in (70, 80, 90, 100, 110):
        f.text(x0 + (n - 67) * sc - 20, 162, 50, 20, f"{n}", 13, MUTE, align=PP_ALIGN.CENTER)
    # 開口100の縦線
    mark = x0 + (100 - 67) * sc
    f.rect(mark, 180, 2, 4 * rh + 8, WARN)
    # 目盛りの100は上で出したので、縦線ラベルは行わず重なりを避ける

    ys = f.rows(len(BABY_GATE), top=top, rh=rh, highlight=2)
    for (name, rng, hi, note), y in zip(BABY_GATE, ys):
        # レンジ幅は表記から雑に。hi-lo で棒
        lo = 67 if "67" in rng or rng.startswith("〜") else int(rng.split("〜")[0])
        w = max((hi - lo) * sc, 8)
        x = x0 + (lo - 67) * sc
        hot = hi < 100
        c1, c2 = (WARNB, WARN) if hot else (NAVY2, NAVY)
        f.bar(x, y + 16, w, 28, c1, c2, NAVY if not hot else WARN, 2, radius=0.3)
        f.text(64, y + 12, 280, 26, name, 17, INK, bold=True)
        f.text(64, y + 38, 280, 22, f"{rng}cm", 14, MUTE)
        f.text(x + w + 12, y + 16, 200, 28, note, 15, WARN if hot else NAVY, bold=True)

    f.footer("「対応幅」見出しではなく、パーツごとの取付幅レンジで判定します。")


# ---------------------------------------------------------------- スーツケース：機内持ち込み

AIRLINE_ROWS = [
    # 製品短縮, ≥100席, <100席, Peach, Jetstar
    ("ace パリセイド3-Z",     "○", "×", "○", "×"),
    ("PROTECA スタリアCXR",   "○", "○", "○", "○"),
    ("EDGELINK（通常）",      "○", "×", "○", "×"),
    ("EDGELINK（拡張）",      "×", "×", "×", "×"),
    ("Legend Walker 5516-48", "○", "×", "○", "×"),
]


def cabin_bag_airline_fit_outer_dims_eyecatch(f):
    """機内持ち込み表記でも、全列○はPROTECAだけ。"""
    f.header("全列○は PROTECA だけ",
             "メーカー外寸を ANA/JAL・100席未満・Peach・Jetstar に当てた結果",
             key="115", key_label="ANA/JALの和上限", key_unit="cm")

    cols = [("≥100席", 430), ("＜100席", 560), ("Peach", 690), ("Jetstar", 820)]
    for label, x in cols:
        f.text(x, 168, 110, 22, label, 14, MUTE, align=PP_ALIGN.CENTER)

    ys = f.rows(len(AIRLINE_ROWS), top=196, rh=54, highlight=1)
    for (name, a, b, c, d), y in zip(AIRLINE_ROWS, ys):
        f.text(64, y + 12, 340, 28, name, 17, INK, bold=True)
        for val, x in zip((a, b, c, d), (430, 560, 690, 820)):
            color = NAVY if val == "○" else WARN
            f.text(x, y + 12, 110, 28, val, 22, color, bold=True, align=PP_ALIGN.CENTER)

    f.footer("「機内持ち込み対応」でも、Jetstarと100席未満で落ちる製品が多いです。")


# ---------------------------------------------------------------- 本体 vs 外寸

BODY_OUTER = [
    ("PROTECA スタリアCXR", 6),
    ("PROTECA ポケットライナー2", 8),
    ("Legend Walker 5516-48", 11),
    ("ace フレットボード 68L", 10),
    ("ace フレットボード 100L", 9),
]


def cabin_bag_body_vs_outer_dims_eyecatch(f):
    """本体と外寸の3辺和差は6〜11cm。見るのは外寸側。"""
    f.header("3辺和の差は 6〜11cm",
             "公式併記の本体サイズと外寸／全体。差の主因は高さ（キャスター＋ハンドル）",
             key="11", key_label="いちばん大きい差", key_unit="cm")

    x0, sc, top, rh = 420, 48.0, 186, 58
    for n in range(0, 13, 2):
        f.text(x0 + n * sc - 16, 162, 40, 20, f"{n}", 13, MUTE, align=PP_ALIGN.CENTER)
    ys = f.rows(len(BODY_OUTER), top=top, rh=rh, highlight=2)
    for (name, delta), y in zip(BODY_OUTER, ys):
        w = delta * sc
        hot = delta == 11
        c1, c2 = (NAVY2, NAVY) if hot else (PALE2, PALE)
        f.bar(x0, y + 14, w, 26, c1, c2, NAVY, 2, radius=0.3)
        f.text(64, y + 14, 340, 28, name, 17, INK, bold=True)
        f.text(x0 + w + 12, y + 14, 80, 28, f"{delta}cm", 18, NAVY, bold=True)

    f.footer("判定に使うのは外寸／全体（キャスター・ハンドル込み）。本体サイズではありません。")


# ---------------------------------------------------------------- 拡張 vs 固定

EXPAND = [
    ("EDGELINK CRUZBOX", 4, "114→118"),
    ("PROTECA フレスターEX", 4, "115→119"),
    ("ACE クレスタ", 4, "115→119"),
    ("Legend Walker 5109-46", 5, "115→120"),
    ("Legend Walker 5525-48", 7, "115→122"),
]


def cabin_bag_expandable_vs_fixed_outer_dims_eyecatch(f):
    """拡張で動くのは奥行だけ。増分4〜7cm。"""
    f.header("拡張で増えるのは奥行だけ",
             "高さ・幅は0。3辺和の増分も奥行と同じ 4〜7cm",
             key="7", key_label="いちばん大きい増分", key_unit="cm")

    x0, sc, top, rh = 420, 70.0, 186, 58
    for n in range(0, 9, 2):
        f.text(x0 + n * sc - 16, 162, 40, 20, f"+{n}", 13, MUTE, align=PP_ALIGN.CENTER)
    ys = f.rows(len(EXPAND), top=top, rh=rh, highlight=4)
    for (name, delta, note), y in zip(EXPAND, ys):
        w = delta * sc
        hot = delta == 7
        c1, c2 = (NAVY2, NAVY) if hot else (PALE2, PALE)
        f.bar(x0, y + 14, w, 26, c1, c2, NAVY, 2, radius=0.3)
        f.text(64, y + 14, 340, 28, name, 17, INK, bold=True)
        f.text(x0 + w + 12, y + 14, 70, 28, f"+{delta}cm", 17, NAVY, bold=True)
        f.text(x0 + w + 90, y + 16, 140, 24, note, 14, MUTE)

    f.footer("機内持ち込み帯（114〜115）は拡張後118〜122。預け入れ天井帯も超え得ます。")


# ---------------------------------------------------------------- 158cm vs リットル

SUM158 = [
    ("ace フレットボード 68L", 151, 68),
    ("Legend Walker 5516-70", 155, 81),
    ("Legend Walker 5528-70", 157, 87),
    ("Samsonite シーライト75", 157, 94),
    ("ace フレットボード 100L", 157, 100),
]


def cabin_bag_outer_sum_158_liters_eyecatch(f):
    """同じ157帯でも容量は68L級から100Lまで。"""
    f.header("同じ157帯でも 68L〜100L",
             "総外寸158cm以内は預け入れの帯。容量（L）の代理ではありません",
             key="100", key_label="157帯の上限側", key_unit="L")

    x0, sc, top, rh = 400, 8.5, 186, 58
    for n in (60, 70, 80, 90, 100):
        f.text(x0 + (n - 60) * sc - 16, 162, 40, 20, f"{n}", 13, MUTE, align=PP_ALIGN.CENTER)
    ys = f.rows(len(SUM158), top=top, rh=rh, highlight=4)
    for (name, outer, lit), y in zip(SUM158, ys):
        w = (lit - 60) * sc
        hot = lit == 100
        c1, c2 = (NAVY2, NAVY) if hot else (PALE2, PALE)
        f.bar(x0, y + 14, max(w, 8), 26, c1, c2, NAVY, 2, radius=0.3)
        f.text(64, y + 10, 320, 24, name, 16, INK, bold=True)
        f.text(64, y + 34, 320, 20, f"総外寸 {outer}cm", 13, MUTE)
        f.text(x0 + max(w, 8) + 12, y + 14, 70, 28, f"{lit}L", 18, NAVY, bold=True)

    f.footer("151cmの68Lから158cmの100Lまで。総外寸が近くても容量は約1.5倍開きます。")


# ---------------------------------------------------------------- 新幹線

SHINKANSEN = [
    ("ace パリセイド3-Z", 115),
    ("PROTECA スタリアCXR", 99),
    ("EDGELINK（通常）", 114),
    ("EDGELINK（拡張）", 118),
    ("Legend Walker 5516-48", 115),
]


def cabin_bag_shinkansen_fit_outer_dims_eyecatch(f):
    """機内持ち込み級はいずれも3辺和160以下。特大予約は不要。"""
    f.header("機内持込級は、特大の手前",
             "東海道・山陽・九州・西九州の特大荷物は3辺和160cm超。照合5製品はすべて以下",
             key="160", key_label="特大のしきい値", key_unit="cm")

    x0, sc, top, rh = 360, 4.0, 186, 58
    for n in (100, 120, 140, 160, 180):
        f.text(x0 + (n - 90) * sc - 18, 162, 50, 20, f"{n}", 13, MUTE, align=PP_ALIGN.CENTER)
    # 160線
    mark = x0 + (160 - 90) * sc
    f.rect(mark, 180, 2, 5 * rh + 8, WARN)

    ys = f.rows(len(SHINKANSEN), top=top, rh=rh, highlight=None)
    for (name, s), y in zip(SHINKANSEN, ys):
        w = (s - 90) * sc
        f.bar(x0, y + 14, w, 26, PALE2, PALE, NAVY, 2, radius=0.3)
        f.text(64, y + 14, 280, 28, name, 17, INK, bold=True)
        f.text(x0 + w + 12, y + 14, 100, 28, f"{s}cm", 18, NAVY, bold=True)

    f.footer("航空機では落ちる外寸でも、新幹線の160までは余裕があります。")


# ---------------------------------------------------------------- カーテン

CURTAIN_W = [
    ("レール170cm", 178.5, True),
    ("レール180cm", 189.0, True),
    ("レール190cm", 199.5, True),
    ("レール195cm", 204.8, False),
    ("レール200cm", 210.0, False),
]


def curtain_ready_made_rail_fit_eyecatch(f):
    """レール×1.05ゆとり。195cmでは幅100×2（合計200）が足りない。"""
    f.header("レール195cmは、幅100×2不足",
             "必要仕上がり幅＝レール×1.05。合計200の既製両開きに当てた結果",
             key="195", key_label="幅100×2の限界超え", key_unit="cm")

    x0, sc, top, rh = 360, 8.0, 186, 58
    # 200の線
    mark = x0 + (200 - 170) * sc
    f.rect(mark, 180, 2, 5 * rh + 8, NAVY)
    f.text(mark - 50, 162, 110, 20, "既製合計200", 13, NAVY, bold=True)

    ys = f.rows(len(CURTAIN_W), top=top, rh=rh, highlight=3)
    for (name, need, ok), y in zip(CURTAIN_W, ys):
        w = (need - 170) * sc
        c1, c2 = (PALE2, PALE) if ok else (WARNB, WARN)
        f.bar(x0, y + 14, max(w, 8), 26, c1, c2, NAVY if ok else WARN, 2, radius=0.3)
        f.text(64, y + 14, 280, 28, name, 18, INK, bold=True)
        label = f"必要{need:g} → ○" if ok else f"必要{need:g} → ×"
        f.text(x0 + max(w, 8) + 12, y + 14, 220, 28, label, 16, NAVY if ok else WARN, bold=True)

    f.footer("丈は床ルール次第。ニトリ式（床−1）と無印式（床−2）で178／200の向きが分かれます。")


# ---------------------------------------------------------------- 食洗機

DISHWASHER = [
    ("Panasonic NP-TH5", 550, "× 450すき間"),
    ("Panasonic NP-TCR5", 470, "× 450すき間"),
    ("東芝 DWS-33B", 420, "○ 420幅"),
    ("アイリス ISHT-5000", 420, "○ 420幅"),
    ("Panasonic NP-TML1", 310, "○ 310幅"),
]


def dishwasher_countertop_fit_outer_dims_eyecatch(f):
    """450mm級すき間に入るのは420幅と310幅。550／470は入らない。"""
    f.header("450mmすき間に入る幅は限られる",
             "想定すき間幅450mmに、公表の本体幅Wを当てた結果",
             key="310", key_label="いちばん細い本体", key_unit="mm")

    x0, sc, top, rh = 400, 1.15, 186, 58
    mark = x0 + 450 * sc
    f.rect(mark, 180, 2, 5 * rh + 8, WARN)
    f.text(mark - 50, 162, 120, 20, "すき間450", 13, WARN, bold=True)

    ys = f.rows(len(DISHWASHER), top=top, rh=rh, highlight=4)
    for (name, wmm, note), y in zip(DISHWASHER, ys):
        ok = wmm <= 450
        c1, c2 = (NAVY2, NAVY) if ok else (WARNB, WARN)
        f.bar(x0, y + 14, wmm * sc, 26, c1, c2, NAVY if ok else WARN, 2, radius=0.3)
        f.text(64, y + 14, 320, 28, name, 16, INK, bold=True)
        f.text(x0 + wmm * sc + 10, y + 14, 200, 28, f"{wmm}mm {note}", 15, NAVY if ok else WARN, bold=True)

    f.footer("閉時奥行は全機種とも想定カウンター600mmに収まります。ドア全開奥行は機種で差が出ます。")


# ---------------------------------------------------------------- 冷蔵庫

FRIDGE = [
    ("Panasonic NR-C37WS2", 600, 200),
    ("シャープ SJ-MF51R", 630, 170),
    ("Panasonic NR-F55WX3", 699, 101),
    ("三菱 MR-WZ61N", 738, 62),
    ("東芝 GR-W600FZS", 745, 55),
]


def fridge_delivery_path_fit_eyecatch(f):
    """想定通路800mmから本体奥行を引く。745mm級は余り55mm。"""
    f.header("奥行745mmで、余りは55mm",
             "想定通路幅800mm − 本体奥行。曲がり角は含まない引き算",
             key="55", key_label="800mm通路の余り", key_unit="mm")

    x0, sc, top, rh = 400, 1.0, 186, 58
    for n in (600, 650, 700, 750, 800):
        f.text(x0 + (n - 580) * sc - 20, 162, 50, 20, f"{n}", 12, MUTE, align=PP_ALIGN.CENTER)
    mark = x0 + (800 - 580) * sc
    f.rect(mark, 180, 2, 5 * rh + 8, WARN)

    ys = f.rows(len(FRIDGE), top=top, rh=rh, highlight=4)
    for (name, depth, rest), y in zip(FRIDGE, ys):
        w = (depth - 580) * sc
        hot = rest == 55
        c1, c2 = (NAVY2, NAVY) if hot else (PALE2, PALE)
        f.bar(x0, y + 14, max(w, 8), 26, c1, c2, NAVY, 2, radius=0.3)
        f.text(64, y + 10, 320, 24, name, 16, INK, bold=True)
        f.text(64, y + 34, 320, 20, f"奥行 {depth}mm", 13, MUTE)
        f.text(x0 + max(w, 8) + 12, y + 14, 160, 28, f"余り {rest}mm", 17, NAVY, bold=True)

    f.footer("容量Lではなく本体奥行で判定。メーカーの「幅＋約10cm」は直立搬入の別軸です。")


FRIDGE_SWING = [
    # 製品名, 本体幅(mm), 扉の横張り出し・図の右側(mm), 表示
    ("Panasonic NR-F55WX3", 685, 361, "361mm"),
    ("シャープ SJ-MF55R", 730, 305, "305mm"),
    ("東芝 GR-W600FZS", 685, 301, "301mm"),
    ("三菱 MR-WZ61N", 685, 269, "269mm"),
    ("日立 R-HZC54Y", 650, 235, "約235mm"),
]


def fridge_side_top_clearance_door_swing_eyecatch(f):
    """左右あきは各5mmで揃うが、扉の横張り出しは機種で大きく違う。"""
    f.header("扉は本体の横へ最大361mm出る",
             "左右あきは各5mmで同じ。違うのは扉を開けたときの横張り出し",
             key="361", key_label="横張り出しの最大", key_unit="mm")

    x0, sc, top, rh = 400, 1.4, 186, 58
    ys = f.rows(len(FRIDGE_SWING), top=top, rh=rh, highlight=0)
    for (name, width, swing, label), y in zip(FRIDGE_SWING, ys):
        hot = swing == 361
        c1, c2 = (NAVY2, NAVY) if hot else (PALE2, PALE)
        f.bar(x0, y + 14, swing * sc, 26, c1, c2, NAVY, 2, radius=0.3)
        f.text(64, y + 10, 320, 24, name, 16, INK, bold=True)
        f.text(64, y + 34, 320, 20, f"本体幅 {width}mm", 13, MUTE)
        f.text(x0 + swing * sc + 12, y + 14, 160, 28, label, 17, NAVY, bold=True)

    f.footer("壁際で扉が十分に開かないときは、壁から10〜20mm（機種による）。")


# ---------------------------------------------------------------- モニターアーム

MONITOR = [
    ("サンワ CR-LAC1405BK", 10, 50),
    ("サンワ CR-LAC116BK", 10, 50),
    ("Ergotron LX", 10, 60),
    ("エレコム DPA-SN01BK", 10, 80),
    ("HUANUO SS43", 20, 89),
]


def monitor_arm_desk_thickness_clamp_fit_eyecatch(f):
    """天板55mmでサンワ50mm上限は外れる。"""
    f.header("天板55mmで、上限50は外れる",
             "公表クランプ可能厚に天板厚を当てる。耐荷重やインチではない",
             key="55", key_label="サンワ50上限が外れる", key_unit="mm")

    x0, sc, top, rh = 380, 7.0, 186, 58
    for n in (10, 30, 50, 70, 90):
        f.text(x0 + (n - 10) * sc - 16, 162, 40, 20, f"{n}", 13, MUTE, align=PP_ALIGN.CENTER)
    mark = x0 + (55 - 10) * sc
    f.rect(mark, 180, 2, 5 * rh + 8, WARN)
    f.text(mark - 30, 162, 80, 20, "天板55", 13, WARN, bold=True)

    ys = f.rows(len(MONITOR), top=top, rh=rh, highlight=0)
    for (name, lo, hi), y in zip(MONITOR, ys):
        w = (hi - lo) * sc
        x = x0 + (lo - 10) * sc
        ok = lo <= 55 <= hi
        c1, c2 = (NAVY2, NAVY) if ok else (WARNB, WARN)
        f.bar(x, y + 14, w, 26, c1, c2, NAVY if ok else WARN, 2, radius=0.3)
        f.text(64, y + 14, 300, 28, name, 16, INK, bold=True)
        f.text(x + w + 10, y + 14, 140, 28, f"{lo}〜{hi}mm", 16, NAVY if ok else WARN, bold=True)

    f.footer("○は天板厚が公表クランプ可能厚レンジに入るときだけです。")


# ---------------------------------------------------------------- タイヤチェーン

TIRE = [
    ("S（QE1〜QE7L）", 124, 524, 401),
    ("M（QE10〜QE14）", 139, 539, 431),
    ("L（QE14L〜QE20）", 168, 539, 381),
]


def tire_chain_case_size_trunk_fit_eyecatch(f):
    """Lは高いが奥行はMより50mm浅い。ヤリス荷室には1ケースいずれも入る。"""
    f.header("Lは高いが、奥行は浅い",
             "カーメイト バイアスロンのケース外寸。品番が大きい＝全部が大きい、ではない",
             key="50", key_label="LがMより浅い", key_unit="mm")

    # 3本の棒：H / W / D をグループ化して見せる
    metrics = [("高さ H", 0), ("幅 W", 1), ("奥行 D", 2)]
    vals = {
        "高さ H": [124, 139, 168],
        "幅 W": [524, 539, 539],
        "奥行 D": [401, 431, 381],
    }
    scales = {"高さ H": 1.8, "幅 W": 0.55, "奥行 D": 0.7}
    labels = ["S", "M", "L"]
    xs = [100, 420, 740]
    for (title, _), x in zip(metrics, xs):
        f.text(x, 170, 280, 24, title, 18, INK, bold=True)
        sc = scales[title]
        base = min(vals[title]) - 20
        for i, (lab, v) in enumerate(zip(labels, vals[title])):
            y = 210 + i * 70
            w = (v - base) * sc
            hot = (title == "奥行 D" and lab == "L") or (title == "高さ H" and lab == "L")
            c1, c2 = (NAVY2, NAVY) if hot else (PALE2, PALE)
            f.bar(x + 40, y, w, 28, c1, c2, NAVY, 2, radius=0.3)
            f.text(x, y, 36, 28, lab, 18, INK, bold=True)
            f.text(x + 40 + w + 8, y, 90, 28, f"{v}mm", 16, NAVY, bold=True)

    f.footer("ヤリス公表荷室（長630×幅1,000×高692）には S／M／Lいずれも1ケースは収まります。")


ORDER = [
    "liter-nanpaku-eyecatch",
    "baby-gate-opening-width-fit-eyecatch",
    "cabin-bag-airline-fit-outer-dims-eyecatch",
    "cabin-bag-body-vs-outer-dims-eyecatch",
    "cabin-bag-expandable-vs-fixed-outer-dims-eyecatch",
    "cabin-bag-outer-sum-158-liters-eyecatch",
    "cabin-bag-shinkansen-fit-outer-dims-eyecatch",
    "curtain-ready-made-rail-fit-eyecatch",
    "dishwasher-countertop-fit-outer-dims-eyecatch",
    "fridge-delivery-path-fit-eyecatch",
    "fridge-side-top-clearance-door-swing-eyecatch",
    "monitor-arm-desk-thickness-clamp-fit-eyecatch",
    "tire-chain-case-size-trunk-fit-eyecatch",
    "donabe-ninzuu-eyecatch",
    "donabe-ninzuu",
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
    "bottle-height-chart",
    "coolerbox-floorplan",
    "coolerbox-daiwa-shimano-yuka",
    "coolerbox-horeizai-oki",
    "coolerbox-nagasa-diagonal",
    "coolerbox-yoryo-danmen",
    "coolerbox-erabikata-eyecatch",
    "konro-donabe-haba",
    "kyatatsu-takasa",
    "kyatatsu-omosa",
    "kyatatsu-kaidan",
    "kyatatsu-fumidai",
    "coolerbox-omosa-eyecatch",
]

FIGURES = {
    "liter-nanpaku-eyecatch": liter_nanpaku_eyecatch,
    "baby-gate-opening-width-fit-eyecatch": baby_gate_opening_width_fit_eyecatch,
    "cabin-bag-airline-fit-outer-dims-eyecatch": cabin_bag_airline_fit_outer_dims_eyecatch,
    "cabin-bag-body-vs-outer-dims-eyecatch": cabin_bag_body_vs_outer_dims_eyecatch,
    "cabin-bag-expandable-vs-fixed-outer-dims-eyecatch": cabin_bag_expandable_vs_fixed_outer_dims_eyecatch,
    "cabin-bag-outer-sum-158-liters-eyecatch": cabin_bag_outer_sum_158_liters_eyecatch,
    "cabin-bag-shinkansen-fit-outer-dims-eyecatch": cabin_bag_shinkansen_fit_outer_dims_eyecatch,
    "curtain-ready-made-rail-fit-eyecatch": curtain_ready_made_rail_fit_eyecatch,
    "dishwasher-countertop-fit-outer-dims-eyecatch": dishwasher_countertop_fit_outer_dims_eyecatch,
    "fridge-delivery-path-fit-eyecatch": fridge_delivery_path_fit_eyecatch,
    "fridge-side-top-clearance-door-swing-eyecatch": fridge_side_top_clearance_door_swing_eyecatch,
    "monitor-arm-desk-thickness-clamp-fit-eyecatch": monitor_arm_desk_thickness_clamp_fit_eyecatch,
    "tire-chain-case-size-trunk-fit-eyecatch": tire_chain_case_size_trunk_fit_eyecatch,
    "donabe-ninzuu-eyecatch": donabe_ninzuu_eyecatch,
    "donabe-ninzuu": donabe_ninzuu,
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
    "bottle-height-chart": bottle_height_chart,
    "coolerbox-floorplan": coolerbox_floorplan,
    "coolerbox-daiwa-shimano-yuka": coolerbox_daiwa_shimano_yuka,
    "coolerbox-horeizai-oki": coolerbox_horeizai_oki,
    "coolerbox-nagasa-diagonal": coolerbox_nagasa_diagonal,
    "coolerbox-yoryo-danmen": coolerbox_yoryo_danmen,
    "coolerbox-erabikata-eyecatch": coolerbox_erabikata_eyecatch,
    "konro-donabe-haba": konro_donabe_haba,
    "kyatatsu-takasa": kyatatsu_takasa,
    "kyatatsu-omosa": kyatatsu_omosa,
    "kyatatsu-kaidan": kyatatsu_kaidan,
    "kyatatsu-fumidai": kyatatsu_fumidai,
    "coolerbox-omosa-eyecatch": coolerbox_omosa_eyecatch,
}
