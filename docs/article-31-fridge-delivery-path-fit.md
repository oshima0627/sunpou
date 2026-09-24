# 記事31 冷蔵庫の搬入：通路幅 × 本体奥行（`/fridge/delivery-path-fit/`）

公開予定 2026-09-24。カテゴリ `fridge`（新設・冷蔵庫）。

docs 番号は `article-30-*` まで使用済みのため、次の空き **31** を採用。

データ取得日はすべて **2026-09-24**。

---

## 1. テーマの決め方

- 週次パイプライン優先トピック「冷蔵庫の搬入：通路幅 × 本体奥行」
- 勝てる型：①メーカー横断（Panasonic／Sharp／Toshiba／Hitachi／Mitsubishi）②カタログ欠落計算（想定通路 − 本体奥行）
- 一次の搬入案内が3社以上＋本体奥行の公式ページが揃ったので fridge で実施（fallback 不要）
- cooler-box は拡張しない
- 図版なし（defaultOgImage フォールバック）

---

## 2. データ源（一次）

### 搬入案内

| 出典 | URL | 使った値 | 取り方 |
|---|---|---|---|
| パナソニック 寸法・設置・搬入 | https://panasonic.jp/store/guide/price/reizo.html | 手掛け含む幅に左右5cmずつ（本体幅＋10cm） | curl + WebFetch。本文に「左右5cmずつ（本体幅＋10cm）」 |
| 日立 FAQ a150 | https://kadenfan.hitachi.co.jp/support/rei/q_a/a150.html | 本体寸法に左右それぞれ10cm程度 | curl。本文一致 |
| 東芝 リビングダイレクト 搬入・設置 | https://shop.toshiba-lifestyle.com/jp/shop/pages/refrigerator_installation.aspx | 商品寸法＋10cm以上 | curl。本文一致 |
| 三菱電機くらトク detail_633 | https://kuratoku.lcx.mitsubishielectric.co.jp/professional/detail_633/ | 本体＋10cm程度／廊下・階段も左右上下10cm以上 | curl。本文一致 |
| シャープ SJ-MF51R 等 | 各仕様ページ | 奥行き薄型63cmで向きを変えてドアが通れる旨 | curl。製品ページ本文 |

### 製品奥行（HTML／公式寸法図から抽出）

| 製品 | 幅 | 奥行 | 高さ | URL | 取り方 |
|---|---|---|---|---|---|
| Panasonic NR-C37WS2 | 600 | 600 | 1850 | https://panasonic.jp/reizo/products/NR-C37WS2/spec.html | 外形寸法 600×600×1850／据付必要奥行600 |
| Panasonic NR-F55WX3 | 685 | 699 | 1828 | https://panasonic.jp/reizo/products/NR-F55WX3/spec.html | 外形 685×699×1828／据付必要奥行699 |
| Panasonic NR-F53HV2 | 650 | 725 | 1850 | https://panasonic.jp/reizo/products/NR-F53HV2/spec.html | 外形 650×725×1850／据付必要奥行725 |
| シャープ SJ-MF51R | 685 | 630 | 1838 | https://jp.sharp/reizo/products/sjmf51r/spec/ | 外形 幅685×奥行630×高さ1,838／最小設置奥行637 |
| シャープ SJ-MF55R | 730 | 630 | 1838 | https://jp.sharp/reizo/products/sjmf55r/spec/ | 外形 幅730×奥行630×高さ1,838／最小設置奥行637 |
| シャープ SJ-MF61R | 785 | 630 | 1855 | https://jp.sharp/reizo/products/sjmf61r/spec/ | 外形 幅785×奥行630×高さ1,855／最小設置奥行630 |
| 東芝 GR-A550FZ | 685 | 699 | 1833 | https://www.toshiba-lifestyle.com/jp/refrigerators/gr-a550fz/spec/ | 奥行（ハンドル・調節脚除く）699／据付必要奥行702 |
| 東芝 GR-W600FZS | 685 | 745 | 1833 | https://www.toshiba-lifestyle.com/jp/refrigerators/gr-w600fzs/spec/ | 奥行（ハンドル・調節脚除く）745／据付必要奥行748 |
| 日立 R-HZC54Y | 650 | 699 | 1843 | https://kadenfan.hitachi.co.jp/rei/lineup/rhzc54y/img/sizeZoom.png | 公式寸法図 PNG。奥行699・幅650・高さ1843。JSON `最小設置奥行寸法`=699 |
| 三菱電機 MR-WZ55N | 650 | 699 | 1833 | https://www.mitsubishielectric.co.jp/home/reizouko/product/mr-wz55n/ | 「547L 幅650×奥行699×高さ1,833mm」 |
| 三菱電機 MR-WZ61N | 685 | 738 | 1833 | https://www.mitsubishielectric.co.jp/home/reizouko/product/mr-wz61n/ | 「608L 幅685×奥行738×高さ1,833mm」 |

### 採用した判定式

- 余り800 = 800 − 奥行（mm）
- 余り900 = 900 − 奥行（mm）
- 想定通路幅は当サイトの仮定（OEM公表ではない）。記事冒頭で明示
- メーカー「幅＋10cm」系は直立搬入目安として並記のみ。余り計算には混ぜない

---

## 3. 検算チェックリスト（独立再計算）

| 製品 | 奥行 | 800−D | 900−D |
|---|---|---|---|
| NR-C37WS2 | 600 | 200 | 300 |
| SJ-MF51R / 55R / 61R | 630 | 170 | 270 |
| NR-F55WX3 / GR-A550FZ / R-HZC54Y / MR-WZ55N | 699 | 101 | 201 |
| NR-F53HV2 | 725 | 75 | 175 |
| MR-WZ61N | 738 | 62 | 162 |
| GR-W600FZS | 745 | 55 | 155 |

**断言:** 2026-09-24 に上表を再計算し、記事マトリクス・カードと一致。

---

## 4. 未検証（`検証済み` に昇格させないこと）

- 実玄関・廊下・エレベーター・階段での搬入可否
- 曲がり角・方向転換に必要なスペースの定量
- 梱包材・台車・作業員ぶんの増分
- ドア取りはずしの可否・配線制約の横断表
- ハンドル込み／除くのメーカー間統一換算
- 設置後の放熱あき・ドア開放時奥行を搬入判定に使うこと
- 価格・在庫・工事費（本文に書かない）

---

## 5. サイト配線

- `site/content/site.json` に `fridge` カテゴリを追加
- `site/content/categories/fridge.md` に topic-stack リード
- 原稿 `site/content/articles/fridge-delivery-path-fit.md`

---

## 6. ビルドトラップ注意

- `assertCardNumbers`: card の `product:` が表行に連続出現（5製品）
- `assertNoRawEmphasis`: 閉じ `**` を `）` の直後に置かない
- 価格表記・¥・在庫を本文に書かない

---

## 7. 次候補メモ

1. cabin-bag: expandable vs non-expand outer-sum の一次クロスチェック
2. dishwasher: article-27 の Sharp／Hitachi 据置外形ギャップ埋め
3. fridge 続編: 据付必要奥行・ドア開放最大奥行を設置側で横断（搬入ではなく設置）
4. fridge: メーカー「幅＋10cm」を本体幅に当てた直立搬入余り表（本記事の奥行回しと対になる）
