'use client';
import { useEffect, useState } from 'react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { PageLink } from '../page-link';
import { ArrowRight } from 'lucide-react';

const phaseValues: Record<string,string> = {'#phase-1':'first','#phase-2':'use','#phase-3':'interaction'};
export function PhaseRoadmap(){
  const [phase,setPhase]=useState('first');
  useEffect(()=>{const sync=()=>setPhase(phaseValues[window.location.hash]||'first');sync();window.addEventListener('hashchange',sync);return()=>window.removeEventListener('hashchange',sync)},[]);
  const selectPhase=(value:unknown)=>{const next=String(value);setPhase(next);const hash=Object.keys(phaseValues).find(key=>phaseValues[key]===next)||'#phase-1';window.history.replaceState(null,'',hash)};
  return <>
  <header className="phase-roadmap-intro"><h1>Build the first trial in three parts.</h1><p className="lead">First assess the guidance. Then test whether it helps with coding. Finally, test whether interaction adds value while the agent works.</p><p>Each phase ends with an inspectable result and a decision about the next step. The <PageLink className="text-link" href="/progress">progress page</PageLink> stays focused on the current phase.</p></header>
  <Tabs value={phase} onValueChange={selectPhase} className="phase-roadmap-tabs">
    <TabsList className="phase-options" aria-label="Choose a phase to read about">
      <TabsTrigger id="phase-1" value="first"><span>01</span><strong>Reconstruct guidance</strong><small>Our current focus</small></TabsTrigger>
      <TabsTrigger id="phase-2" value="use"><span>02</span><strong>Test its use</strong><small>After assessing the guidance</small></TabsTrigger>
      <TabsTrigger id="phase-3" value="interaction"><span>03</span><strong>Test interaction</strong><small>After testing use in coding</small></TabsTrigger>
    </TabsList>
    <TabsContent value="first" className="phase-detail-card">
      <span className="eyebrow">PHASE 1 / GUIDANCE</span><h2>Can the layer produce defensible rules?</h2>
      <p>Choose one repository and a few different kinds of decisions. Let the drafter prepare guidance from permitted evidence, then let a separate verifier check its claims.</p><p>Independently assess the draft, the accepted guide and the verifier’s decisions. Look for supported rules, omissions, incorrect claims, exceptions and uncertainty.</p>
      <div className="phase-detail-columns"><div><h3>Build now</h3><p>Controlled input packs, separate drafting and verification, independent guidance assessment, and records of evidence, decisions and preparation cost.</p></div><div><h3>The result</h3><p>A guide and an assessment we can inspect. Decide whether to test it in a coding task, repair preparation or stop.</p></div></div>
      <p className="phase-limit">This phase does not run a coding comparison. It cannot show that the guide improves code, saves time or benefits from interaction.</p>
      <div className="phase-actions"><PageLink href="/">Read the Phase 1 plan <ArrowRight size={16}/></PageLink><PageLink href="/progress">See progress to date <ArrowRight size={16}/></PageLink></div>
    </TabsContent>
    <TabsContent value="use" className="phase-detail-card">
      <span className="eyebrow">PHASE 2 / USE IN A CODING TASK</span><h2>Does the guide help an agent make a real change?</h2>
      <p>Compare two groups on the same historical tasks: Sources only, and Sources and prepared guidance. Both receive the same ordinary review checkpoints, correction opportunities and total method allowance.</p><p>The guidance is fixed before the coding tasks are revealed. Its preparation cost counts in the comparison. Independent assessment checks whether the code fulfils the task and respects the applicable rules.</p>
      <div className="phase-detail-columns"><div><h3>Add in this phase</h3><p>Isolated coding execution, ordinary reviews before and during work, checks when a plan changes, and independently qualified code assessment.</p></div><div><h3>The result</h3><p>A comparison of code quality, failures and total cost. Decide whether the guide is useful enough to investigate interaction, whether to revise the method or whether to stop.</p></div></div>
      <p className="phase-limit">A guide that reads well may still be unhelpful in practice. Phase 1 does not answer this question. If its guide or assessment has been tuned on a case, keep that history visible and do not call the later result independent confirmation.</p>
      <div className="phase-actions"><PageLink href="/trial-method#comparison">Read the comparison safeguards <ArrowRight size={16}/></PageLink></div>
    </TabsContent>
    <TabsContent value="interaction" className="phase-detail-card">
      <span className="eyebrow">PHASE 3 / INTERACTION DURING WORK</span><h2>Does consultation and checking add further value?</h2>
      <p>Add the interactive condition: the agent can consult the layer and the checker can ask it to explain how its plan or work respects the guidance. Required checks can pause work, request a correction or stop the attempt.</p><p>Run all three groups under the same settings: Sources only; Sources and prepared guidance; Sources, prepared guidance and interaction. Match review triggers, correction opportunities and budgets across them.</p>
      <div className="phase-detail-columns"><div><h3>Add in this phase</h3><p>Structured consultation, the interactive checker and an independent assessment of its interventions. Test these components for their actual roles before relying on their results.</p></div><div><h3>The result</h3><p>Evidence about whether interaction improves the work beyond a fixed guide and ordinary reviews, including unnecessary objections, failures and added cost.</p></div></div>
      <p className="phase-limit">We will not compare a new interactive group with old scores from Phase 2 and attribute the difference to interaction. All three groups need a matched comparison in this phase.</p>
      <div className="phase-actions"><PageLink href="/trial-method#during-work">Read how reviews work during execution <ArrowRight size={16}/></PageLink></div>
    </TabsContent>
  </Tabs>
  <details className="after-trial" id="what-could-follow"><summary>What could follow the first trial?</summary><p>If the first trial justifies it, a separate confirmation study will freeze the method and test fresh decision families that did not shape the guidance, agents or scoring. Its question, measures, sample size and spending limits must be fixed before examining results.</p><p>Further repositories, models, cost projections and production studies are possible later choices. Owner approval, ongoing maintenance and a dashboard for reviewing rules would each need their own evidence and participants where relevant. They are not prerequisites for this first trial.</p></details>
</>}
