# Claim 5 environment and command

Fixed command:

```bash
uv run --locked python repro/run_campaign.py
```

Claim 5 itself is a deterministic source-structure audit with one active CPU
thread. It is rerun inside the cumulative Hugging Face `cpu-upgrade` job
because the inherited command also includes the uncertain-runtime Lean proof.
