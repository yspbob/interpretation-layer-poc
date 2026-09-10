import { PageLink } from './page-link';

import { ArrowUpRight, Layers3, BookOpen, Activity } from 'lucide-react';
import type { ReactNode } from 'react';
export const chapterUrl='https://yspbob.github.io/AI-Playbook/AI_Engineering_Playbook.html#4-the-interpretation-layer';
export function Shell({active,children}:{active:'experiment'|'progress',children:ReactNode}){
return <><a className="skip-link" href="#main">Skip to content</a><header className="masthead"><div className="masthead-inner"><PageLink href="/" className="brand"><span className="brand-mark"><Layers3 size={22}/></span><span><strong>Interpretation layer</strong><small>AI ENGINEERING PLAYBOOK</small></span></PageLink><a className="chapter-link" href={chapterUrl} target="_blank" rel="noreferrer">Chapter 4 <ArrowUpRight size={16}/></a></div></header><div className="nav-bar"><div className="nav-inner"><nav aria-label="Main sections"><PageLink href="/" aria-current={active==='experiment'?'page':undefined}><BookOpen size={17}/>The experiment</PageLink><PageLink href="/progress" aria-current={active==='progress'?'page':undefined}><Activity size={17}/>Progress & findings</PageLink></nav><span className="study-id">IL / POC 001</span></div></div><main id="main" className="workspace">{children}</main><footer className="site-footer"><span>AI Engineering Playbook · Interpretation layer validation</span><span>Research in progress · Updated as the study develops</span></footer></>
}
