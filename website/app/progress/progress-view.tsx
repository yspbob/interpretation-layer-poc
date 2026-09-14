"use client";
import { type ReactNode } from "react";
import { sitePath } from "../site-path";
import { PageLink } from "../page-link";
import { ArrowRight, Check, ShieldQuestion, ArrowUpRight } from "lucide-react";
import { DetailGroup, Disclosure } from "../details";

const project = "https://github.com/yspbob/interpretation-layer-poc/blob/main/";
const steps = [
  {title: "Find useful source material", state: "Complete", body: "We reviewed examples from four public software projects. Some give us clear rules and exceptions to investigate. This is a starting pool; we will not run an experiment on every example."},
  {title: "Prepare and rehearse the tests", state: "Complete", body: "We prepared four separate cases for checking the AI reviewers. We checked the expected answers against sources and actual software behaviour. The software that sends the tests and saves the responses now passes a full rehearsal with locally supplied answers."},
  {title: "Check the real connection and the AI reviewers", state: "Next", body: "Verify the model connection, agree the final settings and spending limit, then test the reviewers. They must recognise supported guidance, mistakes and missing rules before we rely on their judgements."},
  {title: "Ask the layer to prepare guidance", state: "Not started", body: "Choose the final cases and permitted evidence. The layer will draft guidance and check it. We will save the original draft, any corrections and the final result, including empty or unsuccessful results."},
  {title: "Assess the guidance and decide what follows", state: "Not started", body: "Report which claims the evidence supports, which important rules were missed and what preparation cost. Use that result to decide whether to test the guidance on coding tasks, revise the approach or stop."},
];

function ReportLink({path, children}: {path: string; children: ReactNode}) {
  return <a className="text-link" href={project + path} target="_blank" rel="noreferrer">{children} <ArrowUpRight size={15}/></a>;
}
function Heading({number, label, children}: {number: string; label: string; children: ReactNode}) {
  return <div className="section-heading"><span className="section-no">{number}</span><div><span className="eyebrow">{label}</span><h2>{children}</h2></div></div>;
}

export function ProgressView() {
  return <div className="progress-readable">
    <div className="page-heading"><span className="eyebrow">PHASE 1 PROGRESS · UPDATED 14 SEPTEMBER 2026</span></div>
    <p className="progress-context">This study tests a proposed interpretation layer. It would read a software project’s code and documentation, then prepare guidance for AI coding agents. We want to find out whether that guidance is supported by the evidence and covers the important rules in the selected material.</p>
    <section className="progress-intro">
      <div>
        <div className="status-line"><span className="pill green"><Check size={13}/>Test rehearsal complete</span><span className="pill neutral">The layer is still untested</span></div>
        <h1>We have rehearsed the tests.<br/><em>We have not tested the layer yet.</em></h1>
        <p className="lead">Before we judge the layer’s guidance, we need to know whether its reviewers can recognise mistakes. We have prepared the examples and rehearsed the software that will run those checks. No AI reviewer has taken those tests yet.</p>
      </div>
      <aside className="credibility-card">
        <div className="credibility-heading"><ShieldQuestion size={21}/><span className="eyebrow">THE QUESTION FOR PHASE 1</span></div>
        <h2>Can the layer produce guidance we can justify?</h2>
        <p>We will check whether its claims follow from the selected evidence and whether it misses important rules within that scope.</p>
        <p>Testing whether the guidance improves coding comes in Phase 2. Interaction, maintenance and return on investment are outside this phase.</p>
        <PageLink href="/" className="text-link">Read the Phase 1 plan <ArrowRight size={16}/></PageLink>
      </aside>
    </section>

    <nav className="progress-jumps" aria-label="On this progress page">
      <a href="#process">Our next steps</a><a href="#technical-status">What is ready</a><a href="#risks">What remains untested</a><a href="#findings">What we have learned</a><a href="#evidence">Supporting records</a>
    </nav>

    <section className="current-next" aria-labelledby="next-step-title">
      <div><span className="eyebrow">NEXT</span><h2 id="next-step-title">Check the actual model connection.</h2><p>The rehearsal used responses supplied locally. We still need to verify model access, request limits, usage reporting and account settings for the real service. The planned familiarity screen also needs its controlled connection.</p></div>
      <div><h3>Then run the reviewer tests.</h3><p>The model, instructions, scoring rules and spending limit must be fixed before we inspect any answers. No paid model requests are authorised yet.</p><p>We will use the four prepared cases. We are not expanding the test bank or building a general testing platform for this step.</p></div>
    </section>

    <section className="section-block" id="process">
      <Heading number="01" label="THE PATH THROUGH PHASE 1">Where we are in the work</Heading>
      <ol className="study-roadmap">{steps.map((step, i) => <li key={step.title} className={`roadmap-stage ${step.state === "Next" ? "roadmap-next" : ""}`} aria-current={step.state === "Next" ? "step" : undefined}>
        <span className={`roadmap-number ${step.state === "Complete" ? "roadmap-done" : ""}`}>{step.state === "Complete" ? <Check size={18}/> : i + 1}</span>
        <div><div className="roadmap-heading"><h3>{step.title}</h3><span className={`pill ${step.state === "Complete" ? "green" : step.state === "Next" ? "amber" : "neutral"}`}>{step.state}</span></div><p>{step.body}</p></div>
      </li>)}</ol>
    </section>

    <section className="section-block" id="technical-status">
      <Heading number="02" label="COMPLETED PREPARATION">What is ready</Heading>
      <p className="section-intro">Before we can judge the layer, we need examples with justified answers and a reliable way to put them to the reviewers. We prepared the examples first, then checked the software that sends them. The remaining step is to see how the AI reviewers actually answer.</p>
      <DetailGroup>
        <Disclosure id="qualification-case" title="Four cases are ready for testing the reviewers" summary="They include correct guidance, mistakes and missing information.">
          <p>Each case concerns a different kind of software behaviour. We prepared examples that a reviewer should accept, examples it should challenge and examples where the evidence cannot settle the answer. The expected decisions are supported by published sources and recorded behaviour checks.</p>
          <p>These are called qualification cases because they test whether a reviewer is ready for its job. There are 72 questions across three review roles. Each is planned twice to check consistency, giving 144 planned responses. Repetitions do not make these 144 independent cases.</p>
          <p>We challenged every expected answer and corrected defects in the test material. The detailed record includes 42 behaviour checks and 13 deliberately introduced faults that those checks detected. Codex prepared and reviewed this material; there is no independent human certification.</p>
          <p>The answers stay private so the models cannot receive them as part of the test. The private files are currently on the preparation PC; GitHub does not transfer them to the laptop.</p>
          <ReportLink path="research/development/astra-preparation/BANK-READINESS.md">Read the case preparation and audit</ReportLink>
        </Disclosure>
        <Disclosure id="provider-connection" title="The software completed the full test schedule in simulation" summary="It checks inputs, saves responses and keeps one spending record for the batch.">
          <span id="phase1-harness"/>
          <p>The runner sends each role only its permitted material. Each request starts without another attempt’s conversation or answers. It saves the scheduled order, the exact requests, returned responses and reported usage.</p>
          <p>These checks matter because a test would be misleading if a reviewer saw the hidden answer, received an extra attempt or used more resources without that being recorded.</p>
          <p>All 72 software tests passed. We also rehearsed the complete 144 request schedule with artificial inputs, and separately with the actual prepared case inputs. Every response was supplied locally. No live model service was contacted.</p>
          <p>A failed answer remains in the record and is not automatically retried. If usage is unknown, the batch stops and keeps the reserved allowance. Passing these checks does not verify the real service’s billing or an AI’s answers.</p>
          <ReportLink path="research/development/phase1-harness/QUALIFICATION-BATCH.md">Read the runner checks and limits</ReportLink>
        </Disclosure>
        <Disclosure id="review-roles" title="What each AI reviewer will do" summary="Checking a draft and judging that check are separate jobs.">
          <p>The verifier is part of the layer. It checks proposed rules while the guide is being prepared, and its feedback can lead to corrections.</p>
          <p>The guidance assessor examines the saved guide after preparation is finished. It checks each claim against the evidence, then checks our separately prepared reference for rules the guide missed. Its findings do not change that guide during the measured attempt.</p>
          <p>Astra remains the model for the controlled workflow. Fable 5.1 will provide an additional assessment through Claude Desktop. It receives the guide and permitted evidence without Astra’s verdict. This review is agreed, but it has not run yet.</p>
          <p>We will compare their answers after both are saved. A disagreement must be resolved by the source evidence or a behaviour check. Agreement alone does not establish correctness: both models could miss the same exception or rely on a faulty reference.</p>
          <p>We also examine Astra’s verifier decisions to understand whether its review helped or introduced mistakes. This explains how the layer reached its result.</p>
          <ReportLink path="research/development/astra-preparation/QUALIFICATION.md">Read the proposed pass criteria</ReportLink>
        </Disclosure>
      </DetailGroup>
    </section>

    <section className="section-block" id="risks">
      <Heading number="03" label="STILL OPEN">What remains untested</Heading>
      <p className="section-intro">There are no experimental guidance results and no qualified AI reviewers. These are the remaining limits and decisions that matter before we can report a Phase 1 result.</p>
      <DetailGroup>
        <Disclosure id="assessment" title="Whether the AI reviewers can make sound decisions" summary="Prepared answers and simulated responses cannot establish this.">
          <p>We must run the prepared questions through the actual model and apply the agreed pass criteria. A correct label with a wrong explanation will not pass. A reviewer that fails must remain recorded as failing.</p>
          <p>If those answers lead us to change its instructions, the affected cases become development material. We cannot keep practising on the same cases and then call them an independent test.</p>
        </Disclosure>
        <Disclosure id="containment" title="Whether the real connection meets the study’s requirements" summary="The local checks have passed; the live configuration still needs verification.">
          <span id="technical-readiness-detail"/>
          <p>We need to verify the available model, supported request settings, input allowance, usage reporting and account data settings. The batch currently accepts only local simulated responses. It has no live execution switch.</p>
          <p>References reserved for assessment, expected answers and our research notes must stay out of the drafter’s and verifier’s inputs. The exact request and access configuration must be checked before model tests begin.</p>
          <PageLink className="text-link" href="/#phase-controls">Read the access controls in the plan <ArrowRight size={15}/></PageLink>
        </Disclosure>
        <Disclosure id="familiarity-status" title="Whether the model already knows the source material" summary="An early recall check found no specific match, but that is limited evidence.">
          <span id="astra-preparation"/>
          <p>We asked fresh Astra subagents about six source excerpts and six controls, repeating each question. None of the 24 responses exactly matched its target. One control response was empty.</p>
          <p>This does not prove that Astra is unfamiliar with the projects. The subagents were told not to use tools, but tool access was not disabled. The controlled screening connection remains unfinished.</p>
          <p>Reading the supplied code during a test is intended. Carrying over another test’s answers or our private research is not.</p>
          <ReportLink path="research/development/astra-preparation/SUBAGENT-SCREEN.md">Read the preliminary screen</ReportLink>
        </Disclosure>
        <Disclosure id="settings" title="The final cases, settings and spending approval" summary="The reviewer test cases are prepared; the guidance experiment still needs its final selection.">
          <span id="references"/>
          <p>We still need to select the cases for the guidance experiment and fix their permitted evidence. A central requirement that the evidence cannot justify will stay outside scoring. Public documentation cannot establish an unrecorded owner decision.</p>
          <p>Astra remains selected for the controlled workflow. Its proposed preparation ceiling of $150 is not spending approval. Fable’s additional desktop review will use the included Max allowance and stop if paid credits are needed.</p>
          <p>We must check Fable’s app settings and save complete input and response records before using sealed test cases. Its reviews will be reported separately because we have not demonstrated the same controls as the API runner.</p>
          <ReportLink path="research/development/astra-preparation/FABLE-DESKTOP.md">Read the additional review procedure</ReportLink>
          <p>Before paid calls, we will present the verified configuration and a concrete allocation for approval.</p>
        </Disclosure>
      </DetailGroup>
    </section>

    <section className="section-block" id="findings">
      <Heading number="04" label="LESSONS FROM PREPARATION">What we have learned so far</Heading>
      <p className="section-intro">These observations have improved the test design. They are not evidence that the interpretation layer improves engineering work.</p>
      <DetailGroup>
        <Disclosure id="rule-exceptions" title="The guide needs to explain when extra work is necessary" summary="The same instruction can be necessary in one situation and redundant in another.">
          <p>Consider an application that records the history of edits. Its standard editing function might save the old value automatically. Code that writes directly to the record may need to save that old value itself.</p>
          <p>This illustrates why we include exceptions in the tests. A guide should explain both situations. Telling the agent to add the same step everywhere would duplicate work the application already does. Telling it the application always handles that step would leave the direct edit without the required history.</p>
          <p>The source review found this kind of distinction in NetBox, a system for recording infrastructure. The tests therefore need both a situation where the instruction is needed and a valid alternative where it is not.</p>
          <ReportLink path="research/development/playbook-and-original-poc-review.md">Read the original source review</ReportLink>
        </Disclosure>
        <Disclosure id="docs" title="Documentation and implementation can tell different stories" summary="A useful guide needs to explain the disagreement.">
          <p>HTTPX is a library for making web requests. Its guide discourages setting cookies separately on each client request, while the inspected code still accepts them with a warning. Copying the guide alone would miss that distinction.</p>
          <p>The assessment must distinguish a recommendation from what the code actually permits. The same care applies when documentation describes an exception or a commitment that code cannot prove.</p>
          <a className="text-link" href={sitePath("/evidence/cross-repository-inventory-review.md")} download>Read the source review <ArrowUpRight size={15}/></a>
        </Disclosure>
        <Disclosure id="boundaries" title="A test can wrongly penalise a correct answer" summary="We found defects by challenging our own expected answers.">
          <p>One supposedly equivalent example assumed a starting state that its scope did not require. Another rule did not clearly distinguish a successful operation from failure in the next step. Recorded counterexamples showed why the wording needed correction.</p>
          <p>We also clarified that stating a rule correctly in one place does not excuse a contradictory claim elsewhere. The earlier versions remain preserved so the changes can be inspected.</p>
          <ReportLink path="research/development/astra-preparation/BANK-READINESS.md">Read the audit findings</ReportLink>
        </Disclosure>
        <Disclosure id="supply" title="More examples do not always mean more evidence" summary="Several examples can concern the same underlying decision.">
          <p>The initial review screened 84 records. Of these, 52 were candidates for further development, covering 39 named groups of related decisions. These are candidate counts, not completed experiments.</p>
          <p>Repeated questions help show whether an answer is consistent. To test whether guidance works across different changes, we will need genuinely different tasks in a later phase.</p>
        </Disclosure>
      </DetailGroup>
    </section>

    <section className="section-block" id="evidence">
      <Heading number="05" label="OPTIONAL DETAIL">Supporting work and records</Heading>
      <p className="section-intro">The public development examples helped us build the method. Their answers are already published, so they cannot serve as untouched tests of a reviewer trained on them.</p>
      <DetailGroup>
        <Disclosure id="netbox-bulk-candidate" title="NetBox: undoing an edit can leave a notification behind" summary="A development example that connects evidence across an application.">
          <p>NetBox stores infrastructure records. In the inspected batch editing path, undoing a failed database change did not necessarily remove the notification already waiting in memory. That could leave a message about a change that had not been saved.</p>
          <p>The reproduction checked four requests at each of three historical versions. The later version removed notifications for failed batches while preserving those for successful edits. No worker sent the notifications during the check.</p>
          <p>This establishes a behaviour worth investigating. It does not show that an agent needs prepared guidance to understand it.</p>
          <ReportLink path="research/development/netbox-bulk-error-candidate/reproduction.md">Read the reproduction</ReportLink>
        </Disclosure>
        <Disclosure id="h06-guidance-case" title="HTTPX: custom authentication can bypass normal framework work" summary="A development example with documented behaviour and exceptions.">
          <p>HTTPX supports both ordinary and asynchronous web requests. Its authentication code can share common logic, but a custom implementation can bypass work the framework normally performs.</p>
          <p>The development case records six related decisions and 15 local behaviour checks. It helps us build assessment tools. Because documentation explains parts of the rule, it is not proof of discovering an undocumented decision.</p>
          <ReportLink path="research/development/h06-guidance-assessment/README.md">Read the development case</ReportLink>
        </Disclosure>
        <Disclosure id="history" title="Earlier preparation and how the work reached this point" summary="A short history, with the original records available.">
          <span id="recorded-checks"/>
          <p>On 5 September, the source review established the candidate pool. On 8 September, an example about closing HTTP responses exercised the proposed workflow with answers written in advance.</p>
          <p>The following work developed the HTTPX and NetBox cases, the guidance workflow and the model connection. On 13 September, four separate reviewer test cases were prepared and their expected answers audited. On 14 September, the batch runner completed its offline checks and full schedule rehearsals.</p>
          <ReportLink path="research/development/h04-response-lifetime/README.md">Read the earlier workflow example</ReportLink>
        </Disclosure>
        <Disclosure id="reports" title="Plans, source inventory and detailed test records" summary="Use these when you need the full evidence rather than this progress summary.">
          <span id="repos"/><span id="inventory"/>
          <ul className="progress-record-links">
            <li><a href={sitePath("/evidence/working-poc-plan.md")} download>Current working plan</a></li>
            <li><a href={sitePath("/evidence/cross-repository-inventory-review.md")} download>Review of the candidate source material</a></li>
            <li><ReportLink path="research/development/astra-preparation/BANK-READINESS.md">Reviewer case audit</ReportLink></li>
            <li><ReportLink path="research/development/phase1-harness/QUALIFICATION-BATCH.md">Batch runner checks</ReportLink></li>
          </ul>
        </Disclosure>
        <Disclosure id="implementation-takeaways" title="Ideas to carry into a practical implementation" summary="Kept as design lessons, with their evidence and uncertainty.">
          <span id="phase-transition-status"/>
          <p>We are keeping a separate record of lessons about evidence, review, guidance reuse and maintenance. They remain design ideas until tested.</p>
          <p>If we move to coding comparisons, we will retain unsuccessful preparation and its cost, rather than select only the guides that scored well. Tasks intended to reuse guidance must be chosen before that guidance is drafted.</p>
          <ReportLink path="research/implementation-takeaways.md">Read the implementation takeaways</ReportLink>
        </Disclosure>
      </DetailGroup>
    </section>
    <div className="route-footer"><span>Phase 1 is about the guidance itself. Coding and interaction come later.</span><PageLink href="/">Read the plan <ArrowRight size={18}/></PageLink></div>
  </div>;
}
