# 記事28 モニターアーム 天板厚×クランプ適合（`/monitor-arm/desk-thickness-clamp-fit/`）

公開予定 2026-09-16。カテゴリ `monitor-arm`（新設・モニターアーム）。

docs 番号は `article-27-*` まで使用済みのため、次の空き **28** を採用。

---

## 1. データ源（一次・2026-09-16）

### Ergotron（LX Desk Monitor Arm 45-241 系）

| 出典 | URL | 使った値 |
|---|---|---|
| Dimensional & Range of Motion（© Ergotron DIM2-056） | https://itworkshop.lv/documents/catalog/10121/45-241-026-DistriNode-02.pdf | Desk Clamp 厚み帯: ＜10mm／12〜35mm／37〜60mm。全体上限 ＜60mm。下側寸法 81〜131mm を図面に記載 |
| LX Desk Monitor Arm 文献 | https://media.ergotron.com/reserved/resources/lx-deskmountarms-fur-ea-orig.pdf | VESA 75×75・100×100。Extension ≤25″（64cm）。Low-Profile は 25〜35mm |
| How to choose clamp attachment | https://www.ergotron.com/portals/0/literature/contract/choose-clamp-attachment-en.pdf | LX 標準2ピースの厚み上限 ＜2.4″（60mm）。グロメット穴 8〜51mm・厚み上限57mm |

本記事のクランプ厚レンジは **10〜60mm**（図面の最小帯と最大60mmを結合）。

### サンワサプライ（corporate `sanwa.co.jp`）

| 出典 | URL | 使った値 |
|---|---|---|
| CR-LAC1405BK | https://www.sanwa.co.jp/product/syohin?code=CR-LAC1405BK | クランプ可能厚 10〜50mm／グロメット 10〜80mm。VESA 75×75・100×100 |
| CR-LAC101BK | https://www.sanwa.co.jp/product/syohin?code=CR-LAC101BK | クランプ可能厚 10〜85mm／グロメット 10〜40mm。VESA 75×75・100×100 |
| CR-LAC116BK | https://www.sanwa.co.jp/product/syohin?code=CR-LAC116BK | クランプ可能厚 10〜50mm／グロメット 10〜55mm。**クランプ金具の奥行き 38mm**。VESA 75×75・100×100 |

### エレコム

| 出典 | URL | 使った値 |
|---|---|---|
| DPA-SN01BK | https://www.elecom.co.jp/products/DPA-SN01BK.html | 取り付け可能天板厚 クランプ 10〜80mm／グロメット 10〜40mm。VESA 75×75・100×100。外形 幅約114×奥行約490×高さ約540mm |

### HUANUO

| 出典 | URL | 使った値 |
|---|---|---|
| SS43 Single Monitor Arm | https://www.huanuo.com/products/single-monitor-arm-rgb-heavy-duty-mount | C-clamp／grommet とも desk thickness **0.8″–3.5″**。VESA 75×75・100×100。Reach 記載 24.8″ |

換算: 0.8×25.4＝20.32mm → **約20mm**、3.5×25.4＝88.9mm → **約89mm**。マトリクスは **20〜89mm**。

### AmazonBasics JP

| 出典 | 結果 |
|---|---|
| Amazon.co.jp 商品ページ等 | 通販ページのため契約 C2 で出典不可 → **クランプ厚は本記事で未検証** |

### 採用した判定式

- 天板厚 `T`（mm）がクランプ公表レンジ `[lo, hi]` に入れば ○（端点含む）
- HUANUO はインチ公表を mm に換算（上表）
- グロメット厚・耐荷重・インチ対応は主判定に混ぜない（参考列のみ）
- クランプ奥行き vs デスクオーバーハングは、公式が奥行きを出した機種だけ本文に書く

---

## 2. 検算チェックリスト（独立再計算）

| T (mm) | Ergotron 10〜60 | CR-LAC1405 10〜50 | CR-LAC101 10〜85 | CR-LAC116 10〜50 | DPA-SN01 10〜80 | SS43 20〜89 |
|---|---|---|---|---|---|---|
| 15 | ○ | ○ | ○ | ○ | ○ | × |
| 25 | ○ | ○ | ○ | ○ | ○ | ○ |
| 50 | ○ | ○ | ○ | ○ | ○ | ○ |
| 55 | ○ | × | ○ | × | ○ | ○ |
| 60 | ○ | × | ○ | × | ○ | ○ |
| 70 | × | × | ○ | × | ○ | ○ |
| 80 | × | × | ○ | × | ○ | ○ |
| 85 | × | × | ○ | × | × | ○ |
| 90 | × | × | × | × | × | × |

**断言:** 2026-09-16 に上表を再計算し、記事マトリクスと一致。天板55で50mm上限の2機だけ×。天板15で HUANUO だけ×。天板85で CR-LAC101 と HUANUO のみ○。

---

## 3. 未検証（`検証済み` に昇格させないこと）

- AmazonBasics のクランプ厚（通販のみ・メーカー独立ページなし）
- 各機のクランプ奥行き vs 特定デスクのはみ出し実測（CR-LAC116BK の 38mm 以外は未取得または図面解釈のみ）
- 天板の材質強度・ハニカム空洞・ガラス天板の可否
- モニター重量・インチ適合の実機確認
- グロメット穴位置と天板穴径の実測
- 入手条件（本文に書かない）

---

## 4. 図版

なし（eyecatch / ogImage 省略。defaultOgImage にフォールバック）。

---

## 5. ビルドトラップ注意

- `assertCardNumbers`: card の `product:` が表行に連続出現（6製品名をカード・表で一致）
- `assertNoRawEmphasis`: 閉じ `**` を `）` の直後に置かない
- 入手条件や販売チャネルを本文に書かない
- `site.json` に `monitor-arm` カテゴリを追加済みであること

---

## 6. カテゴリ新設

- slug: `monitor-arm`
- name: モニターアーム
- `site/content/categories/monitor-arm.md`
- `site/content/site.json` categories 配列に追記

---

## 7. メモ

- ユーザー方針（2026-09-16）: Workers Builds が green になったら確認待ちせず squash merge してよい
- DPA-SL06BK は公式で販売終了のため、現行の DPA-SN01BK を採用
