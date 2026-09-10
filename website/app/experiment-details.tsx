import { sitePath } from './site-path';
import { ArrowUpRight, ArrowRight } from 'lucide-react';
import { DetailGroup, Disclosure, RepositoryCards } from './details';
import { PageLink } from './page-link';
import { chapterUrl } from './ui';
import { ProductionDifference } from './production-difference';
import { FamiliarityChecks } from './familiarity-checks';

export function ExperimentDetails(){return <>
  <section className="section-block" id="method">
    <div className="section-heading"><span className="section-no">04</span><div><span className="eyebrow">THE EXPERIMENT, STEP BY STEP</span><h2>The coding comparison in Phases 2 and 3</h2></div></div>
    <p className="section-intro">Within the selected repository, we will ask agents to make the same code change with different kinds of help. We will compare the work they produce and the effort it took. The sequence below starts with case selection and guidance preparation. The same guide can then be used for several compatible tasks.</p>

    <ol className="method-steps" aria-label="The four steps in one experiment">
      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">1</span><h3>Choose a task and establish how to judge the result</h3></div>
        <div className="method-step-content">
          <p>Each test will ask an agent to repeat a real change from a project’s history. Before the agent starts, the case record must explain what that change needed to achieve and which project rules applied at the time. Those rules need supporting evidence. A pattern repeated in code is not automatically a requirement. The original solution and the assessment of it stay hidden from the agent.</p>
          <DetailGroup><Disclosure id="choose-case" title="How are tasks selected and assessment criteria established?">
            <p>We inspected one version of each repository to find potential test cases. For a selected task, we will return to the code as it stood before the original change. That may be a different version from the one initially inspected.</p><p>The task requirements and project rules must also belong to that time. Later documentation cannot introduce an obligation that the original developer did not have.</p>
            <p><strong>Start with the evidence.</strong> Each case uses a published requirement or decision. Its scope is checked against the code, and any disagreement is recorded. Neither the documentation nor the implementation is assumed to be correct.</p>
            <p><strong>Check that the assessment can tell the difference.</strong> Each case includes:</p><ul className="plain-list"><li>A valid solution.</li><li>A deliberately incorrect change.</li><li>A legitimate exception or alternative.</li></ul><p>The tests and source evidence must show why the valid solutions are acceptable and the incorrect change is not. A second valid solution can provide the alternative. We will not invent an exception just to complete the list.</p><p>If the evidence cannot settle an important requirement, the case stays out of the scored comparison. Other uncertainties remain recorded. Passing a few tests is not enough if they miss behaviour that matters to the task.</p>
            <p><strong>Keep the coverage in perspective.</strong> The existing candidate pool covers NetBox, Wagtail, Paperless-ngx and HTTPX. The first trial will select one of them and a small set of distinct decision families. Screening four repositories does not commit the trial to running all four.</p>
            <RepositoryCards/>
          </Disclosure></DetailGroup>
        </div>
      </li>

      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">2</span><h3>Prepare and verify guidance before the coding tasks begin</h3></div>
        <div className="method-step-content">
          <p>The interpretation layer’s drafter examines the project files it is allowed to read and proposes guidance. A separate verifier checks whether the evidence supports each claim.</p><p>Neither receives the later coding tasks. We save the accepted guidance before revealing those tasks, then reuse it for the associated comparisons. The drafter does not start again for every agent attempt.</p>
          <p>The guide belongs to a specific code version and set of permitted sources. Different repositories, historical versions or conditions for source access may need different guides. We choose the files the drafter may read without using the hidden solution to guide that choice. Otherwise, even the selection of files could give away the answer.</p>
          <ProductionDifference production="An initial review would reconstruct candidate rules from the existing system. After verification and owner approval, agents would reuse the released guidance. Later reviews would examine changed evidence, new exceptions and possible new rules." poc="The drafter and verifier prepare a fixed guidance version for its declared tasks. The verifier’s acceptance means that a claim has evidence support; it is not owner approval. The guide stays unchanged while those tasks are compared." limit="The pilot can examine preparation and repeated use. It cannot show that nightly reviews or another maintenance schedule keep production guidance up to date."/>
          <DetailGroup>
            <Disclosure id="allowed-evidence" title="Does the layer read the documentation, or work the rule out from code?">
              <p>We want to distinguish reading a rule in documentation from working it out through code. The experiment therefore uses two sets of permitted inputs. A model may already know the project in either case.</p><p> Each project’s actual <code>AGENTS.md</code> files, including applicable instructions for the relevant directories, are supplied from the starting revision to every group in the comparison. If those instructions state a tested rule, the case is classified as using documented guidance. Missing files are recorded as absent.</p>
              <ul className="plain-list">
                <li><strong>Code without a disclosed rule.</strong> Eligible cases do not state the target rule in their applicable AGENTS.md instructions. Other written material that gives away the rule is withheld from every group in this test. The same restrictions apply to each group. The layer uses the remaining code evidence, or acknowledges that the rule cannot be established. If a policy is hidden and the code offers no way to work it out, we cannot expect the agent to discover it. We can test whether the layer recognises that it does not have enough evidence.</li>
                <li><strong>Using documentation.</strong> The declared documents are available. The assessment checks whether the layer understands their scope, preserves exceptions and notices disagreements with the code.</li>
              </ul>
              <p>Each claim must say where it came from. A rule copied from a guide will not be reported as a rule inferred from code. The verifier uses only the material allowed in that test; it cannot consult the hidden assessment to repair the guide.</p>
              <p>Only claims accepted by the verifier enter the guide. Preparation stops when its budget or allowed revisions are exhausted. Both groups then receive the same accepted claims. If none were accepted, both receive an empty guide.</p><p>We retain that outcome rather than trying again until a useful guide appears. Missing or incorrect guidance is part of what the experiment needs to measure.</p><p>After the guide is saved, a separate assessor checks its quality. That assessment asks whether its claims are supported, where they came from and whether important requirements are missing. The verifier cannot provide the independent verdict on its own work.</p><p>The website’s examples are illustrations. The actual guidance supplied to an experimental agent will be prepared under this procedure.</p>
            </Disclosure>
            <Disclosure id="familiarity-checks" title="Can the model already recall the project or the historical fix?"><FamiliarityChecks/></Disclosure>
            <Disclosure id="isolation" title="How is withheld assessment material kept out of the inputs?">
              <p>Each role receives only its permitted input pack. Historical solutions and final assessment material stay outside coding and environments used during work and review. The <a className="text-link" href="#technical-setup">technical setup</a> explains the execution boundaries and permitted communication routes.</p>
              <p>The input audit must also look for disclosures in comments, tests, examples and dependencies. Removing the obvious guide does not establish that its contents have been withheld.</p>
              <p>Public code may already be familiar to a model from training. The first pilot therefore makes a limited claim: it compares whether prepared guidance and structured checking help on tasks from public projects whose requirements have supporting evidence. It does not establish that a model inferred the rule entirely from the supplied code. Using matched models, tasks and budgets does not remove this limitation.</p>
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
            <li><strong>Sources and prepared guidance.</strong> The agent also receives the guide prepared in step 2.</li>
            <li><strong>Sources, prepared guidance and interaction.</strong> The agent receives that same guide and consults the layer about its plan and actions.</li>
          </ul>
          <p className="caption">The technical plan calls these groups DIRECT, GUIDE and INTERACT, in the same order.</p>
          <p>All three groups get ordinary review and opportunities to correct mistakes. The interactive group also receives targeted questions about how it applies the rules. The rules that trigger review and correction limits are the same across groups, and all reviewing counts towards the agreed budget.</p>
          <DetailGroup><Disclosure id="during-work" title="What does the checker do while the agent works?">
            <p><strong>Before the first edit,</strong> the interactive agent consults the layer and submits a plan. It explains what it will reuse, what it will change and which rules or exceptions apply. A separate checker assesses whether those proposed actions follow the evidence.</p>
            <p><strong>During implementation,</strong> the runner checks incoming code submissions against the approved plan. At the configured review points, and whenever a material change of approach is detected, it pauses further work and sends the plan and changes to the checker. The checker assesses the applicable rules and exceptions while the task is still in progress, so a blocking issue can be corrected before work continues.</p>
            <p><strong>After a check,</strong> the agent receives “proceed”, “revise” or “unresolved”, with a reason. The proposed limit is two correction rounds at each required review point. If the task needs a decision that remains unresolved, the attempt stops. It also stops if the agent cannot satisfy the check within the correction allowance.</p><p>Uncertainty unrelated to completing the task is recorded without blocking valid work. Unfinished work still goes to assessment.</p>
            <p><strong>If the approach changes,</strong> a new dependency, a different component to reuse or a new claimed exception requires an updated plan. Tests must establish that the runner catches undeclared changes too. These checks during work are triggered by submissions and detected changes; the checkpoint schedule and limits are defined before the run.</p>
            <p><strong>Before completion,</strong> every group submits its final code for review, with the same correction allowance. After completion or a stop, the code goes to independent evaluation and receives no further correction opportunity from that evaluator.</p>
            <p>The checker can see the task, plan, changes and permitted evidence. It cannot see the hidden assessment answers or the coding agent’s private reasoning.</p><p>The checker cannot rewrite the saved guidance. If it finds that the guide conflicts with the sources, it can explain the conflict and ask the agent to change its proposed action. The defect in the guide stays in the record.</p><p>Questions needing an owner’s authority remain unresolved. We cannot settle them by supplying an unrecorded human answer during a run.</p>
            <p>Reviewers in the other groups can still identify mistakes and request corrections. They use their group’s sources and, where supplied, guidance. The intended difference is the structured consultation and targeted questions, not the mere presence of a reviewer. Instructions and budgets are specified and tested before runs.</p>
          </Disclosure></DetailGroup>
        </div>
      </li>

      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">4</span><h3>Assess the work and record its cost</h3></div>
        <div className="method-step-content">
          <p>A separate evaluator assesses both the historical implementation and the agent’s change using the same criteria prepared in step 1:</p>
          <ul className="plain-list">
            <li><strong>Task correctness:</strong> does the implementation deliver the required behaviour?</li>
            <li><strong>Guardrail compliance:</strong> does it follow the applicable project rules, including legitimate exceptions? Those rules must have supporting evidence.</li>
          </ul>
          <p>If the historical code violates a guardrail and the agent avoids that violation while completing the task correctly, the agent receives credit for the improvement. A different valid solution is not penalised for differing from the original. Points and weighting are fixed before scored runs.</p>
          <p>The assessment is prepared from project evidence before the runs. It cannot impose a later policy or turn a repeated coding pattern into a mandatory rule without justification.</p>
          <p>The layer’s generated guidance is checked against that evidence too. A rule proposed by the layer cannot become a scoring requirement merely because the layer proposed it.</p>
          <p>We also record whether reviews raised unnecessary objections, whether the task was finished and what the work cost.</p><p>An agent refusing the task, returning an invalid response or leaving work unfinished is an outcome of the method. A genuine failure of the surrounding infrastructure is recorded separately. The rules for handling failures and retries are fixed before the runs.</p>
          <ProductionDifference production="A team would assess whether changes meet its requirements and whether the layer helps its work over time. Operational review and maintenance decisions would involve the responsible people." poc="After an attempt ends, separate assessors examine the saved guidance, code and review decisions against prepared evidence. Historical code is assessed by the same criteria and may itself be wrong. Hidden final scores do not return to the working agent." limit="This independent assessment is part of the research design. It does not replace production accountability or demonstrate a working organisational approval process."/>
          <p>The first comparison tests whether prepared guidance helps. Comparing the two groups that receive guidance tests whether interaction adds a further benefit.</p>
          <DetailGroup>
            <Disclosure id="reliable-judge" title="How will the assessments be shown to be reliable?">
              <p>We need to check every component that makes a judgement. During work, the verifier decides which claims can enter the guide, and reviewers decide whether the agent may continue.</p><p>Afterwards, separate assessors judge the saved guide, final code and review decisions. The verifier cannot provide the independent verdict on its own work.</p><p>Each component must be tested on the kind of decision it will make. Its test must give it only the information it will receive in that role. The procedure is:</p>
              <ol className="plain-list">
                <li><strong>Develop the instructions.</strong> Use examples whose expected assessments are supported by project requirements, documented rules and reproducible tests. The historical implementation may itself contain mistakes. It is evidence to examine, rather than the definition of a correct answer.</li>
                <li><strong>Set the pass criteria in advance.</strong> Decide the acceptable error rates and how much validation evidence is needed before seeing the results.</li>
                <li><strong>Test on fresh cases.</strong> Freeze the instructions, then test them on different kinds of project decisions. Examples used to improve the judge cannot also prove its reliability.</li>
                <li><strong>Measure its mistakes.</strong> Count incorrect work it accepts and correct work it rejects separately. Check that it accepts valid exceptions and recognises insufficient evidence. Repeat grading and vary presentation to see whether irrelevant differences change its verdict.</li>
              </ol>
              <p>The code judge does not see group labels, model names or the generated guide. A separate assessment checks whether review objections were justified by the evidence available at the time. Review transcripts may reveal the group, so that assessment is not fully blinded.</p>
              <p>The expected verdict must be justified by tests that can be repeated or by clear project evidence. Where that is not enough, independent expertise is needed. Agreement between two AI models is not enough. If the evidence cannot settle a judgement, it remains unresolved.</p>
              <p>We will audit scores during the pilot. If an assessor or its criteria change, it must pass validation again. Every affected implementation must then be scored under the revised criteria.</p><p>If a result from the main trial helps us repair the assessment, it becomes development evidence. We will need fresh cases to test the revised method independently.</p>
              <p>Section 9A of the <a className="text-link" href={sitePath("/evidence/working-poc-plan.md")} download>working plan</a> contains the full qualification procedure.</p>
            </Disclosure>
            <Disclosure id="interpret-results" title="What conclusions would the comparison support?">
              <p>To justify the layer, its guidance must have evidence behind it, help with later work and be worth the cost. We assess the guidance itself as well as the code. A successful code change could otherwise conceal unsupported rules in the guide.</p><p>We will also run a small, separate check that gives the agent a known correct rule directly. This asks whether the task could benefit from good guidance at all.</p>
              <p>For the first pilot, agents will repeat real changes previously made in the selected projects. Each task must first pass the checks on its requirements, evidence and assessment.</p>
              <p>Authored development examples and any independently justified later variants are reported separately, as are tests with and without the relevant documentation. A task that states the target rule can test its application, but not the benefit of discovering it.</p>
              <p>Several tasks may test the same underlying decision. The analysis must account for that relationship rather than count every variation or repeated attempt as independent evidence. The first trial will report these relationships and the variation it observes. A separate confirmation study would use that evidence to set a justified sample before its results are seen.</p>
              <p>A positive result would support using the layer for the kinds of public project tasks we tested. The model may already know some of that code, so we could not claim it discovered every rule from unfamiliar sources.</p><p>The pilot also cannot establish that every organisation needs the layer, that an owner approves its rules or that a team would adopt it. Keeping guidance current across an organisation needs a later study.</p><p>Negative and inconclusive results would also inform revisions to Chapter 4.</p>
              <a className="text-link" href={chapterUrl} target="_blank" rel="noreferrer">Read Chapter 4 in the public playbook <ArrowUpRight size={16}/></a>
            </Disclosure>
          </DetailGroup>
        </div>
      </li>
    </ol>

    <div className="method-preparation">
      <h3>When the coding comparison is complete</h3>
      <p>The trial must leave an inspectable record of its inputs, guidance, work, reviews, failures and costs. The report will explain which controls worked within their tested scope and what remains uncertain.</p><p>We then decide whether to proceed, repair the procedure, narrow the question or stop. A favourable result is not required. Independent confirmation after the three phases is a separate decision, using fresh cases.</p>
      <PageLink className="text-link" href="/progress">See preparation, decisions and results <ArrowRight size={16}/></PageLink>
    </div>
    <p className="caption">The <a className="text-link" href={sitePath("/evidence/working-poc-plan.md")} download>working experiment plan</a> records the full method and design decisions. The <PageLink className="text-link" href="/progress#evidence">evidence record and case library</PageLink> are on Progress &amp; findings.</p>
  </section>
</>}
