import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Padded-transformer expressivity: what the evidence actually proves

    **Headline:** Claim 5 is verified. Claims 1–4 remain blocked at their
    complete quantified statements. Claim 4 now has a Lean-verified
    universal *focusing kernel*, which is stronger than finite examples
    but narrower than the paper's family-wide simulation lemma.

    This notebook embeds the released evidence. You do not need to rerun
    Lean or any remote experiment to see the result.
    """)
    return


@app.cell
def _():
    claims = [
        {"claim": 1, "topic": "constant-depth AC0/TC0", "status": "BLOCKED", "confidence": "LOW"},
        {"claim": 2, "topic": "sufficient volume", "status": "BLOCKED", "confidence": "LOW"},
        {"claim": 3, "topic": "looped AC^d/TC^d", "status": "BLOCKED", "confidence": "LOW"},
        {"claim": 4, "topic": "AHAT to SMAT", "status": "BLOCKED", "confidence": "MEDIUM"},
        {"claim": 5, "topic": "theory-only scope", "status": "VERIFIED", "confidence": "HIGH"},
    ]
    return (claims,)


@app.cell
def _(claims, mo):
    rows = "\n".join(
        f"| {row['claim']} | {row['topic']} | {row['status']} | {row['confidence']} |"
        for row in claims
    )
    mo.md(
        f"""
        ## Exact verdicts

        | Claim | Topic | Status | Confidence |
        | ---: | --- | --- | --- |
        {rows}

        `BLOCKED` is deliberate: finite evidence and an incomplete formal
        model cannot verify a universally quantified complexity theorem.
        """
    )
    return


@app.cell
def _(mo):
    bits = mo.ui.slider(2, 16, value=4, label="source precision b")
    bits
    return (bits,)


@app.cell
def _(bits, mo):
    b = bits.value
    mixed = 4 * b
    scaled_gap = 2 ** (2 * b)
    threshold = mixed + 1
    mo.md(
        f"""
        ## Explore the certified Claim 4 inequality

        For `b={b}`, the construction uses mixed precision `4b={mixed}`.
        The scaled minimum score gap is `2^(2b)={scaled_gap}`, while the
        analytic proof needs at least `4b+1={threshold}`.

        **Margin:** `{scaled_gap - threshold}`. The Lean theorem proves this
        is nonnegative for every integer `b>=2`; the slider is explanatory,
        not the proof.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Independent check and control

    The independent stdlib checker imported no reproduction modules:

    - 63 exact resource rows (`b=2..64`) passed.
    - 153 deterministic fixed-point attention cases passed.
    - seed: `260530523`.
    - smallest measured strict underflow margin:
      `4.547473508864641189575195312e-13`.
    - negative control: hard output `1.0`, loose-temperature output `0.5`.

    If the loose-temperature control had matched, the checker would have
    exited nonzero.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why the full lemma is still blocked

    The formal kernel does not encode the complete family-dependent
    mixed-precision range, saturation and iterative rounding through every
    attention operation, or the logspace machine that constructs the SMAT
    family. Those are part of Lemma 3.1's quantifiers.

    The released command is:

    ```bash
    uv run --locked python repro/run_campaign.py
    ```

    Expensive or uncertain work was run on Hugging Face `cpu-upgrade`; no
    GPU was used.
    """)
    return


if __name__ == "__main__":
    app.run()
