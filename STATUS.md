# Status — Padded Transformer Expressivity

**Updated:** 2026-08-15
**Repository:** `MachineLearning-Nerd/icml26-padded-transformer-expressivity`
**Default branch:** `main`
**State:** paper-first documentation and branch/identity normalization complete;
Claims 1–4 remain blocked at their complete universal contracts, and Claim 5
is verified only as a theory-only scope audit.

## Current claim state

| Claim | State | Why |
|---|---|---|
| C1 — constant-depth AC⁰/TC⁰ equivalence | `BLOCKED` | The inclusion graph, repaired routing, and Lean composition checks still import the core transformer/circuit semantics and uniformity obligations. |
| C2 — sufficient volume and width robustness | `BLOCKED` | The exact `D·b` boundary and finite `F_b` correction are audited, but the theorem-level consequence remains part of the unresolved inclusion proof. |
| C3 — looped AC^d/TC^d equivalence | `BLOCKED` | 3,024 finite compositions pass, but no finite table certifies FO-uniformity, completeness, or every `d≥1`. |
| C4 — AHAT to SMAT simulation | `BLOCKED` | Five Lean theorems prove the numerical focusing kernel; the full mixed-precision family constructor and remaining sublayers are not formalized. |
| C5 — theory-only paper scope | `VERIFIED (scoped)` | The source and release audit find definitions, constructions, lemmas, theorems, and proofs, with no paper training/data benchmark. |

## Evidence currently published

- Paper source: arXiv `2605.30523v1`, PDF SHA-256
  `fbc31ec9024e20bef85e4e12a262991f098c093d171d6063d57bcf62419b562b`.
- Claim 4 formal source: Lean `4.32.0`, five kernel-checked theorem reports,
  no `sorryAx` dependency, and source SHA-256
  `be1f47566c7dee4d9ce3ab4f41e63decb0ad52f0ba5de8d299a0fbe46011fd37`.
- Independent Claim 4 checker: 63 resource rows for `b=2..64`, 153
  fixed-point cases across precisions `2..10`, and an expected `0.5` loose-
  temperature discrepancy.
- Claims 1–3: source-pinned proof-obligation ledgers, repaired-routing
  negative control, exact volume checks, 54 deterministic maps, and 3,024
  finite compositions.
- Historical evaluator Space and release manifests remain linked from the
  README and are not relabeled as new theorem verification.

## Open blockers

1. Machine-check the AC⁰ and TC⁰ transformer/circuit inclusions and their
   uniformity semantics.
2. Connect the repaired constant-width routing to the complete source theorem
   without treating imported prose as an executable proof.
3. Formalize the FO-uniform looped construction and both lower inclusions for
   every `d≥1`.
4. Complete the arbitrary-family, mixed-precision AHAT-to-SMAT constructor and
   remaining transformer sublayers for Claim 4.

The evidence ledger records these as blockers instead of promoting the finite
checks, source comparisons, or proof composition to a universal theorem.
