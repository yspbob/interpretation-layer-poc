import { PageLink } from './page-link';

import { ArrowDown, ArrowRight, CornerUpLeft, RefreshCw } from 'lucide-react';
import { Shell, chapterUrl } from './ui';
import { DetailGroup, Disclosure, Examples } from './details';
import { ExperimentDetails } from './experiment-details';
import { TechnicalSetup } from './technical-setup';
import { Economics } from './economics';
import { ProductionDifference } from './production-difference';

export const dynamic = 'force-static';
export default function Experiment(){return <Shell active="experiment">
  <div className="page-heading"><span className="eyebrow">AI ENGINEERING PLAYBOOK / CHAPTER 4</span><span className="reading-time">Why this experiment is being run</span></div>
  <section className="intro">
    <div>
      <h1>Will an interpretation layer help an AI agent make better code changes?</h1>
      <p className="lead">An AI agent can read a project’s code and documentation. But it still has to decide which existing patterns to follow, which exceptions matter, and what it should leave alone.</p>
      <p className="intro-explanation">The playbook proposes an <strong>interpretation layer</strong> that turns this evidence into approved guidance, helps agents check a proposed change against it, and supports checks on the resulting work. This POC tests the technical steps using project evidence. It does not certify new guidance on behalf of a project owner.</p>
      <p className="chapter-context">The full proposal is in <a href={chapterUrl} target="_blank" rel="noreferrer">Chapter 4: The interpretation layer</a> of the public AI Engineering Playbook.</p>
      <div className="experiment-jumps"><a className="text-link intro-jump" href="#example">What the layer provides <ArrowDown size={16}/></a><a className="text-link intro-jump" href="#comparison">The comparison <ArrowDown size={16}/></a><a className="text-link intro-jump" href="#method">The method <ArrowDown size={16}/></a><a className="text-link intro-jump" href="#technical-setup">Technical setup <ArrowDown size={16}/></a></div>
    </div>
    <aside className="hypothesis">
      <span className="eyebrow">WHY TEST THIS?</span>
      <p>Does prepared guidance help beyond the sources and ordinary review? Does structured consultation add a further benefit?</p>
      <div className="hypothesis-explanation">A capable agent may already work out the right approach from the sources. Preparing guidance and consulting it takes time and money. The experiment tests whether these steps prevent enough mistakes to justify the effort.</div>
      <div className="hypothesis-foot"><span className="signal-dot"/>Planned method · See Progress &amp; findings for readiness and results.</div>
    </aside>
  </section>

  <section id="example" className="section-block">
    <div className="section-heading"><span className="section-no">01</span><div><span className="eyebrow">GUIDANCE FOR A SPECIFIC TASK</span><h2>What would the layer tell an agent?</h2></div></div>
    <p className="section-intro">When an agent is given a task, it needs to understand how that task fits into the existing system. The layer should identify code the agent can reuse, explain which decisions constrain the change, and show where exceptions apply. The agent should be able to see the evidence behind each answer and whether it represents an approved decision, an observed pattern or a question that still needs review.</p>
    <p className="section-intro">The agent can consult the layer about a proposed approach: whether to extend an existing component, where new code belongs, or whether a change would cross a boundary the project has chosen to preserve. The answer should explain what is allowed and why, or identify the unresolved decision that needs an owner’s judgement. The agent uses those answers in its plan, which can then be checked against the relevant decisions before work proceeds.</p>
    <DetailGroup><Disclosure id="guidance-examples" title="See examples of the guidance an agent could receive" summary="How this applies to change history, conflicting documentation and questions the code cannot answer.">
      <p>NetBox is an open-source application used to document network infrastructure, including devices and their connections. It is one of the four projects in this study.</p>
      <p>In the first example, an agent is asked to write code that renames a device in NetBox. The layer would draw its attention to a related requirement: the change history must preserve the old name as well as the new one. It would also explain when NetBox already handles that requirement, so the agent can choose the right approach.</p>
      <Examples/>
    </Disclosure></DetailGroup>
  </section>

  <section className="section-block">
    <div className="section-heading"><span className="section-no">02</span><div><span className="eyebrow">THE IDEA BEHIND THE LAYER</span><h2>Turn project evidence into guidance for later work</h2></div></div>
    <p className="section-intro section-intro-wide">The production proposal has two cycles. First, the interpretation layer drafts guidance, checks its evidence and sends it for owner review. Agents then reuse the released version across tasks. Later changes can prompt another review; preparing the guidance is not repeated for every coding task. The notes below explain how the POC simplifies this process.</p>
    <div className="guidance-cycles" id="guidance-cycles">
      <section className="guidance-cycle" aria-labelledby="preparation-cycle-title">
        <span className="eyebrow">DRAFTING &amp; APPROVAL CYCLE</span>
        <h3 id="preparation-cycle-title">Establish and maintain the guidance</h3>
        <ol className="cycle-steps">
          <li><h4>Find the evidence</h4><p>Read the relevant code, documentation and recorded decisions, including exceptions and conflicting examples.</p></li>
          <li><h4>Draft and verify the guidance</h4><p>Explain each proposed rule, its scope and its evidence. Check support and contradictions before owner review.</p></li>
          <li><h4>Review and release a version</h4><p>In production, the responsible owner approves the proposed guidance, rejects it or asks for changes. Only approved decisions are released as authoritative guidance.</p></li>
        </ol>
        <p className="cycle-repeat"><RefreshCw size={17} aria-hidden="true"/><span>Review can send a draft back for revision before a version is released.</span></p>
        <p className="cycle-timing"><strong>In this POC:</strong> there is no responsible project owner. The verifier checks whether the evidence supports each claim, and accepted claims form the guide. This does not make them owner-approved rules. The guide is prepared before the coding tasks and stays unchanged during their comparison.</p>
      </section>
      <div className="guidance-connection">
        <ArrowRight className="guidance-connection-arrow" size={28} aria-hidden="true"/>
        <strong>A released guidance version</strong>
        <p>With evidence, scope and exceptions. Owner-approved in production; checked for evidence support in this POC.</p>
        <span>The same version can support many tasks.</span>
      </div>
      <section className="guidance-cycle guidance-cycle-use" aria-labelledby="usage-cycle-title">
        <span className="eyebrow">USAGE CYCLE</span>
        <h3 id="usage-cycle-title">Apply the guidance to each task</h3>
        <ol className="cycle-steps">
          <li><h4>Consult and plan</h4><p>Retrieve the relevant guidance. Identify what can be reused, what constrains the change and which exceptions may apply.</p></li>
          <li><h4>Check the plan</h4><p>Review the proposed approach against the guidance and resolve blocking issues before editing.</p></li>
          <li><h4>Implement and check during work</h4><p>The agent can ask follow-up questions. At defined checkpoints and when the approach changes, the checker reviews the work so far and can require an explanation or correction before it continues.</p></li>
          <li><h4>Check the resulting work</h4><p>Assess the change against the relevant decisions and task requirements. Record objections and unresolved questions.</p></li>
        </ol>
        <p className="cycle-repeat"><RefreshCw size={17} aria-hidden="true"/><span>Objections can send the plan or code back for revision, or stop the attempt.</span></p>
        <p className="cycle-timing"><strong>In this POC:</strong> all groups receive review at the required checkpoints. The interactive group also receives structured questions about the guidance. A necessary unresolved decision stops the attempt; no owner is available to settle it. These are planned checks, not continuous monitoring of every action.</p>
      </section>
      <div className="guidance-feedback"><CornerUpLeft size={21} aria-hidden="true"/><p><strong>New evidence can prompt a guidance review.</strong> Work may expose an outdated rule, a conflict or an unrecorded exception. In production, that evidence goes back for review; it does not automatically change an approved decision. Reviews could run nightly, with earlier review of consequential changes. That cadence is a proposal. This POC records the issue but keeps the guide unchanged.</p></div>
    </div>
    <div className="scope-note" id="pilot-scope"><span>What this POC can test</span><div><p>The first POC uses changes previously made in public projects. Each selected task needs requirements supported by project records and tests that can be repeated. This lets the technical steps be examined without asking maintainers to approve new rules or take part in each run.</p><p><strong>Prior familiarity remains a limitation.</strong> A model may already know the public code. Using the same models, tasks and budgets makes the methods comparable, but cannot prove that an agent worked out a rule solely from the files it received. Separate familiarity checks will look for recalled project details and historical fixes before the pilot. Private changes that alter a rule are an optional later extension; they are not required for this first pilot.</p><p>This limits the claim: evidence verification does not establish owner approval, and a fixed guidance version does not test ongoing maintenance. Later iterations could involve project owners and examine maintenance if these are needed to answer the remaining questions.</p><p>The diagram above describes the full proposal. This pilot prepares a guide for a defined code version and set of permitted sources, then reuses it across the associated tasks. It is not one guide for every repository or historical version. Results from final evaluation cannot be used to repair it during that comparison.</p></div></div>
    <DetailGroup><Disclosure id="production-scope" title="Where does this POC differ from production?" summary="Owner approval, repeated use, maintenance and the way success is measured.">
      <p>The experiment tests a limited part of the production proposal. It checks evidence-supported guidance and its use on historical tasks, without a project owner certifying it. Guidance remains fixed during each comparison, so the pilot does not test whether updates keep it correct over time.</p>
      <p>Production would apply the layer to current engineering work. This POC instead repeats the same task under three conditions, with restricted inputs, matched review rules and independent assessment after each attempt. These controls help compare the methods; they are not a prescription for every production workflow.</p>
      <p>The first pilot also uses public projects and may encounter knowledge a model already has. Familiarity probes can find signs of recall, but cannot certify that a project is unseen. Its cost analysis estimates the return from reusing a fixed guide, not the full economics of a production service.</p>
      <p>The relevant sections below explain each difference where it affects the procedure. <PageLink className="text-link" href="/progress">Progress &amp; findings</PageLink> shows which parts are built or tested.</p>
    </Disclosure></DetailGroup>
    <p className="caption">In this POC, all three groups receive review. The <a className="text-link" href="#during-work">step-by-step method</a> explains the checks before editing, during implementation and at final submission.</p>
  </section>

  <section className="section-block" id="comparison">
    <div className="section-heading"><span className="section-no">03</span><div><span className="eyebrow">THE PROPOSED COMPARISON</span><h2>Separate the value of guidance from the value of checking its use</h2></div></div>
    <p className="section-intro">The design compares agents making the same change under three conditions. This separates the effect of prepared guidance from the additional effect of consultation and checking. The two guidance groups receive the same frozen rules, and preparation costs are recorded. Prompts, budgets and checks are specified and validated before the trial.</p>
    <div className="comparison comparison-three">
      <div><span className="eyebrow">WITHOUT THE EXTRA LAYER</span><h3>The agent works from the sources</h3><p>It searches the code and available documentation, works out what matters for the task, and makes the change. This represents a capable agent doing the work directly.</p></div>
      <div><span className="eyebrow">WITH PREPARED GUIDANCE</span><h3>The agent receives the rules</h3><p>The layer has examined the same sources and written guidance before the task begins. The agent receives that guidance and works with it, without an interactive check by the layer.</p></div>
      <div><span className="eyebrow">WITH GUIDANCE AND INTERACTION</span><h3>The agent checks its proposed actions</h3><p>The agent receives the same guidance, consults the layer about its plan and responds to checks at agreed points. The run records whether those interactions prevent mistakes or add unnecessary work.</p></div>
    </div>
    <div className="review-comparison" id="review-comparison">
      <h3>Every group gets a review</h3>
      <p>All three groups follow the same rules for when review is required and how many corrections are allowed. Each has a plan review, checks during work and a final submission review. Different approaches may trigger different numbers of intermediate checks. What differs is the help available during review:</p>
      <table className="review-comparison-table">
        <caption className="sr-only">What the reviewer checks in each group</caption>
        <thead><tr><th scope="col">Group</th><th scope="col">What the reviewer checks</th></tr></thead>
        <tbody>
          <tr><th scope="row">Sources only</th><td>The plan and code against the available sources, including any applicable AGENTS.md instructions present at the starting revision.</td></tr>
          <tr><th scope="row">Prepared guidance</th><td>The same, with the prepared guidance also available.</td></tr>
          <tr><th scope="row">Guidance and interaction</th><td>The same, plus targeted questions about which rules apply, how the proposed change follows them, and whether an exception is justified.</td></tr>
        </tbody>
      </table>
      <p>This tests whether structured questioning improves the result beyond an ordinary review with guidance available. Every group has the same overall method budget. Preparing guidance uses part of the budget for the groups that receive it; all coding, consultation and review also count.</p>
    </div>
    <ProductionDifference production="A team would use the level of assistance and review appropriate to its work. There would be no need to repeat every change three ways." poc="The same task is attempted with sources alone, with prepared guidance, and with guidance plus structured interaction. Review rules and budgets are matched so that extra review is not mistaken for a benefit of the layer." limit="This tests the selected procedures under controlled conditions. It does not establish how teams would adopt them or which review policy suits every organisation."/>
    <DetailGroup><Disclosure id="fair-comparison" title="What does the layer cost, and when could it pay for itself?">
      <Economics/>
    </Disclosure></DetailGroup>
  </section>

  <ExperimentDetails/>
  <TechnicalSetup/>
  <div className="route-footer"><span>For the work completed so far and the decisions still ahead.</span><PageLink href="/progress">Progress & findings <ArrowRight size={18}/></PageLink></div>
</Shell>}
