"""冷蔵庫記事の写真系アイキャッチ（1200x630 JPG）。python3 tools/figures/fridge_photo_eyecatch.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).parent / "assets" / "fridge-photo-base.jpg"
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
ITEMS = {
    "fridge-delivery-path-fit": ("冷蔵庫の搬入経路", "通路80/90cm、通る？"),
    "fridge-install-clearance-outer-dims": ("冷蔵庫の設置スペース", "奥行は足りる？"),
    "fridge-side-top-clearance-door-swing": ("冷蔵庫の設置スペース", "左右・上のすき間は何mm？"),
}
W, H = 1200, 630
def make(slug, kicker, title):
    im = Image.open(BASE).convert("RGB")
    s = W / im.width
    im = im.resize((W, round(im.height * s)), Image.LANCZOS)
    top = im.height - H
    im = im.crop((0, top, W, im.height))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.rectangle((0, 480, 720, H), fill=(28, 30, 34, 225))
    d.rectangle((0, 480, 12, H), fill=(245, 200, 0, 255))
    im = Image.alpha_composite(im.convert("RGBA"), ov)
    d = ImageDraw.Draw(im)
    fk = ImageFont.truetype(FONT, 28, index=0)
    size = 52
    while True:
        ft = ImageFont.truetype(FONT, size, index=0)
        if d.textlength(title, font=ft) <= 660 or size <= 30: break
        size -= 2
    d.text((40, 500), kicker, font=fk, fill=(245, 200, 0))
    d.text((38, 540), title, font=ft, fill="white")
    d.text((W - 24, H - 16), "寸法帳", font=ImageFont.truetype(FONT, 22, index=0), fill=(90, 90, 90), anchor="rs")
    out = ROOT / "site/public/img" / f"{slug}-photo-eyecatch.jpg"
    im.convert("RGB").save(out, quality=88, optimize=True, progressive=True); print(out)
for k, v in ITEMS.items(): make(k, *v)
