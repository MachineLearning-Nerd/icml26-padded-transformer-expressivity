# Release report

- Previous live judged score: `6/10`
- Conservative projected score range after the proposed change: `6/10`
- Best-supported possible new score: `6/10` (**forecast, not a judge result**)

The release improves rigor, discoverability, and failure disclosure. It does
not support forecasting a point increase because Claims 1–4 remain short of
their exact universal contracts.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 1 | LOW | BLOCKED | Four routes completed; hard AC0/TC0 inclusions are not machine-proved |
| 2 | 1 | 1 | LOW | BLOCKED | Definition verified; robustness still depends on Theorem 4.2 |
| 3 | 1 | 1 | LOW | BLOCKED | Four routes completed; FO-uniform lower bounds remain unmechanized |
| 4 | 1 | 1 | MEDIUM | BLOCKED | Universal focusing kernel proved; full mixed-precision family construction remains open |
| 5 | 2 | 2 | HIGH | VERIFIED | Complete source inventory; cumulative regression preserved |

Current live total: `6/10`. Conservative projected total: `6/10`.
Best-supported possible total: `6/10`, pending the live evaluator.

## Winning evidence snapshot

The cumulative candidate is branch
`orx/cumulative-release-candidate-and-evaluator-audit`, Git
`0c9f970126a6ea082382feaece0d2f969d3ea557`, run
`87539b69-0eaa-4a87-9434-06d807928a7f`. The fixed command passed in
`168.630605` runner seconds on HF `cpu-upgrade`, with 64 logical CPUs visible
and an explicit one-thread cap.

The release audit covered 66 allowlisted text files (196,307 bytes), retained
all 37 judged paths with no historical evidence overwrite, opened 12 files
from the canonical entrypoint, found five current claim pages and zero missing
visibility cells, parsed four report figures, validated the marimo notebook,
and rejected all three release-gate mutations.

## Changes since the previous verdict

- Claim 1: historical assumed-inclusion proof is no longer presented as the
  current verifier; four verification/falsification routes are visible.
- Claim 2: the actual fixed-point alphabet rejects the old binary-capacity
  proxy as full evidence.
- Claim 3: finite truth tables are explicitly historical regression evidence;
  four routes are recorded.
- Claim 4: a pinned Lean kernel proves the universal attention-focusing core,
  an independent checker agrees, and `tau=1` fails by `0.5`.
- Claim 5: unchanged and rerun in the cumulative suite.

## BLOCKED claims

Claims 1–3 lack full semantic complexity-class proof certificates and valid
counterexamples. Claim 4 lacks the complete family-dependent mixed-precision
range, Appendix A.3 operational rounding, and L-uniform constructor proof.

## Publication action

Upload only the committed text allowlist to the existing
`DineshAI/nBuL6HywFX` Space through the Hugging Face commit API, preserve every
judged path, verify the resulting revision and hashes, then mirror the reader
artifacts to GitHub `main`. Publication does not claim a score change.
