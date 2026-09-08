// Pages hosts this project under a repository path; the private site uses /.
export function sitePath(path: string) {
  return `${process.env.NEXT_PUBLIC_BASE_PATH || ''}${path}`;
}
