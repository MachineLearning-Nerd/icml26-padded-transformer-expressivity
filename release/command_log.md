# Material command log

No command below contains a token, credential, or generated run wrapper.

## Startup and source audit

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs 9ca20696-2add-457e-9aa9-5c5502029fa3
git status --short
git rev-parse HEAD
git branch -a
df -h .
orx paper 2605.30523 --full
```

The primary PDF and HTML were retrieved with browser User-Agent
`OpenResearch-Reproduction/1.0`, dated 2026-07-26, and hashed with SHA-256.
The live verdict dataset was filtered by exact
`space_id == "DineshAI/nBuL6HywFX"`. The judged Space was downloaded at exact
revision `f360979669367144cd429766b5952338e263d3d9`.

## Fixed experiment command

```text
uv run --locked python repro/run_campaign.py
```

## Experiment-tree operations

```text
orx create-experiment 9ca20696-2add-457e-9aa9-5c5502029fa3 --title "Frozen baseline: judged reproduction plus uv lock" --run-command "uv run --locked python repro/run_campaign.py"
orx exp run 4f65748b-014e-4d1b-b3d8-4a9ff0cd77da --backend local
orx create-experiment 9ca20696-2add-457e-9aa9-5c5502029fa3 --title "Claim 4: exact softmax underflow certificate" --parent 4f65748b-014e-4d1b-b3d8-4a9ff0cd77da
orx exp run c99ffb0c-e2f5-48f2-b806-46f9ee68aa49 --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm --timeout 1h
orx create-experiment 9ca20696-2add-457e-9aa9-5c5502029fa3 --title "Claim 4: independent checker and evaluator package" --parent c99ffb0c-e2f5-48f2-b806-46f9ee68aa49
orx exp run 7acd1d5f-406a-43dd-9b04-9ba1986e775b --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm --timeout 1h
orx create-experiment 9ca20696-2add-457e-9aa9-5c5502029fa3 --title "Claims 1-3: proof-obligation and falsification audit" --parent 7acd1d5f-406a-43dd-9b04-9ba1986e775b
orx exp run 79c0b1f8-a5f8-41eb-bedb-481ce1568929 --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm --timeout 1h
```

Every run was followed by `orx exp wait`, `orx runs`, and `orx logs`; terminal
run evidence was recorded into the corresponding `orx exp desc`.

## Literature scope checks

```text
orx lit "London Kanade 2025 padded transformers expressivity constant width TC0 AC0"
orx lit "Merrill Sabharwal 2025 fully uniform transformers TC depth looped AHAT"
orx lit "Yang 2026 average hard attention softmax temperature Lemma 25"
```

## Validation and release

```text
uv run --locked marimo check notebooks/padded_transformer_reproduction.py
uv run --locked python repro/run_release_audit.py
git diff --check
git ls-remote origin refs/heads/main
```

The final HF upload and post-publication download commands are appended to the
published report after their exact revisions are known.
