---
title: "ICML 2026 audit — Padded Transformer Expressivity"
emoji: "🧭"
colorFrom: indigo
colorTo: cyan
sdk: static
pinned: false
tags:
  - icml2026-repro
  - paper-2605.30523
---

# ICML 2026 reproduction — Padded Transformer Expressivity

This repository is a paper-first, claim-by-claim audit of [*Revisiting Padded
Transformer Expressivity: Which Architectural Choices Matter and Which Don't*](https://arxiv.org/abs/2605.30523).
It preserves the finite checks, proof-assistant certificate, negative controls,
source pins, and evaluator artifacts while keeping a finite reproduction
separate from an asymptotic complexity theorem.

The repository was formerly named
`icml26-repro-nBuL6HywFX-padded-transformer-expressivity`. Its final public
name is `icml26-padded-transformer-expressivity`.

## Paper in one paragraph

The paper studies how polynomial padding, attention type, width, precision,
uniformity, and looping affect the expressive power of transformers. Its
headline results characterize padded transformer families using circuit classes:
constant precision is associated with AC⁰, logarithmic precision with TC⁰, and
polylogarithmic looping with the corresponding growing-depth classes. The
paper also argues that softmax and average hard attention agree under its
fixed-point and temperature assumptions. The claims are universal statements
over input lengths, model families, and circuit classes—not benchmark metrics.

| Field | Value |
|---|---|
| Paper | *Revisiting Padded Transformer Expressivity: Which Architectural Choices Matter and Which Don't* |
| Authors | Anej Svete, William Merrill, Ryan Cotterell, and Ashish Sabharwal |
| Version | arXiv `2605.30523v1`, submitted 2026-05-28 |
| Primary source | [arXiv:2605.30523](https://arxiv.org/abs/2605.30523) |
| Recorded OpenReview handle | `nBuL6HywFX` |
| Paper implementation | No paper-provided training/data repository is assumed; this repository is the reproduction audit |

## Claim verdicts

These verdicts describe the evidence in this repository, not the truth value
of the paper’s mathematics. `BLOCKED` means the current artifact does not
machine-certify the complete universal contract. It does not mean that a
counterexample was found.

| Claim | Paper statement | Evidence produced here | Verdict |
|---|---|---|---|
| C1 | Under Theorem 4.2’s hypotheses, constant-precision padded L-uniform transformers equal L-uniform AC⁰, and log-precision ones equal L-uniform TC⁰ | Inclusion graph, sufficient-volume witnesses, repaired constant-width routing, proof-obligation ledger, and Lean composition checks | **BLOCKED** |
| C2 | Volume is `V(N)=D(N)b(N)`; sufficient volume is `Ω(log N)` and supports width robustness under the theorem’s restrictions | Exact finite position-capacity checks, the `F_b` cardinality correction, width-lift audit, and theorem-domain checks | **BLOCKED** |
| C3 | `Θ(log^d N)` looping yields FO-uniform AC^d/TC^d in the stated precision regimes | 54 deterministic gate maps and 3,024 finite compositions with source, independent, and falsification routes | **BLOCKED** |
| C4 | Log-precision L-uniform AHAT families have matching SMAT simulators | Lean 4.32 kernel certificate for the numerical focusing kernel, 63 resource rows, 153 independent fixed-point cases, and a loose-temperature negative control | **BLOCKED** |
| C5 | The work is a theory paper rather than an empirical benchmark/training result | Hash-pinned full source inventory and release-scope audit | **VERIFIED (scope audit)** |

The central limitation is explicit: the formal certificate proves the
fixed-point softmax-focusing mechanism and layerwise equality, but the full
AC⁰/TC⁰ inclusions, family constructors, uniformity transformations, and
remaining transformer semantics are still imported or only audited. See
[`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md) for the exact boundary.

## How each claim is produced

| Claim | Producers | Durable evidence and checks |
|---|---|---|
| C1 | `repro/run_theorem42.py`, `repro/run_theorem42_obligations.py`, `repro/run_claim_routes.py`, `formal/PaddedTransformer.lean` | `outputs/summary.json`, `outputs/audit_stdout.json`, `.openresearch/artifacts/claim1/`, and [`docs/THEOREM_4_2_DERIVATION.md`](docs/THEOREM_4_2_DERIVATION.md) |
| C2 | `repro/run_audit.py`, `repro/run_theorem42_obligations.py`, `repro/src/volume.py` | Exact `D·b`/position checks, the insufficient-volume `F_b` control, and `.openresearch/artifacts/claim2/` |
| C3 | `repro/run_audit.py`, `repro/run_claim_routes.py`, `repro/src/circuits.py` | 54 maps, 3,024 compositions, `outputs/summary.json`, and `.openresearch/artifacts/claim3/` |
| C4 | `repro/run_claim4_formal.py`, `repro/run_claim4_independent.py`, `formal/Claim4Exact.lean` | Five kernel-checked theorem reports, no `sorryAx`, 153 finite cases, raw certificates under `.openresearch/artifacts/claim4/raw/`, and the expected-failure control |
| C5 | `repro/run_release_audit.py`, `repro/src/audit.py` | Source inventory, no-data/no-training classification, visibility matrix, and `.openresearch/artifacts/claim5/` |

## Branch map

Every branch is one evidence step in the same linear campaign. The old
`orx/` names are recorded only as provenance; the published repository uses
the following purpose-based names:

| Final branch | Former branch | Purpose |
|---|---|---|
| `main` | `main` | Publication surface and reader-facing documentation |
| `evidence/frozen-baseline-uv-lock` | `orx/frozen-baseline-judged-reproduction-plus-uv-lock` | Freeze the baseline command and environment |
| `evidence/claim-4-softmax-focusing` | `orx/claim-4-exact-softmax-underflow-certificate` | Add the universal numerical focusing certificate |
| `audit/claim-4-independent-checker` | `orx/claim-4-independent-checker-and-evaluator-packag` | Add the independent checker, controls, and evaluator package |
| `audit/claims-1-3-proof-obligations` | `orx/claims-1-3-proof-obligation-and-falsification-au` | Audit Claims 1–3 through source, machine, independent, and falsification routes |
| `release/cumulative-audit` | `orx/cumulative-release-candidate-and-evaluator-audit` | Cumulative regression and evaluator-visible release audit |
| `release/publication-snapshot` | `orx/publication-snapshot-pin-release-run-and-red-tea` | Pin the release snapshot and publication provenance |
| `repair/claim-4-inline-checker` | `orx/post-download-repair-enforce-inline-claim-4-numb` | Enforce the final inline Claim 4 checker values |

The complete old-to-new tip mapping and branch invariants are in
[`BRANCH_AUDIT.md`](BRANCH_AUDIT.md).

## Historical evaluator context

The repository preserves an earlier judged Hugging Face Space and its release
manifest at [`DineshAI/nBuL6HywFX`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX).
Those artifacts are historical provenance for the campaign, not a new claim
that finite checks or this README prove the paper’s asymptotic results. The
published evidence deliberately retains the earlier rejected finite baseline,
the repaired routing proof obligation, the `tau=1` control, and every current
blocker.

## Reproduce

The project is pinned to Python 3.12, NumPy 2.5.1, pytest 9.1.1, and the
checked `uv.lock` environment:

```bash
uv sync --locked
uv run --locked python repro/run_campaign.py
uv run --locked pytest -q repro/tests
```

The campaign includes the pinned Lean/Mathlib bootstrap and is intentionally
the full, potentially long path. For focused checks:

```bash
uv run --locked python repro/run_audit.py
uv run --locked python repro/run_claim4_independent.py
uv run --locked python repro/run_lean_formal_check.py
```

The Lean source itself is pinned by `formal/lean-toolchain` and the formal
audit records Lean `4.32.0`, Mathlib revision
`81a5d257c8e410db227a6665ed08f64fea08e997`, and the source hash. No GPU,
dataset, or model-training run is required by the paper’s theory-only scope.

## Repository layout

- `repro/` — deterministic producers, route validators, and tests.
- `formal/` — Lean source for the Claim 4 numerical kernel and theorem glue.
- `outputs/` — machine-readable finite audit summaries.
- `.openresearch/artifacts/` — claim contracts, route ledgers, limitations, and raw certificates.
- `docs/` — source map, theorem audit, derivation, and formal boundary.
- `reports/reproduction/` — evaluator-facing report and diagrams.
- `release/` — publication allowlist, visibility matrix, command log, and hashes.

## Citation

```bibtex
@inproceedings{svete2026revisiting,
  title     = {Revisiting Padded Transformer Expressivity: Which Architectural Choices Matter and Which Don't},
  author    = {Svete, Anej and Merrill, William and Cotterell, Ryan and Sabharwal, Ashish},
  booktitle = {International Conference on Machine Learning},
  year      = {2026},
  eprint    = {2605.30523},
  archivePrefix = {arXiv}
}
```

For the software record, see [`CITATION.cff`](CITATION.cff).

## Thank you

Thank you to Anej Svete, William Merrill, Ryan Cotterell, and Ashish Sabharwal
for the precise theoretical treatment of padded transformer expressivity and
for making the paper’s definitions, constructions, and proof scope available
for independent auditing. This repository is an audit and reproduction aid;
it is not an official implementation or an assertion of authorship.

## Attribution

The repository’s audit commits are attributed to
`MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`. The
paper and all cited prior work remain the property of their respective authors.
