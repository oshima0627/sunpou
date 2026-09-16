# 記事23 新幹線持ち込み外寸の判定（`/cabin-bag/shinkansen-fit-outer-dims/`）

公開予定 2026-09-16。カテゴリ `cabin-bag`。航空機外寸記事（記事22）の姉妹編。

※ docs に `article-23-liter-nanpaku.md` / `article-23-check-output.md` が既にあるため、本ファイル名は依頼どおり `article-23-shinkansen-fit-outer-dims.md` とする（番号衝突は既知）。

---

## 1. データ源

### JR（公式・2026-09-16）

| 出典 | URL | 使ったルール |
|---|---|---|
| JR東海 荷物案内 | https://railway.jr-central.co.jp/oversized-baggage/ | 特大＝3辺和160cm超〜250cm。要「特大荷物スペースつき座席」事前予約（追加料金なし）。未予約は手数料税込1,000円。250cm超は持込不可。〜160は予約不要 |
| JRおでかけネット | https://www.jr-odekake.net/railroad/service/baggage/ | 同上。対象は東海道・山陽・九州・西九州。無料手回り品：和≤250・長さ2m超不可・30kg以内・2個まで。N700荷棚奥行約42cm／足元概ね和120cmの目安 |

JR東日本公式（kippu / multi/faq / luggage-area）は本環境から403で一次取得できず。他路線の詳細は記事の未検証へ。

### 製品外寸（公式・2026-09-16 再確認）

| 製品 | 外寸 | 和 | URL |
|---|---|---|---|
| ace. パリセイド3-Z 06912 | 50×40×25 | 115 | https://store.ace.jp/shop/g/g06912-03/ |
| PROTECA スタリアCXR 02350 | 45×34×20 | 99 | https://store.ace.jp/shop/g/g02350-02/ |
| EDGELINK CRUZBOX 09145 通常 | 55×34×25 | 114 | https://store.ace.jp/shop/g/g09145-01/ |
| 同上 拡張 | 55×34×29 | 118 | 同上（D25/29） |
| Legend Walker 5516-48 | 全体55×36×24 | 115 | https://legend-walker.com/products/5516-48 |
| Samsonite クァントム Spinner55 | 55.0×37.0×23.0 | 115 | https://www.samsonite.co.jp/samsonite/quanthom/spinner55/silver/ss-162285-1776.html |

Ace系は「キャスター・ハンドルを含む外寸」。Legendは**全体**を採用。Samsoniteは高さにホイール含む旨のみ。

---

## 2. 検算チェックリスト（独立再計算）

判定式:

- ≦160: sum ≤ 160 → 予約不要で持込可
- 160超〜250: 160 < sum ≤ 250 → 特大（要予約）
- 250超: sum > 250 → 持込不可

| 製品 | 和 | ≦160 | 特大帯 | 250超 |
|---|---|---|---|---|
| Ace 06912 | 115 | ○ | — | — |
| Proteca 02350 | 99 | ○ | — | — |
| EDGE 通常 | 114 | ○ | — | — |
| EDGE 拡張 | 118 | ○ | — | — |
| Legend 5516-48 | 115 | ○ | — | — |
| Samsonite Spinner55 | 115 | ○ | — | — |

**断言:** 2026-09-16 に上表を再計算し、記事マトリクスと一致。今回セットはすべて≦160。

---

## 3. 未検証（`検証済み` に昇格させないこと）

- 荷棚・足元の実収納
- 重量と30kg上限の照合
- 拡張時実寸の個体差
- 特大スペース実寸への収まり
- Samsoniteの幅・奥行がキャスター込みか
- 北海道・東北・秋田・山形・上越・北陸の公式再確認（403）
- 在来線の詳細
- 和160超の大型ケース製品

---

## 4. 図版

なし（eyecatch / ogImage 省略）。

---

## 5. ビルドトラップ注意

- `assertCardNumbers`: card の `product:` 文字列が表行に連続して出現すること。`（通常）` / `（拡張）` は LINK 表示名と product 行の両方に入れる
- `assertNoRawEmphasis`: 閉じ `**` を `）` の直後に置かない
- 価格・¥・在庫・送料・安い を本文に書かない（手数料の公式案内「税込1,000円」はルール事実として例外的に記載）
