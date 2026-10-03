/**
 * Inflate AF-wired build from build.z*.txt (zlib+base64) then run.
 * Patches: prefer bannerHtmlSide for right rail; wire left rail (sidebarLeft);
 *          homepage left+right Moshimo rails (pickHome*);
 *          resolveLinks appends a Rakuten text link from content/rakuten-products.json.
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { pathToFileURL } from 'node:url';

const ROOT = import.meta.dirname;
const names = ['build.z1.txt', 'build.z2.txt', 'build.z3.txt', 'build.z4.txt'];
const b64 = names.map((f) => fs.readFileSync(path.join(ROOT, f), 'utf8').trim()).join('');
let code = zlib.inflateSync(Buffer.from(b64, 'base64')).toString('utf8');

const OLD_SIDE = "  let sideKeys = sideExtract.sides;\n  if (!sideKeys.length && site.affiliateEnabled) {\n    const cat = af.categoryAfPool(a.category);\n    if (cat.length) sideKeys = [{ key: cat[0], label: undefined }];\n  }\n  if (leftExtract.lefts.length) {\n    for (const { key } of leftExtract.lefts) {\n      if (!af.isAfEntryKey(key)) {\n        throw new Error(\n          `[[AFLeft:${key}]] \u304c content/links.json \u306b\u3042\u308a\u307e\u305b\u3093` +\n            ' / \u5bfe\u51e6: content/links.json \u306b\u30ad\u30fc\u3092\u8db3\u3059\uff08\u5de6\u30ec\u30fc\u30eb\u306f\u672a\u914d\u7dda\u306e\u305f\u3081 AFSide \u3092\u4f7f\u3046\uff09',\n        );\n      }\n    }\n  }\n  const bodyMd = af.stripBodyAfMarkers(leftExtract.body);\n";
const NEW_SIDE = "  let sideKeys = sideExtract.sides;\n  if (!sideKeys.length && site.affiliateEnabled) {\n    sideKeys = af.pickCategorySideKeys(a.category);\n  }\n  let leftKeys = leftExtract.lefts;\n  if (leftKeys.length) {\n    for (const { key } of leftKeys) {\n      if (!af.isAfEntryKey(key)) {\n        throw new Error(\n          `[[AFLeft:${key}]] \u304c content/links.json \u306b\u3042\u308a\u307e\u305b\u3093` +\n            ' / \u5bfe\u51e6: content/links.json \u306b\u30ad\u30fc\u3092\u8db3\u3059',\n        );\n      }\n    }\n  } else if (site.affiliateEnabled) {\n    leftKeys = af.pickCategoryLeftKeys(a.category, sideKeys);\n  }\n  const bodyMd = af.stripBodyAfMarkers(leftExtract.body);\n";
const OLD_ADS = "  const sideAdsHtml = af.sideAdsWidget(sideKeys);\n";
const NEW_ADS = "  const sideAdsHtml = af.sideAdsWidget(sideKeys);\n  const leftAdsHtml = af.leftAdsWidget(leftKeys);\n";
const OLD_RENDER = "      sidebar: side(\n        // \u76ee\u6b21\u306f\u672c\u6587\u4e2d\u3068\u30b5\u30a4\u30c9\u30d0\u30fc\u306e2\u304b\u6240\u306b\u51fa\u529b\u3057\u3066\u3044\u308b\u304c\u3001**\u540c\u6642\u306b\u898b\u3048\u308b\u306e\u306f\u7247\u65b9\u3060\u3051**\u3002\n        // 901px \u4ee5\u4e0a\u306f\u8ffd\u5f93\u3059\u308b\u30b5\u30a4\u30c9\u30d0\u30fc\u7248\u3001900px \u4ee5\u4e0b\uff08\u30b5\u30a4\u30c9\u30d0\u30fc\u304c\u672c\u6587\u306e\u4e0b\u306b\u843d\u3061\u308b\u5e45\uff09\u306f\n        // \u672c\u6587\u4e2d\u306e\u7248\u3092 CSS \u3067\u51fa\u3057\u5206\u3051\u308b\u3002\u4e21\u65b9\u898b\u3048\u3066\u3044\u305f\u3068\u304d\u306f\u540c\u3058\u30ea\u30b9\u30c8\u304c2\u56de\u4e26\u3093\u3067\u3044\u305f\u3002\n        (hasToc(parsed.headings) ? widget('\u76ee\u6b21', `<div class=\"toc toc--side\">${tocList(parsed.headings)}</div>`, 'widget--toc') : '') +\n        sideAdsHtml +\n        aboutWidget +\n        widget('\u65b0\u7740\u8a18\u4e8b', postListHtml(byRecent.slice(0, 5))) +\n        categoryWidget\n      ),\n";
const NEW_RENDER = "      sidebarLeft: leftAdsHtml,\n      sidebar: side(\n        // \u76ee\u6b21\u306f\u672c\u6587\u4e2d\u3068\u30b5\u30a4\u30c9\u30d0\u30fc\u306e2\u304b\u6240\u306b\u51fa\u529b\u3057\u3066\u3044\u308b\u304c\u3001**\u540c\u6642\u306b\u898b\u3048\u308b\u306e\u306f\u7247\u65b9\u3060\u3051**\u3002\n        // 901px \u4ee5\u4e0a\u306f\u8ffd\u5f93\u3059\u308b\u30b5\u30a4\u30c9\u30d0\u30fc\u7248\u3001900px \u4ee5\u4e0b\uff08\u30b5\u30a4\u30c9\u30d0\u30fc\u304c\u672c\u6587\u306e\u4e0b\u306b\u843d\u3061\u308b\u5e45\uff09\u306f\n        // \u672c\u6587\u4e2d\u306e\u7248\u3092 CSS \u3067\u51fa\u3057\u5206\u3051\u308b\u3002\u4e21\u65b9\u898b\u3048\u3066\u3044\u305f\u3068\u304d\u306f\u540c\u3058\u30ea\u30b9\u30c8\u304c2\u56de\u4e26\u3093\u3067\u3044\u305f\u3002\n        (hasToc(parsed.headings) ? widget('\u76ee\u6b21', `<div class=\"toc toc--side\">${tocList(parsed.headings)}</div>`, 'widget--toc') : '') +\n        sideAdsHtml +\n        aboutWidget +\n        widget('\u65b0\u7740\u8a18\u4e8b', postListHtml(byRecent.slice(0, 5))) +\n        categoryWidget\n      ),\n";

if (!code.includes(OLD_SIDE)) {
  throw new Error('build.mjs patch: sideKeys/leftKeys block not found — z blobs may have changed');
}
code = code.replace(OLD_SIDE, NEW_SIDE);

if (!code.includes(OLD_ADS)) {
  throw new Error('build.mjs patch: sideAdsHtml line not found');
}
code = code.replace(OLD_ADS, NEW_ADS);

if (!code.includes(OLD_RENDER)) {
  throw new Error('build.mjs patch: article sidebar render block not found');
}
code = code.replace(OLD_RENDER, NEW_RENDER);

// Homepage left+right rails (media 689246). Ads only — no about/category widgets.
const OLD_HOME_PRE = "// ---- トップページ\n\n// 各カテゴリの収益記事（front matter の pillar）。site.json のカテゴリ順に並べる。\nconst pillars = site.categories\n  .map((c) => articles.find((a) => a.category === c.slug && a.pillar))\n  .filter(Boolean);\n\nwriteFile(\n";
const NEW_HOME_PRE = "// ---- トップページ\n\n// 各カテゴリの収益記事（front matter の pillar）。site.json のカテゴリ順に並べる。\nconst pillars = site.categories\n  .map((c) => articles.find((a) => a.category === c.slug && a.pillar))\n  .filter(Boolean);\n\nconst homeSideKeys = site.affiliateEnabled ? af.pickHomeSideKeys() : [];\nconst homeLeftKeys = site.affiliateEnabled ? af.pickHomeLeftKeys(homeSideKeys) : [];\nconst homeSideAdsHtml = af.sideAdsWidget(homeSideKeys);\nconst homeLeftAdsHtml = af.leftAdsWidget(homeLeftKeys);\n\nwriteFile(\n";
const OLD_HOME_SIDE = "    // トップだけサイドバーを外す。\n    // 「このサイトについて」は site.description をそのまま出しており、これは本文の\n    // リード文と**一字一句同じ**だった。「カテゴリー」も本文のカテゴリカードと同じ中身。\n    // つまりトップのサイドバーは全部が本文の複製で、読者に新しい情報が1つも無かった。\n    sidebar: side(''),\n";
const NEW_HOME_SIDE = "    // トップのウィジェット（about/category）は本文複製なので出さない。\n    // 広告レールだけ記事と同じく左右に載せる（media 689246・160×600 L≠R）。\n    sidebarLeft: homeLeftAdsHtml,\n    sidebar: side(homeSideAdsHtml),\n";

if (!code.includes(OLD_HOME_PRE)) {
  throw new Error('build.mjs patch: homepage pillars/writeFile prelude not found');
}
code = code.replace(OLD_HOME_PRE, NEW_HOME_PRE);

if (!code.includes(OLD_HOME_SIDE)) {
  throw new Error("build.mjs patch: homepage empty-sidebar block not found");
}
code = code.replace(OLD_HOME_SIDE, NEW_HOME_SIDE);

const OLD_CAT_LOOP = "for (const c of site.categories) {\n  const list = byRecent.filter((a) => a.category === c.slug);\n  const url = `${ORIGIN}/${c.slug}/`;\n  const catTrail = [{ path: '/', label: '\u30db\u30fc\u30e0' }, { label: c.name }];\n  const lead = readCategoryLead(c.slug);\n";
const NEW_CAT_LOOP = "for (const c of site.categories) {\n  const list = byRecent.filter((a) => a.category === c.slug);\n  const url = `${ORIGIN}/${c.slug}/`;\n  const catTrail = [{ path: '/', label: '\u30db\u30fc\u30e0' }, { label: c.name }];\n  const lead = readCategoryLead(c.slug);\n  const catSideKeys = site.affiliateEnabled ? af.pickCategorySideKeys(c.slug) : [];\n  const catLeftKeys = site.affiliateEnabled ? af.pickCategoryLeftKeys(c.slug, catSideKeys) : [];\n  const catLeadHtml = lead && site.affiliateEnabled ? af.insertAdsBetweenH2s(lead, af.categoryAfPool(c.slug)) : lead;\n  const catLeadAd = '';\n  const catPr = (catLeadAd || catSideKeys.length || catLeftKeys.length)\n    ? `<p class=\"pr-notice\">${esc(site.prLabel)}</p>`\n    : '';\n";
if (!code.includes(OLD_CAT_LOOP)) {
  throw new Error('build.mjs patch: category loop header not found');
}
code = code.replace(OLD_CAT_LOOP, NEW_CAT_LOOP);

const OLD_CAT_BODY = "      robots: showCategoryNav ? '' : '<meta name=\"robots\" content=\"noindex,follow\">',\n      sidebar: side(\n        aboutWidget + widget('\u65b0\u7740\u8a18\u4e8b', postListHtml(byRecent.slice(0, 5))) + categoryWidget\n      ),\n      content:\n        // \u5c0e\u5165\u6587\u304c\u3042\u308c\u3070\u305d\u308c\u3092\u4f7f\u3046\uff08h1 \u3082\u5c0e\u5165\u6587\u5074\u306b\u7f6e\u304f\uff09\u3002\u7121\u3051\u308c\u3070\u5f93\u6765\u3069\u304a\u308a\u306e\u898b\u51fa\u3057\u3060\u3051\u3002\n        (lead\n          ? `<div class=\"post cat-lead\">${lead}</div>`\n          : `<h1>${esc(c.name)}\u306e\u8a18\u4e8b\u4e00\u89a7</h1>` +\n            `<p class=\"lead\">${esc(c.name)}\u306b\u3064\u3044\u3066\u3001\u30e1\u30fc\u30ab\u30fc\u516c\u5f0f\u306e\u5bf8\u6cd5\u304b\u3089\u8a08\u7b97\u3057\u3066\u6bd4\u3079\u305f\u8a18\u4e8b\u3067\u3059\u3002</p>`) +\n        `<h2 class=\"section-title\">${esc(c.name)}\u306e\u8a18\u4e8b\uff08${list.length}\u672c\uff09</h2>` +\n";
const NEW_CAT_BODY = "      robots: showCategoryNav ? '' : '<meta name=\"robots\" content=\"noindex,follow\">',\n      sidebarLeft: af.leftAdsWidget(catLeftKeys),\n      sidebar: side(\n        af.sideAdsWidget(catSideKeys) +\n        aboutWidget + widget('\u65b0\u7740\u8a18\u4e8b', postListHtml(byRecent.slice(0, 5))) + categoryWidget\n      ),\n      content:\n        catPr +\n        // \u5c0e\u5165\u6587\u304c\u3042\u308c\u3070\u305d\u308c\u3092\u4f7f\u3046\uff08h1 \u3082\u5c0e\u5165\u6587\u5074\u306b\u7f6e\u304f\uff09\u3002\u7121\u3051\u308c\u3070\u5f93\u6765\u3069\u304a\u308a\u306e\u898b\u51fa\u3057\u3060\u3051\u3002\n        (catLeadHtml\n          ? `<div class=\"post cat-lead\">${catLeadHtml}</div>`\n          : `<h1>${esc(c.name)}\u306e\u8a18\u4e8b\u4e00\u89a7</h1>` +\n            `<p class=\"lead\">${esc(c.name)}\u306b\u3064\u3044\u3066\u3001\u30e1\u30fc\u30ab\u30fc\u516c\u5f0f\u306e\u5bf8\u6cd5\u304b\u3089\u8a08\u7b97\u3057\u3066\u6bd4\u3079\u305f\u8a18\u4e8b\u3067\u3059\u3002</p>`) +\n        catLeadAd +\n        `<h2 class=\"section-title\">${esc(c.name)}\u306e\u8a18\u4e8b\uff08${list.length}\u672c\uff09</h2>` +\n";
if (!code.includes(OLD_CAT_BODY)) {
  throw new Error('build.mjs patch: category sidebar/content block not found');
}
code = code.replace(OLD_CAT_BODY, NEW_CAT_BODY);

// 楽天は商品リンク作成が発行した hb.afl URL だけ。検索語に型番が境界つきで含まれるとき、
// Amazon の .buy の直後へ文字リンクを足す。504px ウィジェットは埋め込まない。
const OLD_RAKUTEN_LOAD = "const links = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/links.json'), 'utf8'));\n";
const NEW_RAKUTEN_LOAD = OLD_RAKUTEN_LOAD + "const rakutenProducts = JSON.parse(fs.readFileSync(path.join(ROOT, 'content/rakuten-products.json'), 'utf8'));\n";
const OLD_RAKUTEN_FN = "function resolveLinks(html) {\n";
const NEW_RAKUTEN_FN = `function rakutenBuyAnchor(term) {
  const hits = [];
  for (const [model, entry] of Object.entries(rakutenProducts)) {
    if (!model || model.startsWith('//')) continue;
    if (!entry || typeof entry.href !== 'string' || entry.href === '') continue;
    // ASCII 英数の外側だけを境界にする。SJ-MF51R は SJ-MF55R に一致しない。
    const escaped = model.replace(/[.*+?^\${}()|[\\]\\\\]/g, '\\\\$&');
    if (new RegExp(\`(?<![A-Za-z0-9])\${escaped}(?![A-Za-z0-9])\`).test(term)) hits.push(model);
  }
  if (hits.length > 1) {
    throw new Error(\`楽天型番が検索語に複数一致しました: \${term} → \${hits.join(', ')}\`);
  }
  if (!hits.length) return '';
  const href = rakutenProducts[hits[0]].href;
  return \`<a class="buy buy--rakuten" rel="nofollow sponsored noopener" target="_blank" href="\${href}">楽天で見る</a>\`;
}

function resolveLinks(html) {
`;
const OLD_RAKUTEN_RETURN =
  '    return `' + '<a class="buy" href="${url}"${aria} rel="nofollow sponsored noopener" target="_blank">${esc(text)}</a>`' + ';\n';
const NEW_RAKUTEN_RETURN =
  '    const amazonHtml = `' + '<a class="buy" href="${url}"${aria} rel="nofollow sponsored noopener" target="_blank">${esc(text)}</a>`' + ';\n' +
  '    return amazonHtml + rakutenBuyAnchor(term);\n';

if (!code.includes(OLD_RAKUTEN_LOAD)) {
  throw new Error('build.mjs patch: links.json load not found');
}
// replace の置換文字列は $& をマッチ全体に展開する。型番エスケープの \\$& を壊さないため関数で渡す。
code = code.replace(OLD_RAKUTEN_LOAD, () => NEW_RAKUTEN_LOAD);

if (!code.includes(OLD_RAKUTEN_FN)) {
  throw new Error('build.mjs patch: resolveLinks function not found');
}
code = code.replace(OLD_RAKUTEN_FN, () => NEW_RAKUTEN_FN);

if (!code.includes(OLD_RAKUTEN_RETURN)) {
  throw new Error('build.mjs patch: resolveLinks amazon return not found');
}
code = code.replace(OLD_RAKUTEN_RETURN, () => NEW_RAKUTEN_RETURN);

const runPath = path.join(ROOT, '.build.stitched.mjs');
fs.writeFileSync(runPath, code);
await import(pathToFileURL(runPath).href + '?t=' + Date.now());
