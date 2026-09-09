import { RuntimeDiagram } from './runtime-diagram';
import { DetailGroup, Disclosure } from './details';
import { PageLink } from './page-link';

export function TechnicalSetup(){return <section className="section-block" id="technical-setup">
  <div className="section-heading"><span className="section-no">05</span><div><span className="eyebrow">TECHNICAL SETUP</span><h2>How the components work together</h2></div></div>
  <p className="section-intro">A runner coordinates the experiment. It supplies each agent with its permitted inputs, passes review messages between roles, controls code execution and records the results. Agents receive separate working environments; the runner controls the connections between them.</p>

  <RuntimeDiagram/>

  <section className="technology-section" id="tools-technologies" aria-labelledby="tools-technologies-title">
    <h3 id="tools-technologies-title">Tools and technologies</h3>
    <p>The experiment needs tools for coordination, model access, isolation, assessment and record keeping. The table names the products and libraries selected for the proposed implementation and identifies the remaining choices. The <PageLink className="text-link" href="/progress#prototype-tools">H04 prototype’s implemented tools</PageLink> are documented on Progress &amp; findings.</p>
    <table className="technology-table">
      <caption className="sr-only">Proposed technologies, their purpose and selection status</caption>
      <thead><tr><th scope="col">Component</th><th scope="col">Technology and reason</th><th scope="col">Choice</th></tr></thead>
      <tbody>
        <tr><th scope="row">Controller</th><td><strong>CPython 3.12: asyncio and subprocess.</strong> Project code dispatches roles, enforces checkpoints and calls VBoxManage with fixed argument lists. No agent orchestration framework is included.</td><td>Chosen for implementation</td></tr>
        <tr><th scope="row">Record validation</th><td><strong>Pydantic 2.</strong> Strict schemas reject unknown fields and wrong types. Separate controller checks enforce byte limits, path permissions, role identity and state transitions.</td><td>Chosen for implementation</td></tr>
        <tr><th scope="row">Virtual machine</th><td><strong>Oracle VirtualBox 7.2 with VBoxManage.</strong> The controller creates a disposable clone, starts it and forcibly stops it when required. Host compatibility must be tested.</td><td>Chosen; compatibility gate</td></tr>
        <tr><th scope="row">Guest system</th><td><strong>Ubuntu Server 24.04 LTS, amd64.</strong> A minimal Linux guest holds the launcher and preinstalled dependencies. All VM network adapters are disabled during execution.</td><td>Chosen for implementation</td></tr>
        <tr><th scope="row">Containers</th><td><strong>Rootless Podman with crun.</strong> Linux cgroup v2 enforces resource limits; seccomp restricts system calls. Each tool batch has a private workspace, no network and no exposed runtime socket.</td><td>Chosen; enforcement to test</td></tr>
        <tr><th scope="row">Input transfer</th><td><strong>pycdlib.</strong> Python builds an ISO containing only the permitted job pack. VirtualBox attaches it as a read-only optical disk; no host folder is shared.</td><td>Chosen for implementation</td></tr>
        <tr><th scope="row">Output transfer</th><td><strong>VirtualBox virtual serial port + pywin32.</strong> A Windows named pipe carries bounded JSON results. pywin32 supplies Windows pipe and access-control APIs; the controller treats every result as untrusted.</td><td>Chosen; transport to test</td></tr>
        <tr><th scope="row">Agent access</th><td><strong>Separate role contexts through a project-specific model gateway.</strong> Provider, model IDs and provider adapter remain open pending access, data-handling and budget decisions. Built-in browsing, execution and shared memory are excluded.</td><td>Provider and models to select</td></tr>
        <tr><th scope="row">Assessment</th><td><strong>Python behaviour checks and pinned project tests.</strong> H04 uses HTTPX MockTransport and custom assertions. Runtime and controller regression tests will use Python unittest; model assessors require separate qualification.</td><td>H04 checks exist; full suite to build</td></tr>
        <tr><th scope="row">Records and sign-in</th><td><strong>JSON, SHA-256, Git for Windows and Git Credential Manager.</strong> GitHub holds separate public and private repositories. Windows Credential Manager keeps Git credentials local; pywin32’s win32cred API will read separately stored model credentials.</td><td>Private repository and runner storage setup pending</td></tr>
      </tbody>
    </table>
    <p className="caption">The proposed stack and interfaces must pass compatibility and boundary tests. The listed product names and major versions are design selections, not claims of installed software. Exact patch versions and image digests are locked after compatibility checks and before execution; model settings are fixed before qualification. The working plan and each run’s manifest record exact versions, dependency pins, configuration and reproduction commands.</p>
  </section>

  <section className="technology-section" id="containers-and-machines" aria-labelledby="containers-and-machines-title">
    <h3 id="containers-and-machines-title">Containers and switching machines</h3>
    <p>The design supports local execution on either Windows machine, using the 32 GB laptop as the common resource baseline. It does not depend on the 64 GB home PC staying on.</p>
    <ul className="plain-list">
      <li><strong>Separate the agents.</strong> Each role has its own model context, permitted input pack and tool workspace. The controller passes only authorised submissions and review messages. Shared memory, retrieval stores and direct agent-to-agent connections are excluded; assessment answers stay outside working roles.</li>
      <li><strong>Prepare a clean environment.</strong> Install pinned dependencies before execution, then disable the VM’s network adapters. The containers run tools and generated code; the Windows controller makes model calls through a separate gateway.</li>
      <li><strong>Limit every transfer.</strong> Supply permitted files on a read-only disk image. Collect bounded results through a virtual serial connection checked by the controller. This interface is part of the boundary that must be tested.</li>
      <li><strong>Reset between tool batches.</strong> Each bounded batch uses a fresh VM and container. Only checked workspace files carry forward. Execution stops before the next review, and environments share no writable caches.</li>
      <li><strong>Switch after a complete comparison.</strong> Run all three groups in a matched block on the same machine. Before continuing elsewhere, verify saved private records, matching environment versions and that machine’s boundary tests.</li>
    </ul>
    <p>The <a className="text-link" href="https://github.com/yspbob/interpretation-layer-poc/blob/main/research/development/isolated-runner-design-v0.1.md" target="_blank" rel="noreferrer">detailed runner design</a> specifies the container restrictions, transfer limits, provisional resource profile, failure handling and private-record workflow. Compatibility and containment must be demonstrated on each host.</p>
  </section>

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
      <p><strong>Proposed implementation:</strong> VirtualBox provides the outer VM boundary, with rootless Podman containers inside an Ubuntu guest. Read-only input images and bounded serial output replace shared folders and guest networking. Hypervisor, guest launcher and host parser vulnerabilities remain possible; the containment claim must state the tested paths and remaining limits.</p>
    </Disclosure>
    <Disclosure id="technical-records" title="What makes a run inspectable and repeatable?">
      <p>Each run records the source revision, file manifests, environment version, model settings, exact supplied inputs and returned outputs, tool activity, review decisions, revisions, stops and resource use. A controller-managed local store retains these records outside agent access; verified saves to the separate private repository support continuation on the other machine. The runner must record an unsuccessful save and prevent continuation that depends on missing evidence. Collection checks paths, symlinks, archive entries, output limits and message order before accepting untrusted artifacts.</p>
      <p>The assessment records task correctness and guardrail compliance separately, including justified improvements over historical code, new violations and unresolved evidence. Public reports exclude credentials and sealed assessment material. Exact models, budgets, scoring weights and acceptance limits belong in the run configuration, fixed before the relevant scored runs.</p>
    </Disclosure>
  </DetailGroup>
  <p className="caption">The method defines the required behaviour. <PageLink className="text-link" href="/progress#technical-status">Progress &amp; findings records component readiness and open technical choices.</PageLink></p>
</section>}
