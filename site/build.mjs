// content/articles/*.md → dist/<slug>/index.html
// content/pages/*.md    → dist/<slug>/index.html（運営者情報などの固定ページ）
//
// 依存は marked のみ。フレームワークは入れていない。
// 実行: node build.mjs   （出力先 dist/ は .gitignore 済み）

import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';

const ROOT = import.meta.dirname;
const DIST = path.join(ROOT, 'dist');

const site = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/site.json'), 'utf8'));
const baseTpl = fs.readFileSync(path.join(ROOT, 'templates/base.html'), 'utf8');

const ORIGIN = site.origin.replace(/\/$/, '');
const catName = (slug) => site.categories.find((c) => c.slug === slug)?.name;

// ---------------------------------------------------------------- utilities

const esc = (s) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** 最小限の front matter パーサ。`key: value` の1行ペアだけを見る。 */
function parseFrontMatter(raw) {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) throw new Error('front matter がありません');
  const meta = {};
  for (const line of m[1].split(/\r?\n/)) {
    if (!line.trim()) continue;
    const i = line.indexOf(':');
    if (i < 0) throw new Error(`front matter の書式が不正: ${line}`);
    meta[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return { meta, body: raw.slice(m[0].length) };
}

const render = (tpl, vars) => tpl.replace(/\{\{(\w+)\}\}/g, (_, k) => (k in vars ? vars[k] : ''));

/**
 * フッターの開示文言。affiliateEnabled=false のうちは出さない。
 * リンクが1本も無いのに「適格販売により収入を得ています」と書くのは事実に反するため。
 */
const disclosureHtml = site.affiliateEnabled
  ? `<p class="disclosure">${esc(site.affiliateDisclosure)}</p>`
  : '';

/**
 * Cloudflare Web Analytics のビーコン。ここで測るのは分母のセッション数だけで、
 * クリック数と注文数はアソシエイト・セントラルのレポートから取る。
 * トークンはHTMLに出る公開値で、秘密情報ではない。
 */
const analyticsHtml = site.webAnalyticsToken
  ? `<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token":"${site.webAnalyticsToken}"}'></script>`
  : '';

/**
 * 本文中の [[LINK:商品名]] を、Amazon の検索結果へのアソシエイトリンクに変換する。
 *
 * なぜ ASIN 直リンクではなく検索リンクなのか（2026-08-25 の判断）:
 *   - 型番違い・色違い・生産終了で、ASIN は「別物を指す」事故を起こす。
 *     このサイトは寸法の正確さが売りなので、指す先がずれるのは致命的
 *   - 検索リンクなら常に現行品を指し、リンク切れにならない
 *
 * 規約上の根拠（アソシエイト・プログラム・ポリシー / 2026-08-25 に本文を確認）:
 *   「商品リスト（検索結果、イベント…を含みます。）と乙サイトのページをリンクした場合、
 *     乙は、特別リンクと関連させた乙のサイト上に追加のオリジナルコンテンツも含めなければなりません。」
 *   → 本サイトは全リンクの隣に自前の計算結果（内寸・本数・自重）を置いているので条件を満たす。
 *
 * affiliateEnabled が false の間はリンクを出さない（リンクが無いのに開示文言を出さないため）。
 */
function resolveLinks(html) {
  return html.replace(/\[\[LINK:([^\]]+)\]\]/g, (_, raw) => {
    // 書き方は2つ:
    //   [[LINK:商品名]]         … 「<商品名>をAmazonで見る」と出す
    //   [[LINK:商品名::表示]]   … 「表示」だけを出す。検索語は商品名のまま
    //
    // 2つ目が要る理由: 表のセルにすでに商品名が書いてあるのに、リンク文言でも
    // フルネームを繰り返していた（2026-08-26 時点で 324本中 139本）。
    // セルは white-space: nowrap なので、繰り返しがそのまま表の横幅になる。
    //
    // ⚠️ 区切りは `|` ではなく `::`。**resolveLinks は Markdown → HTML の後に走る**ので、
    // 表の行に `|` を書くとセルの区切りとして先に解釈され、表が壊れる
    // （2026-08-26 に `|` で実装して実際に壊した。URLが表のHTMLを飲み込んだ）。
    const [term, label] = raw.split('::').map((s) => s.trim());
    if (!term) throw new Error(`[[LINK:...]] の検索語が空です: ${raw}`);
    if (!site.affiliateEnabled) {
      return `<span class="link-todo" title="Amazonアソシエイトの審査合格後にリンクへ差し替え">${esc(label || term)}</span>`;
    }
    if (!site.associateTag) {
      throw new Error('affiliateEnabled=true だが site.json の associateTag が未設定');
    }
    const url = `https://www.amazon.co.jp/s?k=${encodeURIComponent(term)}&tag=${encodeURIComponent(site.associateTag)}`;
    const text = label || `${term}をAmazonで見る`;
    // 短いラベルにすると「Amazonで見る」が何十個も並ぶ。読み上げでは区別が付かないので、
    // 商品名を aria-label で補う（見た目は短いまま、リンクの名前は一意になる）。
    const aria = label ? ` aria-label="${esc(`${term}をAmazonで見る`)}"` : '';
    // rel: nofollow は規約側、sponsored は Google 側の要請。noopener は target=_blank の安全対策。
    return `<a class="buy" href="${url}"${aria} rel="nofollow sponsored noopener" target="_blank">${esc(text)}</a>`;
  });
}

/**
 * 強調記法が解釈されずに残っていないか検査する。
 * CommonMark の flanking ルールは約物（「」。、）を punctuation として扱うため、
 * 「**〜「深さ」**です」のように閉じ側が約物の直後にあると太字にならず ** が本文に出る。
 * 日本語では踏みやすいので、黙って公開されないようビルドを落とす。
 */
function assertNoRawEmphasis(html, file) {
  const m = html.match(/.{0,40}\*\*.{0,40}/);
  if (m) {
    throw new Error(
      `${file}: 太字記法が解釈されずに残っています（CommonMark の flanking ルール）。` +
        ` 該当箇所: ${m[0]}` +
        ' / 対処: 閉じの ** が約物（」。、）の直後に来ないよう、「です。」等を強調の内側に入れる',
    );
  }
}

/**
 * 製品カード。```card のフェンスを HTML に変える。**marked に渡す前**に走らせる。
 *
 * なぜ要るか: リンクの99%が早見表のセルの中にあり、押せる場所が表の外に無かった。
 * 表は一覧するための形で、決めた人が押す形ではない。
 *
 * 画像も価格も載せない（規約上 Creators API が要る）。**載せるのは自前の計算値だけ。**
 * それがそのまま「特別リンクと関連させた追加のオリジナルコンテンツ」の要件も満たす。
 *
 * 書き方:
 *   ```card
 *   product: ダイワ クールラインα3 S1000X
 *   lead: 500mlを6本、床にきれいに並ぶ最小サイズ
 *   内寸の床: 170×260mm
 *   自重: 2.1kg
 *   ```
 * product と lead 以外の行は、そのまま数字の欄になる。
 */
function renderCards(body, file) {
  return body.replace(/^```card\r?\n([\s\S]*?)^```[ \t]*$/gm, (_, block) => {
    const spec = [];
    let product = '';
    let lead = '';
    for (const line of block.split(/\r?\n/)) {
      if (!line.trim()) continue;
      const i = line.indexOf(':');
      if (i < 0) throw new Error(`${file}: card の行に : がありません → ${line}`);
      const k = line.slice(0, i).trim();
      const v = line.slice(i + 1).trim();
      if (k === 'product') product = v;
      else if (k === 'lead') lead = v;
      else spec.push([k, v]);
    }
    if (!product) throw new Error(`${file}: card に product がありません`);
    if (!spec.length) throw new Error(`${file}: card に数字が1つもありません（${product}）`);
    assertCardNumbers(product, spec, body, file);
    const dl = spec.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('');
    return (
      `<aside class="pcard">` +
      (lead ? `<p class="pcard__lead">${esc(lead)}</p>` : '') +
      `<p class="pcard__name">${esc(product)}</p>` +
      `<dl class="pcard__spec">${dl}</dl>` +
      `<p class="pcard__go">[[LINK:${product}::Amazonで見る]]</p>` +
      `<p class="pcard__note">数字はメーカー公表値と、そこからの当サイトの計算です。価格は扱っていません。</p>` +
      `</aside>\n`
    );
  });
}

/**
 * **カードの数字が、その記事の表と食い違っていないかを検査する。**
 *
 * このサイトは「メーカー公表値から計算する」ことが売りなので、
 * カードにだけ古い数字が残る事故は起こしてはいけない。転記ミスはビルドで落とす。
 * 判定は「カードの数字（数値トークン）が、その商品の表の行にすべて現れるか」。
 */
function assertCardNumbers(product, spec, body, file) {
  const rows = body
    .split(/\r?\n/)
    .filter((l) => l.trimStart().startsWith('|') && l.includes(product));
  if (!rows.length) {
    throw new Error(`${file}: カードの商品「${product}」が、この記事のどの表にもありません`);
  }
  const hay = rows.join(' ').replace(/[\s,]/g, '');
  for (const [k, v] of spec) {
    for (const num of v.match(/\d+(?:\.\d+)?/g) || []) {
      if (!hay.includes(num)) {
        throw new Error(
          `${file}: カードの数字が表にありません → ${product} の「${k}: ${v}」の ${num}` +
            ' / 対処: 表の値と合わせるか、表のほうを直す',
        );
      }
    }
  }
}

/**
 * **引用の直後に空行なしで本文を書くと、その行が引用に飲み込まれる**（Markdown の遅延継続）。
 *
 * 2026-08-31 に `/coolerbox/daiwa-shimano/` で実際に起きていた。
 * 「KEEP 46 はおよそ46時間、COOL 60 はおよそ60時間、という意味になります。」という
 * 記事の要点が、灰色の引用ボックスの中に入って本文から降格していた。
 * 原稿を目で見ても引用に見えないので、ビルドで落とす。
 */
function assertNoLazyBlockquote(body, file) {
  const lines = body.split(/\r?\n/);
  for (let i = 0; i < lines.length - 1; i += 1) {
    const cur = lines[i].trimStart();
    const next = lines[i + 1].trimStart();
    if (!cur.startsWith('>')) continue;
    if (!next || next.startsWith('>') || next.startsWith('#') || next.startsWith('|') || next.startsWith('```')) continue;
    throw new Error(
      `${file}:${i + 2}: 引用の直後に空行がないので、この行が引用の中に入ってしまう → ${next.slice(0, 40)}` +
        ' / 対処: 引用と本文のあいだに空行を1つ入れる',
    );
  }
}

/** 表は横スクロールできる箱に入れる（スマホで本文が横に伸びるのを防ぐ）。 */
const wrapTables = (html) =>
  html.replace(/<table>/g, '<div class="table-wrap"><table>').replace(/<\/table>/g, '</table></div>');

/** 本文中の画像を figure にして、alt をキャプションとして見せる。 */
const wrapFigures = (html) =>
  html.replace(
    /<p>(<img src="([^"]+)" alt="([^"]*)"[^>]*>)<\/p>/g,
    (_, img, src, alt) =>
      `<figure class="fig"><img src="${src}" alt="${alt}" loading="lazy" decoding="async">` +
      (alt ? `<figcaption>${alt}</figcaption>` : '') +
      '</figure>',
  );

/** h2 / h3 に id を振り、目次の材料を集める。marked v15 は id を付けないので採番する。 */
function addHeadingIds(html) {
  const headings = [];
  let n = 0;
  const out = html.replace(/<h([23])>([\s\S]*?)<\/h\1>/g, (_, lvl, inner) => {
    n += 1;
    headings.push({ level: Number(lvl), id: `s${n}`, text: inner.replace(/<[^>]+>/g, '').trim() });
    return `<h${lvl} id="s${n}">${inner}</h${lvl}>`;
  });
  return { html: out, headings };
}

/** 目次。h2 を親、h3 を子にした入れ子リストにする。 */
function tocList(headings) {
  const parts = ['<ol>'];
  let subOpen = false;
  for (const h of headings) {
    if (h.level === 2) {
      if (subOpen) { parts.push('</ol></li>'); subOpen = false; }
      parts.push(`<li><a href="#${h.id}">${esc(h.text)}</a></li>`);
    } else {
      if (!subOpen) {
        parts.push(parts.pop().replace(/<\/li>$/, ''), '<ol>');
        subOpen = true;
      }
      parts.push(`<li><a href="#${h.id}">${esc(h.text)}</a></li>`);
    }
  }
  if (subOpen) parts.push('</ol></li>');
  parts.push('</ol>');
  return parts.join('');
}

/** 見出しが少ない記事に目次を出しても邪魔なだけなので出さない。 */
const hasToc = (headings) => headings.filter((h) => h.level === 2).length >= 3;

/** SNSシェア。JS を使わず、各サービスの共有URLへのリンクだけを置く。 */
function shareButtons(title, url) {
  const t = encodeURIComponent(title);
  const u = encodeURIComponent(url);
  const items = [
    ['X', `https://x.com/intent/tweet?text=${t}&url=${u}`],
    ['Facebook', `https://www.facebook.com/sharer/sharer.php?u=${u}`],
    ['はてブ', `https://b.hatena.ne.jp/entry/panel/?url=${u}&title=${t}`],
    ['LINE', `https://social-plugins.line.me/lineit/share?url=${u}`],
  ];
  return `<div class="share"><p class="share__title">この記事をシェア</p><ul>${items
    .map(([label, href]) => `<li><a href="${href}" target="_blank" rel="noopener nofollow">${label}</a></li>`)
    .join('')}</ul></div>`;
}

function writeFile(rel, contents) {
  const full = path.join(DIST, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, contents);
}

function copyDir(from, to) {
  if (!fs.existsSync(from)) return;
  fs.cpSync(from, to, { recursive: true });
}

function readDocs(dir) {
  const full = path.join(ROOT, dir);
  if (!fs.existsSync(full)) return [];
  return fs
    .readdirSync(full)
    .filter((f) => f.endsWith('.md'))
    .sort()
    .map((file) => {
      const { meta, body } = parseFrontMatter(fs.readFileSync(path.join(full, file), 'utf8'));
      for (const key of ['title', 'description', 'slug', 'published', 'updated']) {
        if (!meta[key]) throw new Error(`${file}: front matter に ${key} がありません`);
      }
      const slug = meta.slug.replace(/^\/|\/$/g, '');
      return { ...meta, file, slug, body, url: `${ORIGIN}/${slug}/` };
    });
}

/**
 * カテゴリページの導入文。`content/categories/<slug>.md`（front matter なし・本文だけ）。
 *
 * ⚠️ **2026-09-01 まで、カテゴリ3ページの固有の本文は0文字だった**（定型1文＋記事一覧のみ）。
 * 「クーラーボックス 内寸」のような語の受け皿になる位置なのに、順位を取る材料が無かった
 * （`docs/site-review-2026-09-01.md`）。**書いた数字は記事側と同じ根拠のものだけを置く。**
 */
function readCategoryLead(slug) {
  const p = path.join(ROOT, 'content/categories', `${slug}.md`);
  if (!fs.existsSync(p)) return '';
  const parsed = addHeadingIds(wrapTables(marked.parse(fs.readFileSync(p, 'utf8'))));
  assertNoRawEmphasis(parsed.html, `content/categories/${slug}.md`);
  return resolveLinks(parsed.html);
}

// ---------------------------------------------------------------- build

// dist ごと削除せず中身だけ消す。wrangler dev が監視している間、
// Windows ではディレクトリ自体の削除が EPERM で失敗する。
fs.mkdirSync(DIST, { recursive: true });
for (const entry of fs.readdirSync(DIST)) {
  try {
    fs.rmSync(path.join(DIST, entry), { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
  } catch (err) {
    console.warn(`clean: dist/${entry} を削除できませんでした（${err.code}）。上書きで続行します。`);
  }
}

marked.setOptions({ gfm: true, breaks: false });

const articles = readDocs('content/articles');
const pages = readDocs('content/pages');

for (const a of articles) {
  if (!a.category) throw new Error(`${a.file}: front matter に category がありません`);
  if (!catName(a.category)) throw new Error(`${a.file}: 未定義のカテゴリ「${a.category}」（site.json の categories に追加してください）`);
}

const byRecent = [...articles].sort((a, b) => (a.updated < b.updated ? 1 : -1));

// ---- 共通パーツ

/**
 * カテゴリが1つしかない間は、ナビにもサイドバーにもカテゴリを出さない。
 *
 * 「寸法で選ぶ」の中に「クーラーボックス」しか無い状態では、カテゴリ名はサイト名と
 * ほぼ同義で情報量がゼロになる。2つ目のカテゴリを site.json に足した時点で自動的に出る。
 */
const showCategoryNav = site.categories.length >= 2;

const catNavItems = showCategoryNav
  ? site.categories.map((c) => ({ path: `/${c.slug}/`, label: c.name }))
  : [];

const linkList = (items) => items.map((n) => `<a href="${n.path}">${esc(n.label)}</a>`).join('');

/**
 * ヘッダーのナビは**カテゴリだけ**にする。運営者情報・プライバシーポリシー・サイトマップは
 * 「ユーティリティリンク」で、置き場所はフッター（NN/g "Web Page Footers 101"）。
 * 上部に残してよいのは検索・ログイン・言語切替のような「道具」だけ、とされている。
 *
 * 実測（2026-08-31・375px）：6項目のナビは scrollWidth 706px に対して表示幅 338px しかなく、
 * **368px ぶん（後ろ3項目＝ユーティリティ3件そのもの）が画面外**に出ていた。
 * スクロールバーも非表示にしてあるので、そこに項目があること自体が読者に見えない。
 * カテゴリ3件だけならこの溢れが無くなる。
 */
const navHtml = linkList(catNavItems);

/** フッターは全部載せる（カテゴリ＋ユーティリティ）。読者はここを見に来る。 */
const fnavHtml = linkList([...catNavItems, ...site.nav]);

/** サイドバー。中身が無いときは <aside> ごと出さない（レイアウトが1カラムに畳まれる）。 */
const side = (inner) => (inner ? `<aside class="l-side">${inner}</aside>` : '');

function widget(title, inner, cls = '') {
  return `<div class="widget${cls ? ' ' + cls : ''}"><p class="widget__title">${esc(title)}</p>${inner}</div>`;
}

function postListHtml(list, cls = '') {
  if (!list.length) return '<p>まだありません。</p>';
  return `<ul class="${cls}">${list
    .map(
      (a) =>
        `<li><a href="/${a.slug}/">${esc(a.title)}</a><time datetime="${esc(a.updated)}">${esc(a.updated)}</time></li>`,
    )
    .join('')}</ul>`;
}

const categoryWidget = showCategoryNav
  ? widget(
      'カテゴリー',
      `<ul>${site.categories
        .map((c) => {
          const n = articles.filter((a) => a.category === c.slug).length;
          return `<li><a href="/${c.slug}/">${esc(c.name)}</a><time>${n}記事</time></li>`;
        })
        .join('')}</ul>`,
    )
  : '';

/**
 * トップページ本文に置くカテゴリの入口。
 *
 * これまでカテゴリへの導線は**サイドバーにしか無かった**。サイドバーは 900px 以下で
 * 本文の下に落ちるので、スマホでは記事19本を全部スクロールし切るまでカテゴリが現れない。
 * 本文の先頭に置き直すと、どの幅でも最初の画面で「何を扱う site か」と分岐が見える。
 */
const categoryCards = showCategoryNav
  ? `<nav class="cat-cards" aria-label="カテゴリー">${site.categories
      .map((c) => {
        const n = articles.filter((a) => a.category === c.slug).length;
        return (
          `<a class="cat-card" href="/${c.slug}/">` +
          `<span class="cat-card__name">${esc(c.name)}</span>` +
          `<span class="cat-card__count">${n}記事</span>` +
          `</a>`
        );
      })
      .join('')}</nav>`
  : '';

const aboutWidget = widget('このサイトについて', `<p>${esc(site.description)}</p><p class="widget__more"><a href="/about/">運営者情報と数値の作り方 →</a></p>`);

/**
 * フッターの X へのリンク。site.json の xHandle を空にすると出力しない。
 * 外部リンクなので rel="me" を付けて、サイトとアカウントが同一運営であることを示す。
 */
const snsHtml = site.xHandle
  ? `<p class="sns"><a href="https://x.com/${encodeURIComponent(site.xHandle)}" rel="me noopener" target="_blank">X @${esc(site.xHandle)}</a></p>`
  : '';

const common = {
  lang: site.lang,
  siteName: esc(site.name),
  tagline: esc(site.tagline),
  nav: navHtml,
  fnav: fnavHtml,
  robots: '',
  disclosure: disclosureHtml,
  sns: snsHtml,
  analytics: analyticsHtml,
  ogImage: ORIGIN + site.defaultOgImage,
};

function crumbs(items) {
  const parts = items.map((it, i) =>
    i === items.length - 1 ? `<span>${esc(it.label)}</span>` : `<a href="${it.path}">${esc(it.label)}</a>`,
  );
  return `<nav class="crumbs" aria-label="パンくずリスト">${parts.join(' › ')}</nav>`;
}

/**
 * パンくずの構造化データ。
 *
 * ⚠️ **画面のパンくずは 2026-08-31 から出ていたのに、JSON-LD は1件も出していなかった**
 * （2026-09-01 のレビューで判明）。検索結果にパンくずを出すのはこちらの役目で、
 * `<nav>` を読ませているわけではない。
 *
 * 引数は crumbs() と同じ配列にする。**表示とデータを別々に組み立てると食い違う。**
 * 末尾（現在地）には item を付けない（Google の仕様上こうしてよい）。
 */
function breadcrumbLd(items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((it, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: it.label,
      ...(it.path ? { item: ORIGIN + it.path } : {}),
    })),
  };
}

// ---- 記事ページ

/**
 * front matter の `eyecatch` と同じ画像が本文にも書いてある記事がある。
 * build.mjs は eyecatch を必ず記事の先頭に出すので、**同じ図が1ページに2回出ていた**
 * （2026-08-31 時点で6本。`/coolerbox/coleman-uchinori/`・`/coolerbox/erabikata/`・
 * `/coolerbox/horeizai-maisuu/`・`/cassette-konro/bombe-honsuu/`・
 * `/cassette-konro/nenshou-jikan/`・`/kyatatsu/erabikata/`）。
 *
 * 本文側を消すだけだと、本文側が持っていた**説明的な alt（＝figure のキャプション）が失われる。**
 * 先頭の eyecatch は alt に記事タイトルを入れており、これは「画像の説明」ではないので
 * 代わりにならない。そこで本文側の alt を回収して先頭の eyecatch に移し、
 * キャプションも先頭側に出す。**原稿は書き換えない**（正は content/articles/）。
 */
function liftEyecatchFromBody(a) {
  if (!a.eyecatch) return { body: a.body, alt: '' };
  const lines = a.body.split('\n');
  const tail = '](' + a.eyecatch + ')';
  const i = lines.findIndex((l) => l.startsWith('![') && l.trimEnd().endsWith(tail));
  if (i < 0) return { body: a.body, alt: '' };
  const alt = lines[i].slice(2, lines[i].lastIndexOf(tail));
  lines.splice(i, 1);
  // 画像を抜くと前後の空行が連続して残るので、片方だけ詰める
  if (lines[i] === '' && lines[i - 1] === '') lines.splice(i, 1);
  return { body: lines.join('\n'), alt };
}

for (const a of articles) {
  assertNoLazyBlockquote(a.body, a.file);
  const lifted = liftEyecatchFromBody(a);
  a.eyecatchAlt = lifted.alt;
  const parsed = addHeadingIds(wrapFigures(wrapTables(marked.parse(renderCards(lifted.body, a.file)))));
  assertNoRawEmphasis(parsed.html, a.file);
  const html = resolveLinks(parsed.html);

  // 回収しそこねた重複を黙って公開しない。ここで落とす。
  if (a.eyecatch && html.includes(`src="${a.eyecatch}"`)) {
    throw new Error(
      `${a.file}: eyecatch と同じ画像が本文にも残っている（${a.eyecatch}）` +
        ' / 対処: 本文の ![...](画像) を独立した1行にするか、front matter の eyecatch を別画像にする',
    );
  }
  const cname = catName(a.category);
  const trail = [
    { path: '/', label: 'ホーム' },
    { path: `/${a.category}/`, label: cname },
    { label: a.title },
  ];

  /**
   * 関連記事の並べ方。
   *
   * ⚠️ **2026-09-01 まで「同じカテゴリの新着順」だった。** 記事が増えるほど古い記事が
   * どの関連記事にも出なくなる。実際、クーラーボックスの古い4本
   * （`2l-tateru` `500ml-honsuu` `daiwa-shimano` `horeizai-honsuu`）は
   * **関連記事からの被リンクが0**だった（`docs/site-review-2026-09-01.md`）。
   * いちばん需要のあるキーワードの記事が、内部リンクから落ちていた。
   *
   * 日付順をやめて、こう並べる:
   *   1. そのカテゴリの収益記事（front matter の `pillar`）。**同カテゴリの全記事から必ず張る**
   *   2. 同じカテゴリの残りを「この記事の次」から巡回して取る。
   *      どの記事も同じ回数だけ出るので、古い記事が落ちない
   *   3. それでも5本に足りなければ、他カテゴリの新着で埋める
   */
  const inCat = articles.filter((x) => x.category === a.category);
  const here = inCat.findIndex((x) => x.slug === a.slug);
  const rotated = inCat.slice(here + 1).concat(inCat.slice(0, here));
  const pillar = inCat.find((x) => x.pillar && x.slug !== a.slug);
  const related = [
    ...(pillar ? [pillar] : []),
    ...rotated.filter((x) => x !== pillar),
    ...byRecent.filter((x) => x.category !== a.category),
  ].slice(0, 5);

  const prNotice = site.affiliateEnabled
    ? `<p class="pr-notice">${esc(site.prLabel)}</p>`
    : `<p class="pr-notice pr-notice--pending">現在このページに広告リンクはありません（Amazonアソシエイト審査前）。</p>`;

  // 本文から alt を回収できたときは、それを alt に使い、キャプションとしても見せる。
  // 回収できなかった記事は従来どおり（alt は記事タイトル・キャプションなし）。
  const eyecatch = a.eyecatch
    ? a.eyecatchAlt
      ? `<figure class="eyecatch"><img src="${a.eyecatch}" alt="${esc(a.eyecatchAlt)}" width="1200" height="630" decoding="async">` +
        `<figcaption>${esc(a.eyecatchAlt)}</figcaption></figure>`
      : `<p class="eyecatch"><img src="${a.eyecatch}" alt="${esc(a.title)}" width="1200" height="630" decoding="async"></p>`
    : '';

  writeFile(
    `${a.slug}/index.html`,
    render(baseTpl, {
      ...common,
      title: `${esc(a.title)} | ${esc(site.name)}`,
      description: esc(a.description),
      canonical: a.url,
      ogType: 'article',
      // og:image は PNG（front matter の ogImage）を優先する。
      // 本文の図版（eyecatch）は SVG のままでよいが、SNS のカードは SVG を受け付けない。
      ogImage: ORIGIN + (a.ogImage || a.eyecatch || site.defaultOgImage),
      jsonLd: JSON.stringify([
        {
          '@context': 'https://schema.org',
          '@type': 'Article',
          headline: a.title,
          description: a.description,
          image: ORIGIN + (a.ogImage || a.eyecatch || site.defaultOgImage),
          datePublished: a.published,
          dateModified: a.updated,
          articleSection: cname,
          inLanguage: site.lang,
          mainEntityOfPage: { '@type': 'WebPage', '@id': a.url },
          // 誰が書いたか。数値を自分で計算して出すサイトなので、書き手を明示する
          author: { '@type': 'Person', name: site.author, url: `${ORIGIN}/about/` },
          publisher: { '@type': 'Organization', name: site.name },
        },
        breadcrumbLd(trail),
      ]),
      breadcrumb: crumbs(trail),
      sidebar: side(
        // 目次は本文中とサイドバーの2か所に出力しているが、**同時に見えるのは片方だけ**。
        // 901px 以上は追従するサイドバー版、900px 以下（サイドバーが本文の下に落ちる幅）は
        // 本文中の版を CSS で出し分ける。両方見えていたときは同じリストが2回並んでいた。
        (hasToc(parsed.headings) ? widget('目次', `<div class="toc toc--side">${tocList(parsed.headings)}</div>`, 'widget--toc') : '') +
        aboutWidget +
        widget('新着記事', postListHtml(byRecent.slice(0, 5))) +
        categoryWidget
      ),
      content:
        `<article class="post">` +
        `<p class="cat-label"><a href="/${a.category}/">${esc(cname)}</a></p>` +
        `<h1>${esc(a.title)}</h1>` +
        `<p class="dates"><time datetime="${esc(a.published)}">公開 ${esc(a.published)}</time>${
          a.updated !== a.published ? ` ／ <time datetime="${esc(a.updated)}">更新 ${esc(a.updated)}</time>` : ''
        }</p>` +
        eyecatch +
        prNotice +
        (hasToc(parsed.headings) ? `<nav class="toc toc--inline"><p class="toc__title">目次</p>${tocList(parsed.headings)}</nav>` : '') +
        html +
        shareButtons(a.title, a.url) +
        // 記事が1本しかないうちは「関連記事」の枠だけ出しても意味がないので省く
        (related.length
          ? `<section class="related"><h2 class="related__title">関連記事</h2>${postListHtml(related, 'related__list')}</section>`
          : '') +
        `</article>`,
      year: String(new Date(a.updated).getFullYear()),
    }),
  );
}

// ---- 固定ページ

for (const p of pages) {
  const parsed = addHeadingIds(wrapFigures(wrapTables(marked.parse(p.body))));
  assertNoRawEmphasis(parsed.html, p.file);
  const pageTrail = [{ path: '/', label: 'ホーム' }, { label: p.title }];

  writeFile(
    `${p.slug}/index.html`,
    render(baseTpl, {
      ...common,
      title: `${esc(p.title)} | ${esc(site.name)}`,
      description: esc(p.description),
      canonical: p.url,
      ogType: 'website',
      jsonLd: JSON.stringify([
        {
          '@context': 'https://schema.org',
          '@type': 'WebPage',
          name: p.title,
          description: p.description,
          url: p.url,
          inLanguage: site.lang,
        },
        breadcrumbLd(pageTrail),
      ]),
      breadcrumb: crumbs(pageTrail),
      sidebar: side(
        aboutWidget + widget('新着記事', postListHtml(byRecent.slice(0, 5))) + categoryWidget
      ),
      content: `<article class="post"><h1>${esc(p.title)}</h1><p class="dates"><time datetime="${esc(p.updated)}">更新 ${esc(p.updated)}</time></p>${resolveLinks(parsed.html)}</article>`,
      year: String(new Date(p.updated).getFullYear()),
    }),
  );
}

// ---- カテゴリーページ

for (const c of site.categories) {
  const list = byRecent.filter((a) => a.category === c.slug);
  const url = `${ORIGIN}/${c.slug}/`;
  const catTrail = [{ path: '/', label: 'ホーム' }, { label: c.name }];
  const lead = readCategoryLead(c.slug);
  writeFile(
    `${c.slug}/index.html`,
    render(baseTpl, {
      ...common,
      title: `${esc(c.title || `${c.name}の記事一覧`)} | ${esc(site.name)}`,
      description: c.description || `${c.name}について、メーカー公式の寸法から計算して比べた記事の一覧です。`,
      canonical: url,
      ogType: 'website',
      jsonLd: JSON.stringify([
        {
          '@context': 'https://schema.org',
          '@type': 'CollectionPage',
          name: `${c.name}の記事一覧`,
          url,
          inLanguage: site.lang,
        },
        breadcrumbLd(catTrail),
      ]),
      breadcrumb: crumbs(catTrail),
      // カテゴリが1つの間、このページはトップページと中身がほぼ同じになる。
      // 重複コンテンツとして competing させたくないので noindex にしておく
      // （follow なので記事へのリンクはたどられる）。2つ目のカテゴリができたら自動で index される。
      robots: showCategoryNav ? '' : '<meta name="robots" content="noindex,follow">',
      sidebar: side(
        aboutWidget + widget('新着記事', postListHtml(byRecent.slice(0, 5))) + categoryWidget
      ),
      content:
        // 導入文があればそれを使う（h1 も導入文側に置く）。無ければ従来どおりの見出しだけ。
        (lead
          ? `<div class="post cat-lead">${lead}</div>`
          : `<h1>${esc(c.name)}の記事一覧</h1>` +
            `<p class="lead">${esc(c.name)}について、メーカー公式の寸法から計算して比べた記事です。</p>`) +
        `<h2 class="section-title">${esc(c.name)}の記事（${list.length}本）</h2>` +
        articleCards(list),
      year: String(new Date().getFullYear()),
    }),
  );
}

// ---- 記事カード（トップ・カテゴリー共通）

/**
 * 一覧のサムネ。`/img/<name>.png` に対して `/img/thumb/<name>.png`（幅480px）があれば
 * そちらを使う（`tools/figures/build.py` が焼く）。
 *
 * ⚠️ **2026-09-01 まで 2400px の本体をそのまま240pxの枠で出していた。**
 * トップページの画像だけで 1.35MB あった（`docs/site-review-2026-09-01.md`）。
 * 無い場合は本体にそのまま落とす（図版以外のアイキャッチが増えても壊れないように）。
 */
function thumbOf(src) {
  const small = src.replace(/^\/img\//, '/img/thumb/');
  return fs.existsSync(path.join(ROOT, 'public', small.slice(1)))
    ? { src: small, w: 480, h: 252 }
    : { src, w: 1200, h: 630 };
}

function articleCards(list) {
  if (!list.length) return '<p>記事はまだありません。</p>';
  return `<ul class="article-list">${list
    .map(
      (a) =>
        `<li><a class="article-list__link" href="/${a.slug}/">` +
        (a.eyecatch
          ? (({ src, w, h }) =>
              `<img class="article-list__thumb" src="${src}" alt="" width="${w}" height="${h}" loading="lazy" decoding="async">`)(thumbOf(a.eyecatch))
          : '') +
        `<span class="article-list__body">` +
        `<span class="article-list__cat">${esc(catName(a.category))}</span>` +
        `<span class="article-list__title">${esc(a.title)}</span>` +
        `<span class="article-list__desc">${esc(a.description)}</span>` +
        `<time datetime="${esc(a.updated)}">${esc(a.updated)}</time>` +
        `</span></a></li>`,
    )
    .join('')}</ul>`;
}

// ---- トップページ

writeFile(
  'index.html',
  render(baseTpl, {
    ...common,
    title: `${esc(site.name)} — ${esc(site.tagline)}`,
    description: esc(site.description),
    canonical: `${ORIGIN}/`,
    ogType: 'website',
    jsonLd: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'WebSite',
      name: site.name,
      description: site.description,
      url: `${ORIGIN}/`,
      inLanguage: site.lang,
    }),
    breadcrumb: '',
    // トップだけサイドバーを外す。
    // 「このサイトについて」は site.description をそのまま出しており、これは本文の
    // リード文と**一字一句同じ**だった。「カテゴリー」も本文のカテゴリカードと同じ中身。
    // つまりトップのサイドバーは全部が本文の複製で、読者に新しい情報が1つも無かった。
    sidebar: side(''),
    // h1 はサイト名を繰り返さない（ヘッダーのロゴが40px上で同じ文字列を出している）。
    // ここはサイトが何をする場所かを言う一行にする。
    content:
      `<h1>${esc(site.tagline)}</h1><p class="lead">${esc(site.description)}</p>` +
      categoryCards +
      `<h2 class="section-title">新着記事</h2>` +
      articleCards(byRecent),
    year: String(new Date().getFullYear()),
  }),
);

// ---- サイトマップ（HTML）

const sitemapTrail = [{ path: '/', label: 'ホーム' }, { label: 'サイトマップ' }];

writeFile(
  'sitemap/index.html',
  render(baseTpl, {
    ...common,
    title: `サイトマップ | ${esc(site.name)}`,
    description: '「寸法で選ぶ」の全ページ一覧です。',
    canonical: `${ORIGIN}/sitemap/`,
    ogType: 'website',
    jsonLd: JSON.stringify(breadcrumbLd(sitemapTrail)),
    breadcrumb: crumbs(sitemapTrail),
    sidebar: side(aboutWidget + categoryWidget),
    // 見出しは .post h2（紺の縦棒＋上に5.6remの余白）を使わない。
    // 全ページの索引なのに、区切りごとに記事本文と同じ大きさの見出しと余白が入って、
    // 19本のリストが縦に間延びしていた。索引は詰めて一覧できるほうがいい。
    content:
      '<div class="sitemap"><h1>サイトマップ</h1>' +
      site.categories
        .map(
          (c) =>
            `<h2 class="section-title">${esc(c.name)}</h2>` +
            postListHtml(byRecent.filter((a) => a.category === c.slug), 'link-list'),
        )
        .join('') +
      '<h2 class="section-title">このサイトについて</h2><ul class="link-list">' +
      site.nav.map((n) => `<li><a href="${n.path}">${esc(n.label)}</a></li>`).join('') +
      '</ul></div>',
    year: String(new Date().getFullYear()),
  }),
);

// ---- 404

writeFile(
  '404.html',
  render(baseTpl, {
    ...common,
    title: `ページが見つかりません | ${esc(site.name)}`,
    description: 'お探しのページは見つかりませんでした。',
    canonical: '',
    ogType: 'website',
    // ⚠️ 空にすると `<script type="application/ld+json"></script>` が出て、
    // JSON として壊れたものを配ることになる（2026-09-01 に全ページを JSON.parse して見つけた）。
    jsonLd: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'WebPage',
      name: 'ページが見つかりません',
      inLanguage: site.lang,
    }),
    breadcrumb: '',
    sidebar: side(''),
    content: '<h1>ページが見つかりません</h1><p><a href="/">トップへ戻る</a></p><p><a href="/sitemap/">サイトマップから探す</a></p>',
    year: String(new Date().getFullYear()),
  }),
);

// ---- sitemap.xml / robots.txt

const urls = [
  { loc: `${ORIGIN}/`, lastmod: byRecent[0]?.updated },
  // noindex のカテゴリページは sitemap に載せない
  ...(showCategoryNav ? site.categories.map((c) => ({ loc: `${ORIGIN}/${c.slug}/`, lastmod: byRecent[0]?.updated })) : []),
  ...byRecent.map((a) => ({ loc: a.url, lastmod: a.updated })),
  ...pages.map((p) => ({ loc: p.url, lastmod: p.updated })),
  { loc: `${ORIGIN}/sitemap/`, lastmod: byRecent[0]?.updated },
];

writeFile(
  'sitemap.xml',
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
    .map((u) => `  <url><loc>${u.loc}</loc>${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}</url>`)
    .join('\n')}\n</urlset>\n`,
);

// robots.txt
//
// 2026-08-24 に Cloudflare の「Managed robots.txt」をオフにしたので、
// ここで出力するものが本番の robots.txt そのものになる
// （以前は Cloudflare が管理ブロックをこの上に差し込んでいた）。
//
// Amazonbot だけを明示的に許可しているのは、Amazon Content Partners の条件が
// 「robots.txt で Amazonbot を許可していること」だから。見返りは紹介料 +1%。
// Amazon は学習にも使う可能性があると明記しており、それを承知のうえでの許可。
// 他のAI学習クローラは従来どおり拒否する。
const robotsLines = [
  '# AI学習クローラは既定で拒否。Amazonbot だけ許可している。',
  '# 理由は content/site.json の robots.allowAI のコメントを参照。',
  '',
  ...site.robots.allowAI.flatMap((ua) => [`User-agent: ${ua}`, 'Allow: /', '']),
  ...site.robots.denyAI.flatMap((ua) => [`User-agent: ${ua}`, 'Disallow: /', '']),
  'User-agent: *',
  'Allow: /',
  '',
  `Sitemap: ${ORIGIN}/sitemap.xml`,
  '',
];

writeFile('robots.txt', robotsLines.join('\n'));

// ---- 静的ファイル

copyDir(path.join(ROOT, 'public'), DIST);

/**
 * 図版の SVG は**原稿ではなく素材**なので配信しない。
 *
 * 記事が参照するのは PNG（`tools/svg-to-png.py` が SVG から焼く）。SVG も一緒に配信すると
 * 同じ図が2つのURLで公開され、どの記事からも参照されていない SVG のほうが
 * Google 画像検索に載りうる。favicon.svg は img/ の外なので残る。
 *
 * ⚠️ .assetsignore ではできない。あれは assets.directory（= dist）直下に無いと読まれず、
 * build.mjs は public/ しかコピーしないので dist に置かれない。
 */
{
  const imgDir = path.join(DIST, 'img');
  const dropped = fs.readdirSync(imgDir).filter((f) => f.endsWith('.svg'));
  for (const f of dropped) fs.rmSync(path.join(imgDir, f));
  if (dropped.length) console.log(`  dist/img から SVG ${dropped.length} 枚を除外（PNG が配信対象）`);
}

console.log(`built: ${articles.length} article(s), ${pages.length} page(s), ${site.categories.length} category page(s)`);
for (const a of articles) console.log(`  /${a.slug}/  ${a.title}`);
if (!site.affiliateEnabled) console.log('\n注意: affiliateEnabled=false のため、リンク位置はプレースホルダで出力しています。');
