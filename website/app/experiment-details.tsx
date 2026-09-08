import { sitePath } from './site-path';
import { ArrowUpRight, ArrowRight } from 'lucide-react';
import { DetailGroup, Disclosure, RepositoryCards, EvidenceExplorer, EvidenceDownloads } from './details';
import { PageLink } from './page-link';
import { chapterUrl } from './ui';

export function ExperimentDetails(){return <>
  <section className="section-block" id="method">
    <div className="section-heading"><span className="section-no">04</span><div><span className="eyebrow">THE EXPERIMENT, STEP BY STEP</span><h2>How we intend to run the experiment</h2></div></div>
    <p className="section-intro">We will ask agents to make the same code change with different kinds of help. Then we will compare the work they produce and the effort it took. Here is the proposed sequence for one test.</p>

    <ol className="method-steps" aria-label="The four steps in one experiment">
      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">1</span><h3>Prepare a task we know how to assess</h3></div>
        <div className="method-step-content">
          <p>We choose a project rule with evidence we can inspect, then write a code-change task where that rule matters. Before an agent attempts it, we establish how to recognise a correct change, a real mistake and a valid exception. We keep this assessment outside the agent’s workspace.</p>
          <DetailGroup><Disclosure id="choose-case" title="How do we choose a task and establish the answer?">
            <p>We look for a published requirement or decision, then check its scope against the implementation. If the guide and code disagree, the assessment must explain the disagreement. Copying the guide is not enough.</p>
            <p>We prepare a valid solution and a deliberately incorrect change, and check that our tests distinguish them. We also include a legitimate exception or alternative so the scoring does not demand one particular implementation. If the evidence cannot settle the answer, that part of the case remains unresolved.</p>
            <p>The candidate projects are NetBox, Wagtail, Paperless-ngx and HTTPX. They offer different kinds of engineering decisions, but all four use Python and three use Django. They are not a representative sample of all software projects.</p>
            <RepositoryCards/>
          </Disclosure></DetailGroup>
        </div>
      </li>

      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">2</span><h3>Let the layer prepare its guidance</h3></div>
        <div className="method-step-content">
          <p>The layer examines the allowed project material without seeing the change task. It drafts guidance, and a separate verifier checks whether the evidence supports it. We save the resulting guide before revealing the task, and keep it unchanged during the run.</p>
          <DetailGroup>
            <Disclosure id="allowed-evidence" title="Does the layer read the documentation, or work the rule out from code?">
              <p>We test those two abilities separately.</p>
              <ul className="plain-list">
                <li><strong>Working it out from code.</strong> We remove the documents and other statements that reveal the target rule. The layer has to use the remaining code evidence, or acknowledge that the rule cannot be established.</li>
                <li><strong>Using documentation.</strong> We make the declared documents available. Here we assess whether the layer understands their scope, preserves exceptions and notices disagreements with the code.</li>
              </ul>
              <p>Each claim must say where it came from. A rule copied from a guide will not be reported as a rule inferred from code. The verifier uses only the material allowed in that test; it cannot consult our hidden assessment to repair the guide.</p>
              <p>Missing or incorrect guidance remains part of the result. We also assess unsupported claims and whether the layer recognises uncertainty. The website’s examples are illustrations, not the guidance we will give an experimental agent.</p>
            </Disclosure>
            <Disclosure id="isolation" title="How do we keep the withheld answers out of the run?">
              <p>Each attempt starts in a fresh container and fresh model conversations. Only declared files and network access are allowed. The reference answers and scoring stay outside. We record the actual model inputs, outputs and tool activity, and test that prohibited files and network destinations cannot be reached.</p>
              <p>We must also look for disclosures in comments, tests, examples and dependencies. Removing the obvious guide does not establish that its contents have been withheld.</p>
              <p>Public code may already be familiar to a model from training. Some tests will therefore use unpublished changes that alter the correct rule. We check whether the answer follows the changed code. Harmless renaming should leave the interpretation unchanged. These controls can make the test inspectable; they cannot prove that the original project was absent from training data.</p>
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
            <p><strong>After a check,</strong> the agent receives “proceed”, “revise” or “unresolved”, with a reason. The proposed limit is two correction rounds at each required review point. An unresolved decision, or failure to satisfy the check within that allowance, stops the attempt. We retain unfinished work for assessment.</p>
            <p><strong>If the approach changes,</strong> a new dependency, a different component to reuse or a new claimed exception requires an updated plan. The program controlling the run also compares submitted code with that plan. We must test that it catches undeclared changes of approach.</p>
            <p>The checker can see the task, plan, changes and permitted evidence. It cannot see the hidden answers or the coding agent’s private reasoning. It cannot rewrite the frozen guidance. Questions needing an owner’s authority remain unresolved; we do not insert an unrecorded human answer during a run.</p>
            <p>Reviewers in the other groups can still identify mistakes and request corrections. They use their group’s sources and, where supplied, guidance. The intended difference is the structured consultation and targeted questions, not the mere presence of a reviewer. Exact instructions and budgets still need to be specified and tested.</p>
          </Disclosure></DetailGroup>
        </div>
      </li>

      <li className="method-step">
        <div className="method-step-heading"><span className="method-step-number" aria-hidden="true">4</span><h3>Judge the finished work and compare the cost</h3></div>
        <div className="method-step-content">
          <p>A separate judge assesses the final code against the assessment prepared in step 1. We compare correct changes, missed requirements, unnecessary objections and unfinished attempts. We also count the effort spent preparing guidance, reviewing work and answering questions.</p>
          <p>The first comparison tells us whether prepared guidance helps. Comparing the two groups that receive guidance tells us whether interaction adds a further benefit.</p>
          <DetailGroup>
            <Disclosure id="reliable-judge" title="How do we know the judge is reliable?">
              <p>We first develop its scoring instructions using examples whose answers have been established independently. Then we fix those instructions and test the judge on different decision families. Examples used to improve it cannot also serve as independent validation.</p>
              <p>It must catch convincing but incorrect work, accept valid exceptions and recognise when evidence is insufficient. We measure errors it accepts and correct solutions it rejects separately. We also test whether repeated grading or irrelevant changes in presentation alter its verdict. Group labels and model names are removed from final code scoring; interaction records are assessed separately.</p>
              <p>Acceptable error rates and the amount of validation evidence must be fixed before validation results are seen. The four simple calibration records in the inventory are only starting material. We will audit scores during the pilot and revalidate any revised judge before rescoring all affected groups consistently.</p>
              <p>The verifier, runtime checker and final judge each need to pass tests for their own role. Two AI models agreeing does not establish a reference answer. Without independent expertise to settle an ambiguous case, we must rely on reproducible behaviour or clear published evidence, or leave that judgement unresolved.</p>
              <p>The complete proposed qualification procedure is in section 9A of the <a className="text-link" href={sitePath("/evidence/working-poc-plan.md")} download>working plan</a>. It has not yet been carried out.</p>
            </Disclosure>
            <Disclosure id="interpret-results" title="What would the comparison let us conclude?">
              <p>Useful guidance must be supported by evidence, improve later work and justify its cost. We will also assess the guidance itself, so a correct code change does not conceal unsupported rules. A separate small diagnostic supplies a known rule directly to check whether the task could benefit from correct guidance at all.</p>
              <p>Several tasks may test the same underlying decision. We will account for that relationship rather than count every variation or repeated attempt as independent evidence. The final number of cases and minimum worthwhile improvement remain to be chosen before the main trial.</p>
              <p>A positive result would support the layer in the situations tested. It would not establish universal necessity, owner approval of new rules, adoption by a team or the value of keeping guidance current across an organisation. An inconclusive or negative result would also inform how we revise Chapter 4.</p>
              <a className="text-link" href={chapterUrl} target="_blank" rel="noreferrer">Read Chapter 4 in the public playbook <ArrowUpRight size={16}/></a>
            </Disclosure>
          </DetailGroup>
        </div>
      </li>
    </ol>

    <div className="method-preparation">
      <h3>We will test the procedure before using it to draw conclusions</h3>
      <p>First we will write the missing instructions for the verifier, checker and judge, and work through one complete development case. We will then validate the components on separate material and run a small pilot. What we learn will help us fix the method and size of the main trial before it begins.</p>
      <PageLink className="text-link" href="/progress">See the current step and what remains <ArrowRight size={16}/></PageLink>
    </div>

    <DetailGroup><Disclosure id="method-records" title="Read the full plan or inspect the source evidence">
      <p>The working plan records the proposed method, unresolved choices and changes to the design. The case library contains candidate material; it is not a finished benchmark.</p>
      <EvidenceDownloads/><EvidenceExplorer/>
    </Disclosure></DetailGroup>
  </section>
</>}
