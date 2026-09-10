import { ProductionDifference } from './production-difference';

export function Economics() {
  return <>
    <p>Preparing a guide costs time and money before it helps with any code change. The question is whether savings from later uses recover that initial cost, while the work still meets the same quality requirements.</p>
    <h3>When does the guide pay for itself?</h3>
    <p>For each saved guidance version, the experiment will track the full preparation cost and the costs of the distinct tasks that use it. The report will compare the cumulative cost with doing those same tasks directly from the sources. Failed preparation, unsuccessful tasks and unnecessary reviews remain in the totals.</p>
    <div className="economic-example">
      <h4>An illustration, not a POC result</h4>
      <p>Suppose preparing and verifying a guide costs £60. A satisfactory change costs £10 with sources alone and £7 with the guide, including review and corrections. A saving of £3 per change would recover the £60 after 20 applicable changes. Savings would begin after that.</p>
      <p>If there is no saving per change, there is no financial break-even under those assumptions. If quality gets worse, lower costs alone do not establish a useful return.</p>
    </div>
    <p>The report will distinguish a break-even point actually reached in the tested tasks from an estimate that assumes further reuse. Estimates will show uncertainty and the range of reuse they assume. Several attempts at the same task help measure variability; they do not demonstrate that a guide is useful across different changes.</p>
    <h3>How the comparison stays fair</h3>
    <p>Each group receives the same total method allowance. The groups using guidance pay for preparation from that allowance, leaving the rest for coding and review. If a guide is shared, its preparation cost is divided across the task set chosen before the runs, including failed attempts. The analysis cannot choose a larger reuse set afterwards just to make the guide look cheaper.</p>
    <p>Both guidance methods are compared with sources alone. Comparing guidance with and without interaction also shows whether the extra questioning earns its cost. The physical cost of generating their shared guide is recorded once as experiment spending, even though each method comparison carries its share of preparation.</p>
    <p>Model and tool charges, human effort and elapsed time are reported separately. The study also records the cost of preparing test cases, running the familiarity probes and independently scoring results. These research activities are kept separate from the cost of using the layer. Prices, quality requirements, reuse assumptions and budget limits must be set before the relevant runs.</p>
    <p>Matched attempts use the same coding model, tools, code version and review-model settings. Their order is randomised or balanced, and each starts with a separate history and workspace. Ordinary reviewers can still ask useful questions.</p>
    <ProductionDifference
      production="A live system would also need to account for maintaining guidance, its use by a team, and any defensible value from avoided mistakes. A human could review costs and outcomes before deciding how guidance should change."
      poc="The pilot estimates the economics of a fixed guidance version across a declared set of tasks. It records signals that could inform maintenance, but does not update the guide during the comparison or operate a rule-ROI dashboard."
      limit="This can support a bounded break-even estimate. It cannot establish the full return from running the layer in an organisation. Benefits should be attributed to a guide or related group of rules unless individual-rule attribution is justified."
    />
  </>;
}
