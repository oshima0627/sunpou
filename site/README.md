# site — 「寸法で選ぶ」（Cloudflare Workers Static Assets）

`content/articles/*.md` を HTML に変換して `dist/` に出し、Cloudflare Workers の
Static Assets として配信する。**Worker のコードは無く、アセット配信だけ**の構成。

## デプロイは Git 連携で自動（2026-08-24 設定）

**`main` に push すると Cloudflare Workers Builds がビルドしてデプロイする。**
手元から `npm run deploy` を叩く必要はない（叩いても動くが、Git の履歴とズレるので普段は使わない）。

| 設定 | 値 |
|---|---|
| リポジトリ | `oshima0627/amazon-affiliate` |
| 本番ブランチ | `main` |
| **Root directory（Path）** | **`/site`** ← これを指定しないと `package.json` を見つけられない |
| ビルドコマンド | `npm run build`（依存のインストールは Workers Builds が自動でやる） |
| デプロイコマンド | `npx wrangler deploy` |
| 非本番ブランチ | `npx wrangler versions upload`（プレビュー版を作るだけで本番には出ない） |
| Preview builds | 有効 |

## コマンド（ローカル開発）

```bash
npm install                # 初回のみ
npm run build              # content/ → dist/
npm run dev                # build してから wrangler dev（http://localhost:8787）
npm run deploy             # 手動デプロイ。通常は Git 連携に任せる
```

## デザイン

`tsuzukiblog.org`（SWELL テーマ）を参考に設計パターンを取り込んでいる。**色やコードのコピーではなく、
計測した設計値に合わせている**（`public/styles.css` の冒頭コメント参照）。

| 要素 | 参考サイトの実測値 | このサイト |
|---|---|---|
| 背景 / 本文色 | `#fcfcfc` / `#434347` | **同値** |
| 本文サイズ / 行間 | 16px（本文 p は 17px）/ 1.6 | **同値** |
| H2 | 左に `8px solid #213555`＋極薄背景、`margin-top` 95px | 8px 縦棒＋`rgba(33,53,85,.035)`、`margin-top` 5.6rem |
| H3 | 罫線なし、下パディングのみ | 同じ考え方（罫線なし・余白で区切る） |
| リンク | `#0077c6`・**太字＋下線** | **同値** |
| レイアウト | 本文 716px ＋ サイドバー 304px | 同じ2カラム（900px 以下で1カラム） |
| 目次 | 記事冒頭のボックス | h2/h3 から自動生成（h2 が3個未満の記事には出さない） |

参考サイトはライトのみだが、こちらは `prefers-color-scheme` でダークにも対応させている。

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
| 目次 | h2/h3 に `id` を採番して自動生成。入れ子も正しい |
| 2カラム | デスクトップ 1280px で本文 679px ＋ サイドバー 304px、サイドバーは `sticky` |
| モバイル 375px | **1カラムに落ち、サイドバーは本文の下**（`position: static`）。横スクロールなし |
| 本文リンク | `#0077c6`・太字・下線（参考サイトと同じ）。目次のリンクだけプレーン |

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

## 本番稼働中（2026-08-24 デプロイ）

**https://sunpou.nexeed-lab.com/**

`wrangler.jsonc` の `routes` に `custom_domain: true` で指定しているため、
DNSレコードと証書は Cloudflare 側が自動作成した。

### 本番で確認した結果（curl で実際に叩いた）

| 項目 | 結果 |
|---|---|
| トップ | 200 |
| 記事 `/coolerbox/500ml-honsuu` | 301 で `/` 付きへ正規化 → 200 |
| 存在しないURL | **404** |
| `<html lang>` | `ja` |
| canonical / og:url | `https://sunpou.nexeed-lab.com/coolerbox/500ml-honsuu/`（一致） |
| `/robots.txt`・`/sitemap.xml` | 配信されている |

### ⚠️ robots.txt に Cloudflare が Managed content を差し込んでいる

`/robots.txt` を実際に見ると、**こちらが書いた内容の前に Cloudflare 管理のブロックが挿入されている。**
その中に **`User-agent: Amazonbot` / `Disallow: /`** が含まれている。

```
User-agent: Amazonbot
Disallow: /
```

**Amazonアフィリエイトのサイトで Amazonbot を拒否している状態。**
これは zone（`nexeed-lab.com`）側の Cloudflare 設定（AI Crawl Control / Managed robots.txt）由来で、
このリポジトリの `robots.txt` では上書きできない。

→ **ダッシュボードで Amazonbot を許可に変えるか検討すること**（zone 設定の変更なので未実施）。
なお `Content-Signal: search=yes` と `User-agent: *  Allow: /` は入っているので、
**Googlebot は通る**（検索流入そのものは妨げていない）。

## 未確定

- ~~アクセス解析~~ → **導入済み（2026-08-24）。** Cloudflare Web Analytics。
  ビーコンが実際に `https://cloudflareinsights.com/cdn-cgi/rum` へリクエストを出すところまで確認済み。
  トークンは `content/site.json` の `webAnalyticsToken`（HTMLに出る公開値なので秘密ではない）。
  空にすれば計測タグを出力しない。
  - **測っているのは分母（セッション数）だけ。** クリック数と注文数は
    アソシエイト・セントラルのレポート側から取る
- サイト名「寸法で選ぶ」／Worker 名 `sunpou` は、寸法で決まるジャンル専門という前提で付けた。
  ⚠️ **ランニングコスト系（おむつ用ゴミ箱・ラベルライター）は名前の射程外。**
  当面は価格制約でそもそも書けないジャンルなので問題にならないが、
  将来広げるなら別サイトにするほうが専門性を保てる
