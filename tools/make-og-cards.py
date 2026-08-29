# -*- coding: utf-8 -*-
"""OGPカード（1200x630 PNG）を生成する。
SNSのカードは横500px程度に縮むので、記事の図版をそのまま使うと読めない。
「数字ひとつ＋1行」に絞る。
"""
from PIL import Image, ImageDraw, ImageFont
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

NAVY=(1,65,114); BG=(252,252,252); INK=(67,67,71); MUTE=(111,118,128); BAND=(240,244,248)
FB="C:/Windows/Fonts/YuGothB.ttc"; FM="C:/Windows/Fonts/YuGothM.ttc"
W,H=1200,630
OUT=sys.argv[1] if len(sys.argv)>1 else "."

# (出力名, 大きい数字, 1行の説明)
CARDS=[
 ("site",             "寸法で選ぶ",     "カタログに書いていない寸法を、メーカー公表値から計算する"),
 ("erabikata",        "33製品",         "用途から内寸を逆に引く、クーラーボックスの早見表"),
 ("500ml-honsuu",     "15〜18本",       "同じ20Lでも、500mlの入る本数が違う"),
 ("2l-tateru",        "33製品中9つ",    "2Lペットボトルが立つクーラーボックス"),
 ("horeizai-honsuu",  "6本 と 18本",    "保冷剤1枚。置き方だけでここまで変わる"),
 ("horeizai-maisuu",  "1枚 〜 7枚",     "本数を減らさずに入る保冷剤の枚数"),
 ("yoryo-uchinori",   "28.9〜40.0%",    "外寸の体積のうち、中身に使える割合"),
 ("daiwa-shimano",    "KEEP ＝ COOL",   "ダイワとシマノは同じJIS簡便法の「時間」"),
 ("uchinori-nagasa",  "80Lも60Lも85cm", "内寸の長辺は、容量Lでは決まらない"),
 ("coleman-uchinori", "深さ350mm",      "コールマンは26Lクラスでも2Lが立つ"),
 ("donabe-nangou",    "31〜32.5cm",     "同じ9号の土鍋でも、幅がこれだけ違う"),
 ("kyatatsu-takasa",  "180 の脚立は 1.40m", "型番の数字と、実際に足を置ける高さは40cm違う"),
 ("kyatatsu-kaidan",  "31cm と 69cm",   "伸縮脚では、階段の前後の脚の高低差に届かない"),
 ("kyatatsu-fumidai", "1.61m でも踏台",  "上わくが付くと、80cmを超えても踏台と呼ばれる"),
 ("kyatatsu-omosa",   "1.7kg と 6.3kg",  "同じ高さに立つのに、重さは3.7倍違う"),
 ("kyatatsu-secchi",  "17cm が 108cm",  "広げると奥行はしまうときの最大14.5倍になる"),
 ("kyatatsu-erabikata","42製品",         "届きたい高さから、足を置ける高さを逆に引く早見表"),
 ("konro-bombe",      "1人 5.8本",      "農水省の「6本」に届くのは10℃で全部まかなうとき"),
 ("konro-jikan",      "55分 〜 78分",   "ボンベ1本の連続燃焼時間。割り算では出ない"),
 ("konro-erabikata",  "11機種",         "使いたい鍋の幅と、ボンベ1本でもつ時間から引く早見表"),
 # ここから下は og:image ではなく SNS 投稿に添える用（記事に1対1で対応しない）
 ("sns-rules",        "3つのルール",      "一次情報だけ／計算式を書く／出典URLを付ける"),
 ("sns-konro-kw",     "2.9kW が 10号",   "最大4.1kWの機種は9号まで。火力と鍋の大きさは無関係"),
 ("sns-konro-haba",   "33.4cm ＜ 36cm",  "「10号まで」の機種より、10号土鍋のほうが幅がある"),
]

def fit(draw, text, path, start, maxw):
    """maxw に収まる最大サイズのフォントを返す"""
    s=start
    while s>28:
        f=ImageFont.truetype(path,s)
        bb=draw.textbbox((0,0),text,font=f)
        if bb[2]-bb[0]<=maxw: return f
        s-=2
    return ImageFont.truetype(path,28)

def dimline(d,cx,y,half,w,color):
    hh=int(w*3.5); a=int(w*2.6); x1,x2=cx-half,cx+half
    d.line([(x1,y-hh),(x1,y+hh)],fill=color,width=w); d.line([(x2,y-hh),(x2,y+hh)],fill=color,width=w)
    d.line([(x1,y),(x2,y)],fill=color,width=w)
    d.polygon([(x1,y),(x1+a*2,y-a),(x1+a*2,y+a)],fill=color); d.polygon([(x2,y),(x2-a*2,y-a),(x2-a*2,y+a)],fill=color)

ok=True
for name,big,line in CARDS:
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,12],fill=NAVY)
    d.rectangle([0,H-96,W,H],fill=BAND)
    boxes=[]
    def center(text,font,y,fill,tag):
        bb=d.textbbox((0,0),text,font=font)
        x=(W-(bb[2]-bb[0]))/2-bb[0]
        d.text((x,y),text,font=font,fill=fill)
        boxes.append((tag,x+bb[0],y+bb[1],x+bb[2],y+bb[3]))
    dimline(d,W//2,110,140,7,NAVY); boxes.append(("寸法線",W//2-140,110-25,W//2+140,110+25))
    fbig=fit(d,big,FB,132,1000)
    center(big,fbig,182,NAVY,"数字")
    fline=fit(d,line,FM,40,1020)
    center(line,fline,378,INK,"説明")
    # フッター帯
    fs=ImageFont.truetype(FB,30); fu=ImageFont.truetype(FM,26)
    d.text((60,H-64),"寸法で選ぶ",font=fs,fill=INK)
    bb=d.textbbox((0,0),"sunpou.nexeed-lab.com",font=fu)
    d.text((W-60-(bb[2]-bb[0]),H-60),"sunpou.nexeed-lab.com",font=fu,fill=MUTE)
    boxes.append(("サイト名",60,H-64,60+d.textbbox((0,0),"寸法で選ぶ",font=fs)[2],H-64+34))
    boxes.append(("URL",W-60-(bb[2]-bb[0]),H-60,W-60,H-60+30))
    # 検査
    ov=[f"{boxes[i][0]}×{boxes[j][0]}" for i in range(len(boxes)) for j in range(i+1,len(boxes))
        if boxes[i][1]<boxes[j][3] and boxes[j][1]<boxes[i][3] and boxes[i][2]<boxes[j][4] and boxes[j][2]<boxes[i][4]]
    out=[b[0] for b in boxes if b[1]<0 or b[2]<0 or b[3]>W or b[4]>H]
    if ov or out:
        ok=False; print(f"  ⚠️ {name}: 重なり={ov} 枠外={out}")
    img.save(os.path.join(OUT,f"{name}.png"))
    print(f"  {name}.png  数字={big}")
print("検査:", "全カードOK" if ok else "⚠️ 問題あり")
