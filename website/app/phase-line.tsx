import { PageLink } from './page-link';

export function PhaseLine(){return <nav className="phase-line" aria-label="First trial phases. Phase 1 is the current phase.">
  <ol>
    <li className="phase-stop current-stop"><PageLink href="/" aria-current="step"><span className="station-dot" aria-hidden="true"/><span className="station-label"><span>01 · CURRENT PHASE</span><strong>Reconstruct guidance</strong></span></PageLink></li>
    <li className="phase-stop"><PageLink href="/phases#phase-2"><span className="station-dot" aria-hidden="true"/><span className="station-label"><span>02</span><strong>Test its use</strong></span></PageLink></li>
    <li className="phase-stop"><PageLink href="/phases#phase-3"><span className="station-dot" aria-hidden="true"/><span className="station-label"><span>03</span><strong>Test interaction</strong></span></PageLink></li>
  </ol>
</nav>}
