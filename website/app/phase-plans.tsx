'use client';
import { useEffect, useState, type ReactNode } from 'react';
import { PhaseLine } from './phase-line';
import { PageLink } from './page-link';
export function PhasePlans({guidance,use,interaction,reference}:{guidance:ReactNode,use:ReactNode,interaction:ReactNode,reference:ReactNode}){
  const [selected,setSelected]=useState(1);
  useEffect(()=>{
    const sync=()=>{
      const hash=decodeURIComponent(window.location.hash.slice(1));
      if(!hash){setSelected(1);return;}
      const target=document.getElementById(hash);
      const direct=/^phase-([123])$/.exec(hash);
      const owner=target?.closest<HTMLElement>('[data-phase]');
      setSelected(direct?Number(direct[1]):Number(owner?.dataset.phase||1));
      let parent=target?.parentElement;
      while(parent){if(parent instanceof HTMLDetailsElement)parent.open=true;parent=parent.parentElement;}
      requestAnimationFrame(()=>requestAnimationFrame(()=>target?.scrollIntoView({block:'start'})));
    };
    sync();window.addEventListener('hashchange',sync);window.addEventListener('popstate',sync);
    return()=>{window.removeEventListener('hashchange',sync);window.removeEventListener('popstate',sync);};
  },[]);
  const choose=(phase:number)=>{setSelected(phase);window.history.pushState(null,'',`#phase-${phase}`);};
  return <section className="phase-reader" id="phase-plans" aria-label="The plan by phase">
    <PhaseLine selected={selected} onSelect={choose}/>
    {[guidance,use,interaction].map((content,index)=><div key={index} role="tabpanel" id={`phase-panel-${index+1}`} aria-labelledby={`phase-${index+1}`} hidden={selected!==index+1} data-phase={index+1} className="phase-reading-panel" tabIndex={0}>{content}</div>)}
    <details className="method-reference" id="full-method"><summary>Explore the comparison, technical setup and production proposal</summary><p className="reference-intro">The phase plan above explains what we will do next. Open this reference when you want to examine a particular part in more detail. Coding comparisons belong to Phases 2 and 3; they are not prerequisites for testing guidance in Phase 1.</p>{reference}</details>
    <div className="route-footer"><span>The plan describes what we intend to do. Progress records what has happened.</span><PageLink href="/progress">Progress &amp; findings →</PageLink></div>
  </section>
}
