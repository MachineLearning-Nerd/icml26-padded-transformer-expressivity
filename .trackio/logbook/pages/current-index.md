# Current reproduction status

Paper: [OpenReview nBuL6HywFX](https://openreview.net/forum?id=nBuL6HywFX) ·
[arXiv:2605.30523](https://arxiv.org/abs/2605.30523)

This is the canonical evaluator entrypoint. Current verification appears
first; earlier finite checks and the source-inclusion Lean composition are
preserved as **Historical rejected baseline** evidence and are not the current
verifiers.

## Claim status

| Claim | Exact current status | Current evidence |
| --- | --- | --- |
| 1 — Theorem 4.2 | BLOCKED | Historical finite checks and assumed inclusions do not prove the circuit-class equalities |
| 2 — sufficient volume | BLOCKED | Definition is source-verified; its universal expressivity consequence still depends on Claim 1 |
| 3 — Theorem 5.1 | BLOCKED | Historical finite loop composition does not prove FO-uniform class equality |
| 4 — AHAT to SMAT | BLOCKED | Universal focusing kernel verified; full mixed-precision family construction not yet formalized |
| 5 — theory-only scope | VERIFIED | Source inventory and cumulative audit |

## Navigation

- [Claim 1 — exact current audit](#/claim-1-current)
- [Claim 2 — exact current audit](#/claim-2-current)
- [Claim 3 — exact current audit](#/claim-3-current)
- [Claim 4 — current universal kernel certificate](#/claim-4-current)
- [Claim 5 — theory-only scope](#/claim-5-current)
- [Evaluator visibility matrix](#/visibility-matrix)
- [Release report](#/release-report)
- [Evaluator-blind red-team record](#/evaluator-red-team)
- [Historical rejected baseline — previous canonical index](#/historical-index)
- [Historical rejected baseline — previous Claim 4 finite verifier](#/historical-claim-4)

No finite experiment is described as proof of a universally quantified
complexity or simulation theorem.
