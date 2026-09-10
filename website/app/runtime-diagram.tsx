import { ArrowDown, ArrowLeft, ArrowRight, ArrowUpDown } from 'lucide-react';

export function RuntimeDiagram(){return <figure className="runtime-diagram" id="runtime-architecture" aria-labelledby="runtime-diagram-title runtime-diagram-caption">
  <div className="runtime-heading"><span className="eyebrow">PROPOSED DEPLOYMENT</span><h3 id="runtime-diagram-title">Where each part runs</h3></div>
  <div className="runtime-models">
    <h4>Model provider · separate context for every role</h4>
    <div className="runtime-role-groups">
      <div><span>Preparation</span><p><b>Drafter</b><b>Verifier</b></p></div>
      <div><span>Task work</span><p><b>Coder</b><b>Reviewer / checker</b></p></div>
      <div><span>Independent assessment</span><p><b>Guidance assessor</b><b>Code judge</b><b>Intervention assessor</b></p></div>
    </div>
    <p className="runtime-note">Each outlined role has its own history and permitted inputs. No shared memory, tool sessions or direct connections between roles. Provider and models remain to be selected.</p>
  </div>
  <div className="runtime-api"><ArrowUpDown aria-hidden="true"/><span><strong>Model connection controlled by the runner</strong><br/>Permitted messages and tool requests; credentials stay on Windows.</span></div>
  <div className="runtime-host">
    <h4>Selected Windows machine <span>Sized for the 32 GB laptop · one worker VM at a time</span></h4>
    <div className="runtime-execution">
      <div className="runtime-controller">
        <span className="eyebrow">TRUSTED CONTROL</span><h5>Experiment runner: Python controller</h5>
        <p><strong>CPython 3.12 · asyncio + subprocess</strong><br/>Coordinates when work starts, pauses for review or stops. The amount of custom code is still under review.</p>
        <p><strong>Pydantic 2 + explicit checks</strong><br/>Check who sent each record, what it contains and whether it is allowed at this stage.</p>
        <p><strong>pywin32</strong><br/>Receive serial results through a restricted Windows named pipe.</p>
        <div className="runtime-private"><strong>Separate local data areas</strong><br/>Separate areas hold each role’s history and allowed files, returned results, and assessment records hidden from working agents. The runner selects permitted files; no whole store enters a VM.</div>
      </div>
      <div className="runtime-transfers" aria-label="Permitted controller and guest transfers">
        <div><span><strong>Input</strong><br/>pycdlib<br/>ISO mounted for reading only</span><ArrowRight aria-hidden="true"/></div>
        <div><ArrowLeft aria-hidden="true"/><span><strong>Output</strong><br/>Virtual serial port<br/>JSON with a size limit</span></div>
        <div><span><strong>Control</strong><br/>VBoxManage<br/>Start / stop / discard</span><ArrowRight aria-hidden="true"/></div>
      </div>
      <div className="runtime-vm">
        <span className="eyebrow">OUTER ISOLATION BOUNDARY</span><h5>Oracle VirtualBox 7.2</h5>
        <p><strong>Ubuntu Server 24.04 LTS · amd64</strong><br/>Python guest launcher owns the input disk and serial device.</p>
        <div className="runtime-container"><span className="eyebrow">INNER ISOLATION BOUNDARY</span><h5>Rootless Podman + crun</h5><p>One role’s tools or submitted code.<br/>Image that cannot be changed. Private workspace with size limits.</p><p><strong>cgroup v2 · seccomp</strong><br/>CPU, memory and process limits; restricted system calls.</p></div>
        <p className="runtime-denials">No VM network adapters, shared host folders, clipboard, credentials or socket for controlling the container runtime.</p>
        <p className="runtime-note">Fresh VM and container for each tool batch. Only validated files carry forward.</p>
      </div>
    </div>
    <div className="runtime-assessment"><ArrowDown aria-hidden="true"/><p><strong>After the attempt stops:</strong> the runner supplies anonymised code and permitted evidence to separate assessment contexts. Evaluation code uses a fresh VM. Feedback from hidden tests and final scores do not return to working agents.</p></div>
  </div>
  <div className="runtime-sync"><ArrowUpDown aria-hidden="true"/><p><strong>Git for Windows + Git Credential Manager → GitHub</strong><br/>Public repository: reviewed project files. Separate private repository: hidden case evidence, confidential results and a record of completed comparisons. Phase 1 keeps experimental execution on one qualified host. Editing can continue from either machine. Moving confidential runs later requires a verified save and a qualified destination.</p></div>
  <figcaption id="runtime-diagram-caption">The boxes show where components run and what they may access. The arrows show permitted connections. Read the process above for the order of work. Only the runner on Windows connects to models and GitHub. The offline guest has no general route to either service. These controls require implementation and testing.</figcaption>
</figure>}
