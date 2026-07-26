#!/usr/bin/env python3
"""Independent fail-closed checker for the Claim 4 formal kernel.

This checker deliberately imports no reproduction implementation.  Its exact
integer checks independently reconstruct the resource inequalities used by
``formal/Claim4Exact.lean``.  Decimal arithmetic then exercises the fixed-point
rounding consequence, including ties.  A loose-temperature control must
disagree with average-hard attention or this program exits nonzero.

The finite cases are a cross-check, not evidence for the universal quantifier;
the universal certificate is the Lean kernel check.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import subprocess
import time
from decimal import Decimal, ROUND_HALF_UP, localcontext
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "claim4_independent_checker.json"
SOURCE = ROOT / "formal" / "Claim4Exact.lean"
SEED = 260530523
THREAD_CAP = 1


def decimal_fraction(value: Fraction) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def round_grid(value: Decimal, bits: int) -> Decimal:
    """Round to F_b, using the paper's away-from-zero tie convention."""

    step = Decimal(2) ** (-bits)
    maximum = Decimal(2) ** bits - step
    magnitude = abs(value)
    units = (magnitude / step).to_integral_value(rounding=ROUND_HALF_UP)
    rounded = units * step
    if rounded > maximum:
        rounded = maximum
    return rounded.copy_negate() if value < 0 else rounded


def hard_attention(scores: list[Fraction], values: list[Fraction], bits: int) -> Decimal:
    maximum = max(scores)
    selected = [value for score, value in zip(scores, values) if score == maximum]
    average = sum(selected, Fraction()) / len(selected)
    return round_grid(decimal_fraction(average), bits)


def soft_attention(
    scores: list[Fraction],
    values: list[Fraction],
    bits: int,
    inverse_temperature: int,
) -> tuple[Decimal, list[Decimal]]:
    mixed_bits = 4 * bits
    maximum = max(scores)
    mixed_step = Decimal(2) ** (-mixed_bits)
    with localcontext() as context:
        context.prec = 180
        weights: list[Decimal] = []
        for score in scores:
            argument = decimal_fraction(score - maximum) * inverse_temperature
            ideal_weight = argument.exp()
            weights.append(round_grid(ideal_weight, mixed_bits))
        denominator = sum(weights, Decimal())
        if denominator == 0:
            raise AssertionError("softmax denominator unexpectedly rounded to zero")
        numerator = sum(
            (weight * decimal_fraction(value) for weight, value in zip(weights, values)),
            Decimal(),
        )
        return round_grid(numerator / denominator, bits), weights


def resource_checks() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for bits in range(2, 65):
        mixed_bits = 4 * bits
        inverse_temperature = 1 << (3 * bits)
        scaled_source_grid_gap = inverse_temperature >> bits
        row = {
            "bits": bits,
            "mixed_bits": mixed_bits,
            "inverse_temperature": str(inverse_temperature),
            "temperature_is_mixed_grid_value": True,
            "scaled_source_grid_gap": str(scaled_source_grid_gap),
            "required_exponent_bound": mixed_bits + 1,
            "bound_holds": scaled_source_grid_gap >= mixed_bits + 1,
        }
        if not row["bound_holds"]:
            raise AssertionError(f"resource inequality failed: {row}")
        rows.append(row)
    return rows


def positive_checks() -> tuple[int, Decimal]:
    generator = random.Random(SEED)
    cases = 0
    smallest_underflow_margin = Decimal("Infinity")
    for bits in range(2, 11):
        step = Fraction(1, 1 << bits)
        mixed_half_step = Decimal(2) ** (-(4 * bits + 1))
        inverse_temperature = 1 << (3 * bits)
        for length in (2, 3, 5, 9, 17):
            for maximum_count in range(1, min(length, 4) + 1):
                scores = [Fraction(0)] * maximum_count
                scores.extend(
                    -step * generator.randint(1, 7)
                    for _ in range(length - maximum_count)
                )
                generator.shuffle(scores)
                values = [
                    step * generator.randint(-(1 << bits) + 1, (1 << bits) - 1)
                    for _ in range(length)
                ]
                observed, weights = soft_attention(
                    scores, values, bits, inverse_temperature
                )
                expected = hard_attention(scores, values, bits)
                if observed != expected:
                    raise AssertionError(
                        f"positive case differs at b={bits}, n={length}: "
                        f"{observed} != {expected}"
                    )
                maximum = max(scores)
                for score, weight in zip(scores, weights):
                    if score == maximum and weight != 1:
                        raise AssertionError("maximal exponential did not round to one")
                    if score < maximum:
                        if weight != 0:
                            raise AssertionError("nonmaximal exponential did not underflow")
                        with localcontext() as context:
                            context.prec = 180
                            ideal = (
                                decimal_fraction(score - maximum)
                                * inverse_temperature
                            ).exp()
                        smallest_underflow_margin = min(
                            smallest_underflow_margin, mixed_half_step - ideal
                        )
                cases += 1
    if smallest_underflow_margin <= 0:
        raise AssertionError("strict half-grid underflow margin was not positive")
    return cases, smallest_underflow_margin


def negative_control() -> dict[str, object]:
    bits = 8
    scores = [Fraction(0), Fraction(-1, 1 << bits)]
    values = [Fraction(1), Fraction(0)]
    expected = hard_attention(scores, values, bits)
    loose, weights = soft_attention(scores, values, bits, inverse_temperature=1)
    difference = abs(expected - loose)
    if difference == 0:
        raise AssertionError(
            "negative control unexpectedly matched; loose temperature was not detected"
        )
    return {
        "purpose": "temperature=1 must fail to isolate the focusing mechanism",
        "expected_hard_output": str(expected),
        "loose_temperature_output": str(loose),
        "absolute_difference": str(difference),
        "rounded_weights": [str(weight) for weight in weights],
        "verdict": "EXPECTED_FAIL",
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    started = time.monotonic()
    resources = resource_checks()
    positive_cases, minimum_margin = positive_checks()
    control = negative_control()
    git_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    report = {
        "verdict": "PASS",
        "paper": "2605.30523",
        "claim": 4,
        "role": "independent cross-check; finite cases are not the universal proof",
        "implementation_independence": {
            "imports_reproduction_modules": False,
            "formal_source_sha256": sha256(SOURCE),
        },
        "determinism": {"seed": SEED, "random_module": "Python stdlib MT19937"},
        "resource_certificate": {
            "domain": "all integer b in [2,64], supplemental to symbolic Lean proof",
            "row_count": len(resources),
            "first_row": resources[0],
            "last_row": resources[-1],
            "all_bounds_hold": all(row["bound_holds"] for row in resources),
        },
        "fixed_point_cross_check": {
            "precision_bits": "2..10",
            "cases": positive_cases,
            "tie_patterns": "1..4 maxima where permitted",
            "lengths": [2, 3, 5, 9, 17],
            "minimum_decimal_underflow_margin": str(minimum_margin),
            "verdict": "PASS",
        },
        "negative_control": control,
        "runtime": {
            "git_sha": git_sha,
            "python": platform.python_version(),
            "logical_cpus_visible": os.cpu_count(),
            "thread_cap": THREAD_CAP,
            "runtime_seconds": round(time.monotonic() - started, 6),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("CLAIM4_INDEPENDENT_CHECKER")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
