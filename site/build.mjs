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
  return html.replace(/\[\[LINK:([^\]]+)\]\]/g, (_, label) => {
    if (!site.affiliateEnabled) {
      return `<span class="link-todo" title="Amazonアソシエイトの審査合格後にリンクへ差し替え">${esc(label)}</span>`;
    }
    if (!site.associateTag) {
      throw new Error('affiliateEnabled=true だが site.json の associateTag が未設定');
    }
    const url = `https://www.amazon.co.jp/s?k=${encodeURIComponent(label)}&tag=${encodeURIComponent(site.associateTag)}`;
    // rel: nofollow は規約側、sponsored は Google 側の要請。noopener は target=_blank の安全対策。
    return `<a class="buy" href="${url}" rel="nofollow sponsored noopener" target="_blank">${esc(label)}をAmazonで見る</a>`;
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

const navHtml = [
  ...(showCategoryNav ? site.categories.map((c) => ({ path: `/${c.slug}/`, label: c.name })) : []),
  ...site.nav,
]
  .map((n) => `<a href="${n.path}">${esc(n.label)}</a>`)
  .join('');

function widget(title, inner) {
  return `<div class="widget"><p class="widget__title">${esc(title)}</p>${inner}</div>`;
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

// ---- 記事ページ

for (const a of articles) {
  const parsed = addHeadingIds(wrapFigures(wrapTables(marked.parse(a.body))));
  assertNoRawEmphasis(parsed.html, a.file);
  const html = resolveLinks(parsed.html);
  const cname = catName(a.category);

  // 関連記事は同じカテゴリを優先し、足りない分だけ他カテゴリで埋める。
  // カテゴリが2件以上になると、そうしないと無関係な記事が並ぶ。
  const others = byRecent.filter((x) => x.slug !== a.slug);
  const related = [
    ...others.filter((x) => x.category === a.category),
    ...others.filter((x) => x.category !== a.category),
  ].slice(0, 5);

  const prNotice = site.affiliateEnabled
    ? `<p class="pr-notice">${esc(site.prLabel)}</p>`
    : `<p class="pr-notice pr-notice--pending">現在このページに広告リンクはありません（Amazonアソシエイト審査前）。</p>`;

  const eyecatch = a.eyecatch
    ? `<p class="eyecatch"><img src="${a.eyecatch}" alt="${esc(a.title)}" width="1200" height="630" decoding="async"></p>`
    : '';

  writeFile(
    `${a.slug}/index.html`,
    render(baseTpl, {
      ...common,
      title: `${esc(a.title)} | ${esc(site.name)}`,
      description: esc(a.description),
      canonical: a.url,
      ogType: 'article',
      ogImage: ORIGIN + (a.eyecatch || site.defaultOgImage),
      jsonLd: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Article',
        headline: a.title,
        description: a.description,
        image: ORIGIN + (a.eyecatch || site.defaultOgImage),
        datePublished: a.published,
        dateModified: a.updated,
        articleSection: cname,
        inLanguage: site.lang,
        mainEntityOfPage: { '@type': 'WebPage', '@id': a.url },
        publisher: { '@type': 'Organization', name: site.name },
      }),
      breadcrumb: crumbs([
        { path: '/', label: 'ホーム' },
        { path: `/${a.category}/`, label: cname },
        { label: a.title },
      ]),
      sidebar:
        (hasToc(parsed.headings) ? widget('目次', `<div class="toc toc--side">${tocList(parsed.headings)}</div>`) : '') +
        aboutWidget +
        widget('新着記事', postListHtml(byRecent.slice(0, 5))) +
        categoryWidget,
      content:
        `<article class="post">` +
        `<p class="cat-label"><a href="/${a.category}/">${esc(cname)}</a></p>` +
        `<h1>${esc(a.title)}</h1>` +
        `<p class="dates"><time datetime="${esc(a.published)}">公開 ${esc(a.published)}</time>${
          a.updated !== a.published ? ` ／ <time datetime="${esc(a.updated)}">更新 ${esc(a.updated)}</time>` : ''
        }</p>` +
        eyecatch +
        prNotice +
        (hasToc(parsed.headings) ? `<nav class="toc"><p class="toc__title">目次</p>${tocList(parsed.headings)}</nav>` : '') +
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

  writeFile(
    `${p.slug}/index.html`,
    render(baseTpl, {
      ...common,
      title: `${esc(p.title)} | ${esc(site.name)}`,
      description: esc(p.description),
      canonical: p.url,
      ogType: 'website',
      jsonLd: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        name: p.title,
        description: p.description,
        url: p.url,
        inLanguage: site.lang,
      }),
      breadcrumb: crumbs([{ path: '/', label: 'ホーム' }, { label: p.title }]),
      sidebar: aboutWidget + widget('新着記事', postListHtml(byRecent.slice(0, 5))) + categoryWidget,
      content: `<article class="post"><h1>${esc(p.title)}</h1><p class="dates"><time datetime="${esc(p.updated)}">更新 ${esc(p.updated)}</time></p>${resolveLinks(parsed.html)}</article>`,
      year: String(new Date(p.updated).getFullYear()),
    }),
  );
}

// ---- カテゴリーページ

for (const c of site.categories) {
  const list = byRecent.filter((a) => a.category === c.slug);
  const url = `${ORIGIN}/${c.slug}/`;
  writeFile(
    `${c.slug}/index.html`,
    render(baseTpl, {
      ...common,
      title: `${esc(c.name)}の記事一覧 | ${esc(site.name)}`,
      description: `${c.name}について、メーカー公式の寸法から計算して比べた記事の一覧です。`,
      canonical: url,
      ogType: 'website',
      jsonLd: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        name: `${c.name}の記事一覧`,
        url,
        inLanguage: site.lang,
      }),
      breadcrumb: crumbs([{ path: '/', label: 'ホーム' }, { label: c.name }]),
      // カテゴリが1つの間、このページはトップページと中身がほぼ同じになる。
      // 重複コンテンツとして competing させたくないので noindex にしておく
      // （follow なので記事へのリンクはたどられる）。2つ目のカテゴリができたら自動で index される。
      robots: showCategoryNav ? '' : '<meta name="robots" content="noindex,follow">',
      sidebar: aboutWidget + widget('新着記事', postListHtml(byRecent.slice(0, 5))) + categoryWidget,
      content:
        `<h1>${esc(c.name)}の記事一覧</h1>` +
        `<p class="lead">${esc(c.name)}について、メーカー公式の寸法から計算して比べた記事です。</p>` +
        articleCards(list),
      year: String(new Date().getFullYear()),
    }),
  );
}

// ---- 記事カード（トップ・カテゴリー共通）

function articleCards(list) {
  if (!list.length) return '<p>記事はまだありません。</p>';
  return `<ul class="article-list">${list
    .map(
      (a) =>
        `<li><a class="article-list__link" href="/${a.slug}/">` +
        (a.eyecatch ? `<img class="article-list__thumb" src="${a.eyecatch}" alt="" width="1200" height="630" loading="lazy" decoding="async">` : '') +
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
    sidebar: aboutWidget + categoryWidget,
    content: `<h1>${esc(site.name)}</h1><p class="lead">${esc(site.description)}</p>${articleCards(byRecent)}`,
    year: String(new Date().getFullYear()),
  }),
);

// ---- サイトマップ（HTML）

writeFile(
  'sitemap/index.html',
  render(baseTpl, {
    ...common,
    title: `サイトマップ | ${esc(site.name)}`,
    description: '「寸法で選ぶ」の全ページ一覧です。',
    canonical: `${ORIGIN}/sitemap/`,
    ogType: 'website',
    jsonLd: '',
    breadcrumb: crumbs([{ path: '/', label: 'ホーム' }, { label: 'サイトマップ' }]),
    sidebar: aboutWidget + categoryWidget,
    content:
      '<article class="post"><h1>サイトマップ</h1>' +
      site.categories
        .map(
          (c) =>
            `<h2>${esc(c.name)}</h2>` +
            postListHtml(byRecent.filter((a) => a.category === c.slug)),
        )
        .join('') +
      '<h2>このサイトについて</h2><ul>' +
      site.nav.map((n) => `<li><a href="${n.path}">${esc(n.label)}</a></li>`).join('') +
      '</ul></article>',
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
    jsonLd: '',
    breadcrumb: '',
    sidebar: '',
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

console.log(`built: ${articles.length} article(s), ${pages.length} page(s), ${site.categories.length} category page(s)`);
for (const a of articles) console.log(`  /${a.slug}/  ${a.title}`);
if (!site.affiliateEnabled) console.log('\n注意: affiliateEnabled=false のため、リンク位置はプレースホルダで出力しています。');
