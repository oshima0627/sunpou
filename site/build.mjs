/**
 * Stitch AF-wired build parts then run. Parts are plain JS (readable).
 */
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const ROOT = import.meta.dirname;
const names = ['build.part1.mjs.txt', 'build.part2.mjs.txt', 'build.part3.mjs.txt', 'build.part4.mjs.txt', 'build.part5.mjs.txt'];
const runPath = path.join(ROOT, '.build.stitched.mjs');
fs.writeFileSync(runPath, names.map((f) => fs.readFileSync(path.join(ROOT, f), 'utf8')).join(''));
await import(pathToFileURL(runPath).href + '?t=' + Date.now());
