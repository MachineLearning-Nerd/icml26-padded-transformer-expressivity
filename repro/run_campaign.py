#!/usr/bin/env python3
"""Run the cumulative, fail-closed reproduction suite.

This file is the stable experiment entrypoint. Experiment children may add
verifiers to the suite, but every node inherits the same command:

    uv run --locked python repro/run_campaign.py
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THREAD_CAP_VARIABLES = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)
COMMANDS = (
    ("claim4_universal_formal", (sys.executable, "repro/run_claim4_formal.py")),
    (
        "claim4_independent_checker",
        (sys.executable, "repro/run_claim4_independent.py"),
    ),
    (
        "claims123_route_audit",
        (sys.executable, "repro/run_claim_routes.py"),
    ),
    ("finite_claim_regressions", (sys.executable, "repro/run_audit.py")),
    ("theorem42_graph_regression", (sys.executable, "repro/run_theorem42.py")),
    (
        "theorem42_obligation_regression",
        (sys.executable, "repro/run_theorem42_obligations.py"),
    ),
    ("lean_kernel_regression", (sys.executable, "repro/run_lean_formal_check.py")),
    ("pytest_regression", (sys.executable, "-m", "pytest", "-q")),
)


def main() -> None:
    environment = os.environ.copy()
    for name in THREAD_CAP_VARIABLES:
        environment[name] = "1"

    started = time.monotonic()
    telemetry: dict[str, object] = {
        "paper": "2605.30523",
        "git_sha": subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "required_core_estimate": "2-8 visible cores; proof process capped at 1",
        "selected_backend": "hf",
        "selected_flavor": "cpu-upgrade",
        "selection_reason": "Mathlib bootstrap/cache retrieval has uncertain runtime",
        "logical_cpus_visible": os.cpu_count(),
        "thread_cap": 1,
        "commands": [],
    }

    print("CAMPAIGN_RUN_START")
    print(json.dumps({key: value for key, value in telemetry.items() if key != "commands"}))

    for label, command in COMMANDS:
        command_started = time.monotonic()
        print(f"\n=== {label} ===", flush=True)
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            text=True,
        )
        duration = time.monotonic() - command_started
        record = {
            "label": label,
            "command": list(command),
            "exit_code": completed.returncode,
            "runtime_seconds": round(duration, 6),
        }
        telemetry["commands"].append(record)
        print("COMMAND_RESULT", json.dumps(record), flush=True)
        if completed.returncode:
            raise SystemExit(completed.returncode)

    telemetry["runtime_seconds"] = round(time.monotonic() - started, 6)
    telemetry["verdict"] = "PASS"
    print("\nCAMPAIGN_RUN_SUMMARY")
    print(json.dumps(telemetry, indent=2))


if __name__ == "__main__":
    main()
