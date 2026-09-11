import type { KeyboardEvent } from 'react';
const stations = ['Reconstruct guidance','Test its use','Test interaction'];
export function PhaseLine({selected,onSelect}:{selected:number,onSelect:(phase:number)=>void}){
  const onKey=(event:KeyboardEvent<HTMLButtonElement>,index:number)=>{
    let next=index;
    if(event.key==='ArrowRight')next=(index+1)%3;
    else if(event.key==='ArrowLeft')next=(index+2)%3;
    else if(event.key==='Home')next=0;
    else if(event.key==='End')next=2;
    else return;
    event.preventDefault();onSelect(next+1);document.getElementById(`phase-${next+1}`)?.focus();
  };
  return <div className="phase-line"><p className="phase-line-caption">Explore the plan for each phase <span>Current work: Phase 1</span></p><ol role="tablist" aria-label="First trial phase plans">{stations.map((label,index)=><li key={label} role="presentation" className={`phase-stop ${index===0?'current-stop':''} ${selected===index+1?'selected-stop':''}`}><button type="button" role="tab" aria-label={`Phase ${index+1}: ${label}${index===0?", current work":""}`} id={`phase-${index+1}`} aria-controls={`phase-panel-${index+1}`} aria-selected={selected===index+1} tabIndex={selected===index+1?0:-1} onClick={()=>onSelect(index+1)} onKeyDown={event=>onKey(event,index)}><span className="station-dot" aria-hidden="true"/><span className="station-label"><span>0{index+1}{index===0?' · CURRENT':''}</span><strong>{label}</strong></span></button></li>)}</ol></div>
}
