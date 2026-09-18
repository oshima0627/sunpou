/**
 * Inflate AF-wired build from build.z*.txt (zlib+base64) then run.
 * Applies small layout/rail patches after inflate (keeps z blobs stable).
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { pathToFileURL } from 'node:url';

const ROOT = import.meta.dirname;
const z1parts = ['build.z1a.txt', 'build.z1b.txt'].map((f) => path.join(ROOT, f));
const useSplitZ1 = z1parts.every((f) => fs.existsSync(f));
const names = useSplitZ1
  ? ['build.z1a.txt', 'build.z1b.txt', 'build.z2.txt', 'build.z3.txt', 'build.z4.txt']
  : ['build.z1.txt', 'build.z2.txt', 'build.z3.txt', 'build.z4.txt'];
const b64 = names.map((f) => fs.readFileSync(path.join(ROOT, f), 'utf8').trim()).join('');
let code = zlib.inflateSync(Buffer.from(b64, 'base64')).toString('utf8');

// --- empty-safe left rail wiring (kakei-align; z blobs unchanged) ---
const OLD_LEFT = `  if (leftExtract.lefts.length) {
    for (const { key } of leftExtract.lefts) {
      if (!af.isAfEntryKey(key)) {
        throw new Error(
          \`[[AFLeft:\${key}]] が content/links.json にありません\` +
            ' / 対処: content/links.json にキーを足す（左レールは未配線のため AFSide を使う）',
        );
      }
    }
  }
  const bodyMd = af.stripBodyAfMarkers(leftExtract.body);
  const parsed = addHeadingIds(wrapFigures(wrapTables(marked.parse(renderCards(bodyMd, a.file)))));
  assertNoRawEmphasis(parsed.html, a.file);
  const html = af.insertAdsBetweenH2s(resolveLinks(parsed.html), afPool);
  const sideAdsHtml = af.sideAdsWidget(sideKeys);
`;

const NEW_LEFT = `  const bodyMd = af.stripBodyAfMarkers(leftExtract.body);
  const parsed = addHeadingIds(wrapFigures(wrapTables(marked.parse(renderCards(bodyMd, a.file)))));
  assertNoRawEmphasis(parsed.html, a.file);
  const html = af.insertAdsBetweenH2s(resolveLinks(parsed.html), afPool);
  const sideAdsHtml = af.sideAdsWidget(sideKeys);
  const leftAdsHtml = af.leftAdsWidget
    ? af.leftAdsWidget(leftExtract.lefts)
    : af.sideAdsWidget(leftExtract.lefts);
`;

if (!code.includes(OLD_LEFT)) {
  throw new Error('build.mjs patch: left-rail block not found — z blobs may have changed');
}
code = code.replace(OLD_LEFT, NEW_LEFT);

if (!code.includes('sidebarLeft: leftAdsHtml')) {
  const n = code.replace(
    '      breadcrumb: crumbs(trail),\n      sidebar: side(',
    '      breadcrumb: crumbs(trail),\n      sidebarLeft: leftAdsHtml,\n      sidebar: side(',
  );
  if (n === code) throw new Error('build.mjs patch: article sidebarLeft insert failed');
  code = n;
}

if (!code.includes("sidebarLeft: '',") && !code.includes('sidebarLeft: "",')) {
  const n = code.replace(
    '  ogImage: ORIGIN + site.defaultOgImage,\n};',
    "  ogImage: ORIGIN + site.defaultOgImage,\n  sidebarLeft: '',\n};",
  );
  if (n === code) throw new Error('build.mjs patch: common.sidebarLeft insert failed');
  code = n;
}

const runPath = path.join(ROOT, '.build.stitched.mjs');
fs.writeFileSync(runPath, code);
await import(pathToFileURL(runPath).href + '?t=' + Date.now());
