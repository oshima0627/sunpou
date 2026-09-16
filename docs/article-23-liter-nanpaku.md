# 記事23 スーツケース40Lは何泊？（`/cabin-bag/liter-nanpaku/`）

公開 2026-09-16。カテゴリ `cabin-bag` の第2本。データ取得日はすべて **2026-09-16**。
検算は `python tools/check-article-23.py`（出力は `docs/article-23-check-output.md`）。

---

## 1. テーマの決め方

- Googleサジェスト（`suggestqueries.google.com`、2026-09-16）で「スーツケース 何泊」に
  `60l／40リットル／36l／50リットル／70リットル／64リットル／37リットル／75リットル／35リットル スーツケース 何泊` が並んだ。
  容量を指定した「何泊」需要が最大のかたまり
- 勝てる型（`serp-check.md`）の **①メーカー横断** と **②カタログに無い計算値** の両方を満たす形にした
  （6社の目安を1表に／帯から1泊あたりの容量を逆算／式で当てはめ）

## 2. データ源（公式のみ）

### 社としての目安（容量帯 ↔ 泊数）

| 社 | どこに書いてあるか | 取り方 | 原文の値 |
|---|---|---|---|
| ace | https://store.ace.jp/shop/r/rsuitcase/ 「容量で選ぶ SIZE」 | curl 200 | -29L (1-2泊) / 30-49L (2-3泊) / 50-59L (3-5泊) / 60-79L (5-7泊) / 80-99L (7-10泊) / 100L- (10泊-) |
| Legend Walker | 全ページ共通ナビ「宿泊数・サイズから選ぶ」＝各コレクションのタイトル（`/collections/1-night`, `1-to-2-nights`, `3-to-5-nights`, `5-to-7-nights`, `more-than-1-week`, `more-than-10-berths`） | curl 200 | 日帰り～1泊 26L以下 / 1泊～2泊 27~41L / 3泊～5泊 42~59L / 5泊～7泊 60~79L / 7泊以上 80~99L / 10泊以上 100L~ |
| サムソナイト | https://www.samsonite.co.jp/first_suitcase.html 「4 宿泊数から選ぶ」 | curl 200 | 「スーツケースは 1 泊＝10 リットルをおおよその目安」／4～6泊 50-70リットル台／1週間以上 80リットル以上／1～3泊はキャビン/機内持ち込みサイズ。同 `/category-landing/suitcase-size/`：小型（40リットル以下）／中型（約50～79リットル）4～6泊／大型（80リットル以上）1週間以上 |
| 無印良品（読みもの） | https://www.muji.com/jp/ja/store/articles/staff-blog/newlife/1613625 （2025/08/28） | 実ブラウザ（curl はタイムアウト） | 1泊なら20～30L。2泊なら30～40L、3泊なら40～50L／4泊以上 40～60L／36L→2～3泊の旅行におすすめ／75L→4泊以上／105L→4泊以上の長期旅行 |
| 無印良品（ブランドページ） | https://www.muji.com/jp/suitcase/ 「選べるサイズ」 | 実ブラウザ | 19L 1–2泊 / 35L 2–3泊 / 62L 5–6泊 / 87L 7–8泊 / 104L 9–10泊（⚠️ 2017年の記述。現行商品は 20/36/75/105L で、現行商品ページに泊数の記載なし） |

### 製品ごとの目安

| 社 | 製品 | 容量 | 泊数（原文） | URL | 取り方 |
|---|---|---|---|---|---|
| ニトリ | フレームタイプ キャリーケース 33L | 33L | 1～2泊の短期旅行や出張に最適 | https://www.nitori-net.jp/ec/product/4582548135247s/ | 実ブラウザ（JS描画。`catchCopy` として画面にも表示されるのを確認） |
| ニトリ | フロントオープン ジッパータイプ 38L | 38L | 出張や1～2泊の短期旅行 | https://www.nitori-net.jp/ec/product/4582548135377s/ | 同上 |
| ニトリ | フロントオープン ジッパータイプ 40L | 40L | 2～3泊程度の短期旅行やビジネス出張 | https://www.nitori-net.jp/ec/product/4582548136541s/ | 同上 |
| ニトリ | トップオープン ジッパータイプ 60L | 60L | 4～6泊程度の中長期旅行や出張 | https://www.nitori-net.jp/ec/product/4582548135346s/ | 同上（フレームタイプ 60L `4582548134226s` も同文） |
| RIMOWA | Essential キャビン | 36L | 3～4日のご旅行に理想的 | https://www.rimowa.com/jp/ja/luggage-collection-essential-cabin/83253661.html | 実ブラウザ（curl 403） |
| RIMOWA | Hybrid キャビン | 37L | 3～4泊のご旅行に最適 | https://www.rimowa.com/jp/ja/luggage-collection-hybrid-cabin/88353631.html | 同上 |
| RIMOWA | Essential Sleeve キャビン プラス | 46L | 4～5泊の旅行に最適 | https://www.rimowa.com/jp/ja/luggage-collection-essential-sleeve-cabin-plus/84256631.html | 同上 |
| RIMOWA | Essential チェックイン M | 60L | 1 週間の旅行に理想的 | https://www.rimowa.com/jp/ja/luggage-collection-essential-check-in-m/83263631.html | 同上 |
| RIMOWA | Essential チェックイン L | 85L | 14～15日のご旅行に理想的 | https://www.rimowa.com/jp/ja/luggage-collection-essential-check-in-l/83273661.html | 同上 |
| RIMOWA | Essential トランク プラス | 101L | 2週間以上のご旅行に理想的 | https://www.rimowa.com/jp/ja/luggage-collection-essential-trunk-plus/83280691.html | 同上 |

### 製品カード・製品表（外寸はキャスター・ハンドル込み）

| 製品 | 容量 | 外寸 | 総外寸 | 泊数タグ | URL |
|---|---|---|---|---|---|
| ace. フレットボード 29L 05431 | 29L | H54×W34×D24 | 112 | 1-2泊 | https://store.ace.jp/shop/g/g05431-01/ |
| ace. フレットボード 50L 05432 | 50L | H64×W45×D26 | 135 | 3-5泊 | https://store.ace.jp/shop/g/g05432-12/ |
| ace. フレットボード 68L 05433 | 68L | H72×W51×D28 | 151 | 5-7泊 | https://store.ace.jp/shop/g/g05433-06/ |
| ace. フレットボード 100L 05434 | 100L | H70×W53×D34 | 157 | 10泊- | https://store.ace.jp/shop/g/g05434-01/ |
| ace. パリセイド3-Z 06912 | 37L | H50×W40×D25 | 115 | 2-3泊（本文「2～3泊程度の旅に適した」） | https://store.ace.jp/shop/g/g06912-03/ |
| EDGELINK CRUZBOX 09145 | 32/39L | H55×W34×D25/29 | 114 | 2-3泊 | https://store.ace.jp/shop/g/g09145-01/ |
| Legend Walker 5516-48 | 35L | 全体55×36×24 | — | 1～2泊（タグ） | https://legend-walker.com/products/5516-48 |
| Samsonite クァントム スピナー55 | 35L | 55.0×37.0×23.0 | — | 製品ページに泊数なし。「機内持ち込み対応サイズ」 | https://www.samsonite.co.jp/samsonite/quanthom/spinner55/silver/ss-162285-1776.html |

⚠️ PROTECA スタリアCXR 02350（22L）は、一覧のタグが「1-2泊」（帯 -29L）で本文が「日帰り～1泊程度」。**同じ社のなかで帯と本文がずれる例**。記事には使っていない。

## 3. 取れなかったもの（`未検証`）

- **American Tourister**（`americantourister.jp`）：泊数フィルタ「1～3泊／4～6泊／1週間以上」はあるが容量帯の定義が見つからない
- **TUMI**（`tumi.co.jp`）：製品ライン名に「1～2泊用／1～3泊用／5～7泊用／7～10泊用」。容量との対応表なし
- **DELSEY**（`delsey.co.jp`）：「週末／1週間／1週間＋」の区分のみ
- **シフレ・サンコー・イノベーター**：curl が名前解決できず（`siffler.co.jp` `suncoluggage.co.jp` `innovator-japan.com`）。URL が違う可能性。未取得
- **RIMOWA の「日」と「泊」の区別**：公式に記載なし。計算では同一視
- **無印良品ブランドページの製品表と現行製品の対応**：19/35/62/87/104L は旧表記。現行 20/36/75/105L の商品ページに泊数なし

## 4. 検算（独立再計算）

`tools/check-article-23.py` の出力（`docs/article-23-check-output.md`）と記事の表を突き合わせた。

- 40L：ace 2〜3泊／LW 1〜2泊／Sams 4泊／無印 2泊・3泊・4泊以上の境目（製品 36L は 2〜3泊）／ニトリ 2〜3泊／RIMOWA 36〜37L 3〜4泊 → **記事と一致**
- 60L：ace 5〜7／LW 5〜7／Sams 6／無印 62L 5〜6／ニトリ 4〜6／RIMOWA 1週間 → 一致
- 1泊あたり（抜粋13行）→ 一致（ace 30〜49L 15.0〜16.3 … RIMOWA 85L 5.7〜6.1）
- 当てはめ（10L×泊数＋10〜20L）：ace 4帯○／LW 41L ×・他○／Sams ○／ニトリ 4製品○／無印 19L ×・他4製品○／RIMOWA 5製品× → 一致
- 3辺和：29L 54+34+24=112／50L 64+45+26=135／68L 72+51+28=151／100L 70+53+34=157／06912 115／09145 114・118／Legend 115／Samsonite 115 → 一致（ace の「総外寸」とも一致）

## 5. 図版

`liter-nanpaku-eyecatch`（`tools/figures/figures.py` の `NANPAKU`）。40L の目安を6社ぶん横棒で並べ、右に「2倍」。
ビルドの数値照合（40L・27〜41L・30〜49L・36L・37L・10L・60L・2倍）と重なり検査を通過。

## 6. 次に書けるもの

- 「スーツケース 158cm以内 何リットル」（サジェスト実測で需要あり。ace の 総外寸 と容量が同じページに揃っているので取りやすい）
- 「外寸と総外寸の違い／キャスター分は何cm」（ace は本体サイズと外寸を併記。29L で H47→54、50L で H57→64 と 7cm 差）

## 7. `/article-check` の結果（2026-09-16）

- A1 ビルド 0／A2 0件／A3 リンク位置 5.2%／A4 `liter-nanpaku-eyecatch` は ORDER にある／B1「実測」0件／B2 `未検証` 8箇所／B3 手計算一致
- `source-verifier`：ace・Legend Walker・サムソナイトの帯と製品数値は**すべて一致**。指摘3件を直した
  1. ⚠️ **「ace はペレットで実容量を測る」は削除。** `help_size.aspx` の「ペレット」「実容量」「1L未満の端数」は **HTML コメント内**で画面には出ていない
     （タグを剥がしただけの抽出だとコメントの中身が残る。**`<!-- -->` を先に消してから grep すること**）
  2. サムソナイトの原文は空白入り「1 泊＝10 リットル」。引用はその形に直した
  3. EDGELINK 拡張時の 3辺和 118 は公表がなく当サイトの計算。列名に「当サイトの計算」と明記
- verifier が取得できなかった 12 URL（無印 2・ニトリ 4・RIMOWA 6）は、**メインセッションが実ブラウザで
  記事の文字列をそのまま `includes` で照合し、全件 true**（RIMOWA は `check-in-size` タブ内の fetch、
  ニトリは 40L ページを開いて表示文を確認＋他3件を同一オリジンの fetch、無印はブランドページを開き読みものを fetch）
