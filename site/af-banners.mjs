/**
 * Inflate af-banners from af-banners.z*.txt (zlib+base64).
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { pathToFileURL } from 'node:url';

const ROOT = import.meta.dirname;
const names = ["af-banners.z1.txt", "af-banners.z2.txt"];
const b64 = names.map((f) => fs.readFileSync(path.join(ROOT, f), 'utf8').trim()).join('');
const code = zlib.inflateSync(Buffer.from(b64, 'base64')).toString('utf8');
const runPath = path.join(ROOT, '.af-banners.inflated.mjs');
fs.writeFileSync(runPath, code);
const mod = await import(pathToFileURL(runPath).href + '?t=' + Date.now());
export const createAfHelpers = mod.createAfHelpers;
