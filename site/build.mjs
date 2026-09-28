/**
 * Inflate AF-wired build from build.z*.txt (zlib+base64) then run.
 * Patches: prefer bannerHtmlSide for right rail; wire left rail (sidebarLeft).
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

const runPath = path.join(ROOT, '.build.stitched.mjs');
fs.writeFileSync(runPath, code);
await import(pathToFileURL(runPath).href + '?t=' + Date.now());
