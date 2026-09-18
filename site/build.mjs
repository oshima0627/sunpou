/**
 * Entry: stitch build.body.*.txt then run (MCP push size limit workaround).
 * Logical source = concatenated build.body.N.txt (= AF-wired build.mjs).
 */
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const ROOT = import.meta.dirname;
const names = ['build.body.1.txt', 'build.body.2.txt', 'build.body.3.txt', 'build.body.4.txt'];
const parts = names.map((f) => fs.readFileSync(path.join(ROOT, f), 'utf8'));
const runPath = path.join(ROOT, '.build.stitched.mjs');
fs.writeFileSync(runPath, parts.join(''));
await import(pathToFileURL(runPath).href + '?t=' + Date.now());
