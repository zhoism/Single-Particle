#!/usr/bin/env python3
"""__SKILL_NAME__ wrapper.

One exec call per skill turn. The chain runs internally; OpenClaw sees a single
subprocess invocation that returns a JSON envelope.

Design constraints (do not violate):
  - Single exec entrypoint per turn (Stage 1c latency finding).
  - --dry-run support is mandatory (Tier 2 recovery hook).
  - JSON envelope to stdout; human-readable progress to stderr.
  - No hallucination-safe steps: every command is deterministic.
  - Binaries resolved from PATH (or AMBERHOME) — never hardcoded to the advisor's machine.

Usage:
    wrapper.py --input <path-or-smiles> [--name LIG] [--charge 0] [--output-dir ./] [--dry-run]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


# ---- Constants -----------------------------------------------------------

SKILL_NAME = "__SKILL_NAME__"
REQUIRED_BINS = ["__BIN1__", "__BIN2__"]  # filled in by scaffold step
REQUIRED_ENV = ["AMBERHOME"]  # remove if not applicable


# ---- Envelope ------------------------------------------------------------

def envelope(ok: bool, dry_run: bool, outputs: dict[str, Any] | None = None,
             validation: dict[str, Any] | None = None,
             errors: list[str] | None = None) -> str:
    """Canonical JSON envelope for stdout."""
    return json.dumps({
        "ok": ok,
        "skill": SKILL_NAME,
        "dry_run": dry_run,
        "outputs": outputs or {},
        "validation": validation or {},
        "errors": errors or [],
    }, indent=2)


def die(msg: str, dry_run: bool = False, code: int = 1) -> None:
    print(envelope(ok=False, dry_run=dry_run, errors=[msg]))
    sys.exit(code)


# ---- Preflight -----------------------------------------------------------

def preflight() -> list[str]:
    """Resolve binaries + env. Returns list of error strings; empty = OK."""
    errors: list[str] = []
    for b in REQUIRED_BINS:
        if shutil.which(b) is None:
            errors.append(f"MISSING_BINARY: {b} not on PATH")
    for e in REQUIRED_ENV:
        if not os.environ.get(e):
            errors.append(f"MISSING_ENV: {e} not set")
    return errors


# ---- Steps ---------------------------------------------------------------

def step_1(args: argparse.Namespace, run_dir: Path, dry_run: bool) -> dict[str, Any]:
    """__STEP_1_DESCRIPTION__. Returns a dict of artifacts + diagnostics."""
    cmd = ["__BIN1__", "--example-flag", str(args.input)]
    return run_step("step_1", cmd, run_dir, dry_run)


def step_2(args: argparse.Namespace, run_dir: Path, dry_run: bool, step_1_outputs: dict) -> dict[str, Any]:
    """__STEP_2_DESCRIPTION__. Consumes step_1's output."""
    cmd = ["__BIN2__", "-i", str(step_1_outputs["path"])]
    return run_step("step_2", cmd, run_dir, dry_run)


# ---- Run helper ----------------------------------------------------------

def run_step(name: str, cmd: list[str], run_dir: Path, dry_run: bool) -> dict[str, Any]:
    """Execute or plan a step. Stream stdout/stderr to per-step files."""
    print(f"[{name}] {' '.join(cmd)}", file=sys.stderr)
    if dry_run:
        return {"planned": True, "cmd": cmd, "name": name}

    stdout_path = run_dir / f"{name}.out"
    stderr_path = run_dir / f"{name}.err"
    with stdout_path.open("w") as so, stderr_path.open("w") as se:
        result = subprocess.run(cmd, stdout=so, stderr=se, cwd=run_dir)
    if result.returncode != 0:
        raise RuntimeError(
            f"{name} failed (rc={result.returncode}); see {stderr_path}"
        )
    return {"name": name, "stdout": str(stdout_path), "stderr": str(stderr_path)}


# ---- Validation ----------------------------------------------------------

def validate(args: argparse.Namespace, run_dir: Path) -> dict[str, Any]:
    """Run the validation gates declared in SKILL.md metadata."""
    # Implement skill-specific gates here. Return dict; empty errors list = pass.
    return {"errors": []}


# ---- Main ----------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(prog=SKILL_NAME, description="__GOAL__")
    p.add_argument("--input", required=True, help="__INPUT_DESCRIPTION__")
    p.add_argument("--name", default="LIG", help="Residue name (1–4 chars).")
    p.add_argument("--charge", type=int, default=0, help="Net formal charge.")
    p.add_argument("--output-dir", default="./", help="Where to write artifacts.")
    p.add_argument("--dry-run", action="store_true", help="Plan without executing.")
    args = p.parse_args()

    # Preflight
    pre_errors = preflight()
    if pre_errors and not args.dry_run:
        die("; ".join(pre_errors))

    # Run dir
    run_dir = Path(args.output_dir).resolve() / f"{SKILL_NAME}-run"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Chain
    try:
        s1 = step_1(args, run_dir, args.dry_run)
        s2 = step_2(args, run_dir, args.dry_run, s1)
    except RuntimeError as exc:
        die(str(exc), dry_run=args.dry_run, code=2)

    # Validation (skipped in dry-run)
    if args.dry_run:
        outputs = {"planned_steps": [s1, s2]}
        validation: dict[str, Any] = {}
        errors: list[str] = []
    else:
        v = validate(args, run_dir)
        validation = v
        errors = v.get("errors", [])
        outputs = {
            # Fill in skill-specific output paths
            # "mol2": str(run_dir / f"{args.name}.mol2"),
            # "frcmod": str(run_dir / f"{args.name}.frcmod"),
        }

    print(envelope(ok=not errors, dry_run=args.dry_run,
                   outputs=outputs, validation=validation, errors=errors))
    sys.exit(0 if not errors else 3)


if __name__ == "__main__":
    main()
