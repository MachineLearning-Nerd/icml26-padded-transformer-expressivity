# Branch audit

The original repository had one publication branch and seven `orx/*` evidence
branches. They were a linear campaign rooted at the frozen baseline; no branch
was discarded. Each old ref was preserved in the recovery bundle
`/tmp/icml111-before-identity-20260815.bundle` before identity normalization.

| Former branch | Former tip | Final branch | Final tip after identity normalization | Purpose |
|---|---|---|---|---|
| `main` | `5a2cfef98c48f241cda195ed9fc8f520831d8f6a` | `main` | `a50bdbfe3d21c3a6c43efa4598b4930fe2610834` before documentation commit | Publication surface |
| `orx/frozen-baseline-judged-reproduction-plus-uv-lock` | `182f72a6447eb9bbb512642cdcd21d16eb169233` | `evidence/frozen-baseline-uv-lock` | `da1e439c168aa528ea461399708fe768877e24ab` | Frozen baseline and locked environment |
| `orx/claim-4-exact-softmax-underflow-certificate` | `3779c458a7722d4218bafcb6e1f7250391ca7c6b` | `evidence/claim-4-softmax-focusing` | `b55a8d12a22494d2db145b4b747b9d1826a33406` | Universal numerical focusing certificate |
| `orx/claim-4-independent-checker-and-evaluator-packag` | `d61755f5604e2093f6ff6629bc3996ac1bb27725` | `audit/claim-4-independent-checker` | `9ad50098b386ec6de57cbc211fa01f5e5c4461e5` | Independent checker and evaluator package |
| `orx/claims-1-3-proof-obligation-and-falsification-au` | `3c3c0d56ed844c2961e7c8a63ebe3e4ac2ef2dec` | `audit/claims-1-3-proof-obligations` | `0ac2df5dd98b972f2a7058a382a6c968c422101d` | Claims 1–3 proof-obligation and falsification audit |
| `orx/cumulative-release-candidate-and-evaluator-audit` | `0c9f970126a6ea082382feaece0d2f969d3ea557` | `release/cumulative-audit` | `2ec8e2e224f4aa9348b0bfeacb2895ab5ed5b5cd` | Cumulative release audit |
| `orx/publication-snapshot-pin-release-run-and-red-tea` | `fa57922a01bc6c5dcf1f7c777308a049209f63a7` | `release/publication-snapshot` | `a72b7320384c6239d7ce0f900511c75f32fbacf8` | Publication snapshot and provenance pin |
| `orx/post-download-repair-enforce-inline-claim-4-numb` | `3c1d9ed4f56302a428e8058534904d3c404a4f36` | `repair/claim-4-inline-checker` | `6e4c5aedd347c24ec1b95010771d6deb9f6e311b` | Final inline Claim 4 checker repair |

## Final invariants

- The default branch is `main`.
- The published branch set contains exactly the eight final names in the
  table; no `master` or `orx/*` branch remains.
- All reachable commits use
  `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>` as
  both author and committer.
- The original refs and branch tips remain recoverable from the verified bundle
  created before rewriting.
- The main branch now carries the paper-first documentation, evidence ledger,
  source manifest, citation, and final verifier; those docs do not alter the
  historical purpose of the evidence branches.
