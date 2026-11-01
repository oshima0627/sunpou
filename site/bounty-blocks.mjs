// Amazon の紹介プログラム（Audible / Amazon Music Unlimited）の短い文字ブロック。
// front matter に `bounty: outdoor` のように書いた記事だけ、本文の最後（判断CTAの後・
// シェアと関連記事の前）に1つ出す。バナーではない（`afbody: none` とは独立）。
// 未定義の値を書いたらビルドを落とす。
//
// 文言の決まり: 体験期間・価格・キャンペーン条件は書かない（変わるうえ未確認のため）。
// リンク形式は Amazonアソシエイト ヘルプの公式形式（tag=sunpou-22）。
function mustReplace(code, oldStr, newStr, label) {
  if (code.split(oldStr).length !== 2) throw new Error(`bounty patch: ${label} が1つに定まりません`);
  return code.replace(oldStr, () => newStr);
}

const HELPER = `
const BOUNTY_BLOCKS = {
  outdoor: {
    title: 'キャンプ場までの道のりや、火を囲む夜に',
    lead: '長い運転や焚き火のそばで、オーディオブックや音楽を流しておくのもひとつの過ごし方です。',
    links: [
      { label: 'Audible（オーディオブック）', url: 'https://www.amazon.co.jp/b/ref=adbl_JP_as_0068?ie=UTF8&node=5816607051&tag=sunpou-22' },
      { label: 'Amazon Music Unlimited', url: 'https://www.amazon.co.jp/music/unlimited/?tag=sunpou-22' },
    ],
    note: '詳しくは公式ページで。',
  },
};

function bountyHtml(a) {
  if (!a.bounty) return '';
  const b = BOUNTY_BLOCKS[a.bounty];
  if (!b) {
    throw new Error(\`\${a.file}: front matter の bounty: \${a.bounty} は未定義です（定義: \${Object.keys(BOUNTY_BLOCKS).join(', ')}）\`);
  }
  if (!site.affiliateEnabled) return '';
  return (
    \`<aside class="bounty" aria-label="PR">\` +
    \`<p class="bounty__badge">PR</p>\` +
    \`<p class="bounty__title">\${esc(b.title)}</p>\` +
    \`<p class="bounty__lead">\${esc(b.lead)}</p>\` +
    \`<p class="bounty__links">\` +
    b.links.map((l) => \`<a class="buy" href="\${esc(l.url)}" rel="nofollow sponsored noopener" target="_blank">\${esc(l.label)}</a>\`).join(' ') +
    \` <span class="bounty__note">\${esc(b.note)}</span></p>\` +
    \`</aside>\`
  );
}

`;

export function patchBounty(code) {
  code = mustReplace(code, 'function shareButtons(title, url) {\n', HELPER + 'function shareButtons(title, url) {\n', 'shareButtons 関数');
  code = mustReplace(
    code,
    '        decisionCtaHtml(a.category) +\n        shareButtons(a.title, a.url) +\n',
    '        decisionCtaHtml(a.category) +\n        bountyHtml(a) +\n        shareButtons(a.title, a.url) +\n',
    '記事本文の判断CTA→シェア',
  );
  return code;
}
