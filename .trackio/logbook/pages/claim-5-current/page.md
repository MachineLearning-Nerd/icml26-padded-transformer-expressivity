# Claim 5 — theory-only scope

## Verdict

**VERIFIED. Confidence: HIGH.**

The primary PDF SHA-256 is
`fbc31ec9024e20bef85e4e12a262991f098c093d171d6063d57bcf62419b562b`.
The source inventory covers Sections 2–6 and Appendices A–C: formal
definitions, transformer/circuit constructions, lemmas, theorems, discussion,
and proofs.

No dataset, optimizer, loss, training schedule, checkpoint, empirical
benchmark protocol, or measured model result appears in the paper. The
cumulative source audit emits:

```json
{
  "empirical_benchmark_or_training_protocol": false,
  "source_sections": [
    "2. Preliminaries",
    "3. SMATs Can Simulate AHATs",
    "4. Padded Constant-depth Transformers Are Constant-depth Circuits",
    "5. Looped Padded Transformers Are Highly Uniform Growing-depth Circuits",
    "6. Discussion",
    "A--C formal definitions and proofs"
  ]
}
```

Current checker:
[`repro/run_audit.py`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/blob/main/repro/run_audit.py).
Raw source audit:
[`source_audit.md`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/resolve/main/data/claim5/source_audit.md).
Fixed command:

```bash
uv run --locked python repro/run_campaign.py
```

Limitation: the verdict is about arXiv v1 itself, not every related work cited
by the paper.

Run `8a8dfd82-b82a-4287-8bfe-306ff93c8d8b`, Git
`3c3c0d56ed844c2961e7c8a63ebe3e4ac2ef2dec`, reran the source audit on
Hugging Face `cpu-upgrade` in 3m32s (cumulative runner `199.125634` seconds),
with 64 logical CPUs visible and a one-thread cap. This audit is deterministic;
no stochastic seed applies.

Negative control: the release audit injects a synthetic empirical marker into
the scope classifier and requires the theory-only verdict to be rejected.
