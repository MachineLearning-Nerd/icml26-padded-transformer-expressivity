# Evaluator guide — Claim 4

## Current result

- Exact full-claim verdict: **BLOCKED**
- Universal numerical focusing subclaim: **VERIFIED**
- Current verifier: `repro/run_claim4_formal.py`
- Independent checker and control: `repro/run_claim4_independent.py`
- Fixed command: `uv run --locked python repro/run_campaign.py`

The verifier exits nonzero on a Lean error, forbidden proof escape, toolchain
or dependency mismatch, missing axiom reports, failed independent check, or a
negative control that unexpectedly passes.

The previous 800-case implementation is preserved but is labeled
**Historical rejected baseline**. It is not the current verifier.

## Evidence lookup

Start at the candidate logbook current index and open “Claim 4 — current
universal kernel certificate.” The page states the exact paper contract,
machine-checked scope, raw results, command, compute, control, and limitations
without requiring repository knowledge.
