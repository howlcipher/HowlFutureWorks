# Fire / Terminate a Bot Employee

## Normal termination

1. Freeze new assignments to the employee.
2. Inventory active work, routines, queues, temporary credentials, browser/app sessions, shared files used by the worker, and external service access.
3. **Pause or disable write-capable routines explicitly. Hiding the live Grok Bot is not sufficient because hiding does not pause routines.**
4. Export or document the routine definitions that matter to continuity and preserve required recent run evidence. Grok Bot platform history is bounded and deleting the Bot removes its routines.
5. Capture a curated context snapshot; never copy hidden reasoning or secret material.
6. Create an exit handoff for unfinished work, decisions, pitfalls and authoritative refs.
7. Record final attributable contributions and promote stable successor-relevant lessons into position knowledge.
8. Reassign active work and routine ownership. Recreate/test routines under the successor rather than assuming ownership transfer.
9. Revoke/rotate employee-scoped access where possible and explicitly review shared-computer sign-ins/files. **Deleting a Bot does not itself revoke shared sign-ins or erase shared files.**
10. Record a `terminated` employment event and update the roster status; do not delete the employee directory.
11. Leave the position vacant or begin the separate hire/replacement process.
12. Prefer hiding/retaining the live Bot until archival, handoff and access verification are complete. Delete it only when policy permits and the organization no longer needs its live conversation/routine state.
13. Verify the former employee no longer receives work or privileged execution while its historical organizational record remains readable.

## Emergency path

For suspected compromise or unsafe behavior, run `runbooks/suspend-worker.md` first, then investigate and decide whether to reinstate or terminate.

## Never do

- delete contribution history,
- rewrite old decisions to remove attribution,
- hand predecessor credentials to a successor,
- treat hiding as routine suspension,
- treat live-Bot deletion as credential revocation,
- delete the live Bot before required routine/configuration evidence has been preserved,
- treat deletion of a conversation as the offboarding record.
