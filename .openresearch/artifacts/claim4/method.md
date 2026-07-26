# Claim 4 method

The accepted numerical core uses no finite bound on input length, number of
attention positions, score values, value values, or number of ties.

1. Work at source precision `b>=2` and mixed precision `b'=4b`.
2. Select `tau=2^(-3b)`.
3. Any distinct b-grid score is at least `2^-b` below the maximum. Scaling by
   `1/tau` therefore produces a gap of at least `2^(2b)`.
4. The proved integer inequality `4b+1 <= 2^(2b)` and the standard analytic
   exponential bound imply every nonmaximal exponential is strictly below
   half a mixed grid step.
5. Nearest rounding sends all such exponentials to zero; maximal
   exponentials are exactly one.
6. Finset congruence proves equality of numerator, denominator, and quotient
   for arbitrary finite attention tables and arbitrary values.
7. A separate list induction proves that pointwise-equal replacement layers
   produce equal states through an arbitrary finite stack.

Lean 4.32.0 with pinned Mathlib kernel-checks these steps. The independent
Python checker imports no reproduction modules, reconstructs all resource
inequalities for `b=2..64`, exercises deterministic fixed-point tables, and
requires the `tau=1` negative control to disagree.

The finite Python sweep is a regression and independence check only. It is not
used to discharge a universal quantifier.
