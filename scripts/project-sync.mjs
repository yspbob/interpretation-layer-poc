import { execFileSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

// No shell interpolation, automatic staging, resets, stashes or force pushes.
export function synchronize(root, action) {
  const git = (...args) => execFileSync('git', args, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  if (!['start', 'publish'].includes(action)) throw new Error('Use start or publish.');
  if (git('branch', '--show-current') !== 'main') throw new Error('Use the saved main checkout; integrate other branches explicitly.');
  if (git('status', '--porcelain')) throw new Error('Uncommitted work exists. Preserve and review it before synchronizing.');
  git('fetch', 'origin', 'main');
  if (action === 'start') {
    git('merge', '--ff-only', 'origin/main');
    const ahead = Number(git('rev-list', '--count', 'origin/main..HEAD'));
    return ahead ? `Local work includes ${ahead} unpublished commit(s). Inspect them before continuing.` : 'Latest saved project retrieved.';
  }
  if (Number(git('rev-list', '--count', 'HEAD..origin/main'))) {
    throw new Error('GitHub has work missing locally. Reconcile before publishing; nothing was overwritten.');
  }
  git('push', 'origin', 'HEAD:refs/heads/main');
  const remote = git('ls-remote', 'origin', 'refs/heads/main').split(/\s+/)[0];
  const local = git('rev-parse', 'HEAD');
  if (remote !== local) throw new Error('Remote changed during verification. Fetch and inspect before claiming synchronization.');
  return `Saved to GitHub: ${local}`;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
    const origin = execFileSync('git', ['remote', 'get-url', '--push', 'origin'], { cwd: root, encoding: 'utf8' }).trim();
    if (!['https://github.com/yspbob/interpretation-layer-poc.git', 'https://github.com/yspbob/interpretation-layer-poc', 'git@github.com:yspbob/interpretation-layer-poc.git'].includes(origin)) {
      throw new Error('Unexpected POC remote. Inspect its configuration before syncing.');
    }
    console.log(synchronize(root, process.argv[2]));
  } catch (error) {
    console.error(error.stderr?.toString().trim() || error.message);
    process.exitCode = 1;
  }
}
