  function bodyCreatives(pool) {
    const creatives = [];
    const seenHtml = new Set();
    const keys = (pool || []).filter((key) => isAfEntryKey(key));
    const official = keys.filter((key) => links[key] && links[key].bannerHtml);
    const source = official.length ? official : keys;
    for (const key of source) {
      const html = (links[key] && links[key].bannerHtml) || '';
      if (html) {
        if (seenHtml.has(html)) continue;
        seenHtml.add(html);
        creatives.push({ key, html });
      } else if (!official.length) {
        creatives.push({ key, html: '' });
      }
    }
    // 公式バナーが1種類だけのとき、別画像の bannerHtmlSide を本文2枚目にする（同一HTMLの連続を避ける）。
    if (official.length && creatives.length < 2) {
      for (const key of official) {
        const html = (links[key] && links[key].bannerHtmlSide) || '';
        if (!html || seenHtml.has(html)) continue;
        seenHtml.add(html);
        creatives.push({ key, html });
      }
    }
    creatives.sort((a, b) => rankCreative(a) - rankCreative(b));
    return creatives;
  }

  function rankCreative(c) {
    const geom = c.html ? bannerGeometry(c.html) : null;
    if (geom && geom.w >= 700 && geom.w > geom.h * 1.5) return 0;
    if (geom && geom.w > geom.h * 1.5) return 1;
    if (c.html) return 2;
    return 3;
  }

  function renderBodyCreative(creative) {
    if (creative.html) {
      const geom = bannerGeometry(creative.html);
      const landscape = geom && geom.w > geom.h * 1.5;
      const largeLandscape = landscape && geom.w >= 700;
      let cardCls = 'af-card af-card--box';
      if (largeLandscape) cardCls = 'af-card af-card--wide';
      else if (landscape) cardCls = 'af-card af-card--wide-sm';
      return (
        '<aside class="' + cardCls + '">' +
          '<div class="af-card__banner">' + creative.html + '</div>' +
        '</aside>'
      );
    }
    return renderAfCard(links[creative.key], links[creative.key].label, { side: false, key: creative.key });
  }

  function h2Plain(part) {
    const hm = String(part).match(/^<h2[^>]*>([\s\S]*?)<\/h2>/i);
    return hm ? hm[1].replace(/<[^>]+>/g, '') : '';
  }

  /**
   * 本文の公式バナー。
   * 導入直後（先頭H2の前）に必ず1つ。左レールは 1280px 未満で非表示なので、スマホの最初の広告はここ。
   * 公式が2種以上なら、スキップ見出し以外のH2前にも回転し、直前と同じHTMLは置かない。
   * 1種だけのときは導入直後と、結論（またはまとめ）H2の前だけ。出典などの直前には置かない。
   */
  function insertAdsBetweenH2s(html, pool) {
    const creatives = bodyCreatives(pool);
    if (!creatives.length) return html;
    const parts = html.split(/(?=<h2\b)/i);
    if (parts.length < 2) {
      return html.trim() ? html + renderBodyCreative(creatives[0]) : html;
    }
    const slots = [];
    for (let i = 1; i < parts.length; i++) {
      if (i > 1 && AF_H2_SKIP_RE.test(h2Plain(parts[i]))) continue;
      slots.push(i);
    }
    let useSlots = slots;
    if (creatives.length < 2 && slots.length > 2) {
      const conclusion = slots.find((i) => /結論|まとめ/.test(h2Plain(parts[i])));
      const second = conclusion && conclusion !== slots[0] ? conclusion : slots[slots.length - 1];
      useSlots = [slots[0], second];
    }
    const insertAt = new Map();
    let prevSig = null;
    let rotate = 0;
    for (const idx of useSlots) {
      let chosen = null;
      let advance = 1;
      for (let attempt = 0; attempt < creatives.length; attempt++) {
        const c = creatives[(rotate + attempt) % creatives.length];
        const sig = c.html || c.key;
        if (sig !== prevSig) {
          chosen = c;
          advance = attempt + 1;
          break;
        }
      }
      if (!chosen) continue;
      insertAt.set(idx, chosen);
      prevSig = chosen.html || chosen.key;
      rotate = (rotate + advance) % creatives.length;
    }
    const out = [parts[0]];
    for (let i = 1; i < parts.length; i++) {
      if (insertAt.has(i)) out.push(renderBodyCreative(insertAt.get(i)));
      out.push(parts[i]);
    }
    return out.join('');
  }

  /** カテゴリ一覧の導入直後。公式バナー1つ（横長優先）。プール外のテーマは出さない。 */
  function categoryLeadBanner(category) {
    const creatives = bodyCreatives(categoryAfPool(category));
    if (!creatives.length) return '';
    const wide = creatives.find((c) => {
      const geom = c.html ? bannerGeometry(c.html) : null;
      return geom && geom.w >= 700 && geom.w > geom.h * 1.5;
    });
    return renderBodyCreative(wide || creatives[0]);
  }

