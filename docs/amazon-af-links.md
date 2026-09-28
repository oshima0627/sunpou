# Amazonアソシエイト広告バナー（links.json）

作成日: 2026-09-18
更新: 2026-09-29（左右レール配線 + merchant bannerHtmlSide 追加）

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
| `[[AFLeft:キー]]` | 左レール（`.l-rail`）へ。空なら CSS で非表示。記事では未指定時も `pickCategoryLeftKeys` で自動 |
| （マーカーなし） | `affiliateEnabled` 時、記事の `category` に紐づくキーを自動プール／**左右レール各1本**。`moshimo-*` を同カテゴリで優先。右は `pickCategorySideKeys`、左は `pickCategoryLeftKeys`（右と別キー・160x600 優先） |

## もしも（media 689246）

| キー | カテゴリ | 状態 |
|---|---|---|
| `moshimo-lduvin-suitcase` | cabin-bag | bannerHtml 728x90 + bannerHtmlSide 300x250 (`pl_id=64718`) |
| `moshimo-legend-walker` | cabin-bag | bannerHtml 728x90 + bannerHtmlSide **160x600** (`pl_id=63106`) |
| `moshimo-gifteria-outdoor` | coolerbox | bannerHtml 728x90 + bannerHtmlSide **160x600** (`pl_id=86751`) |
| `moshimo-newtec-outdoor` | coolerbox | bannerHtml 728x90 + bannerHtmlSide 300x250 (`pl_id=70478`) |
| `moshimo-napnap` | baby-gate | bannerHtml 300x250 + bannerHtmlSide 300x250 (`pl_id=29865`) |
| `moshimo-tedemogu` | baby-gate | bannerHtml 728x90 + bannerHtmlSide 300x250 (`pl_id=88553`) |
| `moshimo-amazon` | dishwasher / monitor-arm / tire-chain / curtain / kyatatsu / cassette-konro / fridge | bannerHtml 728x90 (`pl_id=4153`) + bannerHtmlSide 300x250 (`pl_id=4157`)。**160x600 は Amazon に無し** |

左右レール: 記事は `bannerHtmlSide` 必須。右＝カテゴリ内 160x600 優先、左＝右と別キー（残りカテゴリ or グローバル `legend-walker` / `gifteria` の 160x600）。モバイル（&lt;1280px）は左レール非表示、右サイドは既存どおり下へ。measuring は明示 `[[AF:]]` のみ。

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
