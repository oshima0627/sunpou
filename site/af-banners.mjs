/**
 * Amazonアソシエイト CSSバナー（H2間・サイド）。links.json 台帳を引く。
 * もしもURLは拒否。商品画像なし。
 */

const AF_H2_SKIP_RE = /出典|確認できなかった|未確認|この記事で扱っていない|数字の出どころ|広告/;

export function createAfHelpers({ links, site, esc }) {
  function isAfEntryKey(key) {
    return Boolean(key) && !String(key).startsWith('//') && links[key] && typeof links[key] === 'object';
  }

  function assertAssociateUrl(url, key) {
    if (!url) return;
    const tag = site.associateTag || 'sunpou-22';
    if (!String(url).includes(`tag=${tag}`)) {
      throw new Error(
        `links.json の ${key} の url に tag=${tag} がありません` +
          ' / 対処: Associates 発行の検索または商品URLだけを入れる（もしもURLは不可）',
      );
    }
    if (/moshimo\.com|af\.moshimo/i.test(url)) {
      throw new Error(
        `links.json の ${key} にもしもURLが入っています（sunpou では不可）` +
          ' / 対処: Amazon Associates の URL（tag=sunpou-22）に差し替える',
      );
    }
  }

  function renderAfCard(entry, label, { side = false, key = '?' } = {}) {
    const text = label || entry.label;
    if (!text) throw new Error(`AF card (${key}): label がありません`);
    assertAssociateUrl(entry.url, key);
    if (!site.affiliateEnabled || !entry.url) {
      return `<span class="link-todo" title="広告リンク未設定">${esc(text)}</span>`;
    }
    const short = entry.shortLabel || 'Amazon.co.jp';
    const href = esc(entry.url);
    if (side) {
      return (
        `<div class="af-banner-only">` +
          `<a class="af-banner-only__link" href="${href}" rel="nofollow sponsored noopener" target="_blank">` +
            `<span class="af-banner-only__title">${esc(text)}</span>` +
            `<span class="af-banner-only__meta">${esc(short)} <span aria-hidden="true">↗</span></span>` +
          `</a>` +
        `</div>`
      );
    }
    return (
      `<aside class="af-card">` +
        `<a class="af-card__link" href="${href}" rel="nofollow sponsored noopener" target="_blank">` +
          `<span class="af-card__title">${esc(text)}</span>` +
          `<span class="af-card__meta">${esc(short)}<span class="af-card__chev" aria-hidden="true">↗</span></span>` +
        `</a>` +
      `</aside>`
    );
  }

  function extractSideAds(md) {
    const sides = [];
    let body = md.replace(/\[\[AFSide:([^\]]+)\]\]/g, (_, raw) => {
      const [key, label] = raw.split('::').map((x) => x.trim());
      if (!key) throw new Error(`[[AFSide:...]] のキーが空です: ${raw}`);
      sides.push({ key, label });
      return '';
    });
    body = body.replace(/^[ \t]*-[ \t]*\n/gm, '');
    body = body.replace(/\n{3,}/g, '\n\n');
    return { body, sides };
  }

  function extractLeftAds(md) {
    const lefts = [];
    let body = md.replace(/\[\[AFLeft:([^\]]+)\]\]/g, (_, raw) => {
      const [key, label] = raw.split('::').map((x) => x.trim());
      if (!key) throw new Error(`[[AFLeft:...]] のキーが空です: ${raw}`);
      lefts.push({ key, label });
      return '';
    });
    body = body.replace(/^[ \t]*-[ \t]*\n/gm, '');
    body = body.replace(/\n{3,}/g, '\n\n');
    return { body, lefts };
  }

  function sideAdsWidget(sides) {
    if (!sides.length) return '';
    const cards = sides.map(({ key, label }) => {
      if (!isAfEntryKey(key)) {
        throw new Error(
          `[[AFSide:${key}]] が content/links.json にありません` +
            ' / 対処: content/links.json にキーを足す',
        );
      }
      return renderAfCard(links[key], label, { side: true, key });
    });
    return `<div class="af-rail" aria-label="広告">${cards.join('\n')}</div>`;
  }

  function categoryAfPool(category) {
    if (!category) return [];
    return Object.keys(links).filter((key) => {
      if (!isAfEntryKey(key)) return false;
      const cats = links[key].categories;
      return Array.isArray(cats) && cats.includes(category) && links[key].url;
    });
  }

  function collectAfBannerPool(md) {
    const seen = new Set();
    const pool = [];
    const re = /\[\[(?:AF|AFSide|AFLeft):([^\]]+)\]\]/g;
    let m;
    while ((m = re.exec(md)) !== null) {
      const key = m[1].split('::')[0].trim();
      if (!key || seen.has(key)) continue;
      seen.add(key);
      if (!isAfEntryKey(key)) continue;
      if (links[key].url) pool.push(key);
    }
    return pool;
  }

  function stripBodyAfMarkers(md) {
    let body = md.replace(/\[\[AF:([^\]]+)\]\]/g, (_, raw) => {
      const [key] = raw.split('::').map((x) => x.trim());
      if (!key) throw new Error(`[[AF:...]] のキーが空です: ${raw}`);
      if (!isAfEntryKey(key)) {
        throw new Error(
          `[[AF:${key}]] が content/links.json にありません` +
            ' / 対処: content/links.json にキーを足す（url はまだ空でよい）',
        );
      }
      return '';
    });
    body = body.replace(/^[ \t]*-[ \t]*\n/gm, '');
    body = body.replace(/\n{3,}/g, '\n\n');
    return body;
  }

  function insertAdsBetweenH2s(html, pool) {
    if (!pool.length) return html;
    const parts = html.split(/(?=<h2\b)/i);
    if (parts.length < 2) return html;
    let rotate = 0;
    const out = [parts[0]];
    for (let i = 1; i < parts.length; i++) {
      const prev = parts[i - 1];
      const next = parts[i];
      const prevIsContent = /^<h2\b/i.test(prev);
      const nextIsContent = /^<h2\b/i.test(next);
      if (prevIsContent && nextIsContent) {
        const hm = next.match(/^<h2[^>]*>([\s\S]*?)<\/h2>/i);
        const h2text = hm ? hm[1].replace(/<[^>]+>/g, '') : '';
        if (!AF_H2_SKIP_RE.test(h2text)) {
          const key = pool[rotate % pool.length];
          rotate += 1;
          if (!isAfEntryKey(key)) {
            throw new Error(
              `H2間広告のキー ${key} が content/links.json にありません` +
                ' / 対処: content/links.json にキーを足す',
            );
          }
          out.push(renderAfCard(links[key], links[key].label, { side: false, key }));
        }
      }
      out.push(next);
    }
    return out.join('');
  }

  function resolveAfMarkers(html) {
    let out = html.replace(/\[\[AF:([^\]]+)\]\]/g, (_, raw) => {
      const [key, label] = raw.split('::').map((x) => x.trim());
      if (!key) throw new Error(`[[AF:...]] のキーが空です: ${raw}`);
      if (!isAfEntryKey(key)) {
        throw new Error(
          `[[AF:${key}]] が content/links.json にありません` +
            ' / 対処: content/links.json にキーを足す（url はまだ空でよい）',
        );
      }
      return renderAfCard(links[key], label, { side: false, key });
    });
    out = out.replace(/<p>\s*(<aside class="af-card[\s\S]*?<\/aside>)\s*<\/p>/g, '$1');
    return out;
  }

  function validateAfLinks() {
    for (const key of Object.keys(links)) {
      if (!isAfEntryKey(key)) continue;
      assertAssociateUrl(links[key].url, key);
    }
  }

  return {
    isAfEntryKey,
    extractSideAds,
    extractLeftAds,
    sideAdsWidget,
    categoryAfPool,
    collectAfBannerPool,
    stripBodyAfMarkers,
    insertAdsBetweenH2s,
    resolveAfMarkers,
    validateAfLinks,
  };
}
