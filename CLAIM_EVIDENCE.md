# Claim-to-evidence ledger

This ledger separates what the paper claims, what this repository computes,
and why a result is or is not promoted. The paper’s claims are asymptotic and
universal; finite experiments and proof composition are supporting evidence,
not automatic proofs of those claims.

## Shared provenance

- Paper: *Revisiting Padded Transformer Expressivity: Which Architectural
  Choices Matter and Which Don't*, arXiv `2605.30523v1`.
- Primary PDF SHA-256:
  `fbc31ec9024e20bef85e4e12a262991f098c093d171d6063d57bcf62419b562b`.
- Prior primary source used in the derivation: London and Kanade,
  arXiv `2505.21024`, PDF SHA-256
  `c68e8763f1571acc6713886b82f0b3165704bad2ded7fe4437b0c648e89a715b`.
- Lean source certificate: `formal/Claim4Exact.lean`, SHA-256
  `be1f47566c7dee4d9ce3ab4f41e63decb0ad52f0ba5de8d299a0fbe46011fd37`.
- All 21 reachable historical commits were normalized to
  `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`.

## C1 — constant-depth AC⁰/TC⁰ equivalence

**Paper anchor:** Theorem 4.2 and Eqs. (4a–b), with Lemmas 4.1–4.2.
**Verdict:** `BLOCKED`.

### Production path

1. `repro/run_theorem42.py` builds the two inclusion sandwiches from the
   cited source results, the sufficient-volume premise, and width padding.
2. `repro/run_theorem42_obligations.py` records premises, dependencies, source
   anchors, route state, and fail-closed closure decisions.
3. `repro/run_claim_routes.py` runs source, machine, independent-source, and
   falsification routes. The printed two-field layer-2 pointer swap fails on
   all 79 noncoincident source/gate assignments; the explicit six-coordinate
   self/source/gate repair passes those assignments.
4. `formal/PaddedTransformer.lean` kernel-checks theorem composition and the
   repaired routing signatures, while explicitly taking the source inclusions
   as hypotheses.

### Evidence boundary

The inclusion graph is a dependency map, not an independent proof of the
transformer and circuit semantics. Lean checks the new routing and composition
glue but does not formalize AC⁰/TC⁰, L-uniformity, fixed-point arithmetic, or
all source lemmas. A repaired proof sentence is not itself a closed theorem.

## C2 — sufficient volume and width robustness

**Paper anchors:** Definitions 2.1–2.3 and the paragraph after Theorem 4.2.
**Verdict:** `BLOCKED`.

### Production path

- `repro/src/volume.py` and `repro/run_audit.py` check the finite relation
  `V(N)=D(N)b(N)` and the position-encoding threshold
  `D·b≥ceil(log₂N)`.
- The audit checks admissible and insufficient-volume configurations across
  the finite range and records `positions_checked` in `outputs/summary.json`.
- The old binary-coordinate proxy is retained as a negative control: the
  actual fixed-point alphabet has `|F₁|=7`, so at `N=8,D=2` there are 49
  coordinate tuples even though `D·b=2<3`.
- The width-lift construction verifies that extra residual coordinates can be
  held at zero without changing the embedded computation.

### Evidence boundary

The finite capacity correction rejects an over-strong proxy; it does not
falsify the paper’s theorem. The asymptotic width-robustness consequence still
depends on the unresolved inclusion and uniformity obligations recorded under
C1.

## C3 — looped AC^d/TC^d equivalence

**Paper anchor:** Theorem 5.1, Lemma 5.1, and Eqs. (8a–b).
**Verdict:** `BLOCKED`.

### Production path

- `repro/src/circuits.py` constructs deterministic AND/OR/NOT and threshold
  maps and applies them repeatedly.
- `repro/run_audit.py` checks 54 maps and 3,024 exhaustive small truth-table
  compositions through the recorded depths.
- `repro/run_claim_routes.py` and `.openresearch/artifacts/claim3/routes.json`
  add source, independent-primary-source, and falsification routes.

### Evidence boundary

The finite checks support the `f^r` composition mechanism in Lemma 5.1. They do
not construct an FO-uniform circuit family, prove completeness reductions,
establish both class inclusions for every `d≥1`, or close the AHAT-to-SMAT
transfer used by the growing-precision lower bound.

## C4 — log-precision AHAT-to-SMAT simulation

**Paper anchor:** Lemma 3.1 and proof equations (31)–(36).
**Verdict:** `BLOCKED` for the full paper contract; numerical kernel
`VERIFIED_SCOPED`.

### Production path

1. `formal/Claim4Exact.lean` proves the numerical focusing kernel for every
   finite attention index type, arbitrary ties, and every `b≥2`: with mixed
   precision `4b` and `τ=2⁻³ᵇ`, maximal exponentials round to one and
   nonmaximal exponentials underflow to zero.
2. `repro/run_claim4_formal.py` checks the pinned Lean toolchain, source hash,
   forbidden escape tokens, `#print axioms` output, and absence of `sorryAx`.
   The durable certificate reports five kernel-checked theorems.
3. `repro/run_claim4_independent.py` independently checks all integer `b` in
   `[2,64]`, 153 finite tie/length cases for precisions `2..10`, and a
   `temperature=1` negative control. The hard output is `1.0`, the loose
   softmax output is `0.5`, and the control is expected to fail.

### Evidence boundary

The certificate does not formalize the complete mixed-precision range,
logspace family constructor, residual/MLP/layer-normalization semantics, or
the full arbitrary-family AHAT-to-SMAT transformation. The five theorem
reports and finite checker therefore cannot be promoted to the universal
Lemma 3.1 contract.

## C5 — theory-only paper scope

**Paper anchors:** Sections 1–6 and Appendices A–C.
**Verdict:** `VERIFIED (scope audit)`.

`repro/src/audit.py` inventories the paper sections and
`repro/run_release_audit.py` checks the release package. The source contains
definitions, constructions, lemmas, theorems, discussions, and proofs, but no
paper training protocol, dataset, or measured benchmark. This verifies the
classification of the paper’s scope; it does not validate its mathematics.

## Non-claims

- No finite `N` sweep proves an asymptotic language-class equality.
- A proof gap or a bug in one printed sentence is not a theorem counterexample
  when an admissible repair remains available.
- A Lean theorem with imported hypotheses does not prove those hypotheses.
- Historical evaluator scores and Hugging Face artifacts are provenance, not
  new independent theorem verdicts.
