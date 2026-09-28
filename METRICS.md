# Organizational Metrics

Use a balanced scorecard; never optimize one metric blindly.

- Product/R&D: validated-problem rate, experiment cycle time, promote/kill/defer mix, adoption.
- Delivery: lead time, change-failure rate, escaped defects, rollback rate.
- Reliability: restore time, recurring incidents, stale runbooks.
- Agents: accepted-task success, human intervention, retries, verifier disagreement, policy denials, cost per accepted change.
- Agent efficiency (Runtime Context v2): standing context chars and approximate tokens (`orgctl context-report`), context sources loaded per work item, delegated vs directly executed tasks, retries and no-progress attempts, provider usage/cost where available, usage per accepted result, and context growth across a task where observable. Record run-time signals in the result envelope's optional `efficiency` object. These are weighed together with quality, security, correctness, governance and reliability. Never lower cost by lowering assurance.
- Security: regression pass rate, unresolved high-severity findings, privilege-escalation denials, audit reconstruction success.
