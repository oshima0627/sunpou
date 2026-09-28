# 記事32 拡張前後の外寸・総外寸（`/cabin-bag/expandable-vs-fixed-outer-dims/`）

公開予定 2026-09-28。カテゴリ `cabin-bag`。

docs 番号は `article-31-*` まで使用済みのため、次の空き **32** を採用。

データ取得日はすべて **2026-09-28**。

---

## 1. テーマの決め方

- 週次パイプライン優先トピック「cabin-bag: expandable vs non-expand outer-sum」
- 勝てる型：①メーカー横断（ace／PROTECA／EDGELINK／Legend Walker）②カタログ欠落計算（ΔD・Δ3辺和、158までの余り）
- 通常時と拡張時の公式併記が **13製品**（閾値〜5を大きく上回る）取れたので本トピックで実施（fallback 不要）
- cooler-box は拡張しない
- 図版なし（defaultOgImage フォールバック）

---

## 2. データ源（一次）

### 定義・航空会社

| 出典 | URL | 使った値 | 取り方 |
|---|---|---|---|
| ace 容量・重量・サイズ表記について | https://store.ace.jp/shop/pages/help_size.aspx | 外寸＝突起込み。エキスパンドは奥行を通常/拡張で併記 | curl。HTMLコメント除去後に本文一致 |
| ANA 国内線 無料預け入れ | https://www.ana.co.jp/ja/jp/guide/boarding-procedures/baggage/domestic/free/ | 3辺合計158cm以内・キャスターと持ち手を含む | curl 200 |
| ANA 国際線 無料預け入れ | https://www.ana.co.jp/ja/jp/guide/boarding-procedures/baggage/international/baggage-free/ | 同上 | curl 200 |

### 製品（通常/拡張の公式併記）

| 製品 | 通常 H×W×D | 拡張 H×W×D | 総外寸 通常/拡張 | URL | 取り方 |
|---|---|---|---|---|---|
| EDGELINK CRUZBOX 09145 | 55×34×25 | 55×34×29 | 114 / 118（拡張和は計算） | https://store.ace.jp/shop/g/g09145-01/ | curl。外寸スラッシュ公式。総外寸欄は114のみ→拡張和は当サイト |
| PROTECA フレスターEX 01551 | 55×37×23 | 55×37×27 | 115/119 | https://store.ace.jp/shop/g/g01551-01/ | curl。外寸・総外寸ともスラッシュ公式 |
| ACE クレスタ 06316 | 55×35×25 | 55×35×29 | 115/119 | https://store.ace.jp/shop/g/g06316-02/ | curl |
| ace. トレリスZ 09071 | 52×38×25 | 52×38×29 | 115/119 | https://store.ace.jp/shop/g/g09071-15/ | curl |
| Legend Walker 5109-46 | 53×38×24 | 53×38×29 | 115(+5)→120 | https://legend-walker.com/products/5109-46 | curl。全体・3辺の和の(+N)公式 |
| Legend Walker 5525-48 | 54×36×25 | 54×36×32 | 115(+7)→122 | https://legend-walker.com/products/5525-48 | curl |
| PROTECA トラクション2 01493 | 67×47×26 | 67×47×30 | 140/144 | https://store.ace.jp/shop/g/g01493-02/ | curl |
| Legend Walker 5525-60 | 67×47×28 | 67×47×35 | 142(+7)→149 | https://legend-walker.com/products/5525-60 | curl |
| Legend Walker 5511-70 | 76×50×29 | 76×50×34 | 155(+5)→160 | https://legend-walker.com/products/5511-70 | curl |
| PROTECA トラクション2 01494 | 76×53×28 | 76×53×32 | 157/161 | https://store.ace.jp/shop/g/g01494-11/ | curl |
| Legend Walker 5525-69 | 76×51×30 | 76×51×37 | 157(+7)→164 | https://legend-walker.com/products/5525-69 | curl |
| ACE エスカレラ 05653 | 76×52×30 | 76×52×34 | 158/162 | https://store.ace.jp/shop/g/g05653-01/ | curl |
| PROTECA フレスターEX 01555 | 79×46×33 | 79×46×37 | 158/162 | https://store.ace.jp/shop/g/g01555-13/ | curl |

### 採用した計算

- ΔH / ΔW / ΔD / Δ3辺和 = 拡張 − 通常
- 158までの余り = 158 − 総外寸（負数は超過）
- Legend Walker 拡張総外寸 = 公式「3辺の和 ○(+N)」の ○+N
- EDGELINK 拡張総外寸のみ公式総外寸欄が通常側だけのため、外寸3辺の和で計算し記事・docsに明記

---

## 3. 検算チェックリスト（独立再計算）

| 製品 | 通常和 | 拡張和 | ΔD | Δ和 | 158−通常 | 158−拡張 |
|---|---|---|---|---|---|---|
| EDGELINK 09145 | 114 | 118 | +4 | +4 | +44 | +40 |
| PROTECA 01551 | 115 | 119 | +4 | +4 | +43 | +39 |
| ACE 06316 | 115 | 119 | +4 | +4 | +43 | +39 |
| ace. 09071 | 115 | 119 | +4 | +4 | +43 | +39 |
| LW 5109-46 | 115 | 120 | +5 | +5 | +43 | +38 |
| LW 5525-48 | 115 | 122 | +7 | +7 | +43 | +36 |
| PROTECA 01493 | 140 | 144 | +4 | +4 | +18 | +14 |
| LW 5525-60 | 142 | 149 | +7 | +7 | +16 | +9 |
| LW 5511-70 | 155 | 160 | +5 | +5 | +3 | −2 |
| PROTECA 01494 | 157 | 161 | +4 | +4 | +1 | −3 |
| LW 5525-69 | 157 | 164 | +7 | +7 | +1 | −6 |
| ACE 05653 | 158 | 162 | +4 | +4 | 0 | −4 |
| PROTECA 01555 | 158 | 162 | +4 | +4 | 0 | −4 |

**断言:** 2026-09-28 に上表を再計算し、記事マトリクス・カードと一致。全行で ΔH＝0・ΔW＝0・Δ3辺和＝ΔD。

---

## 4. 未検証（`検証済み` に昇格させないこと）

- 拡張時の実測の個体差
- サムソナイト・RIMOWA・無印など併記未取得ブランド
- 容量リットル増分と奥行増分の関係式
- 空港ゲージ・新幹線の実測適合
- 拡張ファスナー半開きの中間寸法
- ANA型158以外の預け入れ天井（JAL国際線203cm等）への余り表
- 価格・在庫・セール（本文に書かない）

---

## 5. サイト配線

- カテゴリ `cabin-bag` は既存。`site.json` 変更なし
- `site/content/categories/cabin-bag.md` に topic-stack を1セクション追加
- 原稿 `site/content/articles/cabin-bag-expandable-vs-fixed-outer-dims.md`

---

## 6. ビルドトラップ注意

- `assertCardNumbers`: card の `product:` が表行に連続出現（5製品）
- `assertNoRawEmphasis`: 閉じ `**` を `）` の直後に置かない
- ace HTMLはコメント除去後に読む（既存トラップ）
- 価格表記・¥・在庫を本文に書かない
- EDGELINK拡張和は計算である旨を表注記・カード・docsで三重に残す

---

## 7. 次候補メモ

1. fridge 続編: 据付必要奥行・ドア開放最大奥行を設置側で横断（搬入ではなく設置）
2. fridge: メーカー「幅＋10cm」を本体幅に当てた直立搬入余り表
3. dishwasher: article-27 の Sharp／Hitachi 据置外形・ドア開放ギャップ埋め
4. cabin-bag: サムソナイト等の拡張併記が取れた場合の追補、または JAL 203cm 天井での余り表
