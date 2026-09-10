'use client';
import { useEffect, useState } from 'react';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { PageLink } from '../page-link';
import { ArrowRight } from 'lucide-react';

const phaseValues: Record<string,string> = {'#phase-1':'first','#phase-2':'confirmation','#phase-3':'broader'};
export function PhaseRoadmap(){
  const [phase,setPhase]=useState('first');
  useEffect(()=>{const sync=()=>setPhase(phaseValues[window.location.hash]||'first');sync();window.addEventListener('hashchange',sync);return()=>window.removeEventListener('hashchange',sync)},[]);
  const selectPhase=(value:unknown)=>{const next=String(value);setPhase(next);const hash=Object.keys(phaseValues).find(key=>phaseValues[key]===next)||'#phase-1';window.history.replaceState(null,'',hash)};
  return <>
  <header className="phase-roadmap-intro"><h1>A first trial before a wider study.</h1><p className="lead">Each phase answers a different question. We will finish and assess the current work before deciding whether the next phase is justified.</p><p>This page explains the sequence. The <PageLink className="text-link" href="/progress">progress view</PageLink> records what has actually happened in Phase 1.</p></header>
  <Tabs value={phase} onValueChange={selectPhase} className="phase-roadmap-tabs">
    <TabsList className="phase-options" aria-label="Choose a phase to read about">
      <TabsTrigger id="phase-1" value="first"><span>01</span><strong>A credible first trial</strong><small>Our current focus</small></TabsTrigger>
      <TabsTrigger id="phase-2" value="confirmation"><span>02</span><strong>Test on fresh cases</strong><small>Decide after the first trial</small></TabsTrigger>
      <TabsTrigger id="phase-3" value="broader"><span>03</span><strong>Investigate broader use</strong><small>Only where evidence justifies it</small></TabsTrigger>
    </TabsList>
    <TabsContent value="first" className="phase-detail-card">
      <span className="eyebrow">PHASE 1 / THE FIRST TRIAL</span><h2>Can we test the layer credibly on a small set of real tasks?</h2>
      <p>Use one repository and a few different kinds of project decisions. Compare the same tasks with sources alone, with prepared guidance, and with guidance plus interaction.</p>
      <p>Keep the controls that make the comparison trustworthy. Every agent must receive only its permitted inputs. Reviews and budgets must be matched, and the results need independent assessment against justified evidence.</p>
      <div className="phase-detail-columns"><div><h3>What this phase produces</h3><p>An inspectable trial report showing guidance, code changes, review decisions, failures and costs. It should tell us whether the procedure works and what needs changing.</p></div><div><h3>The decision at the end</h3><p>Proceed, repair the procedure, narrow the question or stop. A favourable result is not required to learn something useful.</p></div></div>
      <p className="phase-limit">This is a feasibility trial. A small set of tasks cannot establish that the layer helps across software development or is ready for production.</p>
      <div className="phase-actions"><PageLink href="/">Read the Phase 1 plan <ArrowRight size={16}/></PageLink><PageLink href="/progress">See progress to date <ArrowRight size={16}/></PageLink></div>
    </TabsContent>
    <TabsContent value="confirmation" className="phase-detail-card">
      <span className="eyebrow">PHASE 2 / INDEPENDENT CONFIRMATION</span><h2>Does the result hold on cases that did not shape the method?</h2>
      <p>The first trial will help us refine the procedure. If we proceed, a separate study will test it on fresh decision families that were not used to tune the agents, rules or assessment.</p>
      <p>Before that study begins, we will fix the question, measures, worthwhile improvement, sample size and cost limits. The results will include uncertainty, unsuccessful attempts and any limits on what we can conclude.</p>
      <div className="phase-detail-columns"><div><h3>What belongs here</h3><p>A justified confirmation sample and a frozen method. More detailed estimates of the return from reuse and a second budget level may be included if they answer the selected question and funding permits.</p></div><div><h3>The decision at the end</h3><p>Decide what the evidence supports changing in Chapter 4. A negative or inconclusive result may call for revising the proposal or stopping further work.</p></div></div>
      <p className="phase-limit">This phase need not cover all four repositories. Its scope must support its specific claim. It becomes an execution plan only after the first trial has been assessed.</p>
    </TabsContent>
    <TabsContent value="broader" className="phase-detail-card">
      <span className="eyebrow">PHASE 3 / POSSIBLE EXTENSIONS</span><h2>Where would further evidence change a practical decision?</h2>
      <p>Later work could examine another repository, another model or a different engineering setting. We would choose the next question from what the earlier results leave unresolved.</p>
      <p>Production questions need their own studies. Examples include obtaining owner approval, keeping guidance current and helping a human decide which rules to revise. Those studies may need participants or expertise that this technical POC does not have.</p>
      <div className="phase-detail-columns"><div><h3>Possible technical extensions</h3><p>Broader repository or model coverage and experimental execution on another qualified machine. Each extension needs the controls and evidence appropriate to its scope.</p></div><div><h3>Possible production studies</h3><p>Owner review, maintenance and a dashboard showing the evidence and cost of guidance. These remain ideas for investigation, not promised features.</p></div></div>
      <p className="phase-limit">This is a set of possible directions. It is not a backlog that must be completed before we can learn from Phase 1.</p>
    </TabsContent>
  </Tabs>
</>}
