# Amazonアソシエイト広告バナー（links.json）

作成日: 2026-09-18
更新: 2026-09-24（もしも Amazon.co.jp p_id=170 APPROVED → moshimo-amazon 転記）

## なにをする仕組みか

`site/content/links.json` は広告リンクの台帳です。記事本文の `[[AF:キー]]` / `[[AFSide:キー]]` / `[[AFLeft:キー]]`、およびカテゴリ既定の H2 間自動挿入・サイドバー静音バナーが、ここを引きます。

- **Amazon:** Associates 形式のみ（`tag=sunpou-22`）。Creators API / 商品画像は使わない。`bannerHtml` が無いキーは CSS 自前バナー。
- **もしも:** **media 689246 のみ**（kakei の 687816 は使わない）。管理画面が発行した HTML を `bannerHtml` / `bannerHtmlSide` に文字どおり転記する。URL の推測組み立てはしない。
- 既存の `[[LINK:検索語]]`（表セル・製品カード）はそのまま。

## マーカー

| 書き方 | 効果 |
|---|---|
| `[[AF:キー]]` | プールに入り、H2 間に回転挿入（本文末のマーカーは剥がす） |
| `[[AFSide:キー]]` | 右サイドバーへ静音バナー（本文には出さない） |
| `[[AFLeft:キー]]` | 左レール（`.l-rail`）へ。空なら CSS で非表示 |
| （マーカーなし） | `affiliateEnabled` 時、記事の `category` に紐づくキーを自動プール／サイド1本。`moshimo-*` を同カテゴリで優先。サイドは `bannerHtmlSide` があるキーを優先（`pickCategorySideKeys`） |

## もしも（media 689246）

| キー | カテゴリ | 状態 |
|---|---|---|
| `moshimo-lduvin-suitcase` | cabin-bag | bannerHtml 728x90 転記済み |
| `moshimo-legend-walker` | cabin-bag | bannerHtml 728x90 + bannerHtmlSide 160x600 転記済み |
| `moshimo-gifteria-outdoor` | coolerbox | bannerHtml 728x90 + bannerHtmlSide 160x600 転記済み |
| `moshimo-newtec-outdoor` | coolerbox | bannerHtml 728x90 転記済み |
| `moshimo-napnap` | baby-gate | bannerHtml 300x250 転記済み |
| `moshimo-tedemogu` | baby-gate | bannerHtml 728x90 転記済み |
| `moshimo-amazon` | dishwasher / monitor-arm / tire-chain / curtain / kyatatsu / cassette-konro / fridge | bannerHtml 728x90 (4153) + bannerHtmlSide 300x250 (4157) APPROVED |

cabin-bag / coolerbox / baby-gate は merchant バナー優先。上記以外のカテゴリは `moshimo-amazon` が H2間・サイドのフォールバック。measuring は明示 `[[AF:]]` のみ（categories 空のまま）。

## Amazon プロモーション 170（もしも）

**APPROVED（2026-09-24）。** media 689246 / a_id=5809024 / p_id=170 / pc_id=185。

| キー | 用途 | サイズ / pl_id |
|---|---|---|
| `moshimo-amazon` | カテゴリ固有 moshimo が無い枠の本文・サイド差し替え | body 728x90 `pl_id=4153` / side 300x250 `pl_id=4157` |

対象カテゴリ: dishwasher / monitor-arm / tire-chain / curtain / kyatatsu / cassette-konro / fridge。  
cabin-bag / coolerbox / baby-gate は既存の merchant `moshimo-*` を優先（本キーは入れない）。  
Associates（`tag=sunpou-22`）の検索・商品リンク（`amazon-*` と `[[LINK:]]`）はそのまま維持。media 687816 は使わない。

## 開示

- 記事冒頭の PR 表記（`prLabel`）とフッターの Amazon 開示（`affiliateDisclosure`）は従来どおり。
- サイドバー／左レールの公式バナーに「広告」バッジは付けない（静音）。本文の公式バナーも長文 CTA は付けない。
