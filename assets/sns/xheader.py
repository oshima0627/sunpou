# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import sys; sys.stdout.reconfigure(encoding='utf-8')
NAVY=(1,65,114); BG=(252,252,252); INK=(67,67,71); MUTE=(111,118,128)
FB="C:/Windows/Fonts/YuGothB.ttc"; FM="C:/Windows/Fonts/YuGothM.ttc"
def f(p,s): return ImageFont.truetype(p,s)
W,H=1500,500
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
d.rectangle([0,0,W,10], fill=NAVY)

def center(text, font, y, fill):
    bb=d.textbbox((0,0),text,font=font)
    x=(W-(bb[2]-bb[0]))/2 - bb[0]
    d.text((x,y),text,font=font,fill=fill)
    return (x+bb[0], y+bb[1], x+bb[2], y+bb[3])

boxes=[]
# 寸法線（タイトルの上・中央）
w=7; y=118; half=150
x1,x2=W//2-half, W//2+half
hh=int(w*3.5)
d.line([(x1,y-hh),(x1,y+hh)],fill=NAVY,width=w); d.line([(x2,y-hh),(x2,y+hh)],fill=NAVY,width=w)
d.line([(x1,y),(x2,y)],fill=NAVY,width=w)
a=int(w*2.6)
d.polygon([(x1,y),(x1+a*2,y-a),(x1+a*2,y+a)],fill=NAVY); d.polygon([(x2,y),(x2-a*2,y-a),(x2-a*2,y+a)],fill=NAVY)
boxes.append(("寸法線", x1, y-hh, x2, y+hh))

boxes.append(("タイトル", *center("寸法で選ぶ", f(FB,92), 168, INK)))
boxes.append(("タグライン", *center("カタログに書いていない寸法を、メーカー公表値から計算する", f(FM,32), 290, MUTE)))
boxes.append(("数字", *center("同じ20Lでも15〜18本。2Lが立つのは33製品中9つ。", f(FB,34), 348, NAVY)))
boxes.append(("URL", *center("sunpou.nexeed-lab.com", f(FM,26), 412, MUTE)))

# 検査1: 要素どうしの重なり
ov=[]
for i in range(len(boxes)):
    for j in range(i+1,len(boxes)):
        n1,ax1,ay1,ax2,ay2=boxes[i]; n2,bx1,by1,bx2,by2=boxes[j]
        if ax1<bx2 and bx1<ax2 and ay1<by2 and by1<ay2: ov.append(f"{n1} × {n2}")
# 検査2: 枠外 / アイコンが重なる左下（X ではアバターが左下を覆う）
out=[f"{n} が枠外" for n,x1,y1,x2,y2 in boxes if x1<0 or y1<0 or x2>W or y2>H]
avatar=(0,300,300,H)
hit=[n for n,x1,y1,x2,y2 in boxes if x1<avatar[2] and avatar[0]<x2 and y1<avatar[3] and avatar[1]<y2]
print("重なり:", ov or "なし")
print("枠外:", out or "なし")
print("アバターと干渉:", hit or "なし")
for n,x1,y1,x2,y2 in boxes: print(f"  {n:8s} x {x1:6.0f}-{x2:6.0f}  y {y1:5.0f}-{y2:5.0f}")
img.save("x-header-1500x500.png")
