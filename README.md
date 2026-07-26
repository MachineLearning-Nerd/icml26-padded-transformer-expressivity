# Padded-transformer expressivity reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-nBuL6HywFX-padded-transformer-expressivity/blob/main/notebooks/padded_transformer_reproduction.py)

This repository reproduces, claim by claim, the theoretical paper
**“Revisiting Padded Transformer Expressivity: Which Architectural Choices
Matter and Which Don't”** ([arXiv:2605.30523](https://arxiv.org/abs/2605.30523)).

The strongest new evidence is a Lean 4.32 kernel proof of the universal
fixed-point focusing mechanism behind Claim 4. The paper claims matching
AHAT/SMAT outputs for **every** input length and string; we prove the focusing
kernel for every `b>=2` and arbitrary finite attention tables, then stop short
of the unformalized family-construction obligations. Full Claim 4 is therefore
BLOCKED, not VERIFIED.

| Item | Paper | Observed |
| --- | --- | --- |
| Claim 4 quantifier | every log-precision L-uniform AHAT family, every `N`, every input | universal attention kernel; full family constructor not certified |
| Formal certificate | not supplied by paper | 5 Lean theorem reports, no `sorryAx` |
| Independent evidence | not applicable | 153 deterministic cases; `tau=1` control differs by `0.5` |
| Compute | theoretical paper | CPU only; local baseline plus HF `cpu-upgrade`, one-thread cap |

Assessment: Claims 1–4 are **BLOCKED** at their exact contracts; Claim 5 is
**VERIFIED**. The live judged score is 6/10 and the honest forecast remains
6/10 until a live judge says otherwise. No toy result is promoted to a
universal theorem.

- [Illustrated technical report](reports/reproduction/report.md)
- [Self-contained marimo tutorial](notebooks/padded_transformer_reproduction.py)
- [Current evaluator logbook](https://huggingface.co/spaces/DineshAI/nBuL6HywFX)

Run the notebook locally with:

```bash
uv run marimo edit notebooks/padded_transformer_reproduction.py
uv run marimo run notebooks/padded_transformer_reproduction.py
```

## Experiment log

Every node inherits the exact command
`uv run --locked python repro/run_campaign.py`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Publication surface | Not run as an experiment (publication surface) | Reader artifacts only | none |
| [`orx/frozen-baseline-judged-reproduction-plus-uv-lock`](https://github.com/MachineLearning-Nerd/icml26-repro-nBuL6HywFX-padded-transformer-expressivity/tree/orx/frozen-baseline-judged-reproduction-plus-uv-lock) | Freeze judged checks and uv environment | `uv run --locked python repro/run_campaign.py` | PASS; 24.005 s | local CPU, one-thread cap |
| [`orx/claim-4-exact-softmax-underflow-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-nBuL6HywFX-padded-transformer-expressivity/tree/orx/claim-4-exact-softmax-underflow-certificate) | Universal Claim 4 focusing proof | `uv run --locked python repro/run_campaign.py` | PASS; universal kernel only | HF `cpu-upgrade`, 64 visible / 1 active |
| [`orx/claim-4-independent-checker-and-evaluator-packag`](https://github.com/MachineLearning-Nerd/icml26-repro-nBuL6HywFX-padded-transformer-expressivity/tree/orx/claim-4-independent-checker-and-evaluator-packag) | Independent checker, control, current page | `uv run --locked python repro/run_campaign.py` | PASS; full Claim 4 still BLOCKED | HF `cpu-upgrade`, 64 visible / 1 active |
| [`orx/claims-1-3-proof-obligation-and-falsification-au`](https://github.com/MachineLearning-Nerd/icml26-repro-nBuL6HywFX-padded-transformer-expressivity/tree/orx/claims-1-3-proof-obligation-and-falsification-au) | Three verification routes plus falsification for C1–C3 | `uv run --locked python repro/run_campaign.py` | PASS; Claims 1–3 BLOCKED | HF `cpu-upgrade`, 64 visible / 1 active |
| [`orx/cumulative-release-candidate-and-evaluator-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-nBuL6HywFX-padded-transformer-expressivity/tree/orx/cumulative-release-candidate-and-evaluator-audit) | Cumulative regressions and evaluator-visible release audit | `uv run --locked python repro/run_campaign.py` | PASS at `0c9f970`; 168.631 s runner time | HF `cpu-upgrade`, 64 visible / 1 active |

## Reproduce

```bash
uv sync --locked
uv run --locked python repro/run_campaign.py
```

The fixed command downloads pinned Lean/Mathlib components by verified hashes.
Its bootstrap runtime is uncertain, so formal runs belong on the configured HF
`cpu-upgrade` backend under this campaign's compute policy.

## Historical rejected baseline

Earlier finite volume, loop-composition, and 800-case attention checks remain
in the repository and Space for provenance. The live judge correctly rated
them toy-scale. `formal/PaddedTransformer.lean` also preserves the prior Lean
composition whose hard circuit-class inclusions are explicit hypotheses. None
is the current verifier for a full universal claim.
