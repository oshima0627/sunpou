# site — 「寸法で選ぶ」（Cloudflare Workers Static Assets）

`content/articles/*.md` を HTML に変換して `dist/` に出し、Cloudflare Workers の
Static Assets として配信する。**Worker のコードは無く、アセット配信だけ**の構成。

## コマンド

```bash
npm install                # 初回のみ
npm run build              # content/ → dist/
npm run dev                # build してから wrangler dev（http://localhost:8787）
npm run deploy             # build してから wrangler deploy
```

## 検証済みの動作（2026-08-24・ローカル `wrangler dev` で確認）

実際にブラウザで開いて確認した内容。**推測ではない。**

| 項目 | 結果 |
|---|---|
| 記事ページのビルド | `/coolerbox/500ml-honsuu/` が生成される |
| `lang` / `title` / `description` / `canonical` / OG | すべて出力されている |
| JSON-LD | `@type: Article` で出力 |
| 表5つ | **全て `.table-wrap` の中で横スクロール**（本文は横に伸びない） |
| 375px 幅（モバイル） | `scrollWidth == clientWidth == 375`。**ページ自体は横スクロールしない** |
| 存在しないURL | **HTTP 404** を返し `404.html` を表示 |
| `/sitemap.xml`・`/robots.txt` | 正しい内容で配信 |
| コンソールエラー | なし |
| 開示文言 | `affiliateEnabled=false` のとき**出力されない**（意図どおり） |

## 記事の追加

`content/articles/<name>.md` を作る。front matter は5項目すべて必須（欠けるとビルドが落ちる）。

```markdown
---
title: 記事タイトル
description: 検索結果に出る説明文
slug: coolerbox/500ml-honsuu
published: 2026-08-24
updated: 2026-08-24
---

本文（GFM。表が使える）
```

商品リンクを置きたい位置には `[[LINK:商品名]]` と書く。

## ⚠️ アフィリエイトリンクと開示表記の扱い

`content/site.json` の **`affiliateEnabled` が false のうちは、リンクも開示文言も出力しない。**

理由：リンクが1本も無い状態で「Amazonのアソシエイトとして、〜は適格販売により収入を得ています」と
書くのは**事実に反する**。同じ理由で PR 表記も出さず、代わりに
「現在このページに広告リンクはありません」と表示している。

**Amazonアソシエイトの審査に合格した時点で `affiliateEnabled: true` にする。**
そのとき `build.mjs` の `resolveLinks()` が例外を投げるので、実リンクの解決処理を実装すること
（意図的にそうしてある。true にしただけでリンクが空のまま公開されるのを防ぐため）。

なお開示は**2種類必要**で、片方では足りない。
1. **Amazon規約側** — サイトの目立つ位置に開示文言（`affiliateDisclosure`）
2. **景表法ステマ規制側** — 記事に「PR」「広告」等の表記（`prLabel`）

詳細は `../docs/affiliate-program-facts.md` 第3節・第6節。

## 設定でわざとそうしている箇所

| 設定 | 値 | 理由 |
|---|---|---|
| `assets.not_found_handling` | `"404-page"` | SPA ではないので `"single-page-application"` にしてはいけない。存在しないURLが200を返し、Google に重複コンテンツとして拾われる |
| `assets.html_handling` | `"auto-trailing-slash"`（既定） | canonical を `/slug/` で出しているので、URL 側も末尾スラッシュに正規化して一致させる |
| `main` | **無し** | 動的処理が無いため。必要になったら `main` を足し、`assets.run_worker_first` で対象パスだけ Worker に通す（全部通すと無料枠の10万リクエスト/日を無駄に消費する） |
| `dist` のクリーン | ディレクトリごと消さず中身だけ | `wrangler dev` 起動中に再ビルドすると、Windows ではディレクトリ削除が EPERM で失敗する |

## 公開の前提（2026-08-24 に実際に確認済み）

| 項目 | 状態 |
|---|---|
| Cloudflare アカウント | **あり** — `Oshima6.27@gmail.com's Account` / ID `7f78c5fbb2ed33d229d8b09b1d872fa1` |
| `wrangler login` | **完了済み。** OAuth トークンあり（`workers_scripts (write)` を含む）。`npx wrangler whoami` で確認 |
| 独自ドメイン | **`nexeed-lab.com` を保有**（Cloudflare にゾーン登録済み） |
| Worker 名 `sunpou` の衝突 | **なし**（既存23個と重複していない） |

→ **`npm run deploy` は今すぐ通る状態。**

### ⚠️ ただしデプロイ前に必ず直すこと

**`content/site.json` の `origin` が `https://sunpou.example.workers.dev` のままになっている。**
**canonical と sitemap.xml がこの値を使う**ため、書き換えずに公開すると
Google に存在しないURLを正規URLとして伝えることになる。SEO目的が最初から崩れる。

公開URLの候補：

| 選択肢 | URL | 評価 |
|---|---|---|
| サブドメイン | `sunpou.nexeed-lab.com` | **SEOで最も有利**（既存ドメインの評価を一部引き継げる）。追加費用0円 |
| workers.dev | `sunpou.<subdomain>.workers.dev` | 0円で即公開。共有ドメインなのでSEOは不利 |
| 新規ドメイン | 例 `sunpou.jp` | ブランドを分離できる。年1,500円前後 |

**未決定。** 決まったら `origin` を書き換えてからデプロイする。

## 未確定

- **公開URL（上表）。** これが決まらないとデプロイできない
- **アクセス解析が未導入。** クリック率と購入率の実測が収益モデルの鍵
  （`../docs/serp-check.md`）なので、公開と同時に入れる。
  このアカウントで Cloudflare Web Analytics が使える
- サイト名「寸法で選ぶ」／Worker 名 `sunpou` は、寸法で決まるジャンル専門という前提で付けた。
  ⚠️ **ランニングコスト系（おむつ用ゴミ箱・ラベルライター）は名前の射程外。**
  当面は価格制約でそもそも書けないジャンルなので問題にならないが、
  将来広げるなら別サイトにするほうが専門性を保てる
