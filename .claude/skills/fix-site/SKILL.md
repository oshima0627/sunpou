---
name: fix-site
description: 「寸法で選ぶ」のサイト側（CSS・build.mjs・テンプレート・図版）を直すときの手順。変更したらブラウザで実際に確かめ、検査ツールを通してからコミットする。「デザインを直して」「ビルドを直して」と言われたときに使う。
---

## 手順

### 1. 直す

- CSS：`site/public/styles.css`
- 生成：`site/build.mjs`
- 骨組み：`site/templates/base.html`
- **図版：`tools/figures/figures.py`**（⚠️ **PNG を直接いじらない。SVG も手書きしない**）

### 2. ビルド

```bash
npm run build --prefix site
python tools/figures/build.py <図版名>   # 図版を直したときだけ
```

### 3. ブラウザで実際に見る

```
mcp__Claude_Browser__preview_start（name: "site"）
```

⚠️ **スクロールしたあとのスクリーンショットが真っ白になることがある。**
**縦長のビューポート**（例 1200×2600）にして、スクロールせずに撮る。

⚠️ **「直しました」だけで報告しない。** 変更箇所のスクリーンショットか、
`javascript_tool` で読んだ DOM の値を出す。

### 4. 検査ツールを通す

```bash
python tools/check-link-position.py
```

⚠️ **class 名を変えたら、その class を見ている検査ツールも直す。**
2026-08-31 に目次を `toc` → `toc toc--inline` にしたとき、
`check-link-position.py` の正規表現が完全一致のままで**目次を除外できなくなり、
割合が数ポイント水増しされていた**。

### 5. コミットして push

```bash
git add -A && git commit -m "<何を変えたか>" && git push
```

`main` に入ると Cloudflare が自動でビルド＆デプロイする（2〜3分）。

## 踏みやすい罠

| 罠 | 中身 |
|---|---|
| `margin-inline: auto` | **grid の子に付けると max-content 幅に縮む。** `width: 100%` を併記する（404ページが260pxまで痩せた） |
| `word_wrap = False` | **LibreOffice が尊重しない。** 長い見出しは黙って2行になって下の行に重なる |
| `<p:style>` | 外さないと **LibreOffice がテーマ既定の影を描く。** `shadow.inherit = False` では足りない |
| `.assetsignore` | **`assets.directory`（=`dist`）の直下に無いと読まれない。** `site/.assetsignore` は効いていない |
| 軸の切り方 | **図版の棒グラフは0から描く。** 途中で切ると差が誇張される |

## 完了条件

- ビルドが通っている
- **変更箇所をブラウザで実際に確認した証拠がある**（スクリーンショットか DOM の値）
- `check-link-position.py` が悪化していない
- 図版を触ったなら `tools/figures/build.py` が3つの検査を通っている

## 失敗したとき

| 起きたこと | 対処 |
|---|---|
| dev サーバに繋がらない | `preview_start` をもう一度呼ぶ（落ちていることがある） |
| 画像が壊れて見える | **dist が古い。** `npm run build --prefix site` を先に走らせる |
| ブラウザが古い画面を出す | クエリを付けて開き直す（`?v=2`）。404 がキャッシュされていることがある |
