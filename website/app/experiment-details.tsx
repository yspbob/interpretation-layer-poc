import { sitePath } from './site-path';
import { ArrowUpRight, ArrowRight } from 'lucide-react';
import { DetailGroup, Disclosure, RepositoryCards, EvidenceExplorer, EvidenceDownloads } from './details';
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
          <p>For each backtest, case preparation records the task, the historical implementation and the guardrails that applied to that work. Before an agent attempts it, the assessment establishes the required behaviour, relevant rules and legitimate exceptions. The historical solution and its assessment stay outside the agent’s workspace.</p>
          <DetailGroup><Disclosure id="choose-case" title="How are tasks selected and assessment criteria established?">
            <p>Each case starts from a published requirement or decision, with its scope checked against the implementation. The assessment must explain any disagreement between the rules and historical code, including legitimate exceptions. Neither is automatically treated as correct.</p>
            <p>Each case needs a valid solution and a deliberately incorrect change, with tests that distinguish them. It also needs a legitimate exception or alternative so the scoring does not demand one particular implementation. If the evidence cannot settle the answer, that part of the case remains unresolved.</p>
            <p>The candidate projects are NetBox, Wagtail, Paperless-ngx and HTTPX. They offer different kinds of engineering decisions, but all four use Python and three use Django. They are not a representative sample of all software projects.</p>
            <RepositoryCards/>
          </Disclosure></DetailGroup>
        </div>
      </li>

      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">2</span><h3>Let the layer prepare its guidance</h3></div>
        <div className="method-step-content">
          <p>The layer examines the allowed project material without seeing the change task. It drafts guidance, and a separate verifier checks whether the evidence supports it. The resulting guide is saved before the task is revealed and stays unchanged during the run.</p>
          <DetailGroup>
            <Disclosure id="allowed-evidence" title="Does the layer read the documentation, or work the rule out from code?">
              <p>The experiment tests those two abilities separately.</p>
              <ul className="plain-list">
                <li><strong>Working it out from code.</strong> The input pack excludes documents and other statements that reveal the target rule. The layer has to use the remaining code evidence, or acknowledge that the rule cannot be established.</li>
                <li><strong>Using documentation.</strong> The declared documents are available. The assessment checks whether the layer understands their scope, preserves exceptions and notices disagreements with the code.</li>
              </ul>
              <p>Each claim must say where it came from. A rule copied from a guide will not be reported as a rule inferred from code. The verifier uses only the material allowed in that test; it cannot consult the hidden assessment to repair the guide.</p>
              <p>Missing or incorrect guidance remains part of the result. The assessment also covers unsupported claims and whether the layer recognises uncertainty. The website’s examples are illustrations, not the guidance supplied to an experimental agent.</p>
            </Disclosure>
            <Disclosure id="isolation" title="How will agents stay within their boundaries?">
              <p><strong>Containment is a requirement before model runs. It has not yet been implemented or validated.</strong> The design requires isolation for every role and run, with fresh conversations, fixed input packs and private working storage. Agents must not share writable caches, workspaces or access to one another’s history.</p>
              <p>The Hugging Face incident shows why separate conversations are insufficient. Agents used a shared package service as an unauthorised message board and reached the internet through it. <a className="text-link" href="https://openai.com/index/hugging-face-incident-and-the-road-ahead/" target="_blank" rel="noreferrer">Read OpenAI’s account</a> and <a className="text-link" href="https://huggingface.co/blog/agent-intrusion-technical-timeline" target="_blank" rel="noreferrer">Hugging Face’s technical account</a>.</p>
              <ul className="plain-list">
                <li><strong>Control every exchange.</strong> An external controller must validate permitted messages between roles. Other network access must be blocked, including indirect routes through supporting services.</li>
                <li><strong>Prepare dependencies beforehand.</strong> Runs receive fixed, read-only dependencies and no live package service. A required environment change stops the attempt for review.</li>
                <li><strong>Protect assessment and enforcement.</strong> Historical solutions and final assessment material stay outside the coding and checking environments. The final judge receives only its assessment pack. Candidate code runs separately from the scorer; credentials, permissions, logs and stop controls remain outside agent-writable environments.</li>
                <li><strong>Test attempted boundary crossings.</strong> Before model calls, controlled tests must cover unauthorised communication, answer access, indirect internet access and attempts to alter enforcement. An external supervisor must stop affected runs and preserve evidence if containment fails.</li>
              </ul>
              <p>The current file-broker checks do not establish containment. The runner must record its actual boundaries and test results. The claim will be protection against specified, tested escape paths, with remaining limitations stated; absolute prevention cannot be guaranteed.</p>
              <p>The input audit must also look for disclosures in comments, tests, examples and dependencies. Removing the obvious guide does not establish that its contents have been withheld.</p>
              <p>Public code may already be familiar to a model from training. Some tests will therefore use unpublished changes that alter the correct rule. The assessment checks whether the answer follows the changed code. Harmless renaming should leave the interpretation unchanged. These controls can make the test inspectable; they cannot prove that the original project was absent from training data.</p>
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
          <p>All three groups get ordinary review and opportunities to correct mistakes. The interactive group also receives targeted questions about how it applies the rules. The required review points and correction limits are the same across groups, and all reviewing counts towards the agreed budget.</p>
          <DetailGroup><Disclosure id="during-work" title="What does the checker do while the agent works?">
            <p><strong>Before the first edit,</strong> the interactive agent consults the layer and submits a plan. It explains what it will reuse, what it will change and which rules or exceptions apply. A separate checker assesses whether those proposed actions follow the evidence.</p>
            <p><strong>After a check,</strong> the agent receives “proceed”, “revise” or “unresolved”, with a reason. The proposed limit is two correction rounds at each required review point. An unresolved decision, or failure to satisfy the check within that allowance, stops the attempt. Unfinished work remains in the assessment.</p>
            <p><strong>If the approach changes,</strong> a new dependency, a different component to reuse or a new claimed exception requires an updated plan. The program controlling the run also compares submitted code with that plan. Tests must establish that it catches undeclared changes of approach.</p>
            <p>The checker can see the task, plan, changes and permitted evidence. It cannot see the hidden answers or the coding agent’s private reasoning. It cannot rewrite the frozen guidance. Questions needing an owner’s authority remain unresolved; the procedure does not permit an unrecorded human answer during a run.</p>
            <p>Reviewers in the other groups can still identify mistakes and request corrections. They use their group’s sources and, where supplied, guidance. The intended difference is the structured consultation and targeted questions, not the mere presence of a reviewer. Exact instructions and budgets still need to be specified and tested.</p>
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
          <p>If the historical code violates a guardrail and the agent avoids that violation while completing the task correctly, the agent receives credit for the improvement. A different valid solution is not penalised for differing from the original. Exact points and weighting still need to be defined.</p>
          <p>The scoring rules are established independently of the layer’s generated guidance, before the comparison. A rule invented by the layer cannot earn it credit. The assessment also records unnecessary objections, unfinished attempts and the cost of preparation and review.</p>
          <p>The first comparison tests whether prepared guidance helps. Comparing the two groups that receive guidance tests whether interaction adds a further benefit.</p>
          <DetailGroup>
            <Disclosure id="reliable-judge" title="How will the judge’s reliability be established?">
              <p>Scoring instructions are first developed using examples whose answers have been established independently. The instructions are then frozen and the judge is tested on different decision families. Examples used to improve it cannot also serve as independent validation.</p>
              <p>It must catch convincing but incorrect work, accept valid exceptions and recognise when evidence is insufficient. Validation measures errors it accepts and correct solutions it rejects separately. It also tests whether repeated grading or irrelevant changes in presentation alter its verdict. Group labels and model names are removed from final code scoring; interaction records are assessed separately.</p>
              <p>Acceptable error rates and the amount of validation evidence must be fixed before validation results are seen. The four simple calibration records in the inventory are only starting material. Pilot scores will be audited, and any revised judge must pass validation again before all affected groups are rescored consistently.</p>
              <p>The verifier, runtime checker and final judge each need to pass tests for their own role. Two AI models agreeing does not establish that an assessment is correct. Without independent expertise to settle an ambiguous case, the judgement must rest on reproducible behaviour or clear published evidence, or remain unresolved.</p>
              <p>The complete proposed qualification procedure is in section 9A of the <a className="text-link" href={sitePath("/evidence/working-poc-plan.md")} download>working plan</a>. It has not yet been carried out.</p>
            </Disclosure>
            <Disclosure id="interpret-results" title="What conclusions would the comparison support?">
              <p>Useful guidance must be supported by evidence, improve later work and justify its cost. The guidance itself also needs assessment, so a correct code change does not conceal unsupported rules. A separate small diagnostic supplies a known rule directly to check whether the task could benefit from correct guidance at all.</p>
              <p>Several tasks may test the same underlying decision. The analysis must account for that relationship rather than count every variation or repeated attempt as independent evidence. The final number of cases and minimum worthwhile improvement remain to be chosen before the main trial.</p>
              <p>A positive result would support the layer in the situations tested. It would not establish universal necessity, owner approval of new rules, adoption by a team or the value of keeping guidance current across an organisation. Inconclusive and negative results would also inform revisions to Chapter 4.</p>
              <a className="text-link" href={chapterUrl} target="_blank" rel="noreferrer">Read Chapter 4 in the public playbook <ArrowUpRight size={16}/></a>
            </Disclosure>
          </DetailGroup>
        </div>
      </li>
    </ol>

    <div className="method-preparation">
      <h3>The procedure needs testing before its results can support conclusions</h3>
      <p>Component contracts and one development case now exist, with scripted decisions and executable checks. Isolated role execution and containment testing are the next implementation task, followed by component validation on separate material and a small pilot. Those findings will inform the method and size of the main trial before it begins.</p>
      <PageLink className="text-link" href="/progress">See the current step and what remains <ArrowRight size={16}/></PageLink>
    </div>

    <DetailGroup><Disclosure id="method-records" title="Read the full plan or inspect the source evidence">
      <p>The working plan records the proposed method, unresolved choices and changes to the design. The case library contains candidate material; it is not a finished benchmark.</p>
      <EvidenceDownloads/><EvidenceExplorer/>
    </Disclosure></DetailGroup>
  </section>
</>}
