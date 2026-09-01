/**
 * front matter の `updated:` を、**git が記録している最終コミット日**に合わせる。
 *
 * なぜ要るか（2026-09-01 のレビューで実際に起きたこと）:
 *   19記事を 9/1 に直した（「26製品」→「33製品」の事実修正を含む）のに、`updated:` は
 *   18本が 8/24・8/25 のまま残っていた。その結果
 *     - sitemap.xml の lastmod が古い（再クロールの合図が出ない）
 *     - JSON-LD の dateModified が古い
 *     - 記事に表示される「更新 2026-08-24」が事実と違う
 *   の3つが同時に起きていた。**事実を直した日を出していない**のは、
 *   一次情報から計算することを売りにしているサイトとしてまずい。
 *
 * 手で書くと必ずまた忘れるので、git から引く。**git が正、front matter が写し。**
 *
 * 使い方:
 *   node tools/sync-updated.mjs           # 差分を表示するだけ（何も書かない）
 *   node tools/sync-updated.mjs --write    # front matter を書き換える
 *
 * ⚠️ **コミットする前に走らせても意味がない。** git の最終コミット日を見るので、
 * 今回の変更を含めたいなら「コミット → 走らせる → 差分が出たら直してもう一度コミット」の順になる。
 * 実務では **記事を直したコミットの次に、この同期だけのコミットを置く**のが手数が少ない。
 */
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const WRITE = process.argv.includes('--write');
const DIRS = ['site/content/articles', 'site/content/pages'];

/**
 * そのファイルの**中身が最後に変わった**コミットの日付。
 *
 * ⚠️ **`git log -1` では駄目だった。** この同期そのものがコミットになるので、
 * 次に走らせると「最終コミット日＝同期した日」になり、**毎回ずれ続ける**
 * （実際 about.md / privacy.md が 8/25 → 9/1 に押し上げられた）。
 * **`updated:` の行しか変わっていないコミットは飛ばして**、その手前を見る。
 */
function lastContentChange(rel) {
  const shas = execFileSync('git', ['log', '--format=%H', '--', rel], { cwd: ROOT })
    .toString()
    .trim()
    .split('\n')
    .filter(Boolean);
  for (const sha of shas) {
    const diff = execFileSync('git', ['show', '--format=', '--unified=0', sha, '--', rel], { cwd: ROOT }).toString();
    const edits = diff
      .split('\n')
      .filter((l) => /^[+-]/.test(l) && !/^(\+\+\+|---)/.test(l))
      .map((l) => l.slice(1).trim());
    // 追加も削除も `updated: ...` だけなら、それは日付合わせのコミット
    if (edits.length && edits.every((l) => /^updated:/.test(l))) continue;
    return execFileSync('git', ['log', '-1', '--format=%cs', sha], { cwd: ROOT }).toString().trim();
  }
  return '';
}

let changed = 0;
let checked = 0;

for (const dir of DIRS) {
  const full = path.join(ROOT, dir);
  if (!fs.existsSync(full)) continue;
  for (const file of fs.readdirSync(full).filter((f) => f.endsWith('.md')).sort()) {
    const rel = `${dir}/${file}`;
    const gitDate = lastContentChange(rel);
    // 一度もコミットされていない新規ファイルは触らない（書き手が入れた日付をそのまま使う）
    if (!gitDate) continue;
    checked++;

    const text = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    const m = text.match(/^updated:[ \t]*(\S+)[ \t]*$/m);
    if (!m) {
      console.log(`  ! ${rel}: updated: がありません`);
      continue;
    }
    if (m[1] === gitDate) continue;

    changed++;
    console.log(`  ${rel}: ${m[1]} -> ${gitDate}`);
    if (WRITE) fs.writeFileSync(path.join(ROOT, rel), text.replace(m[0], `updated: ${gitDate}`));
  }
}

console.log(
  changed === 0
    ? `updated: ${checked}件すべて git の最終コミット日と一致しています`
    : WRITE
      ? `updated: ${changed}件 / ${checked}件 を書き換えました`
      : `updated: ${changed}件 / ${checked}件 がずれています（--write で書き換え）`,
);
if (!WRITE && changed > 0) process.exitCode = 1;
