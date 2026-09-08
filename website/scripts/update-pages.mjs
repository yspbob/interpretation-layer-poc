import { cpSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const website = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const built = resolve(website, '.pages-output');
const docs = resolve(website, '../docs');
if (!existsSync(resolve(built, 'index.html')) || !existsSync(resolve(built, 'progress/index.html'))) throw new Error('Run npm run build:pages first');
cpSync(built, docs, { recursive: true });
console.log('Updated docs/ from the validated static build; history preserved.');
