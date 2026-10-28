// 関連記事の埋め方を変える（記事ページ・カテゴリページ）。中身は related-links.inject.js。
// build.mjs が生成するコードに文字列で差し込む。差し込み先が見つからなければビルドを落とす。
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));

function mustReplace(code, oldStr, newStr, label) {
  if (!code.includes(oldStr)) throw new Error(`related-links patch: ${label} not found`);
  return code.replace(oldStr, () => newStr);
}

export function patchRelated(code) {
  const inject = fs.readFileSync(path.join(HERE, 'related-links.inject.js'), 'utf8');

  // 1) ヘルパーを postListHtml の直前に差し込む
  code = mustReplace(code, 'function postListHtml(', inject + 'function postListHtml(', 'postListHtml');

  // 2) 記事ページの related の組み立てを差し替える
  const OLD_RELATED = /  const related = \[\n    \.\.\.\(pillar \? \[pillar\] : \[\]\),\n    \.\.\.rotated\.filter\(\(x\) => x !== pillar\),\n    \.\.\.byRecent\.filter\(\(x\) => x\.category !== a\.category\),\n  \]\.slice\(0, 5\);\n/;
  if (!OLD_RELATED.test(code)) throw new Error('related-links patch: article related block not found');
  code = code.replace(OLD_RELATED, () => '  const related = relatedArticles(a);\n');

  // 3) カテゴリページの記事一覧の後ろに「関連記事」を足す
  code = mustReplace(
    code,
    '`<h2 class="section-title">${esc(c.name)}の記事（${list.length}本）</h2>` +\n        articleCards(list),',
    '`<h2 class="section-title">${esc(c.name)}の記事（${list.length}本）</h2>` +\n        articleCards(list) +\n        categoryRelatedHtml(c.slug),',
    'category list',
  );
  return code;
}
