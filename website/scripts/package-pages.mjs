import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync, existsSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const source = join(root, 'dist/client');
const output = join(root, '.pages-output');
if (dirname(output) !== root || !output.endsWith('.pages-output')) throw new Error('Unsafe staging directory');
const routes = ['progress', 'phases'];
for (const file of ['index.html', ...routes.map(route => `${route}.html`), 'interpretation-layer-poc/_next']) {
  if (!existsSync(join(source, file))) throw new Error(`Missing static export: ${file}`);
}
// This exact project-owned staging directory contains generated files only.
rmSync(output, { recursive: true, force: true });
mkdirSync(output, { recursive: true });
cpSync(join(source, 'interpretation-layer-poc/_next'), join(output, '_next'), { recursive: true });
cpSync(join(source, 'evidence'), join(output, 'evidence'), { recursive: true });
for (const file of ['index.html', 'index.rsc', '404.html', 'favicon.svg']) {
  if (existsSync(join(source, file))) cpSync(join(source, file), join(output, file));
}
for (const route of routes) {
  mkdirSync(join(output, route), { recursive: true });
  cpSync(join(source, `${route}.html`), join(output, route, 'index.html'));
  if (existsSync(join(source, `${route}.rsc`))) cpSync(join(source, `${route}.rsc`), join(output, route, 'index.rsc'));
}
writeFileSync(join(output, '.nojekyll'), '');
for (const page of ['index.html', ...routes.map(route => `${route}/index.html`)]) {
  const html = readFileSync(join(output, page), 'utf8');
  for (const match of html.matchAll(/(?:href|src)="(\/[^"#?]*)/g)) {
    const url = match[1];
    if (!url.startsWith('/interpretation-layer-poc/')) throw new Error(`Unprefixed URL: ${url}`);
    const relative = decodeURIComponent(url.slice('/interpretation-layer-poc/'.length));
    if (!existsSync(join(output, relative))) throw new Error(`Broken local URL: ${url}`);
  }
}
console.log('GitHub Pages package ready: plan, progress, roadmap and referenced local assets verified.');
