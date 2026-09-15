import { execFileSync } from 'node:child_process';
import { resolve } from 'node:path';
import { homedir } from 'node:os';
import { synchronize } from './project-sync.mjs';

// Deliberately separate from public sync: private records never enter that checkout.
const root = resolve(process.argv[3] ?? resolve(homedir(), 'Documents/Codex/poc-private'));
try {
  const origin = execFileSync('git', ['remote', 'get-url', '--push', 'origin'], {cwd: root, encoding: 'utf8'}).trim();
  if (!['https://github.com/yspbob/interpretation-layer-poc-private.git',
        'https://github.com/yspbob/interpretation-layer-poc-private',
        'git@github.com:yspbob/interpretation-layer-poc-private.git'].includes(origin)) {
    throw new Error('Unexpected private repository remote. Nothing synchronized.');
  }
  const visibility = execFileSync('gh', ['repo', 'view', 'yspbob/interpretation-layer-poc-private',
    '--json', 'visibility', '--jq', '.visibility'], {encoding: 'utf8'}).trim();
  if (visibility !== 'PRIVATE') throw new Error('Private visibility not verified. Nothing synchronized.');
  console.log(synchronize(root, process.argv[2]));
} catch (error) {
  console.error(error.stderr?.toString().trim() || error.message);
  process.exitCode = 1;
}
