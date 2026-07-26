# Claim 2 — exact current audit

## Contract and verdict

Definitions 2.1–2.3 source-verify `V(N)=D(N)b(N)` and sufficient volume
`V(N)=Omega(log N)`. The scored claim also says this governs expressivity
robustness under Theorem 4.2. **Verdict: BLOCKED. Confidence: LOW.**

## Four completed routes

| Route | Method | Result |
| --- | --- | --- |
| 1 | Exact source/quantifier audit | Definition verified; consequence depends on Theorem 4.2 |
| 2 | Actual fixed-point alphabet capacity | Rejects the historical binary-cell proxy as a full verifier |
| 3 | London–Kanade scope comparison | Prior endpoint is narrower than arbitrary-width robustness |
| 4 | Assumption-aware falsification | No valid expressivity counterexample found |

The scientific negative control uses Appendix A.3's actual alphabet. At
`N=8,b=1,D=2`, `F_1` has 7 values and `7^2=49>=8`, although the old proxy says
`Db=2<ceil(log2 8)=3`. This does **not** falsify Definition 2.3 or Theorem 4.2;
it proves only that the old finite proxy was not faithful evidence.

Raw ledger:
[`routes.json`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/resolve/main/data/claim2/routes.json).
Current checker:
[`repro/run_claim_routes.py`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/blob/main/repro/run_claim_routes.py).
Fixed command:

```bash
uv run --locked python repro/run_campaign.py
```

Run `8a8dfd82-b82a-4287-8bfe-306ff93c8d8b`, Git
`3c3c0d56ed844c2961e7c8a63ebe3e4ac2ef2dec`, completed on Hugging Face
`cpu-upgrade` in 3m32s (runner `199.125634` seconds), with 64 logical CPUs
visible and a one-thread cap. No stochastic seed applies.
