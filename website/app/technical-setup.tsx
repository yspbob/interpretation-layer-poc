import { ArrowRight, ArrowLeftRight, ArrowDown } from 'lucide-react';
import { DetailGroup, Disclosure } from './details';
import { PageLink } from './page-link';

export function TechnicalSetup(){return <section className="section-block" id="technical-setup">
  <div className="section-heading"><span className="section-no">05</span><div><span className="eyebrow">TECHNICAL SETUP</span><h2>How the components work together</h2></div></div>
  <p className="section-intro">A runner coordinates the experiment. It supplies each agent with its permitted inputs, passes review messages between roles, controls code execution and records the results. Agents receive separate working environments; the runner controls the connections between them.</p>

  <figure className="technical-diagram" aria-labelledby="technical-diagram-caption">
    <div className="technical-flow">
      <div className="technical-node"><span className="eyebrow">INPUTS</span><h3>Prepared input packs</h3><p>Pinned source files, applicable project instructions and each role’s permitted task material.</p></div>
      <ArrowRight className="technical-arrow" aria-hidden="true"/>
      <div className="technical-node technical-controller"><span className="eyebrow">OUTSIDE AGENT CONTROL</span><h3>Runner and controller</h3><p>Dispatch inputs, validate exchanges, enforce checkpoints and stop decisions, and record activity.</p></div>
      <ArrowLeftRight className="technical-arrow" aria-hidden="true"/>
      <div className="technical-node"><span className="eyebrow">SEPARATE ENVIRONMENTS</span><h3>Agent roles and code execution</h3><p>Each role receives its own context and workspace. Generated code executes in a restricted test environment.</p></div>
    </div>
    <div className="technical-handoff"><ArrowDown aria-hidden="true"/><span>After the attempt stops: final artifacts and recorded observations pass to evaluation.</span></div>
    <div className="technical-evaluation"><h3>Independent evaluation</h3><p>The evaluator receives the final code and separately held assessment criteria. Historical and agent implementations are assessed under the same rules. Final scores and hidden-test feedback do not return to the running agents.</p></div>
    <figcaption id="technical-diagram-caption">Planned data flow. Arrows represent permitted transfers through the runner; they do not imply shared agent storage or unrestricted connections.</figcaption>
  </figure>

  <DetailGroup>
    <Disclosure id="technical-inputs" title="What does each role receive?">
      <p>Each input pack has a manifest: a list of permitted files with hashes that identify their exact contents. The runner checks the manifest before dispatch and starts a fresh context for each role and run.</p>
      <ul className="plain-list">
        <li><strong>Drafter and verifier:</strong> the permitted project evidence and instructions. The verifier also receives the proposed claims. Neither receives the later change task or final assessment.</li>
        <li><strong>Coder and reviewer:</strong> the task, permitted sources and applicable project instructions. GUIDE and INTERACT also receive the same frozen generated guidance. Reviewers receive the submitted plan and changes; they do not receive the coder’s private reasoning.</li>
        <li><strong>Assessment roles:</strong> a guidance assessor checks the frozen guide against separately prepared evidence; an intervention assessor checks review decisions against what was knowable at the time. These records stay outside the live roles.</li>
        <li><strong>Final code judge:</strong> the code to assess, task requirements, guardrail criteria and independently produced test observations. Origin, treatment and model labels are withheld for individual code scoring.</li>
      </ul>
      <p>The project’s actual <code>AGENTS.md</code> files, including applicable directory-specific instructions, are taken from the backtest’s starting revision. The same applicable files are supplied across all three groups. Their absence is recorded rather than filled with invented instructions. If they state a tested rule, that case is classified as using documented guidance.</p>
    </Disclosure>
    <Disclosure id="technical-execution" title="How are plans, reviews and model calls coordinated?">
      <p>The runner tracks the state of each attempt: awaiting a plan, awaiting review, permitted to work, awaiting a revision, or stopped. It accepts only exchanges allowed for that role and stage. A material change of approach returns the attempt to plan review. Unresolved decisions, exhausted limits and containment failures trigger the specified stop procedure.</p>
      <p>During implementation, incoming code submissions are checked against the approved plan. The runner pauses at configured review points and on detected material changes, then passes the relevant plan and code to the reviewer. Work resumes only after the required decision permits it. The same review-trigger rules and correction limits apply across all three groups. Different approaches can trigger different checks; the runner must enforce pauses on new coding turns and mutating tool actions.</p>
      <p>A model gateway makes the authorised model calls and records usage. Credentials remain outside the agent workspace. The controller passes only the required questions, submissions and decisions between roles; it does not expose a general command interface. Checking a message’s format does not establish that its content is trustworthy. Gateway requests have fixed model-provider destinations and bounded payloads; the gateway cannot serve as a general URL fetcher.</p>
      <p>Candidate code runs separately from the controller and the full assessment store. Common task checks may return permitted feedback during work. Final evaluation uses a separate assessment path after the attempt ends. The evaluator must test resistance to modified tests and forged success reports, rather than trust a candidate’s claim that its checks passed.</p>
    </Disclosure>
    <Disclosure id="technical-isolation" title="How is access beyond the test environment restricted?">
      <p>The design requires agents to have no general access to the host machine, other runs or external services. The runner still needs narrowly defined routes to supply inputs, pass permitted review messages and collect outputs. Those interfaces are part of the isolation boundary and must be tested too.</p>
      <ul className="plain-list">
        <li><strong>Restrict and record communication.</strong> Permitted exchanges pass through the external controller. Other routes must be blocked, including indirect communication through shared services.</li>
        <li><strong>Minimise and test exposed services.</strong> Each agent receives only the tools, storage and network capabilities its task requires. Every exposed capability is reviewed for unintended access. The controller and gateway are trusted components whose versions, permissions and behaviour must also be tested. Preinstalled, read-only dependencies are one way to remove a live service from the execution environment.</li>
        <li><strong>Protect the host and assessment.</strong> Host files, credentials and administrative controls stay outside agent access. Workspaces and caches cannot provide shared writable channels. The controller, stop mechanism and assessment records remain protected from agent writes.</li>
        <li><strong>Test attempted boundary crossings.</strong> Controlled probes check file access, communication between roles and runs, direct and indirect network access, and attempts to alter enforcement. The relevant checks are repeated after environment changes. Detected failures stop affected runs and preserve the evidence.</li>
      </ul>
      <p>The Hugging Face incident demonstrated how a shared package service could become an unintended message board and a route to the internet. It motivates reviewing all exposed services, not only package installation. <a className="text-link" href="https://openai.com/index/hugging-face-incident-and-the-road-ahead/" target="_blank" rel="noreferrer">OpenAI’s account</a> and <a className="text-link" href="https://huggingface.co/blog/agent-intrusion-technical-timeline" target="_blank" rel="noreferrer">Hugging Face’s technical account</a> describe the incident.</p>
      <p>The runner must record its isolation boundaries and the results of tests that attempt to cross them. These tests establish protection against the routes examined, with remaining limitations stated. They cannot guarantee that escape is impossible.</p>
      <p><strong>Architecture choice to resolve:</strong> a disposable virtual machine around restricted execution is a candidate design. The isolation technology and controller interfaces must be selected and tested against these requirements; the diagram does not prescribe a specific platform.</p>
    </Disclosure>
    <Disclosure id="technical-records" title="What makes a run inspectable and repeatable?">
      <p>Each run records the source revision, file manifests, environment version, model settings, exact supplied inputs and returned outputs, tool activity, review decisions, revisions, stops and resource use. An external audit store retains these records so an agent cannot rewrite its own history. Collection checks paths, symlinks, archive entries, output limits and message order before accepting untrusted artifacts.</p>
      <p>The assessment records task correctness and guardrail compliance separately, including justified improvements over historical code, new violations and unresolved evidence. Public reports exclude credentials and sealed assessment material. Exact models, budgets, scoring weights and acceptance limits belong in the run configuration, fixed before the relevant scored runs.</p>
    </Disclosure>
  </DetailGroup>
  <p className="caption">The method defines the required behaviour. <PageLink className="text-link" href="/progress#technical-status">Progress &amp; findings records component readiness and open technical choices.</PageLink></p>
</section>}
