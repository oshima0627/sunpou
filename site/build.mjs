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
 * 審査に合格してリンクを貼る時点で true にする。
 */
const disclosureHtml = site.affiliateEnabled
  ? `<p class="disclosure">${esc(site.affiliateDisclosure)}</p>`
  : '';

/**
 * 本文中の [[LINK:商品名]] を処理する。
 *
 * 審査に合格するまで（affiliateEnabled=false）はリンクを出さない。
 * 未承認のうちにタグ付きリンクを貼っても計測されないうえ、
 * 「Amazonのアソシエイトとして…」の開示文言だけが先に出ている状態を避けたい。
 */
function resolveLinks(html, opts) {
  return html.replace(/\[\[LINK:([^\]]+)\]\]/g, (_, label) => {
    if (!opts.affiliateEnabled) {
      return `<span class="link-todo" title="Amazonアソシエイトの審査合格後にリンクへ差し替え">${esc(label)}</span>`;
    }
    // 合格後はここで実リンクに差し替える。URL は content/links.json 等に外出しする想定。
    throw new Error(`affiliateEnabled=true だがリンクの実体が未実装: ${label}`);
  });
}

/** 表は横スクロールできる箱に入れる（スマホで本文が横に伸びるのを防ぐ）。 */
const wrapTables = (html) =>
  html.replace(/<table>/g, '<div class="table-wrap"><table>').replace(/<\/table>/g, '</table></div>');

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

// dist ごと削除せず、中身だけ消す。
// wrangler dev が dist を監視している間、Windows ではディレクトリ自体の削除が
// EPERM/EBUSY で失敗する（dev を起動したまま再ビルドすると必ず踏む）。
// 個別の削除が失敗しても、後続の書き込みで上書きされるので続行してよい。
fs.mkdirSync(DIST, { recursive: true });
for (const entry of fs.readdirSync(DIST)) {
  try {
    fs.rmSync(path.join(DIST, entry), { recursive: true, force: true, maxRetries: 5, retryDelay: 100 });
  } catch (err) {
    console.warn(`clean: dist/${entry} を削除できませんでした（${err.code}）。上書きで続行します。`);
  }
}

marked.setOptions({ gfm: true, breaks: false });

const articleDir = path.join(ROOT, 'content/articles');
const files = fs.existsSync(articleDir)
  ? fs.readdirSync(articleDir).filter((f) => f.endsWith('.md')).sort()
  : [];

const articles = [];

for (const file of files) {
  const raw = fs.readFileSync(path.join(articleDir, file), 'utf8');
  const { meta, body } = parseFrontMatter(raw);

  for (const key of ['title', 'description', 'slug', 'published', 'updated']) {
    if (!meta[key]) throw new Error(`${file}: front matter に ${key} がありません`);
  }

  const slug = meta.slug.replace(/^\/|\/$/g, '');
  const url = `${ORIGIN}/${slug}/`;

  let html = wrapTables(marked.parse(body));
  html = resolveLinks(html, site);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: meta.title,
    description: meta.description,
    datePublished: meta.published,
    dateModified: meta.updated,
    inLanguage: site.lang,
    mainEntityOfPage: { '@type': 'WebPage', '@id': url },
    publisher: { '@type': 'Organization', name: site.name },
  };

  // PR表記は「広告が実際に含まれるとき」に出す。リンクが無い状態で
  // 「広告が含まれます」と書くのは事実に反する。
  const prNotice = site.affiliateEnabled
    ? `<p class="pr-notice">${esc(site.prLabel)}</p>`
    : `<p class="pr-notice pr-notice--pending">現在このページに広告リンクはありません（Amazonアソシエイト審査前）。</p>`;

  writeFile(
    `${slug}/index.html`,
    render(baseTpl, {
      lang: site.lang,
      title: `${esc(meta.title)} | ${esc(site.name)}`,
      description: esc(meta.description),
      canonical: url,
      siteName: esc(site.name),
      ogType: 'article',
      jsonLd: JSON.stringify(jsonLd),
      breadcrumb: `<nav class="crumbs"><a href="/">${esc(site.name)}</a> › <span>${esc(meta.title)}</span></nav>`,
      content: `
        <article>
          <h1>${esc(meta.title)}</h1>
          <p class="dates">
            <time datetime="${esc(meta.published)}">公開 ${esc(meta.published)}</time>
            ${meta.updated !== meta.published ? ` ／ <time datetime="${esc(meta.updated)}">更新 ${esc(meta.updated)}</time>` : ''}
          </p>
          ${prNotice}
          ${html}
        </article>`,
      disclosure: disclosureHtml,
      year: String(new Date(meta.updated).getFullYear()),
    }),
  );

  articles.push({ ...meta, slug, url });
}

// ---- トップページ

const list = articles.length
  ? `<ul class="article-list">${articles
      .map(
        (a) =>
          `<li><a href="/${a.slug}/">${esc(a.title)}</a><p>${esc(a.description)}</p><time datetime="${esc(a.updated)}">${esc(a.updated)}</time></li>`,
      )
      .join('')}</ul>`
  : '<p>記事はまだありません。</p>';

writeFile(
  'index.html',
  render(baseTpl, {
    lang: site.lang,
    title: `${esc(site.name)} — ${esc(site.tagline)}`,
    description: esc(site.description),
    canonical: `${ORIGIN}/`,
    siteName: esc(site.name),
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
    content: `<h1>${esc(site.name)}</h1><p class="lead">${esc(site.description)}</p>${list}`,
    disclosure: disclosureHtml,
    year: String(new Date().getFullYear()),
  }),
);

// ---- 404

writeFile(
  '404.html',
  render(baseTpl, {
    lang: site.lang,
    title: `ページが見つかりません | ${esc(site.name)}`,
    description: 'お探しのページは見つかりませんでした。',
    canonical: '',
    siteName: esc(site.name),
    ogType: 'website',
    jsonLd: '',
    breadcrumb: '',
    content: '<h1>ページが見つかりません</h1><p><a href="/">トップへ戻る</a></p>',
    disclosure: disclosureHtml,
    year: String(new Date().getFullYear()),
  }),
);

// ---- sitemap / robots

const urls = [{ loc: `${ORIGIN}/`, lastmod: articles[0]?.updated }, ...articles.map((a) => ({ loc: a.url, lastmod: a.updated }))];

writeFile(
  'sitemap.xml',
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls
    .map((u) => `  <url><loc>${u.loc}</loc>${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}</url>`)
    .join('\n')}\n</urlset>\n`,
);

writeFile('robots.txt', `User-agent: *\nAllow: /\n\nSitemap: ${ORIGIN}/sitemap.xml\n`);

// ---- 静的ファイル

copyDir(path.join(ROOT, 'public'), DIST);

console.log(`built ${articles.length} article(s) → dist/`);
for (const a of articles) console.log(`  /${a.slug}/  ${a.title}`);
if (!site.affiliateEnabled) console.log('\n注意: affiliateEnabled=false のため、リンク位置はプレースホルダで出力しています。');
