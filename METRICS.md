# Organizational Metrics

Use a balanced scorecard; never optimize one metric blindly.

- Product/R&D: validated-problem rate, experiment cycle time, promote/kill/defer mix, adoption.
- Delivery: lead time, change-failure rate, escaped defects, rollback rate.
- Reliability: restore time, recurring incidents, stale runbooks.
- Agents: accepted-task success, human intervention, retries, verifier disagreement, policy denials, cost per accepted change.
- Agent efficiency (Runtime Context v2, reinforced by HowlPlane-first execution): standing context chars and approximate tokens (`orgctl context-report`), context sources loaded per work item, SELF vs HowlPlane execution, executor selected, retries, failovers, no-progress attempts, persistent Grok participation, human interventions, accepted results, Plane-caused repair tasks, improvement work opened from repeated evidence, provider usage/cost where available, and context growth across a task where observable. Record run-time signals in the result envelope's optional `efficiency` object. These are weighed together with quality, security, correctness, governance and reliability. Never lower cost by lowering assurance.
- Security: regression pass rate, unresolved high-severity findings, privilege-escalation denials, audit reconstruction success.
