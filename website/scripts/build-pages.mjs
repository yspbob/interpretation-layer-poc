Object.assign(process.env, { DEPLOY_TARGET: 'github-pages', NEXT_PUBLIC_BASE_PATH: '/interpretation-layer-poc', NEXT_PUBLIC_SITE_URL: 'https://yspbob.github.io/interpretation-layer-poc/' });
process.argv = [process.execPath, 'vinext', 'build'];
// Let native build handles close naturally on Windows. Preserve the CLI's
// requested exit status; calling process.exit while they close asserts in libuv.
process.exit = (code = 0) => { process.exitCode = code; };
await import('../node_modules/vinext/dist/cli.js');
