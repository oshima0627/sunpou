/**
 * Inflate AF-wired build from build.z*.txt (zlib+base64) then run.
 * Patches sidebar pool to prefer bannerHtmlSide when present.
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { pathToFileURL } from 'node:url';

const ROOT = import.meta.dirname;
const names = ['build.z1.txt', 'build.z2.txt', 'build.z3.txt', 'build.z4.txt'];
const b64 = names.map((f) => fs.readFileSync(path.join(ROOT, f), 'utf8').trim()).join('');
let code = zlib.inflateSync(Buffer.from(b64, 'base64')).toString('utf8');

const OLD_SIDE = `  let sideKeys = sideExtract.sides;
  if (!sideKeys.length && site.affiliateEnabled) {
    const cat = af.categoryAfPool(a.category);
    if (cat.length) sideKeys = [{ key: cat[0], label: undefined }];
  }
`;

const NEW_SIDE = `  let sideKeys = sideExtract.sides;
  if (!sideKeys.length && site.affiliateEnabled) {
    sideKeys = af.pickCategorySideKeys
      ? af.pickCategorySideKeys(a.category)
      : (() => {
          const cat = af.categoryAfPool(a.category);
          return cat.length ? [{ key: cat[0], label: undefined }] : [];
        })();
  }
`;

if (!code.includes(OLD_SIDE)) {
  throw new Error('build.mjs patch: sideKeys block not found — z blobs may have changed');
}
code = code.replace(OLD_SIDE, NEW_SIDE);

const runPath = path.join(ROOT, '.build.stitched.mjs');
fs.writeFileSync(runPath, code);
await import(pathToFileURL(runPath).href + '?t=' + Date.now());
