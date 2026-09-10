export function RuntimeOverview(){return <>
  <section className="runtime-process" id="runtime-process" aria-labelledby="runtime-process-title">
    <h3 id="runtime-process-title">The process before the machinery</h3>
    <p>The experiment has two connected activities: preparing guidance and using it on engineering tasks. Independent assessment examines the resulting work separately. The experiment runner coordinates these activities and enforces their boundaries.</p>
    <div className="runtime-process-stage">
      <span className="eyebrow">PREPARATION · BEFORE TASK WORK</span><h4>Prepare and freeze the guidance</h4>
      <p>The runner gives the drafter the project evidence it is allowed to read. A separate verifier checks the proposed claims. The accepted claims form a saved version of the guide.</p><p>This checks the evidence behind the claims. It does not supply approval from a project owner.</p><p>The two groups using guidance receive that same saved guide for the tasks assigned to it. The group using sources alone receives the permitted project files and instructions.</p>
    </div>
    <div className="runtime-process-stage">
      <span className="eyebrow">TASK USE · REPEATED FOR EACH COMPARISON GROUP</span><h4>Plan, review and carry out the change</h4>
      <p>Each attempt starts in a separate model session. The coding agent submits a plan for review.</p><p>Once the reviewer permits work, the runner starts a limited batch of tools or code in an isolated environment. It collects the results and closes that environment before deciding what may happen next.</p><p>The work returns to review at the required checkpoints and when the approach changes substantially. The group with interaction also receives questions about how it applies the guidance. All groups follow the same review rules and resource limits.</p>
      <p>The cycle repeats until the attempt finishes or a stop rule ends it. Each role retains only its permitted history and files. The guide stays frozen during task use; it is not redrafted after each tool batch.</p>
    </div>
    <div className="runtime-process-stage">
      <span className="eyebrow">INDEPENDENT ASSESSMENT · OUTSIDE THE LIVE TASK CYCLE</span><h4>Assess the work and preserve the record</h4>
      <p>After an attempt ends, separate assessors examine its code and review decisions. The saved guide is also assessed independently of the verifier that accepted it.</p><p>The code assessment asks whether the task was completed correctly and whether the applicable project rules were followed. It uses the same criteria for the agent’s code and the original historical implementation. Hidden assessment feedback does not return to the working agents.</p>
      <p>The runner preserves outcomes and costs, including failed and unfinished attempts. All three methods for a matched task and repeat are run on the same machine. Its private records must be saved and verified before work continues on the other machine.</p>
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
    <figcaption id="execution-tree-caption"><p>One worker container runs inside one virtual machine at a time. Each tool batch gets a fresh environment. Assessment code runs in a separate fresh environment.</p><p>The AI models run at the provider. The runner on Windows manages their separate sessions. The diagram below shows which connections are permitted.</p></figcaption>
  </figure>
</>}
