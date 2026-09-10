import { ProductionDifference } from './production-difference';
import { PageLink } from './page-link';

export function Economics() {
  return <>
    <p>Preparing a guide costs time and money before it helps with any code change. We will measure whether savings from later uses recover that initial cost. The work must still meet the same quality requirements.</p>
    <h3>What Phase 1 will record</h3>
    <p>For each guide, we will add its preparation cost to the cost of the tasks that use it. We will compare that total with the cost of doing those same tasks from the sources alone.</p><p>Failed preparation, unfinished tasks and unnecessary reviews will stay in the totals. Counting only successful work would give a misleading picture of the cost.</p>
    <div className="phase-later-note"><p>Phase 1 will record actual costs and any reuse observed in its tasks. Detailed estimates about future savings belong to a later study. <PageLink className="text-link" href="/phases#phase-2">See Phase 2 on the roadmap.</PageLink></p></div>
    <details className="economic-later"><summary>Why we are keeping the idea of cost recovery</summary><div className="economic-example">
      <h4>An illustration, not a POC result</h4>
      <p>Suppose preparing and verifying a guide costs £60. A satisfactory change costs £10 with sources alone and £7 with the guide. Both amounts include review and corrections.</p><p>The guide saves £3 per change. If that saving continues, 20 applicable changes would recover the £60 spent on preparation. Savings would begin after that.</p>
      <p>If using the guide costs as much or more per change, further use would not recover its preparation cost. If quality gets worse, spending less does not by itself establish a useful return.</p>
    </div>
    <p>We will report whether the guide recovered its preparation cost during the experiment.</p><p>A later study may estimate how many more changes would be needed. That estimate would explain its assumptions about future use and how uncertain the answer is. Where the evidence does not support a saving, it would say that the cost may never be recovered.</p><p>Trying the same task several times tells us how consistent the results are. To find out whether the guide helps with other changes, we need to test it on different tasks.</p>
    </details><h3>How the comparison stays fair</h3>
    <p>Each group gets the same total spending allowance. The groups using guidance pay for its preparation from that allowance, leaving the rest for coding, tools, questions and review.</p><p>When several tasks can use the same guide, we divide its preparation cost equally across those tasks. We choose that set before the runs and keep unsuccessful tasks in it. We cannot add more tasks afterwards just to make preparation look cheaper.</p>
    <p>We compare each guidance group with the group using sources alone. We also compare the two guidance groups with each other. That shows whether the extra interaction improves the work enough to justify its cost.</p><p>The experiment prepares their shared guide once. When comparing the methods, each carries the preparation cost it would incur if used on its own. The total study spending records that shared preparation only once.</p>
    <h3>What else will the cost report show?</h3>
    <p>Money, human effort and elapsed time will be reported separately.</p><p>Preparing test cases, checking familiarity and independently scoring results also cost resources. Those are research costs, so we will report them separately from the cost of using each method. Prices, quality requirements and the tasks sharing a guide must be recorded before the relevant runs.</p>
    <p>The comparison uses the same coding model, tools, code version and ordinary review settings across groups. Each attempt starts with a separate history and workspace. We will vary the order of the groups so that one method does not always run first. Ordinary reviewers can still ask useful questions.</p>
    <ProductionDifference
      production="A live system would also need to account for maintaining guidance, its use by a team, and any defensible value from avoided mistakes. A human could review costs and outcomes before deciding how guidance should change."
      poc="The first trial records preparation and use costs for its selected tasks. The guide stays unchanged. Detailed estimates of future return and a dashboard for managing rules belong to later work."
      limit="These results could show when a tested guide recovers its cost. They would not establish the full return for an organisation. Where several rules help with the same change, we will assess their combined value unless the evidence supports attributing it to individual rules."
    />
  </>;
}

export function BudgetSelection() {
  return <>
    <p>First, we will agree how much the whole study can spend. That includes preparing the experiment, checking the assessment tools, running the trials and assessing their results.</p>
    <p>We will then try all three ways of working on a few separate development tasks. These tasks will help us understand what preparation, coding, questions, review and corrections actually cost. They will stay out of the independent tests used to support our final conclusions.</p>
    <p>Before those trials, we will record how their results will guide the budget choice. We want each method to have enough room to make a serious attempt and complete the required reviews. We will not choose the amount that happens to make the layer look best. The exact amounts and selection criteria still need to be agreed.</p>
    <p>For the two methods using a guide, preparation uses part of that allowance. We will fix both its spending limit and the tasks sharing that cost before the comparison.</p>
    <p>Once calibration is complete, we will fix the allowance before the scored comparison begins. An agent that runs out of budget stops, and its unfinished work remains part of the results.</p>
    <p>Phase 1 will use one selected allowance. A second budget comparison is deferred to Phase 2 if it is justified and funded. For now, conclusions about cost will apply only to the allowance and tasks actually tested.</p>
    <p><PageLink className="text-link" href="/progress#technical-status">See Progress &amp; findings for the calibration status and decisions still to make.</PageLink></p>
  </>;
}
