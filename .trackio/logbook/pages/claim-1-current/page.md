# Claim 1 — exact current audit

## Contract and verdict

Theorem 4.2 asserts two language-class equalities for every admissible width
function under sufficient volume, polynomial padding, and polynomial maximum
width. **Verdict: BLOCKED. Confidence: LOW.**

The previous Lean theorem is not the current verifier: it takes the four hard
source inclusions as hypotheses and proves their set-equality composition.

## Four completed routes

| Route | Method | Result |
| --- | --- | --- |
| 1 | Eight-edge source inclusion reconstruction | Dependency graph closes only if hard inclusions are accepted |
| 2 | Lean signature, kernel, and axiom inspection | 11 reports pass; semantic inclusions remain hypotheses |
| 3 | London–Kanade primary-scope comparison | Supports log-width endpoints, not the new arbitrary-width theorem |
| 4 | Assumption-aware falsification | Printed routing contradicted; admissible repair works; no theorem counterexample |

Raw ledger:
[`routes.json`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/resolve/main/data/claim1/routes.json).
Current checker:
[`repro/run_claim_routes.py`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/blob/main/repro/run_claim_routes.py).
The preserved Lean boundary is visible in
[`formal/PaddedTransformer.lean`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/blob/main/formal/PaddedTransformer.lean).
Fixed command:

```bash
uv run --locked python repro/run_campaign.py
```

The validator requires all four distinct routes and rejects unsupported
promotion to VERIFIED. Finite tables are regressions only.

Control: deleting the fourth falsification route or changing the verdict to
VERIFIED must make `repro/run_claim_routes.py` exit nonzero. The scientific
routing control also requires the printed swap to fail and the admissible
repair to pass.

Run `8a8dfd82-b82a-4287-8bfe-306ff93c8d8b`, Git
`3c3c0d56ed844c2961e7c8a63ebe3e4ac2ef2dec`, completed on Hugging Face
`cpu-upgrade` in 3m32s (runner `199.125634` seconds). It saw 64 logical CPUs
and capped all numeric/proof work at one thread. No stochastic seed applies to
this symbolic/source route audit.

## Remaining blockers

A complete certificate must define transformer and circuit semantics and prove
all AC0/TC0 lower and upper inclusions, repaired routing, and uniformity. No
such certificate exists in the candidate.
