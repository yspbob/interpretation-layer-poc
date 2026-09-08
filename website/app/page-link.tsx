import type { ComponentPropsWithoutRef } from 'react';
import { sitePath } from './site-path';

// Use document navigation: Vinext's client Link handler throws in the hosted
// build before it changes routes. These read-only views support full page loads.
export function PageLink({children, href, ...props}: ComponentPropsWithoutRef<'a'>) {
  const target = href?.startsWith('/') && !href.startsWith('//') ? sitePath(href.endsWith('/') ? href : `${href}/`) : href;
  return <a {...props} href={target}>{children}</a>;
}
