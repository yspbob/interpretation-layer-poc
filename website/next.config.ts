import type { NextConfig } from 'next';

const nextConfig: NextConfig = process.env.DEPLOY_TARGET === 'github-pages'
  ? { output: 'export', assetPrefix: '/interpretation-layer-poc' }
  : {};

export default nextConfig;
