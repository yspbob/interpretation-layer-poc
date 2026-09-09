import { PageLink } from './page-link';

import { ArrowDown, ArrowRight, CornerUpLeft, RefreshCw } from 'lucide-react';
import { Shell, chapterUrl } from './ui';
import { DetailGroup, Disclosure, Examples } from './details';
import { ExperimentDetails } from './experiment-details';
import { TechnicalSetup } from './technical-setup';

export const dynamic = 'force-static';
export default function Experiment(){return <Shell active="experiment">
  <div className="page-heading"><span className="eyebrow">AI ENGINEERING PLAYBOOK / CHAPTER 4</span><span className="reading-time">Why this experiment is being run</span></div>
  <section className="intro">
    <div>
      <h1>Will an interpretation layer help an AI agent make better code changes?</h1>
      <p className="lead">An AI agent can read a project’s code and documentation. But it still has to decide which existing patterns to follow, which exceptions matter, and what it should leave alone.</p>
      <p className="intro-explanation">The playbook proposes an <strong>interpretation layer</strong> that turns this evidence into approved guidance, helps agents check a proposed change against it, and supports checks on the resulting work. This experiment asks which parts of that process help, and whether the improvement justifies the effort.</p>
      <p className="chapter-context">The full proposal is in <a href={chapterUrl} target="_blank" rel="noreferrer">Chapter 4: The interpretation layer</a> of the public AI Engineering Playbook.</p>
      <div className="experiment-jumps"><a className="text-link intro-jump" href="#example">What the layer provides <ArrowDown size={16}/></a><a className="text-link intro-jump" href="#technical-setup">Technical setup <ArrowDown size={16}/></a></div>
    </div>
    <aside className="hypothesis">
      <span className="eyebrow">WHY TEST THIS?</span>
      <p>Does preparing the guidance help? Does checking the agent’s work against it add a further benefit?</p>
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
    <p className="section-intro section-intro-wide">The layer connects two cycles: one establishes the guidance; the other uses it during engineering work. Drafting and approval happen before that guidance can be used as an approved decision, but they are not repeated for every task.</p>
    <div className="guidance-cycles" id="guidance-cycles">
      <section className="guidance-cycle" aria-labelledby="preparation-cycle-title">
        <span className="eyebrow">DRAFTING &amp; APPROVAL CYCLE</span>
        <h3 id="preparation-cycle-title">Establish and maintain the guidance</h3>
        <ol className="cycle-steps">
          <li><h4>Find the evidence</h4><p>Read the relevant code, documentation and recorded decisions, including exceptions and conflicting examples.</p></li>
          <li><h4>Draft and verify the guidance</h4><p>Explain each proposed rule, its scope and its evidence. Check support and contradictions before owner review.</p></li>
          <li><h4>Review and release a version</h4><p>The responsible owner approves, rejects or requests changes. Only approved decisions are released as approved guidance.</p></li>
        </ol>
        <p className="cycle-repeat"><RefreshCw size={17} aria-hidden="true"/><span>Review can send a draft back for revision before a version is released.</span></p>
        <p className="cycle-timing"><strong>Initially:</strong> establish the baseline.<br/><strong>When evidence or decisions change:</strong> recheck affected guidance and retain, revise or retire it through review.</p>
      </section>
      <div className="guidance-connection">
        <ArrowRight className="guidance-connection-arrow" size={28} aria-hidden="true"/>
        <strong>Approved guidance</strong>
        <p>A version with its evidence, scope and exceptions.</p>
        <span>The same version can support many tasks.</span>
      </div>
      <section className="guidance-cycle guidance-cycle-use" aria-labelledby="usage-cycle-title">
        <span className="eyebrow">USAGE CYCLE</span>
        <h3 id="usage-cycle-title">Apply the guidance to each task</h3>
        <ol className="cycle-steps">
          <li><h4>Consult and plan</h4><p>Retrieve the relevant guidance. Identify what can be reused, what constrains the change and which exceptions may apply.</p></li>
          <li><h4>Check and carry out the approach</h4><p>Review the plan against the guidance, make the change and recheck material changes of approach.</p></li>
          <li><h4>Check the resulting work</h4><p>Assess the change against the relevant decisions and task requirements. Record objections and unresolved questions.</p></li>
        </ol>
        <p className="cycle-repeat"><RefreshCw size={17} aria-hidden="true"/><span>Objections can send the plan or code back for revision, or stop the attempt.</span></p>
        <p className="cycle-timing"><strong>For each task:</strong> use the applicable guidance without reopening every approved decision.</p>
      </section>
      <div className="guidance-feedback"><CornerUpLeft size={21} aria-hidden="true"/><p><strong>New evidence can prompt a guidance review.</strong> Work may expose an outdated rule, a conflict or an unrecorded exception. Send that evidence back to the drafting and approval cycle; it does not automatically change an approved decision.</p></div>
    </div>
    <div className="scope-note"><span>What this POC can test</span><div><p>The first POC is designed as a self-contained experiment to minimise dependencies on project maintainers, organisational approvals and ongoing operational involvement. Public code and recorded decisions provide a basis for testing whether guidance is supported by evidence and helps with later work.</p><p>This limits the claim: evidence verification does not establish owner approval, and a fixed guidance version does not test ongoing maintenance. Later iterations could involve project owners and examine maintenance if these are needed to answer the remaining questions.</p><p>The diagram above describes the full proposal. This pilot freezes guidance before each matched comparison; feedback from final evaluation cannot be used to repair it during a run.</p></div></div>
    <div className="working-loop">
      <h3>How agent review is designed to work in this POC</h3>
      <p><strong>Planned review procedure.</strong> In the interactive condition, a separate checking agent would assess the coding agent’s proposed approach and its resulting changes. It would use the same permitted evidence and the guidance prepared before the task, without access to the withheld assessment.</p>
      <ol className="numbered-detail">
        <li><strong>Check the plan before the first edit.</strong><p>The coding agent asks the layer what to reuse and which rules apply. It then submits the components it will change, the rules it will follow and any exception it intends to use. The checker assesses that reasoning, rather than merely looking for citations.</p></li>
        <li><strong>Make objections lead to a recorded decision.</strong><p>The checker returns “proceed”, “revise” or “unresolved”, with a reason. A request to revise goes back to the coding agent. The pilot proposal allows at most two correction rounds per checkpoint; an unresolved decision or an exhausted allowance stops the attempt and is recorded for later assessment.</p></li>
        <li><strong>Check a changed approach before work continues.</strong><p>If the agent needs a new dependency, changes the component it plans to reuse, or relies on a new exception, it must submit an updated plan. The program running the experiment would also compare each submitted code change with the plan. A mismatch sends the attempt back for review.</p></li>
        <li><strong>Judge the code independently at the end.</strong><p>All conditions run the same task checks. In each backtest, a separate evaluator assesses both the agent’s change and the historical implementation for task correctness and compliance with the applicable guardrails. If the agent avoids a violation in the historical code while completing the task correctly, that counts in its favour. Matching the original code is not the goal.</p></li>
      </ol>
      <p className="caption">Owner approval of new decisions, renewal of guidance and checks across an organisation’s systems remain outside this pilot.</p>
    </div>
  </section>

  <section className="section-block">
    <div className="section-heading"><span className="section-no">03</span><div><span className="eyebrow">THE PROPOSED COMPARISON</span><h2>Separate the value of guidance from the value of checking its use</h2></div></div>
    <p className="section-intro">The design compares agents making the same change under three conditions. This separates the effect of prepared guidance from the additional effect of consultation and checking. The two guidance groups receive the same frozen rules, and preparation costs are recorded. Prompts, budgets and checks are specified and validated before the trial.</p>
    <div className="comparison comparison-three">
      <div><span className="eyebrow">WITHOUT THE EXTRA LAYER</span><h3>The agent works from the sources</h3><p>It searches the code and available documentation, works out what matters for the task, and makes the change. This represents a capable agent doing the work directly.</p></div>
      <div><span className="eyebrow">WITH PREPARED GUIDANCE</span><h3>The agent receives the rules</h3><p>The layer has examined the same sources and written guidance before the task begins. The agent receives that guidance and works with it, without an interactive check by the layer.</p></div>
      <div><span className="eyebrow">WITH GUIDANCE AND INTERACTION</span><h3>The agent checks its proposed actions</h3><p>The agent receives the same guidance, consults the layer about its plan and responds to checks at agreed points. The run records whether those interactions prevent mistakes or add unnecessary work.</p></div>
    </div>
    <div className="review-comparison" id="review-comparison">
      <h3>Every group gets a review</h3>
      <p>All three groups have their plans and code reviewed at the same points, with the same number of opportunities to make corrections. What differs is the help available during review:</p>
      <table className="review-comparison-table">
        <caption className="sr-only">What the reviewer checks in each group</caption>
        <thead><tr><th scope="col">Group</th><th scope="col">What the reviewer checks</th></tr></thead>
        <tbody>
          <tr><th scope="row">Sources only</th><td>The plan and code against the available sources, including the project’s actual AGENTS.md instructions.</td></tr>
          <tr><th scope="row">Prepared guidance</th><td>The same, with the prepared guidance also available.</td></tr>
          <tr><th scope="row">Guidance and interaction</th><td>The same, plus targeted questions about which rules apply, how the proposed change follows them, and whether an exception is justified.</td></tr>
        </tbody>
      </table>
      <p>This tests whether structured questioning improves the result beyond an ordinary review with guidance available. Every group has the same overall resource limit, and all review effort counts towards it.</p>
    </div>
  </section>

  <ExperimentDetails/>
  <TechnicalSetup/>
  <div className="route-footer"><span>For the work completed so far and the decisions still ahead.</span><PageLink href="/progress">Progress & findings <ArrowRight size={18}/></PageLink></div>
</Shell>}
