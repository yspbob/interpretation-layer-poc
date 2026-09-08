import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const check = process.argv.includes('--check');
const pairs = [
  ['working_plan_2026-09-05.md', 'working-poc-plan.md'],
  ['plan_changes_2026-09-05.md', 'plan-changes.md'],
];
for (const [source, download] of pairs) {
  const content = readFileSync(resolve(root, 'preregistration/plan', source), 'utf8').replace(/\r\n/g, '\n');
  for (const folder of ['website/public/evidence', 'docs/evidence']) {
    const target = resolve(root, folder, download);
    if (check) {
      if (readFileSync(target, 'utf8').replace(/\r\n/g, '\n') !== content) throw new Error(`Plan copy drift: ${target}`);
    } else writeFileSync(target, content);
  }
}
console.log(check ? 'Plan and change register copies agree.' : 'Updated plan and change register downloads.');
