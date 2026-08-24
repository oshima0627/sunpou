// content/articles/*.md → dist/<slug>/index.html
//
// 依存は marked のみ。フレームワークは入れていない。
// 記事が増えて手に負えなくなったら Astro などに移すが、現状は必要ない。
//
// 実行: node build.mjs   （出力先 dist/ は .gitignore 済み）

import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';

const ROOT = import.meta.dirname;
const DIST = path.join(ROOT, 'dist');

const site = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/site.json'), 'utf8'));
const baseTpl = fs.readFileSync(path.join(ROOT, 'templates/base.html'), 'utf8');

const ORIGIN = site.origin.replace(/\/$/, '');

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

function render(tpl, vars) {
  return tpl.replace(/\{\{(\w+)\}\}/g, (_, k) => (k in vars ? vars[k] : ''));
}

/**
 * フッターの開示文言。
 *
 * affiliateEnabled=false のうちは出さない。リンクが1本も無いのに
 * 「適格販売により収入を得ています」と書くのは事実に反するため。
 */
const disclosureHtml = site.affiliateEnabled
  ? `<p class="disclosure">${esc(site.affiliateDisclosure)}</p>`
  : '';

/**
 * Cloudflare Web Analytics のビーコン。
 *
 * 収益モデルの鍵は「リンククリック率」と「購入率」。クリック数と注文数は
 * アソシエイト・セントラルのレポートから取れるので、ここで測るのは分母の
 * セッション数だけ。トークンはHTMLに出る公開値で、秘密情報ではない。
 */
const analyticsHtml = site.webAnalyticsToken
  ? `<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token":"${site.webAnalyticsToken}"}'></script>`
  : '';

/**
 * 本文中の [[LINK:商品名]] を処理する。
 *
 * 審査に合格するまで（affiliateEnabled=false）はリンクを出さない。
 * true にしただけでリンクが空のまま公開されるのを防ぐため、
 * 実装前に true になっていたら意図的に例外を投げる。
 */
function resolveLinks(html) {
  return html.replace(/\[\[LINK:([^\]]+)\]\]/g, (_, label) => {
    if (!site.affiliateEnabled) {
      return `<span class="link-todo" title="Amazonアソシエイトの審査合格後にリンクへ差し替え">${esc(label)}</span>`;
    }
    throw new Error(`affiliateEnabled=true だがリンクの実体が未実装: ${label}`);
  });
}

/** 表は横スクロールできる箱に入れる（スマホで本文が横に伸びるのを防ぐ）。 */
const wrapTables = (html) =>
  html.replace(/<table>/g, '<div class="table-wrap"><table>').replace(/<\/table>/g, '</table></div>');

/**
 * h2 / h3 に id を振り、目次の材料を集める。
 * marked v15 は見出しに id を付けないので、ここで採番する。
 * 日本語見出しからスラッグを作ると読めないURLになるため連番にしている。
 */
function addHeadingIds(html) {
  const headings = [];
  let n = 0;
  const out = html.replace(/<h([23])>([\s\S]*?)<\/h\1>/g, (_, lvl, inner) => {
    n += 1;
    const id = `s${n}`;
    headings.push({ level: Number(lvl), id, text: inner.replace(/<[^>]+>/g, '').trim() });
    return `<h${lvl} id="${id}">${inner}</h${lvl}>`;
  });
  return { html: out, headings };
}

/** 目次。h2 を親、h3 を子にした入れ子リストにする。 */
function renderToc(headings) {
  // 見出しが少ない記事に目次を出しても邪魔なだけなので出さない
  if (headings.filter((h) => h.level === 2).length < 3) return '';

  const parts = ['<nav class="toc"><p class="toc__title">目次</p><ol>'];
  let subOpen = false;

  for (const h of headings) {
    if (h.level === 2) {
      if (subOpen) { parts.push('</ol></li>'); subOpen = false; }
      parts.push(`<li><a href="#${h.id}">${esc(h.text)}</a></li>`);
    } else {
      if (!subOpen) {
        // 直前の h2 の </li> を開き直して、その中に子リストを作る
        const last = parts.pop();
        parts.push(last.replace(/<\/li>$/, ''), '<ol>');
        subOpen = true;
      }
      parts.push(`<li><a href="#${h.id}">${esc(h.text)}</a></li>`);
    }
  }
  if (subOpen) parts.push('</ol></li>');
  parts.push('</ol></nav>');
  return parts.join('');
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

// ---- 1) 全記事を先に読む（サイドバーの「ほかの記事」に全件必要なため）

const articleDir = path.join(ROOT, 'content/articles');
const files = fs.existsSync(articleDir)
  ? fs.readdirSync(articleDir).filter((f) => f.endsWith('.md')).sort()
  : [];

const articles = files.map((file) => {
  const { meta, body } = parseFrontMatter(fs.readFileSync(path.join(articleDir, file), 'utf8'));
  for (const key of ['title', 'description', 'slug', 'published', 'updated']) {
    if (!meta[key]) throw new Error(`${file}: front matter に ${key} がありません`);
  }
  const slug = meta.slug.replace(/^\/|\/$/g, '');
  return { ...meta, file, slug, body, url: `${ORIGIN}/${slug}/` };
});

const byRecent = [...articles].sort((a, b) => (a.updated < b.updated ? 1 : -1));

// ---- 2) サイドバー

function buildSidebar(currentSlug) {
  const others = byRecent.filter((a) => a.slug !== currentSlug);
  const list = others.length
    ? `<ul>${others
        .map(
          (a) =>
            `<li><a href="/${a.slug}/">${esc(a.title)}</a><time datetime="${esc(a.updated)}">${esc(a.updated)}</time></li>`,
        )
        .join('')}</ul>`
    : '<p>いまはこの記事だけです。</p>';

  return `<div class="widget">
      <p class="widget__title">このサイトについて</p>
      <p>${esc(site.description)}</p>
    </div>
    <div class="widget">
      <p class="widget__title">ほかの記事</p>
      ${list}
    </div>`;
}

const common = {
  lang: site.lang,
  siteName: esc(site.name),
  tagline: esc(site.tagline),
  disclosure: disclosureHtml,
  analytics: analyticsHtml,
};

// ---- 3) 記事ページ

for (const a of articles) {
  const parsed = addHeadingIds(wrapTables(marked.parse(a.body)));
  const html = resolveLinks(parsed.html);
  const toc = renderToc(parsed.headings);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: a.title,
    description: a.description,
    datePublished: a.published,
    dateModified: a.updated,
    inLanguage: site.lang,
    mainEntityOfPage: { '@type': 'WebPage', '@id': a.url },
    publisher: { '@type': 'Organization', name: site.name },
  };

  // PR表記は広告が実際に含まれるときだけ出す
  const prNotice = site.affiliateEnabled
    ? `<p class="pr-notice">${esc(site.prLabel)}</p>`
    : `<p class="pr-notice pr-notice--pending">現在このページに広告リンクはありません（Amazonアソシエイト審査前）。</p>`;

  const dates = `<p class="dates"><time datetime="${esc(a.published)}">公開 ${esc(a.published)}</time>${
    a.updated !== a.published ? ` ／ <time datetime="${esc(a.updated)}">更新 ${esc(a.updated)}</time>` : ''
  }</p>`;

  writeFile(
    `${a.slug}/index.html`,
    render(baseTpl, {
      ...common,
      title: `${esc(a.title)} | ${esc(site.name)}`,
      description: esc(a.description),
      canonical: a.url,
      ogType: 'article',
      jsonLd: JSON.stringify(jsonLd),
      breadcrumb: `<nav class="crumbs"><a href="/">${esc(site.name)}</a> › <span>${esc(a.title)}</span></nav>`,
      sidebar: buildSidebar(a.slug),
      content: `<article class="post"><h1>${esc(a.title)}</h1>${dates}${prNotice}${toc}${html}</article>`,
      year: String(new Date(a.updated).getFullYear()),
    }),
  );
}

// ---- 4) トップページ

const list = byRecent.length
  ? `<ul class="article-list">${byRecent
      .map(
        (a) =>
          `<li><a href="/${a.slug}/">${esc(a.title)}</a><p>${esc(a.description)}</p><time datetime="${esc(a.updated)}">${esc(a.updated)}</time></li>`,
      )
      .join('')}</ul>`
  : '<p>記事はまだありません。</p>';

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
    sidebar: `<div class="widget"><p class="widget__title">このサイトについて</p><p>${esc(site.description)}</p></div>`,
    content: `<h1>${esc(site.name)}</h1><p class="lead">${esc(site.description)}</p>${list}`,
    year: String(new Date().getFullYear()),
  }),
);

// ---- 5) 404

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
    content: '<h1>ページが見つかりません</h1><p><a href="/">トップへ戻る</a></p>',
    year: String(new Date().getFullYear()),
  }),
);

// ---- 6) sitemap / robots

const urls = [
  { loc: `${ORIGIN}/`, lastmod: byRecent[0]?.updated },
  ...byRecent.map((a) => ({ loc: a.url, lastmod: a.updated })),
];

writeFile(
  'sitemap.xml',
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
    .map((u) => `  <url><loc>${u.loc}</loc>${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}</url>`)
    .join('\n')}\n</urlset>\n`,
);

writeFile('robots.txt', `User-agent: *\nAllow: /\n\nSitemap: ${ORIGIN}/sitemap.xml\n`);

// ---- 7) 静的ファイル

copyDir(path.join(ROOT, 'public'), DIST);

console.log(`built ${articles.length} article(s) → dist/`);
for (const a of articles) console.log(`  /${a.slug}/  ${a.title}`);
if (!site.affiliateEnabled) console.log('\n注意: affiliateEnabled=false のため、リンク位置はプレースホルダで出力しています。');
