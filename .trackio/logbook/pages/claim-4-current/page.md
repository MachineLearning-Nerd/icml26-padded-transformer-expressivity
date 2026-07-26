# Claim 4 — current universal kernel certificate

## Exact paper claim

Lemma 3.1 states: for every logarithmic-precision L-uniform AHAT family
`{T_N}`, there exists a logarithmic-precision L-uniform SMAT family `{T'_N}`
whose outputs match for every natural `N` and every `w in Sigma^N`.

Source anchors: Section 3, Lemma 3.1; Appendix C.1, Eqs. (31)–(36);
fixed-point Definitions A.1–A.3. Primary PDF SHA-256:
`fbc31ec9024e20bef85e4e12a262991f098c093d171d6063d57bcf62419b562b`.

## Verdict

**Full Claim 4: BLOCKED. Universal attention-focusing kernel: VERIFIED.**

The current evidence is materially stronger than the historical 800 cases:
Lean proves the numerical kernel for every `b>=2`, arbitrary finite attention
index types, arbitrary score and value tables, and arbitrary tie patterns.
It does not yet prove every obligation of the family-wide source lemma.

## What the kernel proves

At source precision `b`, choose mixed precision `b'=4b` and
`tau=2^(-3b)`. Distinct b-grid scores have gap at least `2^-b`. The Lean proof
establishes

```text
4b + 1 <= 2^(2b)
exp(-2^(2b)) < 2^(-4b-1).
```

Thus mixed-grid nearest rounding sends every nonmaximal exponential to zero
and every maximal exponential to one. Finset congruence then gives exact
equality of the hard and rounded-soft numerator, denominator, and quotient,
including ties. No maximum sequence length is assumed.

## Reproduce

Pinned command:

```bash
uv run --locked python repro/run_campaign.py
```

Current source:

- [`formal/Claim4Exact.lean`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/blob/main/formal/Claim4Exact.lean)
- [`repro/run_claim4_formal.py`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/blob/main/repro/run_claim4_formal.py)
- [`repro/run_claim4_independent.py`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/blob/main/repro/run_claim4_independent.py)

The cumulative command is fail-closed and exits nonzero on a kernel-check
failure, a dependency mismatch, an independent-check failure, or a negative
control that unexpectedly matches.

## Raw current output

Formal run on Hugging Face `cpu-upgrade`:

```json
{
  "verdict": "lean_kernel_verified",
  "toolchain": "leanprover/lean4:v4.32.0",
  "mathlib_revision": "81a5d257c8e410db227a6665ed08f64fea08e997",
  "kernel_checked_theorems": 5,
  "sorry_ax_dependency": false,
  "logical_cpus_visible": 64,
  "thread_cap": 1,
  "source_sha256": "be1f47566c7dee4d9ce3ab4f41e63decb0ad52f0ba5de8d299a0fbe46011fd37",
  "formal_runtime_seconds": 191.602762,
  "cumulative_runtime_seconds": 199.074833
}
```

Experiment wall time was approximately 3m30s. Required core estimate was one active proof
core with 2–8 visible cores sufficient; `cpu-upgrade` was selected because
the pinned Mathlib bootstrap/cache runtime was uncertain. The actual runner
saw 64 logical CPUs and capped numeric/proof threads at one.

The formal certificate is available as
[`formal_certificate_run_96a14223.json`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/resolve/main/data/claim4/formal_certificate_run_96a14223.json).
The independent checker is rerun by the same command; its raw JSON is
[`claim4_independent_checker.json`](https://huggingface.co/spaces/DineshAI/nBuL6HywFX/resolve/main/data/claim4/claim4_independent_checker.json)
from run `96a14223-d5c0-43bd-aa53-00053a068b62`.
That run used Git
`d61755f5604e2093f6ff6629bc3996ac1bb27725`.

## Independent checker and negative control

The independent checker imports no reproduction implementation. It
reconstructs the integer resource inequality using exact integers, exercises
fixed-point ties and multiple attention lengths with deterministic seed
`260530523`, and checks that every constructed nonmaximal exponential rounds
to zero.

The control intentionally uses `tau=1` for scores `[0,-2^-8]` and values
`[1,0]`. It must differ from the hard output. The checker treats an accidental
match as a failure, isolating temperature focusing rather than testing a
vacuous invariant.

## Limitations

The source lemma also requires a family-dependent mixed-precision range large
enough for arbitrary `N` and `D`, Appendix A.3 iterative rounding and
saturation throughout the attention computation, a logspace family
constructor, every remaining sublayer, and layer induction. Those obligations
are not in the current certificate. Consequently, this page does not claim
that Lemma 3.1 itself is verified.
