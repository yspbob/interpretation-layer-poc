import { sitePath } from './site-path';
import { ArrowUpRight, ArrowRight } from 'lucide-react';
import { DetailGroup, Disclosure, RepositoryCards } from './details';
import { PageLink } from './page-link';
import { chapterUrl } from './ui';

export function ExperimentDetails(){return <>
  <section className="section-block" id="method">
    <div className="section-heading"><span className="section-no">04</span><div><span className="eyebrow">THE EXPERIMENT, STEP BY STEP</span><h2>How the experiment is designed to run</h2></div></div>
    <p className="section-intro">The experiment will ask agents to make the same code change with different kinds of help, then compare the work they produce and the effort it took. Here is the proposed sequence for one test.</p>

    <ol className="method-steps" aria-label="The four steps in one experiment">
      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">1</span><h3>Prepare a task with a defensible assessment</h3></div>
        <div className="method-step-content">
          <p>For each backtest, case preparation records the task, the historical implementation and the guardrails that applied to that work. Before an agent attempts it, the assessment establishes the required behaviour, relevant rules and legitimate exceptions. Here, guardrails mean evidence-supported constraints that apply to the task, rather than every pattern found in the code. The historical solution and its assessment stay outside the agent’s workspace.</p>
          <DetailGroup><Disclosure id="choose-case" title="How are tasks selected and assessment criteria established?">
            <p>Each historical case starts from the code before the original change. The task and applicable rules must be tied to that time; later documentation cannot silently introduce a new requirement. The repository snapshots in the candidate inventory are discovery material, not necessarily those historical starting points.</p>
            <p><strong>Start with the evidence.</strong> Each case uses a published requirement or decision. Its scope is checked against the code, and any disagreement is recorded. Neither the documentation nor the implementation is assumed to be correct.</p>
            <p><strong>Check that the assessment can tell the difference.</strong> Each case includes:</p><ul className="plain-list"><li>A valid solution.</li><li>A deliberately incorrect change.</li><li>A legitimate exception or alternative.</li></ul><p>Tests and source evidence must distinguish these outcomes. A second valid solution can provide the alternative; an exception is not invented to fill the list. Where the evidence cannot settle a judgement, it remains unresolved. A case whose central requirement depends on undocumented intent or disputed interpretation is excluded from scored pilot comparisons. Passing tests alone does not establish that the case or its coverage is sufficient.</p>
            <p><strong>Keep the coverage in perspective.</strong> The candidate projects are NetBox, Wagtail, Paperless-ngx and HTTPX. They cover different engineering decisions, but all use Python and three use Django. Findings from these projects cannot represent all software development.</p>
            <RepositoryCards/>
          </Disclosure></DetailGroup>
        </div>
      </li>

      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">2</span><h3>Let the layer prepare its guidance</h3></div>
        <div className="method-step-content">
          <p>The layer examines the allowed project material without seeing the change task. It drafts guidance, and a separate verifier checks whether the evidence supports it. The resulting guide is saved before the task is revealed and stays unchanged during the run. Its source scope is chosen without clues from the hidden solution.</p>
          <DetailGroup>
            <Disclosure id="allowed-evidence" title="Does the layer read the documentation, or work the rule out from code?">
              <p>The experiment compares two input conditions. Neither condition rules out prior model knowledge of the project. Each project’s actual <code>AGENTS.md</code> files, including applicable directory-specific instructions, are supplied from the starting revision to all three groups. If those instructions state a tested rule, the case is classified as using documented guidance. Missing files are recorded as absent.</p>
              <ul className="plain-list">
                <li><strong>Code without a disclosed rule.</strong> Eligible cases do not state the target rule in their applicable AGENTS.md instructions. Other narrative disclosures are withheld consistently across the matched groups. The layer uses the remaining code evidence, or acknowledges that the rule cannot be established. A hidden policy that cannot be inferred is a test of uncertainty, not a rule the agent is expected to discover.</li>
                <li><strong>Using documentation.</strong> The declared documents are available. The assessment checks whether the layer understands their scope, preserves exceptions and notices disagreements with the code.</li>
              </ul>
              <p>Each claim must say where it came from. A rule copied from a guide will not be reported as a rule inferred from code. The verifier uses only the material allowed in that test; it cannot consult the hidden assessment to repair the guide.</p>
              <p>Only claims admitted by the verifier enter the guide. Preparation has a fixed budget and revision limit; when it ends, both guidance groups receive the same admitted subset, even if it is empty. Missing or incorrect guidance remains part of the result. After the guide is frozen, a separate assessment checks its support, provenance and coverage against the prepared case evidence. The verifier’s approval is not itself a score of guidance quality. The website’s examples are illustrations, not the guidance supplied to an experimental agent.</p>
            </Disclosure>
            <Disclosure id="isolation" title="How is withheld assessment material kept out of the inputs?">
              <p>Each role receives only its permitted input pack. Historical solutions and final assessment material stay outside coding and runtime-review environments. The <a className="text-link" href="#technical-setup">technical setup</a> explains the execution boundaries and permitted communication routes.</p>
              <p>The input audit must also look for disclosures in comments, tests, examples and dependencies. Removing the obvious guide does not establish that its contents have been withheld.</p>
              <p>Public code may already be familiar to a model from training. The first pilot therefore makes a limited claim: it compares whether prepared guidance and structured checking help on evidence-backed public-project tasks. It does not establish that a model inferred the rule entirely from the supplied code. Using matched models, tasks and budgets does not remove this limitation.</p>
              <p>Private variants that change the correct rule are a possible later extension, not a prerequisite for the first pilot. Writing the change and tests ourselves, or obtaining another AI’s agreement, would not by itself validate the case. Such a variant needs a meaningful requirement, a consistent implementation and independently justified assessment evidence. Ambiguous variants remain development material. Harmless renaming can check robustness, but cannot establish that the original project was unfamiliar.</p>
            </Disclosure>
          </DetailGroup>
        </div>
      </li>

      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">3</span><h3>Run the same task three ways</h3></div>
        <div className="method-step-content">
          <p>Separate agent attempts receive the same task and the same allowed project sources. What changes is the help they receive:</p>
          <ul className="method-groups">
            <li><strong>Sources only.</strong> The agent works out what matters from the code and available documentation.</li>
            <li><strong>Sources and guidance.</strong> The agent also receives the guide prepared in step 2.</li>
            <li><strong>Sources, guidance and interaction.</strong> The agent receives that same guide and consults the layer about its plan and actions.</li>
          </ul>
          <p>All three groups get ordinary review and opportunities to correct mistakes. The interactive group also receives targeted questions about how it applies the rules. The review-trigger rules and correction limits are the same across groups, and all reviewing counts towards the agreed budget.</p>
          <DetailGroup><Disclosure id="during-work" title="What does the checker do while the agent works?">
            <p><strong>Before the first edit,</strong> the interactive agent consults the layer and submits a plan. It explains what it will reuse, what it will change and which rules or exceptions apply. A separate checker assesses whether those proposed actions follow the evidence.</p>
            <p><strong>During implementation,</strong> the runner checks incoming code submissions against the approved plan. At the configured review points, and whenever a material change of approach is detected, it pauses further work and sends the plan and changes to the checker. The checker assesses the applicable rules and exceptions while the task is still in progress, so a blocking issue can be corrected before work continues.</p>
            <p><strong>After a check,</strong> the agent receives “proceed”, “revise” or “unresolved”, with a reason. The proposed limit is two correction rounds at each required review point. A necessary decision that remains unresolved, or failure to satisfy the check within that allowance, stops the attempt. Unrelated uncertainty is recorded without blocking otherwise valid work. Unfinished work remains in the assessment.</p>
            <p><strong>If the approach changes,</strong> a new dependency, a different component to reuse or a new claimed exception requires an updated plan. Tests must establish that the runner catches undeclared changes too. These in-run checks are triggered by submissions and detected changes; the checkpoint schedule and limits are defined before the run.</p>
            <p><strong>Before completion,</strong> every group submits its final code for review, with the same correction allowance. After completion or a stop, the code goes to independent evaluation and receives no further correction opportunity from that evaluator.</p>
            <p>The checker can see the task, plan, changes and permitted evidence. It cannot see the hidden answers or the coding agent’s private reasoning. It cannot rewrite the frozen guidance. If the guide is wrong, it can explain the conflict and request a source-supported change to the proposed action; that defect in the guide is recorded. Questions needing an owner’s authority remain unresolved; the procedure does not permit an unrecorded human answer during a run.</p>
            <p>Reviewers in the other groups can still identify mistakes and request corrections. They use their group’s sources and, where supplied, guidance. The intended difference is the structured consultation and targeted questions, not the mere presence of a reviewer. Instructions and budgets are specified and tested before runs.</p>
          </Disclosure></DetailGroup>
        </div>
      </li>

      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">4</span><h3>Judge the finished work and compare the cost</h3></div>
        <div className="method-step-content">
          <p>A separate evaluator assesses both the historical implementation and the agent’s change using the same criteria prepared in step 1:</p>
          <ul className="plain-list">
            <li><strong>Task correctness:</strong> does the implementation deliver the required behaviour?</li>
            <li><strong>Guardrail compliance:</strong> does it follow the applicable, evidence-supported rules and legitimate exceptions?</li>
          </ul>
          <p>If the historical code violates a guardrail and the agent avoids that violation while completing the task correctly, the agent receives credit for the improvement. A different valid solution is not penalised for differing from the original. Points and weighting are fixed before scored runs.</p>
          <p>The assessment is prepared from project evidence before the runs. It cannot impose a later policy or turn a repeated coding pattern into a mandatory rule without justification.</p>
          <p>The layer’s generated guidance is checked against that evidence too. A rule proposed by the layer cannot become a scoring requirement merely because the layer proposed it.</p>
          <p>Separate records show whether reviews raised unnecessary objections, whether the task was finished, and how much preparation and review cost. Refusals, invalid agent outputs and unfinished attempts remain outcomes. Genuine infrastructure failures and any retries are reported separately, under rules fixed before the runs.</p>
          <p>The first comparison tests whether prepared guidance helps. Comparing the two groups that receive guidance tests whether interaction adds a further benefit.</p>
          <DetailGroup>
            <Disclosure id="reliable-judge" title="How will the assessments be shown to be reliable?">
              <p>The verifier and runtime reviewers need reliability tests for the decisions they make. Separate assessors judge the frozen guidance, final code and review interactions. Each assessment job must be qualified for its own inputs and purpose; a verifier cannot grade its own success.</p>
              <ol className="plain-list">
                <li><strong>Develop the instructions.</strong> Use examples whose expected assessments are supported by project requirements, documented rules and reproducible tests. The historical implementation is evidence to examine, and may itself contain mistakes; it does not define the correct answer.</li>
                <li><strong>Set the pass criteria in advance.</strong> Decide the acceptable error rates and how much validation evidence is needed before seeing the results.</li>
                <li><strong>Test on fresh cases.</strong> Freeze the instructions, then test them on different kinds of project decisions. Examples used to improve the judge cannot also prove its reliability.</li>
                <li><strong>Measure its mistakes.</strong> Count incorrect work it accepts and correct work it rejects separately. Check that it accepts valid exceptions and recognises insufficient evidence. Repeat grading and vary presentation to see whether irrelevant differences change its verdict.</li>
              </ol>
              <p>The code judge does not see group labels, model names or the generated guide. A separate assessment checks whether review objections were justified by the evidence available at the time. Review transcripts may reveal the group, so that assessment is not fully blinded.</p>
              <p>The expected assessment must rest on reproducible behaviour or clear project evidence, with independent expertise where needed. Agreement between two AI models is not enough. If the evidence cannot settle a judgement, it remains unresolved.</p>
              <p>Scores are audited during the pilot. If an assessor or its criteria change, it must pass validation again, and all affected implementations are rescored consistently. A main-trial result used to repair the assessment becomes exploratory; confirmation requires fresh cases.</p>
              <p>Section 9A of the <a className="text-link" href={sitePath("/evidence/working-poc-plan.md")} download>working plan</a> contains the full qualification procedure.</p>
            </Disclosure>
            <Disclosure id="interpret-results" title="What conclusions would the comparison support?">
              <p>Useful guidance must be supported by evidence, improve later work and justify its cost. The guidance itself also needs assessment, so a correct code change does not conceal unsupported rules. A separate small diagnostic supplies a known rule directly to check whether the task could benefit from correct guidance at all.</p>
              <p>The first pilot’s scored task comparisons use eligible historical backtests. Authored development examples and any independently justified later variants are reported separately, as are tests with and without the relevant documentation. A task that states the target rule can test its application, but not the benefit of discovering it. Several tasks may test the same underlying decision. The analysis must account for that relationship rather than count every variation or repeated attempt as independent evidence. The number of cases and minimum worthwhile improvement are set before the main trial.</p>
              <p>A positive result would support the layer on the tested public-project tasks, with possible prior familiarity. It would not prove inference from previously unseen code. It would not establish universal necessity, owner approval of new rules, adoption by a team or the value of keeping guidance current across an organisation. Inconclusive and negative results would also inform revisions to Chapter 4.</p>
              <a className="text-link" href={chapterUrl} target="_blank" rel="noreferrer">Read Chapter 4 in the public playbook <ArrowUpRight size={16}/></a>
            </Disclosure>
          </DetailGroup>
        </div>
      </li>
    </ol>

    <div className="method-preparation">
      <h3>Validation precedes the main trial</h3>
      <p>The execution boundary is tested before any model calls. Each assessment role must qualify before the pilot uses its scores. A small pilot then tests the full procedure before a main trial supports conclusions. Findings from the pilot inform the method and size of the main trial.</p>
      <PageLink className="text-link" href="/progress">See preparation, decisions and results <ArrowRight size={16}/></PageLink>
    </div>
    <p className="caption">The <a className="text-link" href={sitePath("/evidence/working-poc-plan.md")} download>working experiment plan</a> records the full method and design decisions. The <PageLink className="text-link" href="/progress#evidence">evidence record and case library</PageLink> are on Progress &amp; findings.</p>
  </section>
</>}
