import { PageLink } from './page-link';

import { ArrowDown, ArrowRight, CornerUpLeft, RefreshCw } from 'lucide-react';
import { Shell, chapterUrl } from './ui';
import { DetailGroup, Disclosure, Examples } from './details';
import { ExperimentDetails } from './experiment-details';
import { TechnicalSetup } from './technical-setup';
import { Economics, BudgetSelection } from './economics';
import { ProductionDifference } from './production-difference';

export const dynamic = 'force-static';
export default function Experiment(){return <Shell active="experiment">
  <div className="page-heading"><span className="eyebrow">AI ENGINEERING PLAYBOOK / CHAPTER 4</span><span className="reading-time">THE CURRENT PHASE PLAN</span></div>
  <section className="intro">
    <div>
      <h1>Start with a small, credible trial.</h1>
      <p className="lead">The first phase will test the interpretation layer on a few real tasks from one repository. We want to find out whether the procedure works, whether its guidance is defensible and what the comparison can tell us.</p>
      <p className="intro-explanation">The playbook’s <strong>interpretation layer</strong> turns project evidence into guidance and helps agents check their work against it. We will test those technical steps here. A small first trial will provide preliminary evidence, not a conclusion about every project or approval from an owner.</p>
      <p className="chapter-context">The full proposal is in <a href={chapterUrl} target="_blank" rel="noreferrer">Chapter 4: The interpretation layer</a> of the public AI Engineering Playbook.</p>
      <div className="experiment-jumps"><a className="text-link intro-jump" href="#example">What the layer provides <ArrowDown size={16}/></a><a className="text-link intro-jump" href="#comparison">The comparison <ArrowDown size={16}/></a><a className="text-link intro-jump" href="#method">The method <ArrowDown size={16}/></a><a className="text-link intro-jump" href="#technical-setup">Technical setup <ArrowDown size={16}/></a></div>
    </div>
    <aside className="hypothesis">
      <span className="eyebrow">WHY TEST THIS?</span>
      <p>Does prepared guidance help beyond the sources and ordinary review? Does structured consultation add a further benefit?</p>
      <div className="hypothesis-explanation">A capable agent may already work out the right approach from the sources. Preparing guidance and consulting it takes time and money. The experiment tests whether these steps prevent enough mistakes to justify the effort.</div>
      <div className="hypothesis-foot"><span className="signal-dot"/>Phase 1 plan · Actual work and results are recorded separately.</div>
    </aside>
  </section>

  <section className="phase-scope" aria-labelledby="phase-scope-title">
    <div><span className="eyebrow">THE BOUNDARY OF THIS PHASE</span><h2 id="phase-scope-title">Enough to learn from the first comparison.</h2><p>Use one repository, a few distinct decision families and one qualified execution machine. Keep all three comparison groups, with fixed model settings for each required role.</p></div>
    <div><h3>What must be trustworthy</h3><p>The evidence, permitted inputs, review checkpoints, budgets and independent assessment. Failures and unfinished work stay in the record.</p><h3>What this phase delivers</h3><p>A report of what ran, what worked, what failed and what it cost. Then decide whether to proceed, repair the procedure or stop.</p></div>
    <div className="phase-scope-links"><PageLink href="/progress">See progress to date <ArrowRight size={16}/></PageLink><PageLink href="/phases">Read the wider roadmap <ArrowRight size={16}/></PageLink></div>
  </section>

  <section id="example" className="section-block">
    <div className="section-heading"><span className="section-no">01</span><div><span className="eyebrow">GUIDANCE FOR A SPECIFIC TASK</span><h2>What would the layer tell an agent?</h2></div></div>
    <p className="section-intro">When an agent is given a task, it needs to understand how that task fits into the existing system. The layer should identify code the agent can reuse, explain which decisions constrain the change, and show where exceptions apply. Each answer should show its evidence. It should also make clear whether it describes an approved decision, a pattern observed in the code or a question still awaiting review.</p>
    <p className="section-intro">The agent can consult the layer about a proposed approach: whether to extend an existing component, where new code belongs, or whether a change would cross a boundary the project has chosen to preserve. The answer should explain what is allowed and why. If the evidence cannot settle an important decision, the layer should say so. In production, that question would go to an owner.</p><p className="section-intro">The agent uses these answers to write its plan. The plan is then checked against the relevant decisions before work proceeds.</p>
    <DetailGroup><Disclosure id="guidance-examples" title="See examples of the guidance an agent could receive" summary="How this applies to change history, conflicting documentation and questions the code cannot answer.">
      <p>NetBox is an application with public source code used to document network infrastructure, including devices and their connections. It is one of the four projects in this study.</p>
      <p>In the first example, an agent is asked to write code that renames a device in NetBox. The layer would draw its attention to a related requirement: the change history must preserve the old name as well as the new one. It would also explain when NetBox already handles that requirement, so the agent can choose the right approach.</p>
      <Examples/>
    </Disclosure></DetailGroup>
  </section>

  <section className="section-block">
    <div className="section-heading"><span className="section-no">02</span><div><span className="eyebrow">THE IDEA BEHIND THE LAYER</span><h2>Turn project evidence into guidance for later work</h2></div></div>
    <DetailGroup><Disclosure id="production-cycles" title="Read the full playbook cycle and the POC’s simplifications" summary="Preparing guidance, owner approval, repeated use and later maintenance.">
    <p className="section-intro section-intro-wide">Before agents can use the interpretation layer, it needs to build an initial understanding of the system. It examines the code, documentation and recorded decisions, then drafts guidance explaining which rules apply and why. In production, that guidance is checked and sent to the responsible owner for approval.</p><p className="section-intro section-intro-wide">Once approved, the guidance can help agents with many coding tasks. They consult the relevant rules when planning a change and check their work against them as they proceed. The layer does not reconstruct the rules each time a new task begins.</p><p className="section-intro section-intro-wide">The guidance also needs to stay current. Changes to the system may reveal a new rule, an exception or a reason to revise existing guidance. Those findings go through review before the guidance changes.</p><p className="section-intro section-intro-wide">Our POC tests the initial preparation and repeated use of guidance. It has no project owner to approve the rules, and it keeps the guidance unchanged during each comparison. Ongoing maintenance is outside this pilot.</p>
    <div className="guidance-cycles" id="guidance-cycles">
      <section className="guidance-cycle" aria-labelledby="preparation-cycle-title">
        <span className="eyebrow">DRAFTING &amp; APPROVAL CYCLE</span>
        <h3 id="preparation-cycle-title">Establish and maintain the guidance</h3>
        <ol className="cycle-steps">
          <li><h4>Find the evidence</h4><p>Read the relevant code, documentation and recorded decisions, including exceptions and conflicting examples.</p></li>
          <li><h4>Draft and verify the guidance</h4><p>Explain where each proposed rule applies and what evidence supports it. Check for contradictions before sending it for owner review.</p></li>
          <li><h4>Review and release a version</h4><p>In production, the responsible owner approves the proposed guidance, rejects it or asks for changes. Only approved decisions are released as authoritative guidance.</p></li>
        </ol>
        <p className="cycle-repeat"><RefreshCw size={17} aria-hidden="true"/><span>Review can send a draft back for revision before a version is released.</span></p>
        <p className="cycle-timing"><strong>In this POC:</strong> there is no responsible project owner. The verifier checks whether the evidence supports each claim, and accepted claims form the guide. This does not make them rules approved by an owner. The guide is prepared before the coding tasks and stays unchanged during their comparison.</p>
      </section>
      <div className="guidance-connection">
        <ArrowRight className="guidance-connection-arrow" size={28} aria-hidden="true"/>
        <strong>A released guidance version</strong>
        <p>The guide explains where each rule applies and includes its evidence and exceptions. Production adds owner approval. This POC checks the evidence.</p>
        <span>The same version can support many tasks.</span>
      </div>
      <section className="guidance-cycle guidance-cycle-use" aria-labelledby="usage-cycle-title">
        <span className="eyebrow">USAGE CYCLE</span>
        <h3 id="usage-cycle-title">Apply the guidance to each task</h3>
        <ol className="cycle-steps">
          <li><h4>Consult and plan</h4><p>Retrieve the relevant guidance. Identify what can be reused, what constrains the change and which exceptions may apply.</p></li>
          <li><h4>Check the plan</h4><p>Review the proposed approach against the guidance and resolve blocking issues before editing.</p></li>
          <li><h4>Implement and check during work</h4><p>The agent can ask further questions. At defined checkpoints and when the approach changes, the checker reviews the work so far and can require an explanation or correction before it continues.</p></li>
          <li><h4>Check the resulting work</h4><p>Assess the change against the relevant decisions and task requirements. Record objections and unresolved questions.</p></li>
        </ol>
        <p className="cycle-repeat"><RefreshCw size={17} aria-hidden="true"/><span>Objections can send the plan or code back for revision, or stop the attempt.</span></p>
        <p className="cycle-timing"><strong>In this POC:</strong> all groups receive review at the required checkpoints. The interactive group also receives structured questions about the guidance. If the task needs a decision that the evidence cannot settle, the attempt stops. No project owner is available to answer it. These are planned checks, not continuous monitoring of every action.</p>
      </section>
      <div className="guidance-feedback"><CornerUpLeft size={21} aria-hidden="true"/><p><strong>New evidence can prompt a guidance review.</strong> Work may expose an outdated rule, a conflict or an unrecorded exception. In production, that evidence goes back for review. It cannot change an approved decision by itself. Reviews could run nightly, with earlier review of consequential changes. That cadence is a proposal. This POC records the issue but keeps the guide unchanged.</p></div>
    </div>
    </Disclosure></DetailGroup>
    <div className="scope-note" id="pilot-scope"><span>What this POC can test</span><div><p>Phase 1 selects changes previously made in one public project. Each selected task needs requirements supported by project records and tests that can be repeated. This lets the technical steps be examined without asking maintainers to approve new rules or take part in each run.</p><p><strong>Prior familiarity remains a limitation.</strong> A model may already know the public code. Using the same models, tasks and budgets makes the methods comparable, but cannot prove that an agent worked out a rule solely from the files it received. Separate familiarity checks will look for recalled project details and historical fixes before the pilot.</p><p>The results will concern the technical steps. They cannot show that a project owner approves the guidance or that a maintenance process keeps it current. Later iterations could involve project owners and examine maintenance if these are needed to answer the remaining questions.</p><p>The diagram above describes the full proposal. This pilot prepares a guide for a defined code version and set of permitted sources, then reuses it across the associated tasks. It is not one guide for every repository or historical version. Results from final evaluation cannot be used to repair it during that comparison.</p></div></div>
    <DetailGroup><Disclosure id="production-scope" title="Where does this POC differ from production?" summary="Owner approval, repeated use, maintenance and the way success is measured.">
      <p>The experiment tests a limited part of the production proposal. It checks whether guidance has evidence behind it and helps with historical tasks. No project owner certifies that guidance. Guidance remains fixed during each comparison, so the pilot does not test whether updates keep it correct over time.</p>
      <p>Production would apply the layer to current engineering work. This POC instead repeats the same task under three conditions, with restricted inputs, matched review rules and independent assessment after each attempt. These controls help us compare the methods fairly. A production team would choose a workflow suited to its own work.</p>
      <p>The first trial uses a public project and may encounter knowledge a model already has. Familiarity probes can find signs of recall, but cannot certify that a project is unseen. Its cost analysis estimates the return from reusing a fixed guide, not the full economics of a production service.</p>
      <p>The relevant sections below explain each difference where it affects this trial. Broader studies have their own place on the roadmap. <PageLink className="text-link" href="/progress">Progress &amp; findings</PageLink> shows which parts are built or tested.</p>
    </Disclosure></DetailGroup>
    <p className="caption">In this POC, all three groups receive review. The <a className="text-link" href="#during-work">detailed method</a> explains the checks before editing, during implementation and at final submission.</p>
  </section>

  <section className="section-block" id="comparison">
    <div className="section-heading"><span className="section-no">03</span><div><span className="eyebrow">THE PROPOSED COMPARISON</span><h2>Separate the value of guidance from the value of checking its use</h2></div></div>
    <p className="section-intro">We will ask agents to make the same change with three different kinds of help. Comparing the first two groups shows whether a prepared guide helps. Comparing the last two shows whether consulting the layer and answering its questions adds anything further.</p>
    <div className="comparison comparison-three">
      <div><span className="eyebrow">WITHOUT THE EXTRA LAYER</span><h3>Sources only</h3><p>It searches the code and available documentation, works out what matters for the task, and makes the change. This represents a capable agent doing the work directly.</p></div>
      <div><span className="eyebrow">WITH PREPARED GUIDANCE</span><h3>Sources and prepared guidance</h3><p>The layer has examined the same sources and written guidance before the task begins. The agent receives that guidance and works with it, with ordinary review but without the layer’s structured questions.</p></div>
      <div><span className="eyebrow">WITH GUIDANCE AND INTERACTION</span><h3>Sources, prepared guidance and interaction</h3><p>The agent receives the same guidance, consults the layer about its plan and responds to checks at agreed points. The run records whether those interactions prevent mistakes or add unnecessary work.</p></div>
    </div>
    <div className="review-comparison" id="review-comparison">
      <h3>Every group gets a review</h3>
      <p>Every group has its plan reviewed before editing, receives checks during work and submits its final code for review. The rules for when a review is required and how many corrections are allowed are the same for all three.</p><p>Different approaches may trigger different numbers of checks during implementation. For example, a substantial change of plan requires another review.</p><p>The groups differ in the help available throughout planning, implementation and review. The table shows how that difference applies to the reviewer:</p>
      <table className="review-comparison-table">
        <caption className="sr-only">What the reviewer checks in each group</caption>
        <thead><tr><th scope="col">Group</th><th scope="col">What the reviewer checks</th></tr></thead>
        <tbody>
          <tr><th scope="row">Sources only</th><td>The plan and code against the available sources, including any applicable AGENTS.md instructions present at the starting revision.</td></tr>
          <tr><th scope="row">Sources and prepared guidance</th><td>The reviewer checks the plan and code against the sources and the prepared guidance.</td></tr>
          <tr><th scope="row">Sources, prepared guidance and interaction</th><td>The reviewer has the same sources and guide. The layer also asks the agent which rules apply and how its proposed action follows them. An agent claiming an exception must explain why it is justified.</td></tr>
        </tbody>
      </table>
      <p>This comparison tests whether the extra questions improve the result when ordinary review and guidance are already available.</p><p>Each group gets the same total spending allowance. For the group using sources alone, it pays for coding, tools and review. For the two groups using guidance, it also pays for drafting and verifying the guide. That leaves less to spend on the task itself.</p><p>When several tasks reuse the same guide, its preparation cost is shared across those tasks. We choose that task set before the experiment begins.</p>
    </div>
    <ProductionDifference production="A team would use the level of assistance and review appropriate to its work. There would be no need to repeat every change three ways." poc="The same task is attempted with sources alone, with prepared guidance, and with guidance plus structured interaction. Review rules and budgets are matched so that extra review is not mistaken for a benefit of the layer." limit="This tests the selected procedures under controlled conditions. It does not establish how teams would adopt them or which review policy suits every organisation."/>
    <DetailGroup><Disclosure id="fair-comparison" title="What does the layer cost, and when could it pay for itself?">
      <Economics/>
    </Disclosure><Disclosure id="budget-selection" title="How will we choose the spending allowance?" summary="Development tasks help us choose an allowance before the scored comparison."><BudgetSelection/></Disclosure></DetailGroup>
  </section>

  <ExperimentDetails/>
  <TechnicalSetup/>
  <div className="route-footer"><span>For completed work, today’s blocker and the next step in Phase 1.</span><PageLink href="/progress">Progress & findings <ArrowRight size={18}/></PageLink></div>
</Shell>}
