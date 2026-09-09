import type { Metadata } from 'next';
import { Source_Sans_3, Source_Serif_4 } from 'next/font/google';
import './globals.css';
import { sitePath } from './site-path';

const sourceSans = Source_Sans_3({
  variable: '--font-source-sans',
  subsets: ['latin'],
});

const sourceSerif = Source_Serif_4({
  variable: '--font-source-serif',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: {default:'Interpretation Layer | Playbook Validation', template:'%s | Interpretation Layer'},
  description: 'Testing whether the AI Engineering Playbook’s interpretation layer earns its place. Explore the experiment, evidence, progress and limits of the study.',
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'https://yspbob.github.io/interpretation-layer-poc/'),
  icons: {icon:sitePath('/favicon.svg')},
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${sourceSans.variable} ${sourceSerif.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
