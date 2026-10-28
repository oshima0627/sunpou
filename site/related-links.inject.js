// ⚠️ このファイルは単体では動かない。related-links.mjs が build.mjs の生成コード
// （.build.stitched.mjs）の `function postListHtml(` の直前に文字列として差し込む。
// `articles` `byRecent` `site` `esc` `postListHtml` は差し込み先のスコープのものを使う。
//
// 2026-10-28: 「関連記事」の埋め方を変えた。
//   * それまでは同カテゴリが5本に満たないと「全カテゴリの新着」で埋めていた。
//     1本しかないカテゴリ（ベビーゲート・遮光カーテン・食洗機・モニターアーム・タイヤチェーン）の記事は、
//     新着の洗濯機記事へ5本とも流れ、自分は他の記事から1本も張られていなかった。
//   * 今は「同カテゴリ（収益記事→この記事の次から巡回）」→「近いカテゴリ」の順に埋める。
//     近いカテゴリは RELATED_CATEGORIES で明示する（寸法の悩みが地続きのもの同士だけ）。
//   * 近いカテゴリの記事は、この記事の同カテゴリ内の順番ぶんだけずらして取るので、
//     どの記事も同じくらいの回数、他カテゴリから張られる。

// 近いカテゴリ（近い順）。ここに無いカテゴリは従来どおり新着で埋める。
const RELATED_CATEGORIES = {
  coolerbox: ['cassette-konro'],
  'cassette-konro': ['coolerbox'],
  'cabin-bag': ['tire-chain'],
  'tire-chain': ['cabin-bag'],
  washer: ['fridge', 'dishwasher'],
  fridge: ['washer', 'dishwasher'],
  dishwasher: ['fridge', 'washer'],
  kyatatsu: ['curtain'],
  curtain: ['baby-gate', 'monitor-arm', 'kyatatsu'],
  'baby-gate': ['curtain', 'monitor-arm'],
  'monitor-arm': ['curtain', 'baby-gate'],
};

function rotateBy(list, n) {
  if (!list.length) return list;
  const k = ((n % list.length) + list.length) % list.length;
  return list.slice(k).concat(list.slice(0, k));
}

/** 近いカテゴリの記事を、カテゴリ順を offset ぶんずらしながら1本ずつ交互に取る。 */
function crossCategoryPool(category, offset) {
  const cats = rotateBy(RELATED_CATEGORIES[category] || [], offset);
  const lists = cats.map((slug) => {
    const inCat = articles.filter((x) => x.category === slug);
    const pillar = inCat.find((x) => x.pillar);
    const rest = rotateBy(inCat.filter((x) => x !== pillar), offset);
    return pillar ? [pillar, ...rest] : rest;
  });
  const out = [];
  for (let i = 0; lists.some((l) => i < l.length); i++) {
    for (const l of lists) if (i < l.length) out.push(l[i]);
  }
  return out;
}

/** 記事ページの「関連記事」（最大 同カテゴリ5本＋近いカテゴリ2本、同カテゴリが少ないときは合計5本まで近いカテゴリで埋める）。 */
function relatedArticles(a) {
  const inCat = articles.filter((x) => x.category === a.category);
  const here = inCat.findIndex((x) => x.slug === a.slug);
  const rotated = inCat.slice(here + 1).concat(inCat.slice(0, here));
  const pillar = inCat.find((x) => x.pillar && x.slug !== a.slug);
  const same = [...(pillar ? [pillar] : []), ...rotated.filter((x) => x !== pillar)].slice(0, 5);
  const crossN = Math.max(2, 5 - same.length);
  const cross = crossCategoryPool(a.category, here).slice(0, crossN);
  const picked = [...same, ...cross];
  if (picked.length >= 5) return picked;
  return [...picked, ...byRecent.filter((x) => !picked.includes(x) && x.category !== a.category)].slice(0, 5);
}

/** カテゴリページの「関連記事」。近いカテゴリの記事を最大6本。 */
function relatedForCategory(slug) {
  const cats = RELATED_CATEGORIES[slug] || [];
  const lists = cats.map((s) => {
    const inCat = byRecent.filter((x) => x.category === s);
    const pillar = inCat.find((x) => x.pillar);
    return pillar ? [pillar, ...inCat.filter((x) => x !== pillar)] : inCat;
  });
  const out = [];
  for (let i = 0; lists.some((l) => i < l.length) && out.length < 6; i++) {
    for (const l of lists) if (i < l.length && out.length < 6) out.push(l[i]);
  }
  return out;
}

function categoryRelatedHtml(slug) {
  const list = relatedForCategory(slug);
  if (!list.length) return '';
  const names = (RELATED_CATEGORIES[slug] || [])
    .map((s) => site.categories.find((c) => c.slug === s))
    .filter(Boolean)
    .map((c) => `<a href="/${c.slug}/">${esc(c.name)}</a>`)
    .join('・');
  return (
    `<section class="related"><h2 class="related__title">関連記事</h2>` +
    `<p class="lead lead--tight">あわせて確認したい寸法の記事です（${names}）。</p>` +
    postListHtml(list, 'related__list') +
    `</section>`
  );
}

