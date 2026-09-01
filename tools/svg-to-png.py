# -*- coding: utf-8 -*-
"""site/public/img/*.svg を PNG に変換する。

なぜ PNG にするか：
  SVG の文字は x/y を直接指定して置いてある。**フォントが違う端末では文字幅が変わり、
  隣の文字とぶつかったり画面外にはみ出したりする**（2026-08-31 に実際に2枚で起きていた）。
  PNG に焼けば、こちらで確認した見た目がそのまま全端末で出る。

なぜ Chrome で描くか：
  日本語のフォント指定・字間・約物の詰めを正しく解釈できるレンダラが要る。
  cairosvg / rsvg は日本語の扱いが弱い。**表示確認に使ったのと同じエンジンで焼く**のが確実。

使い方:
  python tools/svg-to-png.py            # 全部
  python tools/svg-to-png.py 名前 名前  # 指定したものだけ（拡張子なし）

⚠️ **SVG が正（マスター）。PNG は生成物。** 図を直すときは SVG を直してから再実行する。
⚠️ 実行前に `getBBox` の重なり検査を通しておくこと（崩れたまま焼くと固定される）。
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "site", "public", "img")
SCALE = 2      # 2倍で焼いて、表示は等倍。高解像度画面でぼけない
COLORS = 256   # 減色。この図はグラデーションが無いので劣化しない（下の計測を参照）

# 2026-08-31 に coolerbox-yoryo-eyecatch で計測：
#   減色なし 154KB（実際に使われている色は 2370 色）
#   256色    59KB（-62%）／ 最大差 34/255・差が8を超える画素は 0.10%（文字の縁だけ）
#   64色     50KB       ／ 最大差 53/255・0.51%
# → 256色を採用。1KB あたりの見た目の損失がいちばん小さい。

CHROME_CANDIDATES = [
    r"C:/Program Files/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    os.path.expanduser("~/AppData/Local/Google/Chrome/Application/chrome.exe"),
]


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.isfile(p):
            return p
    raise SystemExit("Chrome が見つかりません。CHROME_CANDIDATES にパスを足してください")


def viewbox(svg_text):
    m = re.search(r'viewBox="([\d.\s-]+)"', svg_text)
    if not m:
        raise ValueError("viewBox がありません")
    parts = [float(x) for x in m.group(1).split()]
    return int(round(parts[2])), int(round(parts[3]))


def convert(chrome, path, outdir):
    name = os.path.splitext(os.path.basename(path))[0]
    svg = open(path, encoding="utf-8").read()
    w, h = viewbox(svg)
    out = os.path.join(outdir, name + ".png")

    # SVG をそのまま Chrome に読ませると余白が付くので、ぴったりの HTML に埋めて撮る
    html = (
        "<!doctype html><meta charset=utf-8>"
        "<style>html,body{margin:0;padding:0;background:#fff}"
        f"svg{{display:block;width:{w}px;height:{h}px}}</style>" + svg
    )
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        tmp = f.name
    try:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-sandbox",
            f"--force-device-scale-factor={SCALE}",
            f"--window-size={w},{h}",
            f"--screenshot={out}",
            "file:///" + tmp.replace("\\", "/"),
        ]
        r = subprocess.run(cmd, capture_output=True, timeout=90)
        if not os.path.isfile(out):
            raise RuntimeError(r.stderr.decode("utf-8", "replace")[-400:])
    finally:
        os.unlink(tmp)

    # Chrome の出力は 24bit のまま。平面塗りの図なので減色すると半分以下になる
    raw = os.path.getsize(out)
    im = Image.open(out).convert("RGB")
    im.quantize(colors=COLORS, method=Image.MEDIANCUT, dither=Image.NONE).save(out, optimize=True)
    return name, w, h, os.path.getsize(out), raw


def powerpoint_managed():
    """PowerPoint 版に移行済みの図の名前。

    ⚠️ **ここにある図を SVG から焼き直してはいけない。** PowerPoint で作った PNG を
    古い SVG の見た目で上書きしてしまう。正は `tools/figures/figures.py`。
    """
    fig = os.path.join(ROOT, "tools", "figures", "figures.py")
    if not os.path.isfile(fig):
        return set()
    src = open(fig, encoding="utf-8").read()
    body = src[src.index("ORDER = ["):src.index("FIGURES = {")]
    return set(re.findall(r'"([a-z0-9-]+)"', body))


def main():
    chrome = find_chrome()
    only = set(sys.argv[1:])
    paths = sorted(glob.glob(os.path.join(IMG, "*.svg")))
    managed = powerpoint_managed()
    blocked = [p for p in paths
               if os.path.splitext(os.path.basename(p))[0] in managed
               and (not only or os.path.splitext(os.path.basename(p))[0] in only)]
    if blocked:
        names = ", ".join(sorted(os.path.splitext(os.path.basename(p))[0] for p in blocked))
        raise SystemExit(
            f"この図は PowerPoint 版に移行済みです: {names}"
            " / SVG から焼くと PowerPoint で作った PNG を上書きします。"
            " 対処: 直すなら tools/figures/figures.py を直して"
            " `python tools/figures/build.py <名前>` を実行してください")
    if only:
        paths = [p for p in paths if os.path.splitext(os.path.basename(p))[0] in only]
    if not paths:
        raise SystemExit("対象の SVG がありません")

    total = raw_total = 0
    print(f"{'name':40}{'viewBox':>11}{'減色前':>8}{'PNG':>8}")
    for p in paths:
        name, w, h, size, raw = convert(chrome, p, IMG)
        total += size
        raw_total += raw
        print(f"{name:40}{f'{w}x{h}':>11}{raw // 1024:>6}KB{size // 1024:>6}KB")
    print(f"\n{len(paths)}枚 / 合計 {total // 1024}KB（減色前 {raw_total // 1024}KB）/ 実解像度は {SCALE}倍")


if __name__ == "__main__":
    main()
