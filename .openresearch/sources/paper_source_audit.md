# Primary-source audit

- Paper: arXiv `2605.30523v1`, “Revisiting Padded Transformer
  Expressivity: Which Architectural Choices Matter and Which Don’t”
- Browser-UA PDF URL: `https://arxiv.org/pdf/2605.30523`
- PDF retrieval: `2026-07-26T22:06:59+05:30`
- PDF SHA-256:
  `fbc31ec9024e20bef85e4e12a262991f098c093d171d6063d57bcf62419b562b`
- Browser-UA HTML URL: `https://ar5iv.labs.arxiv.org/html/2605.30523`
- HTML retrieval: `2026-07-26T22:07:00+05:30`
- HTML SHA-256:
  `c2f964460955c9047dfb96cd4aa93b8a6384af6ae98d9bcde7451028626ef318`

## Exact scored anchors and quantifiers

1. **Claim 1 — Theorem 4.2, Eqs. (4a–b).** Under sufficient volume
   (Definition 2.3), polynomial padding, and width at most polynomial, for
   any width function `D(N)`, constant-precision `LPT^0_{c,D}` equals
   L-uniform `AC^0`, and log-precision `LPT^0_{l,D}` equals L-uniform
   `TC^0`.
2. **Claim 2 — Definitions 2.1–2.3 and the paragraph after Theorem 4.2.**
   Width and precision are natural-valued functions of input length,
   `V(N) := D(N)b(N)`, and sufficient volume means
   `V(N) = Ω(log N)`. The theorem’s robustness conclusion applies only
   when this premise and its other domain restrictions hold.
3. **Claim 3 — Theorem 5.1, Eqs. (8a–b).** For every integer `d ≥ 1`,
   constant-precision, log-width, polynomially padded LPT families with
   `Θ(log^d N)` looping equal FO-uniform `AC^d`; log-precision,
   constant-width counterparts equal FO-uniform `TC^d`.
4. **Claim 4 — Lemma 3.1.** For every logarithmic-precision L-uniform AHAT
   family, there exists a logarithmic-precision L-uniform SMAT family whose
   output matches for every `N ∈ ℕ` and every `w ∈ Σ^N`.
5. **Claim 5 — Sections 1–6 and Appendices A–C.** This is a theory paper;
   it specifies definitions, constructions, and proofs, not a new empirical
   benchmark, dataset, training procedure, or measured model result.

All asymptotic results retain the paper’s fixed-point semantics, uniformity,
padding, width/precision regime, and “sufficiently large `N`” conventions.
