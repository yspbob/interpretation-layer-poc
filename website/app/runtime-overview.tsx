export function RuntimeOverview(){return <>
  <section className="runtime-process" id="runtime-process" aria-labelledby="runtime-process-title">
    <h3 id="runtime-process-title">The process before the machinery</h3>
    <p>The experiment has two connected activities: preparing guidance and using it on engineering tasks. Independent assessment examines the resulting work separately. The experiment runner coordinates these activities and enforces their boundaries.</p>
    <div className="runtime-process-stage">
      <span className="eyebrow">PREPARATION · BEFORE TASK WORK</span><h4>Prepare and freeze the guidance</h4>
      <p>The runner supplies the drafter with permitted project evidence. A separate verifier checks the proposed claims, and supported claims form a versioned guide. This is evidence-based verification, without project-owner certification. The same frozen guide goes to GUIDE and INTERACT for the declared set of tasks; DIRECT works from the permitted sources and project instructions.</p>
    </div>
    <div className="runtime-process-stage">
      <span className="eyebrow">TASK USE · REPEATED FOR EACH COMPARISON GROUP</span><h4>Plan, review and carry out the change</h4>
      <p>Each attempt starts with a fresh coder context. The coder submits a plan for review. When work is permitted, the runner dispatches a bounded batch of tools or code into an isolated environment, collects the results and closes that environment. Required checkpoints and material changes return the work to review. INTERACT adds targeted questions about the guidance; all groups follow the matched review policy and resource limits.</p>
      <p>The cycle repeats until the attempt finishes or a stop rule ends it. Each role retains only its permitted history and files. The guide stays frozen during task use; it is not redrafted after each tool batch.</p>
    </div>
    <div className="runtime-process-stage">
      <span className="eyebrow">INDEPENDENT ASSESSMENT · OUTSIDE THE LIVE TASK CYCLE</span><h4>Assess the work and preserve the record</h4>
      <p>After an attempt stops, separate assessment roles examine its code and review decisions. The frozen guide is assessed independently of the verifier that admitted it. Code assessment checks task correctness and applicable guardrails, using the same criteria for agent and historical implementations. Hidden assessment feedback does not return to the working agents.</p>
      <p>The runner preserves outcomes and costs, including failed and unfinished attempts. A complete DIRECT, GUIDE and INTERACT comparison block stays on one machine. Its private records must be saved and verified before work continues on the other machine.</p>
    </div>
  </section>
  <figure className="execution-tree" id="execution-tree" aria-labelledby="execution-tree-title execution-tree-caption">
    <h3 id="execution-tree-title">Where the containers run</h3>
    <pre>{`Windows laptop or home PC
├─ Experiment runner
│  └─ Python controller
└─ VirtualBox
   └─ Ubuntu VM (offline)
      └─ Podman container
         └─ Tools or code`}</pre>
    <figcaption id="execution-tree-caption">One worker container inside one VM runs at a time. Each tool batch gets a fresh VM and container; assessment code uses a separate fresh environment. The AI models run at the provider, with separate role contexts managed by the runner on Windows. The detailed diagram below shows the permitted connections.</figcaption>
  </figure>
</>}
