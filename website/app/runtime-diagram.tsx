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
  <div className="runtime-api"><ArrowUpDown aria-hidden="true"/><span><strong>Runner-only model API connection</strong><br/>Permitted messages and tool requests; credentials stay on Windows.</span></div>
  <div className="runtime-host">
    <h4>Active Windows machine <span>32 GB laptop or 64 GB home PC · one worker VM at a time</span></h4>
    <div className="runtime-execution">
      <div className="runtime-controller">
        <span className="eyebrow">TRUSTED CONTROL</span><h5>Experiment runner — Python controller</h5>
        <p><strong>CPython 3.12 · asyncio + subprocess</strong><br/>Proposed coordination utilities; custom scope under review. Enforce dispatch, review pauses and stops.</p>
        <p><strong>Pydantic 2 + explicit checks</strong><br/>Validate records, roles, paths, sizes and message order.</p>
        <p><strong>pywin32</strong><br/>Receive serial results through a restricted Windows named pipe.</p>
        <div className="runtime-private"><strong>Separate local data areas</strong><br/>Role histories and packs · untrusted results · sealed assessment store. The runner selects permitted files; no whole store enters a VM.</div>
      </div>
      <div className="runtime-transfers" aria-label="Permitted controller and guest transfers">
        <div><span><strong>Input</strong><br/>pycdlib<br/>Read-only ISO</span><ArrowRight aria-hidden="true"/></div>
        <div><ArrowLeft aria-hidden="true"/><span><strong>Output</strong><br/>Virtual serial port<br/>Bounded JSON</span></div>
        <div><span><strong>Control</strong><br/>VBoxManage<br/>Start / stop / discard</span><ArrowRight aria-hidden="true"/></div>
      </div>
      <div className="runtime-vm">
        <span className="eyebrow">OUTER ISOLATION BOUNDARY</span><h5>Oracle VirtualBox 7.2</h5>
        <p><strong>Ubuntu Server 24.04 LTS · amd64</strong><br/>Python guest launcher owns the input disk and serial device.</p>
        <div className="runtime-container"><span className="eyebrow">INNER ISOLATION BOUNDARY</span><h5>Rootless Podman + crun</h5><p>One role’s tools or submitted code.<br/>Read-only image + private bounded workspace.</p><p><strong>cgroup v2 · seccomp</strong><br/>CPU, memory and process limits; restricted system calls.</p></div>
        <p className="runtime-denials">No VM network adapters, shared host folders, clipboard, credentials or container-runtime socket.</p>
        <p className="runtime-note">Fresh VM and container for each tool batch. Only validated files carry forward.</p>
      </div>
    </div>
    <div className="runtime-assessment"><ArrowDown aria-hidden="true"/><p><strong>After the attempt stops:</strong> the runner supplies anonymised code and permitted evidence to separate assessment contexts. Evaluation code uses a fresh VM. Hidden-test feedback and final scores do not return to working agents.</p></div>
  </div>
  <div className="runtime-sync"><ArrowUpDown aria-hidden="true"/><p><strong>Git for Windows + Git Credential Manager → GitHub</strong><br/>Public repository: reviewed project files. Separate private repository: sealed cases, confidential records and completed-block ledger. Verify the save before switching machines; each machine keeps its own installation and credentials.</p></div>
  <figcaption id="runtime-diagram-caption">Boxes mark deployment and access boundaries; arrows show permitted interfaces, not a single drafting-and-usage sequence. Only the host runner uses model and GitHub connections. The offline guest has no general route to either service. These controls require implementation and testing.</figcaption>
</figure>}
