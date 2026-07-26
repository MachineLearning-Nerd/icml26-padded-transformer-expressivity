# Claim 1 source audit

Theorem 4.2 quantifies over every width function `D(N)` satisfying sufficient
volume and a polynomial upper bound. Equation (4a) concerns constant precision
and L-uniform AC0; Eq. (4b) concerns log precision and L-uniform TC0.
Polynomial padding and the paper's fixed-point transformer semantics remain in
force.

The proof is a sandwich:

- Theorem 4.1 supplies log-width endpoints from London–Kanade.
- Lemma 4.1 claims the new constant-width log-precision lower inclusion.
- Lemma 4.2 claims polynomial-width/precision upper inclusions.
- volume arithmetic and zero-padding are used to cover intermediate widths.

The judged Lean theorem takes these semantic inclusions as hypotheses. That is
why a kernel check of the set-equality composition does not close Claim 1.
