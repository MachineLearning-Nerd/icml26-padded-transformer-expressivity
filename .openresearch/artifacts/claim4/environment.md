# Claim 4 environment and command

Fixed command inherited by every experiment node:

```bash
uv run --locked python repro/run_campaign.py
```

- Python: pinned to `3.12.*` by `.python-version` and `pyproject.toml`
- Python dependency resolution: `uv.lock`
- Lean: `leanprover/lean4:v4.32.0`
- Mathlib: `81a5d257c8e410db227a6665ed08f64fea08e997`
- Lean Linux archive SHA-256:
  `5320dc308f108775904d865b05df386e6bc7dee254e030a90177e8fcc36f0fbe`
- leantar v0.1.20 archive SHA-256:
  `1789878731efbd6eb56515dbe511f7836547defde237cf5e4b29e78eaedaeb86`
- Numeric/proof thread cap: 1
- Selected compute: Hugging Face `cpu-upgrade`
- Selection reason: pinned Mathlib bootstrap and cache retrieval have uncertain
  runtime, so the task is ineligible for local execution under the campaign
  compute contract.

Actual allocation and runtime are recorded by the command itself and copied
from the terminal run log into the raw certificate.
