# 記事27 据置食洗機 設置外寸×キッチン制約（`/dishwasher/countertop-fit-outer-dims/`）

公開予定 2026-09-16。カテゴリ `dishwasher`（新設・食洗機（据置））。

docs 番号は `article-26-*` まで使用済みのため、次の空き **27** を採用。

---

## 1. データ源（一次・2026-09-16）

### パナソニック（外形・設置の目安・壁あき）

| 出典 | URL | 使った値 |
|---|---|---|
| 比較表 | https://panasonic.jp/dish/comparison.html | TH5/TZ500/TA5: 550×344＜579＞×598／TSK2: 550×290＜433＞×500＜612＞／TSP1・TSP2: 550×341＜433＞×600＜712＞／TCR5: 470×300＜598＞×460＜467＞／TML1・TMLK1: 310×225＜485＞×435。設置の目安も同表 |
| NP-TH5 仕様 | https://panasonic.jp/dish/products/NP-TH5/spec.html | 約 幅550×奥行344＜579＞×高さ598mm |
| NP-TSP1 仕様 | https://panasonic.jp/dish/products/NP-TSP1/spec.html | 約 幅550×高さ600＜712＞×奥行341＜…＞mm |
| 設置のつくり方 | https://panasonic.jp/dish/installation.html | 正面置き／タテ置き、壁あき注記への導線 |
| AR設置 | https://panasonic.jp/dish/contents/ar.html | 壁あき0.5cm以上（TML1・TMLK1除く）、寸法は目安 |
| カタログPDF 2026/春 | https://panasonic.jp/content/dam/panasonic/jp/ja/catalog/pdf/dishwasher.pdf | 外形・0.5cmあき・ドア開放は外形と異なる旨 |

### 東芝

| 出典 | URL | 使った値 |
|---|---|---|
| DWS-33B | https://www.toshiba-lifestyle.com/jp/dish-drye/dws-33b/ | 外形 420×435×465mm。ドア開放時寸法の記載なし → 開時 `未検証` |

### アイリスオーヤマ

| 出典 | URL | 使った値 |
|---|---|---|
| 食器洗い乾燥機 商品情報 | https://www.irisohyama.co.jp/products/electrical-appliances/cooking-appliances/other-cooking-appliances/dishwasher/dishwasher | ISHT-5000-W／KISHT-5000-W 商品サイズ 420×445×435mm。ドア開放時なし → 開時 `未検証` |

### シャープ・日立（二次試行）

| 出典 | 結果 |
|---|---|
| シャープ公式の据置食洗機製品探索 | 現行据置の外形一次ページを確認できず → **`未検証`** |
| 日立 家電ファン | 据置食洗機の現行外形を確認できず → **`未検証`** |

### 採用した判定式

- 閉時D≤600／開時D≤600（想定カウンター奥行600mm）
- W≤450（想定450mm級すき間）
- 壁あき込み必要幅 = W+5（パナソニック0.5cm・片側）。本体Wの450判定には混ぜない
- 吊戸棚下の実キッチン高さ → キッチン固有OEM無しのため **常に `未検証`**（設置の目安は参考併記のみ）

---

## 2. 検算チェックリスト（独立再計算）

### 開時余り（600 − D_open）

| 製品 | D_open | 余り |
|---|---|---|
| NP-TH5 | 579 | +21 |
| NP-TSK2 | 433 | +167 |
| NP-TSP1 | 433 | +167 |
| NP-TCR5 | 598 | +2 |
| NP-TML1 | 485 | +115 |

**断言:** 開時でいちばん厳しい一次公表は NP-TCR5（+2）。いちばん余裕があるのはスリム系の+167。

### 幅450判定

| 製品 | W | W≤450 |
|---|---|---|
| NP-TH5 / TSK2 / TSP1 | 550 | × |
| NP-TCR5 | 470 | × |
| NP-TML1 | 310 | ○ |
| 東芝 DWS-33B | 420 | ○ |
| アイリス ISHT-5000-W | 420 | ○ |

**断言:** 2026-09-16 に上表を再計算し、記事マトリクスと一致。

---

## 3. 未検証（`検証済み` に昇格させないこと）

- シャープ・日立の据置外形
- 東芝・アイリスのドア開放時最大寸法
- 特定キッチンのカウンター実測・すき間実測・吊戸棚下高さ
- 蛇口干渉・ホース取り回し・床の水平
- 分岐水栓適合・工事可否
- ビルトイン開口寸法
- 洗浄・騒音・価格・在庫（本文に書かない）

---

## 4. 図版

なし（eyecatch / ogImage 省略。defaultOgImage にフォールバック）。

---

## 5. ビルドトラップ注意

- `assertCardNumbers`: card の `product:` が表行に連続出現すること（7製品名をカード・表で一致）
- `assertNoRawEmphasis`: 閉じ `**` を `）` の直後に置かない
- 価格表記や入手条件を本文に書かない
- `site.json` に `dishwasher` カテゴリを追加済みであること（無いとビルド落ち）
- 洗浄性能・騒音を主内容にしない（カタログ欠落＝設置外寸）

---

## 6. カテゴリ新設

- slug: `dishwasher`
- name: 食洗機（据置）
- `site/content/categories/dishwasher.md`
- `site/content/site.json` categories 配列に追記

---

## 7. メモ

- ユーザー方針（2026-09-16）: Workers Builds が green になったら確認待ちせず squash merge してよい
- 東芝／アイリスの開時Dが取れたら開時列を昇格できる
