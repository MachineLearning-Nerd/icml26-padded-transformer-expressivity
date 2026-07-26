#!/usr/bin/env python3
"""Fail-closed audit of the four-route ledgers for Claims 1--3.

This checker does not turn a literature audit into a theorem proof.  It enforces
that every low-confidence claim records three materially different
verification routes plus an assumption-satisfying falsification route, and
that unresolved proof obligations force the exact verdict BLOCKED.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLAIMS = (1, 2, 3)
REQUIRED_ROUTE_TYPES = {
    "source_derivation",
    "machine_or_combinatorial_check",
    "independent_primary_source",
    "falsification",
}
OUTPUT = ROOT / "outputs" / "claims123_route_audit.json"


def ledger_path(claim: int) -> Path:
    return ROOT / ".openresearch" / "artifacts" / f"claim{claim}" / "routes.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    claim = ledger.get("claim")
    if claim not in CLAIMS:
        raise ValueError("unexpected claim number")
    if ledger.get("confidence") != "LOW":
        raise ValueError(f"Claim {claim}: route sequence is required only for LOW")
    if ledger.get("final_verdict") != "BLOCKED":
        raise ValueError(f"Claim {claim}: unresolved routes must remain BLOCKED")
    routes = ledger.get("routes")
    if not isinstance(routes, list) or len(routes) != 4:
        raise ValueError(f"Claim {claim}: expected exactly four routes")
    observed_types = {route.get("route_type") for route in routes}
    if observed_types != REQUIRED_ROUTE_TYPES:
        raise ValueError(
            f"Claim {claim}: route types {observed_types} != {REQUIRED_ROUTE_TYPES}"
        )
    for position, route in enumerate(routes, start=1):
        if route.get("route") != position:
            raise ValueError(f"Claim {claim}: route numbering is not 1..4")
        for field in (
            "interpretation",
            "method",
            "source_basis",
            "command",
            "result",
            "why_unresolved",
            "negative_control",
        ):
            if not route.get(field):
                raise ValueError(f"Claim {claim} route {position}: missing {field}")
    falsification = routes[-1]
    if falsification.get("route_type") != "falsification":
        raise ValueError(f"Claim {claim}: fourth route must be falsification")
    if falsification.get("counterexample_status") != "NO_VALID_COUNTEREXAMPLE":
        raise ValueError(
            f"Claim {claim}: BLOCKED requires an unsuccessful valid-counterexample search"
        )
    if not falsification.get("exact_assumptions_retested"):
        raise ValueError(f"Claim {claim}: falsification did not retest assumptions")
    unresolved = ledger.get("unresolved_obligations")
    if not isinstance(unresolved, list) or not unresolved:
        raise ValueError(f"Claim {claim}: BLOCKED requires concrete obligations")
    return {
        "claim": claim,
        "route_count": len(routes),
        "distinct_route_types": sorted(observed_types),
        "falsification_route_present": True,
        "unresolved_obligation_count": len(unresolved),
        "verdict": "BLOCKED",
    }


def proxy_capacity_counterexample() -> dict[str, Any]:
    """Reject the old D*b>=ceil(log2 N) proxy under the paper's actual F_b."""

    n = 8
    bits = 1
    width = 2
    # F_b = {± a 2^-b | a=0..2^(2b)-1}; zero is duplicated.
    fixed_point_cardinality = 2 * ((1 << (2 * bits)) - 1) + 1
    capacity = fixed_point_cardinality**width
    proxy_volume = bits * width
    proxy_required = 3
    if not (proxy_volume < proxy_required and capacity >= n):
        raise AssertionError("expected proxy counterexample was not reconstructed")
    return {
        "purpose": "negative control: reject the historical binary-cell capacity proxy",
        "N": n,
        "b": bits,
        "D": width,
        "paper_F_b_cardinality": fixed_point_cardinality,
        "available_D_tuple_count": capacity,
        "historical_proxy_volume": proxy_volume,
        "historical_proxy_required_ceil_log2_N": proxy_required,
        "result": "PROXY_REJECTED",
        "scope": "does not falsify Definition 2.3 or Theorem 4.2",
    }


def mutation_controls(ledgers: list[dict[str, Any]]) -> dict[str, bool]:
    controls: dict[str, bool] = {}

    missing_route = copy.deepcopy(ledgers[0])
    missing_route["routes"].pop()
    try:
        validate_ledger(missing_route)
    except ValueError:
        controls["missing_falsification_route_rejected"] = True
    else:
        raise AssertionError("missing falsification route was accepted")

    false_promotion = copy.deepcopy(ledgers[1])
    false_promotion["final_verdict"] = "VERIFIED"
    try:
        validate_ledger(false_promotion)
    except ValueError:
        controls["unsupported_verified_promotion_rejected"] = True
    else:
        raise AssertionError("unsupported VERIFIED promotion was accepted")

    missing_assumptions = copy.deepcopy(ledgers[2])
    missing_assumptions["routes"][-1]["exact_assumptions_retested"] = False
    try:
        validate_ledger(missing_assumptions)
    except ValueError:
        controls["assumption_free_counterexample_rejected"] = True
    else:
        raise AssertionError("assumption-free counterexample was accepted")
    return controls


def main() -> None:
    started = time.monotonic()
    ledgers = [
        json.loads(ledger_path(claim).read_text(encoding="utf-8"))
        for claim in CLAIMS
    ]
    results = [validate_ledger(ledger) for ledger in ledgers]
    controls = mutation_controls(ledgers)
    git_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    report = {
        "paper": "2605.30523",
        "verdict": "PASS",
        "interpretation": (
            "PASS means the honest BLOCKED route records are complete and "
            "fail closed; it does not mean Claims 1-3 are verified."
        ),
        "claims": results,
        "ledger_sha256": {
            str(claim): sha256(ledger_path(claim)) for claim in CLAIMS
        },
        "scientific_negative_control": proxy_capacity_counterexample(),
        "validator_negative_controls": controls,
        "runtime": {
            "git_sha": git_sha,
            "python": platform.python_version(),
            "logical_cpus_visible": os.cpu_count(),
            "thread_cap": 1,
            "runtime_seconds": round(time.monotonic() - started, 6),
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("CLAIMS123_ROUTE_AUDIT")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
