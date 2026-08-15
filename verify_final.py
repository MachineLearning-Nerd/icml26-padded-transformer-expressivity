#!/usr/bin/env python3
"""Fail-closed verifier for the published padded-transformer audit package."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CANONICAL = "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
EXPECTED_BRANCHES = {
    "origin/main",
    "origin/evidence/frozen-baseline-uv-lock",
    "origin/evidence/claim-4-softmax-focusing",
    "origin/audit/claim-4-independent-checker",
    "origin/audit/claims-1-3-proof-obligations",
    "origin/release/cumulative-audit",
    "origin/release/publication-snapshot",
    "origin/repair/claim-4-inline-checker",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"VERIFY_FINAL_FAIL: {message}")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load(relative: str) -> dict:
    path = ROOT / relative
    require(path.is_file(), f"missing {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    required = {
        "README.md",
        "STATUS.md",
        "CLAIM_EVIDENCE.md",
        "SOURCE_MANIFEST.md",
        "BRANCH_AUDIT.md",
        "CITATION.cff",
        "outputs/summary.json",
        "outputs/audit_stdout.json",
        "outputs/lean_formal_certificate.json",
        "formal/Claim4Exact.lean",
        "formal/lean-toolchain",
        ".openresearch/artifacts/claim1/routes.json",
        ".openresearch/artifacts/claim2/routes.json",
        ".openresearch/artifacts/claim3/routes.json",
        ".openresearch/artifacts/claim4/raw/formal_certificate_run_96a14223.json",
        ".openresearch/artifacts/claim4/raw/claim4_independent_checker.json",
        ".openresearch/artifacts/claim5/claim_contract.json",
        "repro/run_campaign.py",
        "repro/run_lean_formal_check.py",
        "repro/run_claim4_independent.py",
    }
    tracked = set(git("ls-files").splitlines())
    require(required <= tracked, f"required files are not tracked: {sorted(required - tracked)}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text(encoding="utf-8")
    for phrase in (
        "2605.30523v1",
        "Anej Svete",
        "MachineLearning-Nerd",
        "Thank you",
        "CLAIM_EVIDENCE.md",
        "BLOCKED",
        "VERIFIED (scope audit)",
        "evidence/frozen-baseline-uv-lock",
        "repair/claim-4-inline-checker",
    ):
        require(phrase in readme, f"README missing {phrase!r}")
    for phrase in ("C1", "C2", "C3", "C4", "C5", "BLOCKED", "Lean"):
        require(phrase in status, f"STATUS missing {phrase!r}")
    require("no `master` or `orx/*` branch remains" in branch_audit, "branch audit incomplete")

    summary = load("outputs/summary.json")
    require(summary["paper"]["arxiv"] == "2605.30523", "paper pin mismatch")
    require(summary["claim_3_looped_ACd_TCd_equivalence"]["maximum_composed_depth"] >= 1, "loop audit missing")
    require(summary["claim_4_log_precision_SMAT_simulates_AHAT"]["max_post_round_difference"] == 0, "Claim 4 finite mismatch")
    require(summary["claim_5_theory_only_scope"]["empirical_benchmark_or_training_protocol"] is False, "theory-only scope changed")

    routes = [load(f".openresearch/artifacts/claim{claim}/routes.json") for claim in (1, 2, 3)]
    require(all(route["final_verdict"] == "BLOCKED" for route in routes), "Claims 1-3 must remain blocked")
    require(load(".openresearch/artifacts/claim4/claim_contract.json")["final_verdict"] == "BLOCKED", "Claim 4 verdict changed")
    require(load(".openresearch/artifacts/claim5/claim_contract.json")["final_verdict"] == "VERIFIED", "Claim 5 scope verdict changed")

    formal = load(".openresearch/artifacts/claim4/raw/formal_certificate_run_96a14223.json")
    require(formal["verdict"] == "lean_kernel_verified", "Lean certificate not verified")
    require(formal["kernel_checked_theorems"] == 5, "unexpected Lean theorem count")
    require(formal["sorry_ax_dependency"] is False, "sorryAx dependency present")
    independent = load(".openresearch/artifacts/claim4/raw/claim4_independent_checker.json")
    require(independent["resource_certificate"]["row_count"] == 63, "resource certificate changed")
    require(independent["fixed_point_cross_check"]["cases"] == 153, "finite Claim 4 case count changed")
    require(independent["negative_control"]["absolute_difference"] == "0.50000000", "negative control changed")
    universal = load("outputs/lean_formal_certificate.json")
    source_hash = hashlib.sha256((ROOT / "formal/PaddedTransformer.lean").read_bytes()).hexdigest()
    require(universal["verdict"] == "lean_kernel_verified", "universal Lean certificate not verified")
    require(universal["source_sha256"] == source_hash, "universal Lean source hash mismatch")
    require(universal["forbidden_escape_tokens"] == [], "forbidden Lean escape token present")
    require(universal["kernel_checked_theorems"] == 11, "universal Lean theorem count changed")
    require(len(universal["axiom_reports"]) == 11, "universal Lean axiom report count changed")
    require(universal["sorry_ax_dependency"] is False, "universal Lean certificate has sorryAx")

    remotes = set(git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").splitlines())
    require(remotes == EXPECTED_BRANCHES | {"origin/HEAD"}, f"unexpected remote branches: {sorted(remotes)}")
    require(not any(name.startswith("origin/orx/") for name in remotes), "legacy orx branch remains")
    identities = {
        f"{author} <{email}> | {committer} <{commit_email}>"
        for author, email, committer, commit_email in (
            row.split("\x1f")
            for row in git(
                "log",
                "--all",
                "--format=%an\x1f%ae\x1f%cn\x1f%ce",
            ).splitlines()
        )
    }
    require(identities == {f"{CANONICAL} | {CANONICAL}"}, "non-canonical reachable identity remains")
    require(not git("status", "--porcelain"), "worktree is not clean")
    print("PASS: paper scope, claim ledger, Lean certificate, branches, identity, and cleanup invariants")


if __name__ == "__main__":
    main()
