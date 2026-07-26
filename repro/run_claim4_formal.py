#!/usr/bin/env python3
"""Bootstrap pinned Lean/Mathlib and kernel-check the universal Claim 4 core."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "formal" / "Claim4Exact.lean"
OUTPUT = ROOT / "outputs" / "claim4_formal_certificate.json"
TOOLCHAIN = "leanprover/lean4:v4.32.0"
MATHLIB_REV = "81a5d257c8e410db227a6665ed08f64fea08e997"
LINUX_ZIP_URL = (
    "https://github.com/leanprover/lean4/releases/download/"
    "v4.32.0/lean-4.32.0-linux.zip"
)
LINUX_ZIP_SHA256 = (
    "5320dc308f108775904d865b05df386e6bc7dee254e030a90177e8fcc36f0fbe"
)
LEANTAR_URL = (
    "https://github.com/digama0/leangz/releases/download/v0.1.20/"
    "leantar-v0.1.20-x86_64-unknown-linux-musl.tar.gz"
)
LEANTAR_SHA256 = (
    "1789878731efbd6eb56515dbe511f7836547defde237cf5e4b29e78eaedaeb86"
)
FORBIDDEN = ("sorry", "admit", "axiom", "unsafe")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    print("RUN", json.dumps(command), flush=True)
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="")
    if completed.returncode:
        raise SystemExit(completed.returncode)
    return completed


def ensure_lake(env: dict[str, str]) -> Path:
    elan = shutil.which("elan")
    if elan:
        run([elan, "toolchain", "install", TOOLCHAIN], env=env)
        lake = subprocess.run(
            [elan, "which", "--toolchain", TOOLCHAIN, "lake"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return Path(lake)

    if platform.system() != "Linux" or platform.machine() not in ("x86_64", "amd64"):
        existing = shutil.which("lake")
        if existing:
            return Path(existing)
        raise SystemExit("the pinned bootstrap currently supports Linux x86_64 or elan")

    cache_root = ROOT / ".orx-toolchain"
    lake = cache_root / "lean-4.32.0-linux" / "bin" / "lake"
    leantar = cache_root / "lean-4.32.0-linux" / "bin" / "leantar"
    cache_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="claim4-lean-") as temporary:
        temporary_root = Path(temporary)
        if not lake.exists():
            archive = temporary_root / "lean.zip"
            request = urllib.request.Request(
                LINUX_ZIP_URL,
                headers={"User-Agent": "OpenResearch-Reproduction/1.0"},
            )
            print("Downloading pinned Lean release archive", flush=True)
            with urllib.request.urlopen(request, timeout=120) as response:
                with archive.open("wb") as output:
                    shutil.copyfileobj(response, output)
            observed = sha256(archive)
            if observed != LINUX_ZIP_SHA256:
                raise SystemExit(
                    f"Lean archive SHA-256 mismatch: {observed} != {LINUX_ZIP_SHA256}"
                )
            print("Lean archive SHA-256 verified:", observed, flush=True)
            with zipfile.ZipFile(archive) as bundle:
                bundle.extractall(cache_root)
            for executable in (
                cache_root / "lean-4.32.0-linux" / "bin"
            ).iterdir():
                if executable.is_file():
                    executable.chmod(executable.stat().st_mode | 0o111)

        if not leantar.exists():
            archive = temporary_root / "leantar.tar.gz"
            request = urllib.request.Request(
                LEANTAR_URL,
                headers={"User-Agent": "OpenResearch-Reproduction/1.0"},
            )
            print("Downloading pinned leantar release archive", flush=True)
            with urllib.request.urlopen(request, timeout=120) as response:
                with archive.open("wb") as output:
                    shutil.copyfileobj(response, output)
            observed = sha256(archive)
            if observed != LEANTAR_SHA256:
                raise SystemExit(
                    f"leantar archive SHA-256 mismatch: {observed} != {LEANTAR_SHA256}"
                )
            print("leantar archive SHA-256 verified:", observed, flush=True)
            with tarfile.open(archive, "r:gz") as bundle:
                member = bundle.getmember(
                    "leantar-v0.1.20-x86_64-unknown-linux-musl/leantar"
                )
                extracted = bundle.extractfile(member)
                if extracted is None:
                    raise SystemExit("leantar archive member is not a regular file")
                leantar.write_bytes(extracted.read())
            leantar.chmod(0o755)
    if not lake.exists():
        raise SystemExit(f"expected lake at {lake}")
    return lake


def main() -> None:
    started = time.monotonic()
    source_text = SOURCE.read_text(encoding="utf-8")
    code_only = "\n".join(
        line.split("--", 1)[0] for line in source_text.splitlines()
        if not line.lstrip().startswith("/-")
    )
    found = [token for token in FORBIDDEN if token in code_only.split()]
    if found:
        raise SystemExit(f"forbidden proof escape token(s): {found}")

    env = os.environ.copy()
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        env[name] = "1"

    lake = ensure_lake(env)
    version = run([str(lake), "--version"], env=env).stdout.strip()
    if "4.32.0" not in version:
        raise SystemExit(f"expected Lake/Lean 4.32.0, got {version}")

    run([str(lake), "update"], env=env)
    manifest = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
    packages = {package["name"]: package["rev"] for package in manifest["packages"]}
    if packages.get("mathlib") != MATHLIB_REV:
        raise SystemExit(
            f"expected Mathlib {MATHLIB_REV}, got {packages.get('mathlib')}"
        )
    print("RESOLVED_LAKE_PACKAGES", json.dumps(packages, sort_keys=True))

    run([str(lake), "exe", "cache", "get"], env=env)
    checked = run(
        [str(lake), "env", "lean", str(SOURCE.relative_to(ROOT))],
        env=env,
    )
    transcript = checked.stdout + checked.stderr
    if "sorryAx" in transcript:
        raise SystemExit("Lean reported a sorryAx dependency")
    reports = [
        line for line in transcript.splitlines()
        if "depends on axioms" in line or "does not depend on any axioms" in line
    ]
    if len(reports) != 4:
        raise SystemExit(f"expected four axiom reports, got {len(reports)}")

    certificate = {
        "verdict": "lean_kernel_verified",
        "paper": "2605.30523",
        "claim": 4,
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "toolchain": TOOLCHAIN,
        "mathlib_revision": MATHLIB_REV,
        "resolved_lake_packages": packages,
        "lean_archive_url": LINUX_ZIP_URL,
        "lean_archive_sha256": LINUX_ZIP_SHA256,
        "leantar_archive_url": LEANTAR_URL,
        "leantar_archive_sha256": LEANTAR_SHA256,
        "logical_cpus_visible": os.cpu_count(),
        "thread_cap": 1,
        "kernel_checked_theorems": len(reports),
        "sorry_ax_dependency": False,
        "axiom_reports": reports,
        "runtime_seconds": round(time.monotonic() - started, 6),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    print("CLAIM4_FORMAL_CERTIFICATE")
    print(json.dumps(certificate, indent=2))


if __name__ == "__main__":
    main()
