import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { synchronize } from './project-sync.mjs';

test('two clones preserve dirty work, transfer commits and refuse divergence and rejected pushes', () => {
  const scratch = resolve(dirname(fileURLToPath(import.meta.url)), '../.sync-tests');
  mkdirSync(scratch, { recursive: true });
  const run = mkdtempSync(join(scratch, 'two-machines-'));
  const git = (cwd, ...args) => execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  const remote = join(run, 'remote.git');
  const home = join(run, 'home');
  const laptop = join(run, 'laptop');
  git(run, 'init', '--bare', '--initial-branch=main', remote);
  git(run, 'clone', remote, home);
  const identity = (cwd) => {
    git(cwd, 'config', 'user.name', 'Sync test');
    git(cwd, 'config', 'user.email', 'sync-test@example.invalid');
    git(cwd, 'config', 'commit.gpgsign', 'false');
  };
  identity(home);
  const commit = (cwd, name) => {
    writeFileSync(join(cwd, name), name);
    git(cwd, 'add', '--', name);
    git(cwd, 'commit', '-m', name);
  };
  commit(home, 'initial.txt');
  git(home, 'push', '-u', 'origin', 'main');
  assert.match(synchronize(home, 'publish'), /Saved to GitHub/);
  git(run, 'clone', remote, laptop);
  identity(laptop);
  commit(home, 'finished-work.txt');
  synchronize(home, 'publish');
  assert.match(synchronize(laptop, 'start'), /retrieved/);
  assert.equal(git(laptop, 'rev-parse', 'HEAD'), git(home, 'rev-parse', 'HEAD'));
  writeFileSync(join(laptop, 'unfinished.txt'), 'keep me');
  assert.throws(() => synchronize(laptop, 'start'), /Uncommitted/);
  assert.throws(() => synchronize(laptop, 'publish'), /Uncommitted/);
  git(laptop, 'add', '--', 'unfinished.txt');
  git(laptop, 'commit', '-m', 'laptop work');
  assert.match(synchronize(laptop, 'start'), /unpublished/);
  commit(home, 'home-work.txt');
  synchronize(home, 'publish');
  const laptopHead = git(laptop, 'rev-parse', 'HEAD');
  assert.throws(() => synchronize(laptop, 'start'));
  assert.throws(() => synchronize(laptop, 'publish'), /missing locally/);
  assert.equal(git(laptop, 'rev-parse', 'HEAD'), laptopHead);
  commit(home, 'not-yet-published.txt');
  git(remote, 'config', 'receive.denyNonFastForwards', 'true');
  // A rejecting receive hook simulates a server-side failure after fetch succeeds.
  writeFileSync(join(remote, 'hooks/pre-receive'), '#!/bin/sh\nexit 1\n', { mode: 0o755 });
  assert.throws(() => synchronize(home, 'publish'));
  assert.notEqual(git(remote, 'rev-parse', 'main'), git(home, 'rev-parse', 'HEAD'));
});
