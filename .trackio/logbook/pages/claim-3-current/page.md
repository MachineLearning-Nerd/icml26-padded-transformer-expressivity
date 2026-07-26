# Claim 3 — exact current audit

## Contract and verdict

For every `d>=1`, Theorem 5.1 asserts exact FO-uniform AC^d/TC^d
characterizations for the stated precision/width regimes with
`Theta(log^d N)` looping. **Verdict: BLOCKED. Confidence: LOW.**

## Four completed routes

| Route | Method | Result |
| --- | --- | --- |
| 1 | Lemmas 5.1–5.4 proof decomposition | Coherent plan, but semantic reductions/uniformity not mechanized |
| 2 | Deterministic/exhaustive bounded composition | 54 maps and 3,024 cases pass; finite only |
| 3 | Merrill–Sabharwal primary-scope comparison | Supports growing-precision AHAT endpoint, not both new extensions |
| 4 | Assumption-aware falsification | No valid language-class counterexample found |

Raw ledger:
[`routes.json`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/resolve/main/data/claim3/routes.json).
Current checker:
[`repro/run_claim_routes.py`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/blob/main/repro/run_claim_routes.py).
It fails closed if a fourth falsification route is absent or ignores the
theorem assumptions. The historical truth tables remain regression evidence,
not a universal proof.

Fixed command:

```bash
uv run --locked python repro/run_campaign.py
```

Control: removing the falsification route or its exact-assumption audit must
make the current checker exit nonzero.

Run `8a8dfd82-b82a-4287-8bfe-306ff93c8d8b`, Git
`3c3c0d56ed844c2961e7c8a63ebe3e4ac2ef2dec`, completed on Hugging Face
`cpu-upgrade` in 3m32s (runner `199.125634` seconds), with 64 logical CPUs
visible and a one-thread cap. The finite historical regression is
deterministic; no stochastic seed applies.
