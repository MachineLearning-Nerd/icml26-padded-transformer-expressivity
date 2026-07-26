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
[`routes.json`](../../../../.openresearch/artifacts/claim2/routes.json).
Current checker: `repro/run_claim_routes.py`.
