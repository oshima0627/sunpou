# Amazonアソシエイト広告バナー（links.json）

作成日: 2026-09-18
更新: 2026-09-18（もしも media 689246 登録開始）

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
| （マーカーなし） | `affiliateEnabled` 時、記事の `category` に紐づくキーを自動プール／サイド1本。`moshimo-*` を同カテゴリで優先 |

## もしも（media 689246）

| キー | カテゴリ | 状態 |
|---|---|---|
| `moshimo-lduvin-suitcase` | cabin-bag | bannerHtml 728x90 転記済み |
| `moshimo-legend-walker` | cabin-bag | **stub**（a_id/p_id/pl_id のみ。発行HTML待ち） |
| `moshimo-gifteria-outdoor` | coolerbox | **stub** |
| `moshimo-newtec-outdoor` | coolerbox | **stub** |
| `moshimo-napnap` | baby-gate | **stub** |
| `moshimo-tedemogu` | baby-gate | **stub** |

dishwasher / monitor-arm / tire-chain / curtain / kyatatsu / measuring は Amazon フォールバックのまま。

## Amazon プロモーション 170

**未着手（pending）。** プロモーション 170 の素材・リンクはまだ台帳に入れない。着手時は Associates の発行URLだけを転記する。

## 開示

- 記事冒頭の PR 表記（`prLabel`）とフッターの Amazon 開示（`affiliateDisclosure`）は従来どおり。
- サイドバー／左レールの公式バナーに「広告」バッジは付けない（静音）。本文の公式バナーも長文 CTA は付けない。
