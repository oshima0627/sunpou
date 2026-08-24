# site — 「実寸で選ぶ」（Cloudflare Workers Static Assets）

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

## ⚠️ 公開する前に必要なこと（こちらでは実行できない作業）

1. **Cloudflare アカウントの作成**
2. **`npx wrangler login`** — ブラウザでの OAuth 認可が必要
3. **`content/site.json` の `origin` を実際の公開URLに書き換える**
   → 現在は `https://jissun.example.workers.dev` というプレースホルダ。
   **canonical と sitemap がこの値を使うので、書き換えないまま公開すると
   Google に間違ったURLを伝えることになる**
4. （任意）独自ドメインの取得と紐付け

`npm run deploy` は 2 が済んでいないと失敗する。

## 未確定

- **サイト名「実寸で選ぶ」と Worker 名 `jissun` は仮。** 変えるなら
  `content/site.json` の `name` と `wrangler.jsonc` の `name` の両方
- アクセス解析を入れていない。**クリック率と購入率の実測が収益モデルの鍵**
  （`../docs/serp-check.md`）なので、公開前に何か入れる必要がある
