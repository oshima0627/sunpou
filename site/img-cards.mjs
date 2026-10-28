/**
 * ビルド後に dist/ の HTML を後処理して、画像の転送量を減らす。
 *
 * 1. 記事一覧カード（トップ・カテゴリ）の <img class="article-list__thumb"> を
 *    600×315 の WebP/JPEG（public/img/card/）へ差し替える。表示は 240px 幅なので原寸 1200×630 は過大だった。
 *    サムネが無い画像は原寸のまま残して警告する（ビルドは落とさない）。作り方は tools/make-card-thumbs.py。
 * 2. 記事ページのヒーロー画像（アイキャッチ。最初に見える画像）に fetchpriority="high" を付ける。
 *
 * og:image / JSON-LD の画像は <head> 側で、ここでは触らない（原寸 1200×630 のまま）。
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = import.meta.dirname;
const dist = path.join(ROOT, 'dist');

const THUMB_RE = /<img class="article-list__thumb" src="\/img\/([^"\/]+-photo-eyecatch)\.jpg" alt="([^"]*)" width="1200" height="630"( loading="lazy")?( decoding="async")?>/g;
// 記事ページのヒーロー: <p class="eyecatch"> 内の <img>（loading なし＝即読み込み）
const HERO_RE = /(<p class="eyecatch">\s*<img\b)(?![^>]*fetchpriority)([^>]*>)/g;

let swapped = 0;
let heroes = 0;
const missing = new Set();

function walk(dir, out = []) {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    if (fs.statSync(full).isDirectory()) walk(full, out);
    else if (name.endsWith('.html')) out.push(full);
  }
  return out;
}

for (const file of walk(dist)) {
  const html = fs.readFileSync(file, 'utf8');
  let next = html.replace(THUMB_RE, (whole, stem, alt, lazy, decoding) => {
    const jpg = path.join(dist, 'img/card', stem + '.jpg');
    const webp = path.join(dist, 'img/card', stem + '.webp');
    if (!fs.existsSync(jpg) || !fs.existsSync(webp)) {
      missing.add(stem);
      return whole;
    }
    swapped++;
    return (
      `<picture><source type="image/webp" srcset="/img/card/${stem}.webp">` +
      `<img class="article-list__thumb" src="/img/card/${stem}.jpg" alt="${alt}" width="600" height="315"` +
      `${lazy || ''}${decoding || ''}></picture>`
    );
  });
  next = next.replace(HERO_RE, (whole, a, b) => {
    if (/loading="lazy"/.test(b)) return whole;
    heroes++;
    return `${a} fetchpriority="high"${b}`;
  });
  if (next !== html) fs.writeFileSync(file, next);
}

console.log(`img-cards: 一覧サムネ ${swapped} 枚を card/ に差し替え、ヒーロー ${heroes} 枚に fetchpriority=high`);
if (missing.size) {
  console.warn(`img-cards: ⚠️ card/ にサムネが無い画像があります（原寸のまま配信）。python tools/make-card-thumbs.py を実行してコミットしてください: ${[...missing].join(', ')}`);
}
