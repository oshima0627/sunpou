# 記事22 機内持ち込み外寸の一括判定（`/cabin-bag/airline-fit-outer-dims/`）

公開予定 2026-09-15。カテゴリ `cabin-bag` の第1本。

---

## 1. データ源

### 航空会社（公式・2026-09-15）

| 社 | URL | 使ったルール |
|---|---|---|
| ANA 国内 | https://www.ana.co.jp/ja/jp/guide/boarding-procedures/baggage/domestic/carry-rule/ | ≥100席: 55×40×25 かつ和≤115。＜100: 45×35×20 かつ和≤100。キャスター・ハンドル込み。重量は身の回り品と計10kg |
| JAL 国内 | https://www.jal.co.jp/jp/ja/dom/baggage/inflight/ | 同型のサイズ構造。ハンドル・キャスター・車輪込み |
| Peach | https://www.flypeach.com/lm/ai/airports/baggage/carry_on_bag | **和≤115のみ**（各辺上限の公式記載なし）。キャスター・ハンドル・ポケット込み |
| Jetstar | https://www.jetstar.com/jp/ja/help/carry-on-baggage-what-can-i-bring-on-board | **ライブ再確認済（2026-09-15）**。キャリーケース 56×36×23（ハンドル・ポケット・キャスター込み）。〜2027-02-01: 2個計7kg（Plus7kg等で14kg、1個10kg超不可）。2027-02-02〜 JQ: Priorityなしは座席下40×30×20のみ、Priorityありは＋56×36×23。当該セクションにkg記載なし |
| Skymark | https://www.skymark.co.jp/ja/baggage/cabin.html | 55×40×25・和≤115 |
| AIRDO | https://www.airdo.jp/support/faq/general/baggage/q2.html | 55×40×25の範囲で和≤115 |

### 製品外寸（公式・2026-09-15）

| 製品 | 外寸 | 和 | URL |
|---|---|---|---|
| ace. パリセイド3-Z 06912 | 50×40×25 | 115 | https://store.ace.jp/shop/g/g06912-03/ |
| PROTECA スタリアCXR 02350 | 45×34×20 | 99 | https://store.ace.jp/shop/g/g02350-02/ |
| EDGELINK CRUZBOX 09145 通常 | 55×34×25 | 114 | https://store.ace.jp/shop/g/g09145-01/ |
| 同上 拡張 | 55×34×29 | 118 | 同上 |
| Legend Walker 5516-48 | 全体55×36×24 | 115 | https://legend-walker.com/products/5516-48 |
| Samsonite クァントム Spinner55 | 55.0×37.0×23.0 | 115 | https://www.samsonite.co.jp/samsonite/quanthom/spinner55/silver/ss-162285-1776.html |

Ace系3製品は「キャスター・ハンドルを含む外寸」。Legendは**全体**を採用（本体48×32×24は使わない）。Samsoniteは高さにホイール含む旨のみ明記。

---

## 2. 検算チェックリスト（独立再計算）

判定式（すべて満たせば○）:

- ≥100席型: H≤55 ∧ W≤40 ∧ D≤25 ∧ sum≤115
- ＜100席: H≤45 ∧ W≤35 ∧ D≤20 ∧ sum≤100
- Peach: sum≤115
- Jetstar（記事列）: H≤56 ∧ W≤36 ∧ D≤23（**56×36×23 キャリーケースルール**）

| 製品 | ≥100 | ＜100 | Peach | Jetstar |
|---|---|---|---|---|
| Ace 06912 | ○ | ×（H50） | ○ | ×（W40） |
| Proteca 02350 | ○ | ○ | ○ | ○ |
| EDGE 通常 | ○ | × | ○ | ×（D25） |
| EDGE 拡張 | ×（D29・和118） | × | ×（和118） | × |
| Legend 5516-48 | ○ | × | ○ | ×（D24） |
| Samsonite Spinner55 | ○ | × | ○ | ×（W37） |

**断言:** 2026-09-15 に上表を再計算し、記事マトリクスと一致。全列○は Proteca 02350 のみ。

---

## 3. 未検証（`検証済み` に昇格させないこと）

- 空港ゲージ実測
- 荷物入り重量と各社重量上限の照合
- 拡張時実寸の個体差
- Peach各辺上限の有無（公式は和のみ）
- 客室収納可否
- Samsoniteの幅・奥行がキャスター込みか（高さのみ明記）
- Jetstar 2027-02-02以降（JQ）セクションの**重量上限**（ページにkg記載なし）
- 無印など未取得ブランド

※ Jetstar の **56×36×23** 自体は 2026-09-15 ライブ再確認済み。未検証にしない。

---

## 4. 図版

なし（eyecatch / ogImage 省略）。PowerPoint figures 未作成。
