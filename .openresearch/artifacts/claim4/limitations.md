# Claim 4 limitations and deviations

## What is proved

The universal exact softmax-focusing kernel is Lean-kernel checked for
arbitrary finite attention tables and arbitrary real values at every `b>=2`.
This is not a toy finite-N enumeration.

## What is not proved

- `b'=4b` is an explicit focusing witness. The complete paper construction
  may require a larger family-dependent constant `kappa` to avoid overflow
  while summing up to `N` terms and handling width `D`.
- The formal numerator and denominator are real Finset sums after pointwise
  mixed-grid rounding. They do not encode Appendix A.3 saturation and
  iterative rounding operation by operation.
- The certificate does not implement or prove a logspace transducer that
  emits the entire SMAT family.
- The remaining projections, residual path, MLP, layer normalization, and
  layer-by-layer family induction are not formalized.
- The certificate uses a restricted rounding function whose behavior is
  proved only on the two constructed cases: strictly below half a grid step
  and exactly one. Those are the only cases reached by the kernel theorem.

Therefore the exact Lemma 3.1 contract remains `BLOCKED`; only its universal
attention-focusing subclaim is `VERIFIED`.
