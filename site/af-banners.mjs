/**
 * Inflate af-banners from af-banners.z*.txt (zlib+base64).
 * Patches: pickHomeSideKeys / pickHomeLeftKeys (homepage L≠R 160×600).
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { pathToFileURL } from 'node:url';

const ROOT = import.meta.dirname;
const names = ["af-banners.z1.txt", "af-banners.z2.txt"];
const b64 = names.map((f) => fs.readFileSync(path.join(ROOT, f), 'utf8').trim()).join('');
let code = zlib.inflateSync(Buffer.from(b64, 'base64')).toString('utf8');

const OLD_AFTER_LEFT = `  function pickCategoryLeftKeys(category, rightKeys = []) {
    const used = new Set((rightKeys || []).map((x) => x.key));
    const cat = categoryAfPool(category);
    const withSide = cat.filter((k) => links[k] && links[k].bannerHtmlSide && !used.has(k));
    const tall = withSide.filter(isSkyscraperSide);
    if (tall.length) return [{ key: tall[0], label: undefined }];
    for (const k of SKYSCRAPER_FALLBACKS) {
      if (!used.has(k) && links[k] && links[k].bannerHtmlSide) {
        return [{ key: k, label: undefined }];
      }
    }
    if (withSide.length) return [{ key: withSide[0], label: undefined }];
    if (!used.has('moshimo-amazon') && links['moshimo-amazon'] && links['moshimo-amazon'].bannerHtmlSide) {
      return [{ key: 'moshimo-amazon', label: undefined }];
    }
    return [];
  }

  function collectAfBannerPool(md) {`;

const NEW_AFTER_LEFT = `  function pickCategoryLeftKeys(category, rightKeys = []) {
    const used = new Set((rightKeys || []).map((x) => x.key));
    const cat = categoryAfPool(category);
    const withSide = cat.filter((k) => links[k] && links[k].bannerHtmlSide && !used.has(k));
    const tall = withSide.filter(isSkyscraperSide);
    if (tall.length) return [{ key: tall[0], label: undefined }];
    // トップ（category なし）だけ、グローバル 160×600 で L≠R を維持する。
    // 記事カテゴリではスーツケース／アウトドアの縦長に落とさない（テーマ外れ）。
    if (!category) {
      for (const k of SKYSCRAPER_FALLBACKS) {
        if (!used.has(k) && links[k] && links[k].bannerHtmlSide) {
          return [{ key: k, label: undefined }];
        }
      }
    }
    if (withSide.length) return [{ key: withSide[0], label: undefined }];
    if (
      !used.has('moshimo-amazon') &&
      links['moshimo-amazon'] &&
      links['moshimo-amazon'].bannerHtmlSide &&
      (!category || cat.includes('moshimo-amazon'))
    ) {
      return [{ key: 'moshimo-amazon', label: undefined }];
    }
    return [];
  }

  /**
   * トップページ右サイド: 160×600 を優先（記事 coolerbox と同じく gifteria）。
   * 左は pickHomeLeftKeys で legend など L≠R。
   */
  function pickHomeSideKeys() {
    // R を gifteria 優先にして、L が legend を取れるようにする
    const preferRight = ['moshimo-gifteria-outdoor', ...SKYSCRAPER_FALLBACKS];
    const seen = new Set();
    for (const k of preferRight) {
      if (seen.has(k)) continue;
      seen.add(k);
      if (links[k] && links[k].bannerHtmlSide && isSkyscraperSide(k)) {
        return [{ key: k, label: undefined }];
      }
    }
    for (const k of Object.keys(links)) {
      if (!isAfEntryKey(k)) continue;
      if (links[k] && links[k].bannerHtmlSide && isSkyscraperSide(k)) {
        return [{ key: k, label: undefined }];
      }
    }
    if (links['moshimo-amazon'] && links['moshimo-amazon'].bannerHtmlSide) {
      return [{ key: 'moshimo-amazon', label: undefined }];
    }
    return [];
  }

  /** トップ左レール: 右と別キー。pickCategoryLeftKeys のグローバル 160×600 フォールバックを流用。 */
  function pickHomeLeftKeys(rightKeys = []) {
    return pickCategoryLeftKeys(null, rightKeys);
  }

  function collectAfBannerPool(md) {`;

if (!code.includes(OLD_AFTER_LEFT)) {
  throw new Error('af-banners.mjs patch: pickCategoryLeftKeys block not found — z blobs may have changed');
}
code = code.replace(OLD_AFTER_LEFT, NEW_AFTER_LEFT);

const OLD_EXPORT = `    pickCategorySideKeys,
    pickCategoryLeftKeys,
    collectAfBannerPool,`;
const NEW_EXPORT = `    pickCategorySideKeys,
    pickCategoryLeftKeys,
    pickHomeSideKeys,
    pickHomeLeftKeys,
    collectAfBannerPool,`;

if (!code.includes(OLD_EXPORT)) {
  throw new Error('af-banners.mjs patch: export block not found');
}
code = code.replace(OLD_EXPORT, NEW_EXPORT);

const insertStart = code.indexOf('  function insertAdsBetweenH2s(html, pool) {');
const insertEnd = code.indexOf('  function resolveAfMarkers(html) {');
if (insertStart < 0 || insertEnd < 0 || insertEnd < insertStart) {
  throw new Error('af-banners.mjs patch: insertAdsBetweenH2s bounds not found');
}
const bodySnippet = fs.readFileSync(path.join(ROOT, 'af-body-insert.snippet.js'), 'utf8');
if (!bodySnippet.includes('function categoryLeadBanner')) {
  throw new Error('af-banners.mjs patch: body snippet missing categoryLeadBanner');
}
code = code.slice(0, insertStart) + bodySnippet + code.slice(insertEnd);

const OLD_BODY_EXPORT = `    insertAdsBetweenH2s,
    resolveAfMarkers,`;
const NEW_BODY_EXPORT = `    insertAdsBetweenH2s,
    categoryLeadBanner,
    resolveAfMarkers,`;
if (!code.includes(OLD_BODY_EXPORT)) {
  throw new Error('af-banners.mjs patch: insertAds export not found');
}
code = code.replace(OLD_BODY_EXPORT, NEW_BODY_EXPORT);

const runPath = path.join(ROOT, '.af-banners.inflated.mjs');
fs.writeFileSync(runPath, code);
const mod = await import(pathToFileURL(runPath).href + '?t=' + Date.now());
export const createAfHelpers = mod.createAfHelpers;
