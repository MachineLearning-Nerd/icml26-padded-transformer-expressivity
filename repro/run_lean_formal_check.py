#!/usr/bin/env python3
"""Run the pinned Lean kernel proof and emit a portable certificate."""

from __future__ import annotations

import hashlib
import json
import platform
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "formal" / "PaddedTransformer.lean"
TOOLCHAIN = ROOT / "formal" / "lean-toolchain"
OUTPUT = ROOT / "outputs" / "lean_formal_certificate.json"
FORBIDDEN = re.compile(r"\b(?:sorry|admit|axiom|unsafe)\b")


def strip_lean_comments(source: str) -> str:
    """Remove line and nested block comments before token-policy checks."""
    result: list[str] = []
    i = 0
    depth = 0
    while i < len(source):
        if source.startswith("/-", i):
            depth += 1
            i += 2
        elif depth and source.startswith("-/", i):
            depth -= 1
            i += 2
        elif not depth and source.startswith("--", i):
            newline = source.find("\n", i)
            if newline < 0:
                break
            result.append("\n")
            i = newline + 1
        else:
            if not depth:
                result.append(source[i])
            i += 1
    if depth:
        raise RuntimeError("unterminated Lean block comment")
    return "".join(result)


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    code = strip_lean_comments(source_bytes.decode("utf-8"))
    forbidden = sorted(set(FORBIDDEN.findall(code)))
    if forbidden:
        raise SystemExit(f"forbidden proof escape token(s): {forbidden}")

    toolchain = TOOLCHAIN.read_text(encoding="utf-8").strip()
    elan = shutil.which("elan")
    lean = shutil.which("lean")
    repository_lean = (
        ROOT / ".orx-toolchain" / "lean-4.32.0-linux" / "bin" / "lean"
    )
    if elan:
        lean_command = [elan, "run", toolchain, "lean"]
    elif repository_lean.exists():
        lean_command = [str(repository_lean)]
    elif lean:
        lean_command = [lean]
    else:
        raise SystemExit(
            "Lean/elan not found. Install the pinned toolchain from "
            "formal/lean-toolchain."
        )
    version = subprocess.run(
        [*lean_command, "--version"], check=True, capture_output=True, text=True
    ).stdout.strip()
    expected = toolchain.rsplit("v", 1)[-1]
    if f"version {expected}" not in version:
        raise SystemExit(f"expected Lean {expected}, got: {version}")

    completed = subprocess.run(
        [*lean_command, str(SOURCE.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    transcript = completed.stdout + completed.stderr
    if completed.returncode:
        raise SystemExit(transcript)
    if "sorryAx" in transcript:
        raise SystemExit("Lean reported a sorryAx dependency")
    axiom_reports = [
        line
        for line in transcript.splitlines()
        if "depends on axioms" in line or "does not depend on any axioms" in line
    ]
    if len(axiom_reports) != 11:
        raise SystemExit(f"expected 11 axiom reports, got {len(axiom_reports)}")

    if platform.system() == "Linux" and platform.machine() in ("x86_64", "amd64"):
        archive_name = "lean-4.32.0-linux.zip"
        archive_sha256 = (
            "5320dc308f108775904d865b05df386e6bc7dee254e030a90177e8fcc36f0fbe"
        )
    else:
        archive_name = "lean-4.32.0-darwin_aarch64.tar.zst"
        archive_sha256 = (
            "4faa4757f7ca5e7d9588a9de779550fa58bdf01498edb966f15029e2ea117e4e"
        )

    certificate = {
        "verdict": "lean_kernel_verified",
        "lean_version": version,
        "toolchain": toolchain,
        "official_release_archive": (
            "https://github.com/leanprover/lean4/releases/download/"
            f"v4.32.0/{archive_name}"
        ),
        "release_archive_sha256": archive_sha256,
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "forbidden_escape_tokens": forbidden,
        "sorry_ax_dependency": False,
        "kernel_checked_theorems": 11,
        "axiom_reports": axiom_reports,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")

    print(version)
    print("Lean source SHA-256:", certificate["source_sha256"])
    print("Forbidden escape tokens:", forbidden)
    print("sorryAx dependency: false")
    print("Kernel-checked theorem reports:", len(axiom_reports))
    for line in axiom_reports:
        print(" ", line)
    print("wrote outputs/lean_formal_certificate.json")


if __name__ == "__main__":
    main()
