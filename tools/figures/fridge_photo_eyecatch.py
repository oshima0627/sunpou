"""冷蔵庫記事の写真系アイキャッチ（1200x630 JPG）。記事ごとに別のベース写真を使う。
python3 tools/figures/fridge_photo_eyecatch.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[2]
ASSETS = Path(__file__).parent / "assets"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
# slug: (kicker, title lines, band box (x0,y0,x1,y1) in 1200x630 output)
ITEMS = {
    "fridge-delivery-path-fit": ("冷蔵庫の搬入経路", ["通路80/90cm、", "通る？"], (0, 334, 420, 560)),
    "fridge-install-clearance-outer-dims": ("冷蔵庫の設置スペース", ["奥行は足りる？"], (0, 480, 580, 630)),
    "fridge-side-top-clearance-door-swing": ("冷蔵庫の設置スペース", ["左右・上のすき間は何mm？"], (0, 480, 720, 630)),
}
W, H = 1200, 630
def make(slug, kicker, lines, box):
    im = Image.open(ASSETS / f"{slug}-base.jpg").convert("RGB")
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im = im.crop((0, im.height - H, W, im.height))
    x0, y0, x1, y1 = box
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rectangle(box, fill=(28, 30, 34, 225)); d.rectangle((x0, y0, x0 + 12, y1), fill=(245, 200, 0, 255))
    im = Image.alpha_composite(im.convert("RGBA"), ov); d = ImageDraw.Draw(im)
    fk = ImageFont.truetype(FONT, 28)
    size = 52
    while size > 30:
        ft = ImageFont.truetype(FONT, size)
        if max(d.textlength(l, font=ft) for l in lines) <= (x1 - x0) - 60: break
        size -= 2
    top = y0 + ((y1 - y0) - (40 + len(lines) * (size + 14))) // 2 - 6
    d.text((x0 + 40, top), kicker, font=fk, fill=(245, 200, 0))
    for i, l in enumerate(lines):
        d.text((x0 + 38, top + 40 + i * (size + 14)), l, font=ft, fill="white")
    d.text((W - 24, H - 16), "寸法帳", font=ImageFont.truetype(FONT, 22), fill=(90, 90, 90), anchor="rs")
    out = ROOT / "site/public/img" / f"{slug}-photo-eyecatch.jpg"
    im.convert("RGB").save(out, quality=88, optimize=True, progressive=True); print(out)
for k, v in ITEMS.items(): make(k, *v)
