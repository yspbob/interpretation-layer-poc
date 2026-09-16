# Supervise each allowance handoff

16 September 2026. Development checks only. All previous allocations remain closed.

## Operating sequence for a future approved allocation

Prepare and check the launcher, receipt writer, closure scripts and output locations before launch. Rehearse the complete handoff with artificial account responses. Finish ancillary editing and analysis before a live collector starts.

While collection is active, the supervising task services only control requests, collection status and necessary user updates. For each new scheduled ID:

1. Read the pending request and its creation time. Do not start unrelated work while a request is pending.
2. Call the app's current usage tool for that position. Preserve its returned evidence and the observation time. Never reuse another position's result or manufacture an account observation.
3. Validate identity and the applicable frozen spending policy, then write the receipt atomically. A successful tool call is not proof that the collector received it in time.
4. Confirm consumption or a recorded stop, then wait for the next request. Use short status waits so the supervisor stays available; do not wait through the entire observation deadline.
5. On missing evidence, tool failure, a stop or a missed deadline, preserve records and close. Do not retry a closed allocation or extend its deadline.

Do not run a background commit timer or a second model supervisor. This procedure cannot guarantee that an interactive supervising task will remain responsive. The artificial tests establish the handoff mechanics, not live tool latency or future operator attentiveness.

## Deadline enforcement

The exchange now measures its unchanged 120-second elapsed limit with a monotonic clock, which is unaffected by wall-clock adjustments. It checks the deadline and stop/configuration guard before accepting an existing response and after reading it. The separate observation timestamp still binds the app receipt to the scheduled request, and the batch's existing account, freshness and dispatch guards remain active.

Artificial regression tests reproduced four gaps in the previous exchange: acceptance just after the deadline, acceptance after a slow receipt read crossed the deadline, a ready response bypassing the exchange's guard, and a backward clock adjustment extending the wait. The batch already checks its guard after the exchange; the added exchange checks make the handoff itself fail closed. These are development findings, not the cause of the previously recorded supervisor timeout.

The tests include 144 sequential fresh handoffs, absent receipts, the exact deadline, late receipts, wrong positions, old/future observations, duplicate requests, operator stop and clock rollback. They use a virtual clock and artificial account records; process launches and network connections are forbidden. No subscription or model call is made.

Verification: all 144 offline harness tests passed on the pinned Python environment. This includes an integrated batch reproduction with eight artificial completed responses, a ninth observation timeout, 136 unrun positions, no ninth reservation or collector call, preserved closure records and rejected reuse of the allocation. The focused exchange initially reproduced four failures before the fix; all eleven focused checks subsequently passed. No live account-tool latency or model quality was measured.

## Allocation boundary

The runtime change invalidates prior configuration bindings. No prompt, scoring threshold or frozen packet changes with it. The current runner still requires its original zero-credit account condition and more than 5% included allowance. Continuing project preparation does not define a new qualification spending allocation. A future proposal must state the permitted payment route, limit, stopping policy and new configuration before execution approval.
