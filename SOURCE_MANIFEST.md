# Source and provenance manifest

## Paper

| Field | Value |
|---|---|
| Title | *Revisiting Padded Transformer Expressivity: Which Architectural Choices Matter and Which Don't* |
| Authors | Anej Svete; William Merrill; Ryan Cotterell; Ashish Sabharwal |
| Version | arXiv `2605.30523v1`, submitted 2026-05-28 |
| Abstract/source URL | https://arxiv.org/abs/2605.30523 |
| PDF URL | https://arxiv.org/pdf/2605.30523 |
| PDF SHA-256 | `fbc31ec9024e20bef85e4e12a262991f098c093d171d6063d57bcf62419b562b` |
| HTML URL | https://arxiv.org/html/2605.30523 |
| HTML SHA-256 | `c2f964460955c9047dfb96cd4aa93b8a6384af6ae98d9bcde7451028626ef318` |
| Recorded OpenReview handle | `nBuL6HywFX` |

The retrieval timestamps and exact paper anchors are preserved in
`.openresearch/sources/paper_source_audit.md` and `docs/paper_evidence.md`.

## Prior primary source used by the derivation

| Field | Value |
|---|---|
| Paper | London and Kanade, *Pause Tokens Strictly Increase the Expressivity of Constant-Depth Transformers* |
| URL | https://arxiv.org/pdf/2505.21024 |
| PDF SHA-256 | `c68e8763f1571acc6713886b82f0b3165704bad2ded7fe4437b0c648e89a715b` |
| Use | Prior AC⁰/TC⁰ and routing results cited by the current paper and explicitly imported by the derivation |

## Formal and executable sources

| Source | Pin or integrity record |
|---|---|
| Lean source | `formal/Claim4Exact.lean`, SHA-256 `be1f47566c7dee4d9ce3ab4f41e63decb0ad52f0ba5de8d299a0fbe46011fd37` |
| Lean toolchain | `leanprover/lean4:v4.32.0` in `formal/lean-toolchain` |
| Mathlib | Revision `81a5d257c8e410db227a6665ed08f64fea08e997` |
| Python environment | Python 3.12, NumPy 2.5.1, pytest 9.1.1, marimo pinned by `uv.lock` |
| Reproduction command | `uv run --locked python repro/run_campaign.py` |
| Formal checker | `repro/run_lean_formal_check.py` |
| Independent checker | `repro/run_claim4_independent.py` |

## Durable evidence

- `outputs/summary.json` and `outputs/audit_stdout.json` contain the finite
  audit summaries.
- `.openresearch/artifacts/claim1/` through `claim5/` contain claim contracts,
  methods, route ledgers, source audits, limitations, and evaluator pages.
- `.openresearch/artifacts/claim4/raw/formal_certificate_run_96a14223.json`
  records five kernel-checked theorem reports and no `sorryAx` dependency.
- `.openresearch/artifacts/claim4/raw/claim4_independent_checker.json`
  records 63 resource rows, 153 positive cases, and the expected negative
  control.
- `release/visibility_matrix.json`, `release/upload_manifest.sha256`, and
  `release/hf_upload_allowlist.json` define the historical publication scope.

## Dataset and training classification

The paper is theoretical. No paper dataset, model checkpoint, or training run
is required for its claims. The finite audit uses deterministic truth tables,
fixed-point arithmetic, source text, and a Lean kernel; its CPU/Hugging Face
runtime records are reproducibility metadata rather than paper experiments.

## Historical external artifact

The campaign preserves the judged Space
`DineshAI/nBuL6HywFX` at the immutable revision recorded in
`.openresearch/protected/judged_space_f360979_manifest.sha256`. It is kept for
provenance and is not treated as an official paper implementation.
