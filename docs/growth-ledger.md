# 成長台帳（growth ledger）

サイトに入れた変更と、効果を見るための**ベースライン**を日付つきで残す。
変更の2〜4週間後に、同じ指標をもう一度取って比べる。

- 認証情報・トークン・ログインURLはここに書かない。
- 数字は取得元と期間を必ず添える。推測は書かない。
- 行を足すときは表の末尾に追記する。マージで衝突したら **rebase して両方の行を残す**。

## 1. 変更履歴

| 日付 | 変更 | 対象ページ | PR / マージコミット |
|---|---|---|---|
| 2026-10-28 | A. アフィリエイト開示: Amazonアソシエイト（公式文言）・もしもアフィリエイト・楽天アフィリエイトの利用、記事内リンクの一部が成果報酬リンクであること、広告配信とCookieの説明を追加。運営者情報は変更なし | `/about/` `/privacy/` | #52 / `87e54c2` |
| 2026-10-28 | B. 画像転送量の削減: 一覧カードのサムネを600×315のWebP（JPEGフォールバック）に差し替え、記事ヒーローに `fetchpriority="high"`。OG画像（1200×630）は変更なし。サムネは `tools/make-card-thumbs.py` で生成し `site/public/img/card/` にコミット、HTMLの差し替えは `site/img-cards.mjs` | トップ、全カテゴリページ、全記事（ヒーロー） | #53 / `3eed458` |
| 2026-10-28 | C. 内部リンクの底上げ: 記事ページの「関連記事」を「同カテゴリ→近いカテゴリ」の順に変更、カテゴリページの記事一覧の下に近いカテゴリの「関連記事」を追加。近いカテゴリの定義は `site/related-links.inject.js` の `RELATED_CATEGORIES`。トップの「新着記事」は既に全記事を載せているため変更なし | 全41記事、全11カテゴリページ | #54 / `8313023` |
| （追記） | | | |

## 2. ベースライン（変更前）

### 2-1. Search Console

ドメインプロパティを sunpou で絞り込み。期間 2026-07-27〜2026-10-26。

| 指標 | 過去3か月 | 直近28日 |
|---|---|---|
| クリック数 | 62 | 42 |
| 表示回数 | 4,700 | 2,802 |
| CTR | 1.3% | 1.5% |
| 平均掲載順位 | 8.2 | 8.0 |

サイトマップ（sunpou）のインデックス登録: 54 URL のうち **登録済み 33 / 未登録 21**。未登録は21件すべて「検出 - インデックス未登録」。

上位ページ（過去3か月）:

| ページ | クリック | 表示回数 |
|---|---|---|
| `/cassette-konro/erabikata/` | 22 | 1,306 |
| `/coolerbox/daiwa-shimano/` | 14 | 426 |
| `/cassette-konro/donabe-nangou/` | 5 | （未記録） |
| `/coolerbox/omosa/` | 4 | （未記録） |
| `/kyatatsu/erabikata/` | 4 | （未記録） |

### 2-2. Amazonアソシエイト（トラッキングID sunpou-22）

直近30日（〜2026-10-28）: クリック **60** / 注文商品数 **0** / 紹介料 **¥0**。

### 2-3. 画像転送量（変更B。Chromium、全体をスクロールした時点の画像バイト数）

| ページ | 変更前 | 変更後 |
|---|---|---|
| トップ | 4,878,575 B | 757,678 B |
| `/coolerbox/` | 1,441,285 B | 265,774 B |
| `/washer/` | 655,141 B | 75,592 B |
| トップ（初期表示のみ・PC 1366×768） | 718,829 B | 104,578 B |
| トップ（初期表示のみ・モバイル 390×844 @2x） | 121,803 B | 17,664 B |

もしもアフィリエイトなど第三者の画像は、計測では遮断したため含まない。

### 2-4. 内部被リンク数（変更C）

数え方（ビルド後の `dist/` のHTMLから集計）: **トップ・カテゴリページ・他記事の本文領域**のうち、その記事へのリンクを持つページの数。
自己リンク、ヘッダー・左右の広告レール・サイドバー（全ページ共通の新着5本）・フッター、HTMLサイトマップは数えない。

- 変更前の最小値: **2**（他記事からのリンクが0本。ベビーゲート／遮光カーテン／食洗機／モニターアーム／タイヤチェーンの各1記事。同カテゴリが1本しかなく、関連記事の枠が全カテゴリの新着＝洗濯機記事で埋まっていた）
- 変更後の最小値: **6**（全41記事が3以上）

| 記事 | 変更前 | 変更後 | うち他記事から（前→後） |
|---|---|---|---|
| `/baby-gate/opening-width-fit/` | 2 | 6 | 0 → 2 |
| `/curtain/ready-made-rail-fit/` | 2 | 13 | 0 → 8 |
| `/dishwasher/countertop-fit-outer-dims/` | 2 | 13 | 0 → 9 |
| `/monitor-arm/desk-thickness-clamp-fit/` | 2 | 6 | 0 → 2 |
| `/tire-chain/case-size-trunk-fit/` | 2 | 9 | 0 → 6 |
| `/fridge/delivery-path-fit/` | 4 | 13 | 2 → 9 |
| `/fridge/install-clearance-outer-dims/` | 4 | 7 | 2 → 3 |
| `/fridge/side-top-clearance-door-swing/` | 4 | 7 | 2 → 3 |
| `/cassette-konro/bombe-honsuu/` | 6 | 10 | 4 → 7 |
| `/cassette-konro/donabe-nangou/` | 6 | 10 | 4 → 7 |
| `/cassette-konro/donabe-ninzuu/` | 6 | 9 | 4 → 6 |
| `/cassette-konro/erabikata/` | 6 | 17 | 4 → 14 |
| `/cassette-konro/nenshou-jikan/` | 6 | 9 | 4 → 6 |
| `/cabin-bag/airline-fit-outer-dims/` | 7 | 9 | 5 → 6 |
| `/cabin-bag/body-vs-outer-dims/` | 7 | 9 | 5 → 6 |
| `/cabin-bag/expandable-vs-fixed-outer-dims/` | 7 | 9 | 5 → 6 |
| `/cabin-bag/liter-nanpaku/` | 7 | 9 | 5 → 6 |
| `/cabin-bag/outer-sum-158-liters/` | 7 | 9 | 5 → 6 |
| `/cabin-bag/shinkansen-fit-outer-dims/` | 7 | 8 | 5 → 5 |
| `/coolerbox/horeizai-maisuu/` | 7 | 8 | 5 → 5 |
| `/coolerbox/omosa/` | 7 | 8 | 5 → 5 |
| `/coolerbox/uchinori-nagasa/` | 7 | 7 | 5 → 5 |
| `/kyatatsu/erabikata/` | 7 | 9 | 5 → 6 |
| `/kyatatsu/fumidai-kyatatsu/` | 7 | 9 | 5 → 6 |
| `/kyatatsu/kaidan/` | 7 | 9 | 5 → 6 |
| `/kyatatsu/omosa/` | 7 | 8 | 5 → 5 |
| `/kyatatsu/secchi/` | 7 | 7 | 5 → 5 |
| `/kyatatsu/tenban-takasa/` | 7 | 7 | 5 → 5 |
| `/washer/drum-waterproof-pan-fit/` | 7 | 10 | 5 → 8 |
| `/coolerbox/2l-tateru/` | 8 | 10 | 6 → 7 |
| `/coolerbox/500ml-honsuu/` | 8 | 10 | 6 → 7 |
| `/coolerbox/coleman-uchinori/` | 8 | 10 | 6 → 7 |
| `/coolerbox/yoryo-uchinori/` | 8 | 8 | 6 → 6 |
| `/coolerbox/daiwa-shimano/` | 9 | 10 | 7 → 8 |
| `/coolerbox/horeizai-honsuu/` | 9 | 10 | 7 → 8 |
| `/coolerbox/erabikata/` | 11 | 17 | 9 → 14 |
| `/washer/vertical-lid-open-height/` | 12 | 9 | 10 → 6 |
| `/washer/vertical-waterproof-pan-fit/` | 12 | 8 | 10 → 5 |
| `/washer/drum-door-open-front-space/` | 15 | 13 | 13 → 9 |
| `/washer/lixil-panasonic-pan-inner-depth/` | 15 | 13 | 13 → 9 |
| `/washer/vertical-opening-height/` | 20 | 11 | 18 → 7 |

3未満だった記事（変更前）は、上位の5行（`/baby-gate/opening-width-fit/` `/curtain/ready-made-rail-fit/` `/dishwasher/countertop-fit-outer-dims/` `/monitor-arm/desk-thickness-clamp-fit/` `/tire-chain/case-size-trunk-fit/`）。

## 3. 変更後の数字（2〜4週間後に記入）

取得日: （未記入）

| 指標 | 過去3か月 | 直近28日 |
|---|---|---|
| クリック数 | | |
| 表示回数 | | |
| CTR | | |
| 平均掲載順位 | | |

- サイトマップのインデックス登録（登録済み / 未登録）: 
- 上位ページ（クリック・表示回数）: 
- Amazonアソシエイト（直近30日のクリック / 注文商品数 / 紹介料）: 
- 変更Bの確認（Core Web Vitals や PageSpeed の LCP）: 

## 4. 実験: 直リンク化・バナー削減

別の担当が、記事本文のアフィリエイトリンクとバナーの配置を変える。実施した日、変更内容、対象記事、変更前後の数字（記事ごとのクリック数・注文商品数、Search Console の指標）は、ここに追記する。

| 日付 | 変更内容 | 対象記事 | 変更前の数字 | 変更後の数字 | PR |
|---|---|---|---|---|---|
| （追記） | | | | | |

注意: `/about/` には「広告リンクは、Amazonの検索結果ページに向けています」という記述がある。直リンクに切り替えたら、この記述を実態に合わせて直すこと。
