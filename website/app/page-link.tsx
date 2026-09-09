import type { ComponentPropsWithoutRef } from 'react';
import { sitePath } from './site-path';

// Use document navigation: Vinext's client Link handler throws in the hosted
// build before it changes routes. These read-only views support full page loads.
export function PageLink({children, href, ...props}: ComponentPropsWithoutRef<'a'>) {
  let target = href;
  if (href?.startsWith('/') && !href.startsWith('//')) {
    const boundary = href.search(/[?#]/);
    const path = boundary < 0 ? href : href.slice(0, boundary);
    const suffix = boundary < 0 ? '' : href.slice(boundary);
    target = sitePath(`${path.endsWith('/') ? path : `${path}/`}${suffix}`);
  }
  return <a {...props} href={target}>{children}</a>;
}
