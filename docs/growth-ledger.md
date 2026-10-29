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
| 2026-10-28 | D. Amazonリンクの直リンク化とバナー削減（実験）: 型番・サイズを商品ページで確認できた機種だけ `https://www.amazon.co.jp/dp/<ASIN>?tag=sunpou-22` に切替（台帳 `site/content/amazon-products.json`）。本文の汎用バナー（機種と無関係）を2カテゴリ15記事で廃止。詳細は §4-1 | `/cassette-konro/*` 5記事、`/coolerbox/*` 10記事（about / privacy の文言も実態に合わせて修正） | #56 `2dccfb1`、#57 `c43e6c1` |
| 2026-10-29 | E. 記事41を追加: 冷蔵庫の置き場所を有効幅650/700/760mm・有効奥行650/710/760mmの上限で判定。11機種の最小設置幅と据付必要奥行。幅700mm×奥行650mmは2機種、幅の余裕10mmを足すと1機種。Amazon直リンクは確認できた NR-C37WS2L-K（B0FR8ZC34P）のみ。他機種は未掲載 | `/fridge/niche-width-depth-fit/` と冷蔵庫カテゴリ、既存冷蔵庫3記事からの内部リンク | （PR番号は作成後にこのセルを更新） |
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
| 2026-10-28 | 直リンク化＋本文バナー廃止（2カテゴリ限定） | `/cassette-konro/*` 5記事、`/coolerbox/*` 10記事 | §4-1 の「ベースライン」 | （2〜4週間後に記入） | #56 `2dccfb1`、#57 `c43e6c1` |
| （追記） | | | | | |

注意（対応済み 2026-10-28）: `/about/` と `/privacy/` の「検索結果ページに向けています」という記述は、直リンクと検索リンクの併用に合わせて直した。直リンクの対象を広げたら、「確認できた機種だけ」の記述が実態と合っているか見直す。

### 4-1. 直リンク化・バナー削減（2026-10-28 実施）の記録

**やったこと**
- `[[LINK:商品名]]` の商品名が `content/amazon-products.json` にあれば商品ページ（`/dp/<ASIN>?tag=sunpou-22`）へ。無ければ従来の検索結果ページ。`rel="nofollow sponsored noopener"`、PR表記、フッターの開示文言は変更なし。価格・在庫は出していない。
- 各 ASIN は2026-10-28に商品ページを開き、製品名・型番・サイズ（バリエーション商品はサイズ/型の選択肢まで）が記事の機種と一致するのを確認した。台帳に `amazonTitle`（確認時の商品名）を残してある。
- front matter `afbody: none` を付けた15記事は、H2の間に出していた機種と無関係な汎用バナーを廃止。製品カード・「〜をAmazonで探す」の判断CTA・左右の広告レール（縦型のみ・スクロール追従なし）は従来どおり。レールのクリエイティブは変えていない。
- 規約確認（Associates Central、2026-10-28）: 運営規約 §5 の識別文言「Amazonのアソシエイトとして、［名称］は適格販売により収入を得ています。」は現行フッターのとおり。プログラム・ポリシー（Special Links）は、`tag` を各リンクURLに入れること、商品リンクは当該商品の詳細ページへ直接つなぐこと（検索結果は「商品リスト」扱いで、オリジナルコンテンツを添える条件）、価格・在庫はAmazonが配信するリンクかAPI取得でなければ出せないこと、を定めている。直リンクは許容される形。

**記事ごとの数（バナー / 製品カード / 判断CTA。変更前 → 変更後）と、Amazonリンクのうち直リンク / 全体（変更後）**

| ページ | 変更前 | 変更後 | 直リンク / 全体 |
|---|---|---|---|
| `/cassette-konro/erabikata/` | 8 / 5 / 1（計14） | 0 / 5 / 1（計6） | 23 / 27 |
| `/cassette-konro/donabe-nangou/` | 7 / 1 / 1（計9） | 0 / 1 / 1（計2） | 10 / 12 |
| `/cassette-konro/bombe-honsuu/` | 8 / 1 / 1（計10） | 0 / 1 / 1（計2） | 4 / 6 |
| `/cassette-konro/nenshou-jikan/` | 8 / 1 / 1（計10） | 0 / 1 / 1（計2） | 12 / 16 |
| `/cassette-konro/donabe-ninzuu/` | 6 / 2 / 1（計9） | 0 / 2 / 1（計3） | 8 / 9 |
| `/coolerbox/erabikata/` | 8 / 3 / 1（計12） | 0 / 3 / 1（計4） | 42 / 55 |
| `/coolerbox/daiwa-shimano/` | 7 / 1 / 1（計9） | 0 / 1 / 1（計2） | 5 / 11 |
| `/coolerbox/omosa/` | 8 / 3 / 1（計12） | 0 / 3 / 1（計4） | 20 / 22 |
| `/coolerbox/500ml-honsuu/` | 8 / 1 / 1（計10） | 0 / 1 / 1（計2） | 11 / 13 |
| `/coolerbox/2l-tateru/` | 7 / 1 / 1（計9） | 0 / 1 / 1（計2） | 8 / 10 |
| `/coolerbox/coleman-uchinori/` | 7 / 1 / 1（計9） | 0 / 1 / 1（計2） | 11 / 14 |
| `/coolerbox/uchinori-nagasa/` | 5 / 1 / 1（計7） | 0 / 1 / 1（計2） | 10 / 17 |
| `/coolerbox/horeizai-honsuu/` | 6 / 1 / 1（計8） | 0 / 1 / 1（計2） | 8 / 10 |
| `/coolerbox/horeizai-maisuu/` | 5 / 1 / 1（計7） | 0 / 1 / 1（計2） | 9 / 11 |
| `/coolerbox/yoryo-uchinori/` | 8 / 1 / 1（計10） | 0 / 1 / 1（計2） | 7 / 8 |

- 合計: 本文バナー106 → 0。Amazonリンク241本のうち188本（78%）が商品ページ直リンク。残り53本は未確認機種の検索リンクと、判断CTA（15本）の検索リンク。
- 製品カードが3を超える `/cassette-konro/erabikata/`（5枚）は、カードが記事の本文（スペックの要約）なので減らしていない。

**直リンクにした機種（ASIN。42機種）**: `content/amazon-products.json` を参照（キーが記事の商品名、`amazonTitle` が確認時のAmazon上の商品名）。ダイワは S/VS/VSS 等の型まで一致を確認した。HD II 4800/6000・プロバイザートランクHD II 3500・プロバイザーREX 2800 は、Amazonに「スチロール」仕様のページがあるのでその型で確認した。

**未検証（検索リンクのまま）**
- イワタニ スマート CB-SMT-1: Amazonで該当ページを特定できなかった。
- イワタニ 達人スリムII: 製造から約10年の買い替え対象として載せている旧機種なので、直リンクにしなかった。
- アイリスオーヤマ HUGEL 15L: Amazonで該当ページを特定できなかった。
- シマノ フィクセル 9/12/17/22/30L、スペーザ 250/350、スペーザ ホエール 450/600/650: ラインの違い（ベイシス/リミテッド等）で数値が変わり、記事の数値は複数ラインにまたがる。どのラインを指すか決まらないので、1つのASINに決められない。

**ベースライン（変更前。比べる元）**
- Amazonアソシエイト（sunpou-22）直近30日（〜2026-10-28）: クリック **60** / 注文商品数 **0** / 紹介料 **¥0**。
- Search Console のクリック（過去3か月＝2026-07-27〜2026-10-26）: §2-1 の表のとおり。対象15記事のうち数字があるのは `/cassette-konro/erabikata/` 22、`/coolerbox/daiwa-shimano/` 14、`/cassette-konro/donabe-nangou/` 5、`/coolerbox/omosa/` 4。ほかの11記事の記事別クリックは未記録（比べる時に、変更日より前の同じ長さの期間を取り直して並べる）。
- 参考: `/kyatatsu/erabikata/` 4（このカテゴリは今回触っていない。比較用の「触っていない側」として使える）。

**2〜4週間後の比べ方**
1. 変更日（2026-10-28）の前と後で、同じ長さの期間を取る（例: 後が3週間なら、前は 2026-10-07〜10-27 の3週間）。
2. Search Console: 対象15記事のページ別クリック・表示回数・平均掲載順位。触っていない `/kyatatsu/*` も同じ期間で出して、全体の増減と切り分ける。
3. Amazonアソシエイト: sunpou-22 のクリック数・注文商品数・紹介料を同じ長さの期間で。直リンク化したページから来たクリックを見分ける機能はないので、サイト全体の数で比べる。
4. クリック数が増えて注文商品数が増えない場合は、リンク先の機種（ASIN）がずれていないか、台帳の `amazonTitle` と実際の商品ページを見直す。ASINの出品が終わっていたら台帳から外すと、その商品名は検索リンクに戻る。
5. 戻す場合: #56（カセットコンロ）、#57（クーラーボックス）をそれぞれ revert。

