# -*- coding: utf-8 -*-
"""図版を PowerPoint で作り、PNG に書き出す。

```
python tools/figures/build.py            # 全部
python tools/figures/build.py 名前 名前   # 指定したものだけ
```

出るもの:
  site/public/img/figures.pptx   … 編集できるマスター（1スライド = 1図版）
  site/public/img/<name>.png     … 記事が読む画像（2400x1260 で焼いて等倍表示）

⚠️ **PNG は生成物。直接いじらない。** 直すときは figures.py を直して焼き直す。
⚠️ **pptx を PowerPoint で編集したら、`--from-pptx` で PNG だけ焼き直せる**
   （figures.py からは作り直さない。手で入れた変更が消えるため）。
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image
from pptx import Presentation

import deck
import figures as figmod

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG = os.path.join(ROOT, "site", "public", "img")
THUMB = os.path.join(IMG, "thumb")
THUMB_W = 480          # 一覧のサムネの幅。CSS の枠は240px なので、2倍のディスプレイで等倍。
                       # モバイルは本文幅いっぱい（最大560px）まで広がるが、
                       # ここは図の「棒の並びと差の向き」が見えれば足りる（文字は本文の役目）
ARTICLES = os.path.join(ROOT, "site", "content", "articles")
PPTX = os.path.join(IMG, "figures.pptx")
SCALE = 2
COLORS = 256

SOFFICE = [
    r"C:/Program Files/LibreOffice/program/soffice.exe",
    r"C:/Program Files (x86)/LibreOffice/program/soffice.exe",
    "soffice",
]

sys.stdout.reconfigure(encoding="utf-8")


def find_soffice():
    for p in SOFFICE:
        if os.path.isfile(p):
            return p
    from shutil import which
    p = which("soffice")
    if p:
        return p
    raise SystemExit("LibreOffice が見つかりません（pptx → PNG の書き出しに要ります）")


# 「数値＋単位」で照合するための単位。長いものを先に並べる（mm を m より先に）
UNIT = "製品|本|枚|分|倍|つ|段|号|尺|kg|mm|cm|℃|%|g|m|L"
TOKEN = re.compile(r"(\d+(?:\.\d+)?)(%s)" % UNIT)


def norm(s):
    """比較用にそろえる。図は読みやすさのために空白を入れ、本文は入れない。"""
    return s.replace(" ", "").replace("　", "").replace("〜", "~").replace("～", "~")


def article_text(name):
    """この図を使っている記事の原稿。無ければ空リスト（SNS用の図など）。"""
    out = []
    for p in sorted(glob.glob(os.path.join(ARTICLES, "*.md"))):
        s = open(p, encoding="utf-8").read()
        if "/img/%s.png" % name in s:
            out.append((os.path.basename(p), norm(s)))
    return out


MM = {"mm": 1.0, "cm": 10.0, "m": 1000.0}


def _fmt(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def alternatives(num, unit):
    """同じ値の書き方を全部出す。**どれか1つ本文にあれば合格。**

    吸収するゆれは3つ：

    1. **単位**。図は読みやすさで cm、本文は公表値のまま mm（図「5.6cm」＝ 本文「56mm」）
    2. **末尾の0**（図「6.3cm」＝ 本文「6.30cm」）
    3. **単位を省いた寸法の並び**。本文は `334×274×89mm` と書くので「274mm」は文字列として
       存在しない。**桁数が3以上か小数点を持つ数値に限って**、単位なしの一致も認める。
       ⚠️ 1〜2桁は認めない。「26」を単位なしで通すと、本文の「26Lクラス」で
       「26製品」が合格してしまう（**2026-09-01 まで見逃していたのがこれ**）。
    """
    alts = {num + unit}
    units = MM if unit in MM else {unit: 1.0}
    base = float(num) * units.get(unit, 1.0)
    for u, k in units.items():
        s = _fmt(base / k)
        # ⚠️ **同じ単位のまま末尾の0を落とした形は認めない。**
        # 図の「3.0倍」を本文の「3倍」で通したところ、本文の別の話（「収納時の奥行は3倍以上」）に
        # 当たって合格してしまい、図と本文が 3.0倍 vs 2.2倍 で食い違ったまま通った
        # （2026-09-01。ブラウザで見て気づいた）。桁を落とす向きは当たりやすい。
        if u != unit or s == num:
            alts.add(s + u)
        # 桁を足す向きは具体的になるので認める（図「6.3cm」＝ 本文「6.30cm」）
        alts.add((s + "0" if "." in s else s + ".0") + u)
        if "." in s or len(s.lstrip("0").replace(".", "")) >= 3:
            alts.add(s)
    return alts


def figure_tokens(lines):
    """図に出ている「数値＋単位」。各要素は (図に出ている形, 許す書き方の集合)。"""
    out = {}
    for t in lines:
        for m in TOKEN.finditer(norm(t)):
            src = m.group(1) + m.group(2)
            out[src] = alternatives(m.group(1), m.group(2))
    return sorted(out.items())


def check_numbers(name, lines):
    """図に書いた数値が、**その図を使っている記事の本文**にあるか。

    ⚠️ **2026-09-01 まで、照合の相手は「元の SVG」だった。** それは PowerPoint 移行のときの
    打ち間違いを捕まえる検査で、**記事を書き直して数字が変わっても図が古いまま通る。**
    実際 `/coolerbox/erabikata/` が 26製品 → 33製品 になったとき、図だけ取り残されていた。
    移行は終わって前提が古くなったので、照合の相手を本文に取り替えた。

    返り値: None＝どの記事にも使われていない／[]＝合格／[…]＝本文に無い数値
    """
    arts = article_text(name)
    if not arts:
        return None
    return [src for src, alts in figure_tokens(lines)
            if not any(any(a in body for a in alts) for _, body in arts)]


def check_alt(name, lines):
    """記事に書いた alt の数字が、その図に実際に出ているか。

    ⚠️ **alt が別の図の説明になっている事故が実際に4件あった**（2026-09-01）。
    `kyatatsu-omosa` は 0.8m前後のグラフなのに、alt は 0.5〜0.6m の話を書いていた。
    読み上げでは中身と違う説明が読まれ、検索エンジンにも違う説明が渡る。
    数値の照合（check_numbers）は図→本文の向きなので、この向きは別に見る。
    """
    body = "".join(lines).replace(" ", "")
    bad = []
    for p in sorted(glob.glob(os.path.join(ARTICLES, "*.md"))):
        s = open(p, encoding="utf-8").read()
        for m in re.finditer(r"!\[([^\]]*)\]\(/img/%s\.png\)" % re.escape(name), s):
            for n in re.findall(r"\d+(?:\.\d+)?", m.group(1)):
                if n not in body:
                    bad.append("%s の alt の %s" % (os.path.basename(p), n))
    return sorted(set(bad))


def check_layout(f):
    """文字同士の重なりと、キャンバスからのはみ出しを総当たりで見る。

    ⚠️ **目視では見落とす。** CLAUDE.md が SVG に対して `getBBox()` を要求しているのと
    同じ理由で、PowerPoint 版でも機械で当たり判定を取る。幅は est_width の近似なので、
    **重なり2px までは許容**する（隣接する行の見かけ上の接触を拾わないため）。
    """
    out = []
    bs = f.boxes
    # 脚注の罫線（y=556）が通る帯には文字を置かない。
    # ⚠️ 文字同士の当たり判定だけでは拾えない（罫線は図形なので）。
    # 2026-09-01 に kyatatsu-fumidai で製品名が罫線に乗った。
    for x, y, w, h, t in bs:
        if y < 560 and y + h > 552:
            out.append(f"脚注の罫線に重なる「{t[:18]}」 y={y:.0f}..{y + h:.0f}")
    for i, (x, y, w, h, t) in enumerate(bs):
        if x < 0 or y < 0 or x + w > deck.W + 1 or y + h > deck.H + 1:
            out.append(f"はみ出し「{t[:18]}」 x={x:.0f}..{x + w:.0f} y={y:.0f}..{y + h:.0f}")
        for j in range(i + 1, len(bs)):
            X, Y, Wd, Ht, T = bs[j]
            ox = min(x + w, X + Wd) - max(x, X)
            oy = min(y + h, Y + Ht) - max(y, Y)
            if ox > 2 and oy > 2:
                out.append(f"重なり「{t[:14]}」×「{T[:14]}」 {ox:.0f}x{oy:.0f}px")
    return out


def render(soffice, pptx, outdir):
    filt = ('png:impress_png_Export:{"PixelWidth":{"type":"long","value":%d},'
            '"PixelHeight":{"type":"long","value":%d}}' % (deck.W * SCALE, deck.H * SCALE))
    subprocess.run([soffice, "--headless", "--norestore", "--convert-to", filt,
                    "--outdir", outdir, pptx], capture_output=True, timeout=300)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--from-pptx", action="store_true",
                    help="figures.py から作り直さず、既存の figures.pptx から PNG だけ焼く")
    a = ap.parse_args()

    soffice = find_soffice()
    order = figmod.ORDER
    if a.names:
        unknown = [n for n in a.names if n not in order]
        if unknown:
            raise SystemExit(f"知らない図です: {unknown}\n使えるのは: {', '.join(order)}")

    if not a.from_pptx:
        prs = Presentation()
        prs.slide_width, prs.slide_height = deck.PX(deck.W), deck.PX(deck.H)
        blank = prs.slide_layouts[6]
        problems = []
        for name in order:
            f = deck.Fig(prs.slides.add_slide(blank))
            figmod.FIGURES[name](f)
            bad = check_numbers(name, f.lines)
            if bad is None:
                # どの記事にも貼られていない図（SNS用など）。黙って通さず、書き手に知らせる
                print(f"  ⚠ {name}: どの記事にも使われていないので数値の照合はできていません")
            elif bad:
                problems.append((name, f"本文に無い数値 {bad}"))
            alt = check_alt(name, f.lines)
            if alt:
                problems.append((name, f"図に無い数値が alt にある {alt}"))
            lay = check_layout(f)
            if lay:
                problems.append((name, "; ".join(lay[:3])))
        if problems:
            for n, b in problems:
                print(f"  ✗ {n}: {b}")
            raise SystemExit("figures.py を直してください")
        prs.save(PPTX)
        print(f"pptx: {os.path.relpath(PPTX, ROOT)}（{len(order)}スライド）")

    # 1スライドずつ焼く（LibreOffice の png 書き出しは先頭スライドだけなので分割する）
    src = Presentation(PPTX)
    targets = a.names or order
    print(f"{'name':34}{'PNG':>9}{'thumb':>10}")
    total = 0
    thumb_total = 0
    with tempfile.TemporaryDirectory() as td:
        for i, name in enumerate(order):
            if name not in targets:
                continue
            one = Presentation(PPTX)
            for sl in list(one.slides._sldIdLst)[::-1]:
                idx = list(one.slides._sldIdLst).index(sl)
                if idx != i:
                    one.slides._sldIdLst.remove(sl)
            tmp = os.path.join(td, "one.pptx")
            one.save(tmp)
            render(soffice, tmp, td)
            got = os.path.join(td, "one.png")
            if not os.path.isfile(got):
                raise SystemExit(f"{name}: PNG が出ませんでした")
            out = os.path.join(IMG, name + ".png")
            im = Image.open(got).convert("RGB")
            im.quantize(colors=COLORS, method=Image.MEDIANCUT, dither=Image.NONE).save(
                out, optimize=True)

            # 一覧用の縮小版。
            # ⚠️ **本体は 2400px なのに、記事一覧は240pxの枠で出していた**（2026-09-01 のレビュー）。
            # トップページだけで画像が 1.35MB あり、しかも縮めた図は文字が読めない。
            # 表示する大きさに合わせたものを別に焼いて、一覧はそちらを読む。
            os.makedirs(THUMB, exist_ok=True)
            th = os.path.join(THUMB, name + ".png")
            small = im.resize((THUMB_W, round(THUMB_W * im.height / im.width)), Image.LANCZOS)
            small.quantize(colors=COLORS, method=Image.MEDIANCUT, dither=Image.NONE).save(
                th, optimize=True)

            os.remove(got)
            total += os.path.getsize(out)
            thumb_total += os.path.getsize(th)
            print(f"{name:34}{os.path.getsize(out) // 1024:>7}KB{os.path.getsize(th) // 1024:>8}KB")
    print(f"\n{len(targets)}枚 / 本体 {total // 1024}KB ／ サムネ {thumb_total // 1024}KB")


if __name__ == "__main__":
    main()
