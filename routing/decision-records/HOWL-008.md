# Routing decision — HOWL-008

- work_item: HOWL-008
- recorded_at: 2026-09-21
- task_class: bounded
- risk_tier: R2
- selected_executor: SELF
- selected_profile: null
- eligible_alternatives: [claude, codex, agy]  # astra = codex alias
- selection_reasons:
  - bounded vertical slice; in-repo mission-row pattern to extend
  - SELF sufficient (HOWL-007 = sufficiency evidence for HowlBoard HowlFrame shared-view slices, not standing preference)
  - no measured expected-value for specialist on this navigation/JSON-harden slice
  - quota unknown → constrained; avoid external spend without EV
  - orgctl bounded/R2/coding → SELF_preferred_unless_expected_value
- quota_state: unknown
- required_tools: [coding, git, howlframe]
- verification_required: assurance_independent
- howl007_relationship: evidence_of_sufficiency_not_auto_rule
- notes: Astra=Codex. No permanent ranking. Informational depends_on navigation only.
