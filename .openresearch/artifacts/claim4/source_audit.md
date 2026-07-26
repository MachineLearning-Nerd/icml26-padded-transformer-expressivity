# Claim 4 source audit

## Primary source

- arXiv: `2605.30523v1`
- PDF URL: `https://arxiv.org/pdf/2605.30523`
- Retrieved with browser User-Agent: `2026-07-26T22:06:59+05:30`
- PDF SHA-256:
  `fbc31ec9024e20bef85e4e12a262991f098c093d171d6063d57bcf62419b562b`
- HTML URL: `https://ar5iv.labs.arxiv.org/html/2605.30523`
- Retrieved with browser User-Agent: `2026-07-26T22:07:00+05:30`
- HTML SHA-256:
  `c2f964460955c9047dfb96cd4aa93b8a6384af6ae98d9bcde7451028626ef318`

## Exact contract

Lemma 3.1 universally quantifies over every logarithmic-precision L-uniform
AHAT family. It existentially asserts a logarithmic-precision L-uniform SMAT
family with matching outputs for every natural input length and every string
of that length. This is not a finite-instance or asymptotic-only output claim.

The proof obligations are:

1. Appendix A.3 fixed-point representation, saturation, nearest rounding with
   ties away from zero, and iterative rounding.
2. A source-grid score gap of at least `2^-b`.
3. A sufficiently small, logspace-computable temperature.
4. A constant-factor mixed precision `b'=kappa*b` with enough fractional and
   integer range for scaled scores, exponentials, sums, and value products.
5. Per-layer equality after returning to source precision.
6. Induction through every layer and preservation of L-uniformity.

## Audited paper anchors

- Section 3 and Lemma 3.1: claim statement.
- Appendix A.3, Definitions A.1–A.3: fixed-point operations.
- Appendix A.4: transformer-family and mixed-precision semantics.
- Appendix C.1, Eqs. (31)–(36): gap, temperature, mixed-precision, layer
  induction, and uniformity argument.

## Important distinction

The new Lean certificate reconstructs item 2 and a universal exact
attention-kernel consequence of item 3. It does not silently promote that
kernel into items 4–6. The full paper claim therefore remains `BLOCKED`.
