# -*- coding: utf-8 -*-
# X のヘッダー（1500x500）。
# 方針: 特定ジャンル（クーラーボックス等）の数字を出さない。
#       このアカウントは「寸法で確かめる」という方法の看板なので、方法だけを書く。
from PIL import Image, ImageDraw, ImageFont
import sys; sys.stdout.reconfigure(encoding='utf-8')
NAVY=(1,65,114); BG=(252,252,252); INK=(67,67,71); MUTE=(111,118,128)
FB="C:/Windows/Fonts/YuGothB.ttc"; FM="C:/Windows/Fonts/YuGothM.ttc"
def f(p,s): return ImageFont.truetype(p,s)
W,H=1500,500
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
d.rectangle([0,0,W,10], fill=NAVY)
boxes=[]
def center(text, font, y, fill, name):
    bb=d.textbbox((0,0),text,font=font)
    x=(W-(bb[2]-bb[0]))/2 - bb[0]
    d.text((x,y),text,font=font,fill=fill)
    boxes.append((name, x+bb[0], y+bb[1], x+bb[2], y+bb[3]))

# 寸法線（favicon と同じモチーフ）
w=7; y=112; half=150; x1,x2=W//2-half, W//2+half; hh=int(w*3.5); a=int(w*2.6)
d.line([(x1,y-hh),(x1,y+hh)],fill=NAVY,width=w); d.line([(x2,y-hh),(x2,y+hh)],fill=NAVY,width=w)
d.line([(x1,y),(x2,y)],fill=NAVY,width=w)
d.polygon([(x1,y),(x1+a*2,y-a),(x1+a*2,y+a)],fill=NAVY); d.polygon([(x2,y),(x2-a*2,y-a),(x2-a*2,y+a)],fill=NAVY)
boxes.append(("寸法線", x1, y-hh, x2, y+hh))

center("寸法で選ぶ", f(FB,92), 162, INK, "タイトル")
center("カタログに書いていない寸法を、メーカー公表値から計算する", f(FM,32), 284, MUTE, "タグライン")
center("一次情報だけを使う ／ 計算式を書く ／ 出典URLを付ける", f(FB,30), 342, NAVY, "方法")
center("sunpou.nexeed-lab.com", f(FM,26), 404, MUTE, "URL")

# 検査: 重なり / 枠外 / アバター（X では左下が隠れる）
ov=[f"{boxes[i][0]} × {boxes[j][0]}" for i in range(len(boxes)) for j in range(i+1,len(boxes))
    if boxes[i][1]<boxes[j][3] and boxes[j][1]<boxes[i][3] and boxes[i][2]<boxes[j][4] and boxes[j][2]<boxes[i][4]]
out=[n for n,x1_,y1_,x2_,y2_ in boxes if x1_<0 or y1_<0 or x2_>W or y2_>H]
av=(0,300,300,H)
hit=[n for n,x1_,y1_,x2_,y2_ in boxes if x1_<av[2] and av[0]<x2_ and y1_<av[3] and av[1]<y2_]
print("重なり:", ov or "なし"); print("枠外:", out or "なし"); print("アバターと干渉:", hit or "なし")
for n,a1,b1,a2,b2 in boxes: print(f"  {n:8s} x {a1:6.0f}-{a2:6.0f}  y {b1:5.0f}-{b2:5.0f}")
img.save("x-header-1500x500.png")
