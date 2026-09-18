/**
 * Entry: stitch build.body.*.txt then run (MCP push size limit workaround).
 * Logical source = build.body.1.txt + build.body.2.txt (= former monolithic build.mjs).
 * Stitched file is written next to this entry so import.meta.dirname stays site/.
 */
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const ROOT = import.meta.dirname;
const parts = ['build.body.1.txt', 'build.body.2.txt'].map((f) =>
  fs.readFileSync(path.join(ROOT, f), 'utf8'),
);
const runPath = path.join(ROOT, '.build.stitched.mjs');
fs.writeFileSync(runPath, parts.join(''));
await import(pathToFileURL(runPath).href + '?t=' + Date.now());
