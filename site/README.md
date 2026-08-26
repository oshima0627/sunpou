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
| **ヘッダー** | 高さ94px／背景`#fdfdfd`／罫線なし＋`box-shadow 0 1px 4px rgba(0,0,0,.12)`／z-index 100 | **同値** |
| **ロゴ** | テキスト 24px・700・`#333` | **同値** |
| **ナビ** | 16px・400・`#333`／padding 左右12px／letter-spacing 0.4px／右寄せ | **同値** |

⚠️ ヘッダーで意図的に変えている点：
- 参考サイトはデスクトップ `position: relative`／モバイル `sticky`。**こちらは両方 sticky**（追従の実用性を取った）
- 参考サイトのモバイルは**ハンバーガーメニュー**。こちらは JS を持たない方針なので
  **ナビを横スクロールの1行**にした。折り返すとヘッダーが113pxになり sticky で画面を圧迫するため。
  結果、モバイルの高さは参考サイトと同じ **84px**
- **タグラインはヘッダーから外した**（参考サイトに無いため）。`<title>` とサイドバーには残している
| 目次 | 記事冒頭のボックス | h2/h3 から自動生成（h2 が3個未満の記事には出さない） |

参考サイトはライトのみでダークモードを持たないため、こちらも `color-scheme: light` でライト固定にしている。

### 参考サイトに合わせて入れた機能

| 機能 | 実装 |
|---|---|
| グローバルナビ | カテゴリ＋固定ページ。`content/site.json` の `categories` と `nav` から生成 |
| パンくず | ホーム › カテゴリ › 記事 |
| アイキャッチ | front matter の `eyecatch`。og:image と JSON-LD の image も兼ねる |
| 目次 | h2/h3 から自動生成。**本文冒頭とサイドバーの2箇所**（参考サイトと同じ） |
| 本文の図版 | `![alt](/img/…)` を `<figure>` に変換し、alt をキャプションとして表示 |
| SNSシェア | X／Facebook／はてブ／LINE。**JS を使わず共有URLへのリンクだけ** |
| 関連記事 | 記事下に他記事。**0件のときはセクションごと出さない** |
| カテゴリーページ | `/coolerbox/` を自動生成（ただし下記の条件つき） |
| 記事カード | サムネイル＋カテゴリラベル＋説明＋更新日 |
| サイドバー | 目次／このサイトについて／新着記事／カテゴリー |
| フッターナビ | ヘッダーと同じ項目 |
| ページトップ | `href="#"` のみ。JS なし |
| 固定ページ | `content/pages/*.md` → 運営者情報・プライバシーポリシー。サイトマップは自動生成 |

### ⚠️ カテゴリが1つの間の扱い

`site.json` の `categories` が**1件しかない間**は、次の3つを自動で抑制している
（`showCategoryNav`）。**2件目を足した時点で自動的に元に戻る。**

| 対象 | 1カテゴリのとき | 理由 |
|---|---|---|
| ヘッダー／フッターのナビ | **カテゴリを出さない** | 「寸法で選ぶ」の中の「クーラーボックス」はサイト名とほぼ同義で、情報量がゼロ |
| サイドバーの「カテゴリー」 | **出さない** | 同上 |
| `/<category>/` ページ | **`noindex,follow`**／sitemap.xml からも除外 | トップページと中身がほぼ同じで、**重複コンテンツとして競合する**ため |

カテゴリページ自体は**残していて 200 で見られる**。記事のパンくず（ホーム › クーラーボックス › 記事）と
`/sitemap/` からたどれるので、導線は切れていない。`follow` なので記事へのリンクもたどられる。

### 参考サイトにあるが入れていないもの（理由つき）

| 機能 | 入れていない理由 |
|---|---|
| **著者プロフィール（経歴・写真）** | **運営者の情報を持っていないため。捏造しない。** `content/pages/about.md` に記入欄だけ用意した |
| サイト内検索 | 静的サイトで全文検索を実装しても、記事が1本では機能しない。記事が増えてから |
| アーカイブ（年月別） | 同上 |

## 画像

`public/img/` の SVG は手書き。写真素材は使っていない。

⚠️ **日本語テキストは字面が広いので、SVG では文字同士が重なりやすい。**
実際に3枚すべてで重なりが出た（見出しの行間不足、近接するラベル同士）。
**目視ではなく、ブラウザで `getBBox()` を取って総当たりで交差判定して直した。**
図を足したり文言を変えたときは、同じ方法で確認すること。

```js
// ブラウザのコンソールで実行する検査（重なりと枠外はみ出しを列挙）
const svg = document.querySelector('svg');
const t = [...svg.querySelectorAll('text')].map(e => ({s: e.textContent.trim(), ...e.getBBox()}));
t.flatMap((a,i) => t.slice(i+1).filter(b =>
  a.x < b.x+b.width && b.x < a.x+a.width && a.y < b.y+b.height && b.y < a.y+a.height
).map(b => a.s + ' × ' + b.s));
```

| ファイル | 用途 |
|---|---|
| `coolerbox-500ml-eyecatch.svg` | 記事01のアイキャッチ兼 og:image（1200×630）。内寸22×39cmに丸型ボトルが5列3行で並ぶ図 |
| `coolerbox-floorplan.svg` | 本文の図版。**床面積が同じ858cm²でも15本と12本に分かれる**ことを示す図 |
| `favicon.svg` | 寸法線のアイコン |

### ⚠️ og:image は必ず PNG（2026-08-25 に対応済み）

**X に投稿したらカード画像が表示されなかった。原因は og:image が SVG だったこと。**
多くのSNSは og:image に SVG を受け付けない。

**対応：記事ごとに「OGPカード」PNG（1200×630）を用意し、`og:image` はそちらを指す。**
本文の図版（`eyecatch`）は **SVGのまま**でよい。

| | |
|---|---|
| 生成スクリプト | **`tools/make-og-cards.py`**（Pillow／Windowsの游ゴシックを使用） |
| 出力先 | `site/public/img/og/*.png` |
| 実行 | `python tools/make-og-cards.py site/public/img/og` |
| front matter | `ogImage: /img/og/<name>.png`（`eyecatch` とは別のキー） |
| 既定値 | `site.json` の `defaultOgImage`（`/img/og/site.png`） |
| 優先順 | `ogImage` → `eyecatch` → `defaultOgImage` |

⚠️ **Cloudflare Workers Builds は Python を実行しない。生成した PNG は必ずコミットする。**

**カードは図版の縮小版にしない。** SNSのカードは横500px程度に縮むので、
内寸や凡例を描き込んだ図版は読めなくなる。**「大きい数字ひとつ＋説明1行」**に絞ってある。
スクリプトは**文字の重なりと枠外を実測で検査**してから保存する。

⚠️ **Xはカードをキャッシュする。** og:image を直しても**既存の投稿のカードは更新されないことがある。**
その場合は投稿し直しになる（ピン留めも付け直し）。**カードを直してから投稿する**のが手戻りがない。

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
| **モバイル 375px の再検査（2026-08-26）** | ボタンとカードを入れたあとに測り直した。**ページの横スクロールなし**（`scrollWidth`=`clientWidth`=360）／**表もカードも親からはみ出さない**／タップ目標は表内 **25×266px以上**・カード内 38×159px（**WCAG 2.5.8 AA の 24×24px を満たす**）／同セル内の隣接ボタン間 75px |
| ⚠️ **収益記事2本の表内ボタン** | **375px では画面外**（脚立 596px・クーラーボックス 436px の位置）。カードが表の外の押せる場所として効いている。詳細は `docs/link-appearance-2026-08-26.md` |
| 本文リンク | `#0077c6`・太字・下線（参考サイトと同じ）。目次のリンクだけプレーン |
| **Amazonリンク（`.buy`）** | **琥珀色のボタン**（`--warn-bg` / `--warn-line` ＋ 文字 `#7a4a00`）。下線なし、末尾に `↗`。**コントラスト比 7.11:1（AAA）**。2026-08-26 まで指定が無く本文リンクと同じ見た目だった |

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

商品リンクを置きたい位置には `[[LINK:商品名]]` と書く。書き方は2つある。

| 書き方 | 出るもの | 使う場面 |
|---|---|---|
| `[[LINK:商品名]]` | **商品名をAmazonで見る** | リンクがそのセルで**商品名を名乗る唯一の場所**のとき |
| `[[LINK:商品名::表示]]` | **表示** | セルにすでに商品名が書いてあるとき（`::Amazonで見る` を使う） |

⚠️ **区切りは `|` ではなく `::`。** `resolveLinks()` は **Markdown → HTML の変換後**に走るので、
表の行に `|` を書くと**セルの区切りとして先に解釈されて表が壊れる**
（2026-08-26 に `|` で実装して実際に壊した。検索URLが表のHTMLを丸ごと飲み込んだ）。

⚠️ **短い表示にしたときは `aria-label` に「商品名をAmazonで見る」が入る。**
「Amazonで見る」が何十個も並ぶと読み上げで区別が付かないため。build.mjs が自動で付ける。

**同じセルに商品名が既出なら短い表示にする。** 表のセルは `white-space: nowrap` なので、
繰り返した分がそのまま表の横幅になる（2026-08-26 に139本を短縮し、最大セル幅が 1658px → 1047px になった）。

### 製品カード

早見表の外に「決めた人が押す場所」を作るブロック。**表は一覧するための形で、押す形ではない。**

````markdown
```card
product: ダイワ クールラインα3 S1000X
lead: 500mlを6本、床にきれいに並ぶ最小サイズ
内寸: 170×260×220mm
自重: 2.1kg
```
````

- `product` … リンクの検索語であり、見出しにもなる（必須）
- `lead` … 1行の説明（任意）
- それ以外の行は、そのまま数字の欄になる（1つ以上必須）

⚠️ **画像も価格も載せない。** 規約上 Creators API が要り、その条件は「過去30日間に適格販売10件」
（`docs/link-appearance-2026-08-26.md`）。**主役は自前の計算値。**
これがそのまま「特別リンクと関連させた追加のオリジナルコンテンツ」の要件も満たす。

⚠️ **カードの数字は、その記事の表と突き合わせてビルド時に検査している**（`assertCardNumbers`）。
カードに書いた数値が、その商品の表の行に無ければ**ビルドが落ちる。** 転記ミスを黙って公開しないため。
（2026-08-26 に、わざと 350mm → 351mm にしてビルドが落ちることを確認した。）

### ⚠️ 日本語で太字を書くときの注意

CommonMark の flanking ルールは約物（`「」。、`）を punctuation として扱うため、
**閉じの `**` が約物の直後にあり、かつ直後に文字が続く**と太字にならず `**` が本文に出る。

```markdown
✗ 見るべきなのは、**内寸の「深さ」**です。      閉じが「」の直後 → 効かない
✗ **内寸の「深さ」を見てください。**カタログでは  閉じが。の直後で、後ろに文字 → 効かない
○ 見るべきなのは、**内寸の「深さ」です。**
○ **内寸の「深さ」を見てください。**
  カタログでは…                                 閉じの後ろが改行なら効く
```

**ビルドが検出して落とすので見逃すことはない**（`assertNoRawEmphasis`）。
落ちたらエラーメッセージの該当箇所を上のどちらかの形に直す。

## ⚠️ アフィリエイトリンクと開示表記の扱い

`content/site.json` の **`affiliateEnabled` が false のうちは、リンクも開示文言も出力しない。**

理由：リンクが1本も無い状態で「Amazonのアソシエイトとして、〜は適格販売により収入を得ています」と
書くのは**事実に反する**。同じ理由で PR 表記も出さず、代わりに
「現在このページに広告リンクはありません」と表示している。

### 2026-08-25：`affiliateEnabled: true` に切り替えた

アソシエイトの**申請が完了**し（トラッキングID **`sunpou-22`**）、リンクを掲載できる状態になったので有効にした。
**本審査は「180日以内に3件の適格販売」が発生してから始まる。**

`resolveLinks()` は **Amazon の検索結果へのリンク**を生成する。ASIN 直リンクにしていない理由：

- 型番違い・色違い・生産終了で **ASIN は「別物を指す」事故を起こす。**
  このサイトは寸法の正確さが売りなので、リンク先がずれる作り方は採らない
- 検索リンクなら常に現行品を指し、リンク切れにならない

**規約上の根拠**（アソシエイト・プログラム・ポリシー本文／2026-08-25 に確認）:

> 商品リスト（検索結果、イベント…を含みます。）と乙サイトのページをリンクした場合、乙は、
> **特別リンクと関連させた乙のサイト上に追加のオリジナルコンテンツも含めなければなりません。**

→ 全リンクの隣に自前の計算結果（内寸・本数・自重）があるので条件を満たしている。

生成される形：

```html
<a class="buy" href="https://www.amazon.co.jp/s?k=<商品名>&tag=sunpou-22"
   rel="nofollow sponsored noopener" target="_blank">商品名をAmazonで見る</a>
```

⚠️ `associateTag` が未設定のまま `affiliateEnabled: true` にすると**ビルドが例外を投げる**（安全装置）。

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

### robots.txt と AIクローラの方針（2026-08-24 変更）

**Cloudflare の「Managed robots.txt」をオフにしたので、`build.mjs` が出力するものが本番の
robots.txt そのものになった。** 内容は `content/site.json` の `robots` で管理する。

| | 対象 |
|---|---|
| **許可** | **Amazonbot のみ** |
| 拒否 | Applebot-Extended／Bytespider／CCBot／ClaudeBot／Claude-User／Google-Extended／GPTBot／meta-externalagent／PetalBot／Timpibot |

**Amazonbot を許可している理由：** Amazon Content Partners の条件が
「robots.txt で Amazonbot を許可していること」で、見返りが**紹介料 +1%**。

⚠️ **ただし、このプログラムは現在アメリカ在住者限定で、日本からは登録できない。**
登録ページに「You're based in the United States / We are starting with US-based partners.
Stay tuned as we continue to expand.」と明記されている。
**+1% は当面得られない。** 許可を維持しているのは、将来日本に拡大したときに
robots.txt 側の条件を満たしておくため。

Amazon は学習にも使う可能性があると明記しており、それを承知のうえでの許可。
**対価が無い状態で学習を許すことになるので、方針を変えたければ
`content/site.json` の `robots.allowAI` から Amazonbot を外し、
Cloudflare の AI Crawl Control でも Amazonbot をブロックに戻す。**

⚠️ `Applebot-Extended` と `Google-Extended` は **robots.txt でしか表現できない**オプトアウト表記。
実体のあるクローラではないので Cloudflare の AI Crawl Control には出てこない。ここに書かないと消える。

**実際のブロック（enforcement）は Cloudflare の AI Crawl Control 側**で、ゾーン `nexeed-lab.com` に対して
AI Crawler カテゴリ15件をブロック、Amazonbot のみ許可、という設定になっている。
robots.txt は宣言、AI Crawl Control は強制、という二層構成。

### ⚠️ 旧：robots.txt に Cloudflare が Managed content を差し込んでいた（解消済み）

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
