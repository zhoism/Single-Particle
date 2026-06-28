#!/usr/bin/env python3
"""Oracle + regression test for the irest/ntx restart-coherence gate.

Background: a restart (irest=1) continues the step counter and therefore needs
inherited velocities, so it is only legal with a velocity-reading ntx (4/5/6/7;
5 is the modern standard). irest=1 with ntx=1 reads coordinates only and AMBER
aborts. The validator (check_amber.py) had ZERO irest/ntx awareness until this
gate. The reverse case (ntx=5, irest=0 — read velocities but restart the clock
fresh) is legal and must NOT fire. Minimization (imin=1) is out of scope.

This test:
  (A) ORACLE     — synthetic minimal &cntrl namelists across the legal/illegal
      matrix, including omitted-key AMBER defaults (imin=0, irest=0, ntx=1). Each
      case carries an explicit human ground-truth bool AND is cross-checked
      against an INDEPENDENT regex parser (NOT the gate's parse path), so the
      test cannot silently "agree with" a buggy gate.
  (B) REGRESSION — over every real curated GREEN production .in in project-prime,
      assert the gate fires on NONE of them; assert the corpus actually contained
      restart stages (irest=1) so "0 fires" is not vacuous; and cross-check the
      engine verdict against the independent oracle on real data.

Stdlib only; runs under py3.9 (system) and py3.11 (conda prime-amber).
Run:  python3 test_restart_coherence.py      (exit 0 = all pass, 1 = a failure)
"""
import importlib.util
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
CHECK_AMBER = HERE.parents[1] / "checks" / "check_amber.py"
RULE = "irest/ntx incoherent"           # the Finding.rule this gate emits


def load_validator():
    spec = importlib.util.spec_from_file_location("check_amber_under_test", CHECK_AMBER)
    mod = importlib.util.module_from_spec(spec)
    # Register before exec: py3.14's dataclasses resolves cls.__module__ via
    # sys.modules, so an unregistered module raises AttributeError on @dataclass.
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)         # safe: main() is __main__-guarded
    return mod


# ---- independent oracle (its OWN parser; never imports the gate's logic) ----
def cntrl_body(text: str) -> str:
    """The &cntrl block body with Fortran '!' comments removed FIRST (so a '/'
    inside a comment cannot truncate the block) and scoped to the namelist (so
    keyword-looking prose in a title line is ignored). Independent of the gate's
    parse_namelists path."""
    scrubbed = re.sub(r"!.*", "", text)
    m = re.search(r"&cntrl\b(.*?)(?:/|&end\b)", scrubbed, re.IGNORECASE | re.DOTALL)
    return m.group(1) if m else ""


def oracle_fire(text: str) -> bool:
    """Re-derive the gate verdict from scratch — independent of the gate's parser
    (a regex scan over the comment-stripped &cntrl block, NOT parse_namelists; if
    test and gate shared a parser a parser bug would hide). AMBER defaults applied
    (imin=0, irest=0, ntx=1).
    """
    body = cntrl_body(text)

    def getint(key: str, default: int) -> int:
        m = re.search(rf"(?i)\b{key}\s*=\s*(-?\d+)", body)
        return int(m.group(1)) if m else default

    return (getint("imin", 0) == 0 and getint("irest", 0) == 1
            and getint("ntx", 1) not in (4, 5, 6, 7))


def gate_fires(rep) -> bool:
    """True iff the engine raised OUR restart-coherence FAIL (ignore other rules)."""
    return any(f.level == "FAIL" and f.rule == RULE for f in rep.findings)


def cntrl(*lines: str) -> str:
    return "&cntrl\n  " + "\n  ".join(lines) + "\n/\n"


def write_in(text: str) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".in", delete=False)
    f.write(text)
    f.close()
    return Path(f.name)


# (name, mdin text, human ground-truth: should the restart gate FAIL?)
CASES = [
    # --- illegal: restart (irest=1) without a velocity-reading ntx -> MUST fire ---
    ("irest=1 ntx=1 (classic illegal)",          cntrl("imin=0,", "irest=1,", "ntx=1,"), True),
    ("irest=1 ntx omitted (default 1)",          cntrl("imin=0,", "irest=1,"),           True),
    ("irest=1 ntx=2",                            cntrl("imin=0,", "irest=1,", "ntx=2,"), True),
    ("irest=1 ntx=3",                            cntrl("imin=0,", "irest=1,", "ntx=3,"), True),
    ("irest=1 ntx=0 (invalid ntx)",              cntrl("imin=0,", "irest=1,", "ntx=0,"), True),
    # --- legal -> must NOT fire ---
    ("irest=0 ntx=1 (fresh heat)",               cntrl("imin=0,", "irest=0,", "ntx=1,"), False),
    ("irest=0 ntx=5 (REVERSE case, legal)",      cntrl("imin=0,", "irest=0,", "ntx=5,"), False),
    ("irest=1 ntx=5 (standard restart)",         cntrl("imin=0,", "irest=1,", "ntx=5,"), False),
    ("irest=1 ntx=4 (legacy velocity-read)",     cntrl("imin=0,", "irest=1,", "ntx=4,"), False),
    ("irest=1 ntx=6 (legacy velocity-read)",     cntrl("imin=0,", "irest=1,", "ntx=6,"), False),
    ("irest=1 ntx=7 (legacy velocity-read)",     cntrl("imin=0,", "irest=1,", "ntx=7,"), False),
    ("imin=1 irest=1 ntx=1 (minimization skip)", cntrl("imin=1,", "irest=1,", "ntx=1,"), False),
    ("irest omitted (default 0) ntx=1",          cntrl("imin=0,", "ntx=1,"),             False),
    ("all defaults (only imin=0 present)",       cntrl("imin=0,"),                       False),
    ("irest=0 ntx omitted",                      cntrl("imin=0,", "irest=0,"),           False),
    # --- parser robustness: a '/' inside a ! comment must NOT truncate the block ---
    # (legal restart whose comment carries 'coords/velocities' — a buggy parser drops
    #  ntx, defaults it to 1, and false-FAILs a legal file)
    ("legal restart, '/' in comment before ntx",
     "&cntrl\n  imin=0,\n  irest=1,  ! restart: reads coords/velocities from rst\n  ntx=5,\n/\n",
     False),
    # (illegal restart whose comment carries 'kcal/mol/A^2' before irest — a buggy
    #  parser drops irest, defaults it to 0, and false-PASSes an illegal file)
    ("illegal restart, '/' in comment before irest",
     "&cntrl\n  imin=0,  ! backbone restraint 2.0 kcal/mol/A^2\n  irest=1,\n  ntx=1,\n/\n",
     True),
    # --- restraintmask with a '!' negation INSIDE quotes, on its own line (a real
    #     restrained-stage shape): the line-local comment-strip eats only that
    #     line's tail, so imin/irest/ntx (separate lines) are still read correctly ---
    ("legal restart w/ restraintmask='!@H=' on own line, ntx=5",
     "&cntrl\n  imin=0,\n  irest=1,\n  ntx=5,\n  ntr=1,\n  restraintmask='!@H=',\n/\n",
     False),
    ("illegal restart w/ restraintmask='!@H=' on own line, ntx=1",
     "&cntrl\n  imin=0,\n  irest=1,\n  ntx=1,\n  ntr=1,\n  restraintmask='!@H=',\n/\n",
     True),
]


def main() -> int:
    mod = load_validator()
    check_amber_in = mod.check_amber_in
    fails = []

    def check(name, cond):
        print(f"  {'PASS' if cond else 'FAIL'}  {name}")
        if not cond:
            fails.append(name)

    print("(A) ORACLE — synthetic minimal &cntrl matrix")
    for name, text, expect in CASES:
        # 1) the independent parser agrees with the human ground-truth literal
        check(f"[indep oracle == ground-truth] {name}", oracle_fire(text) == expect)
        # 2) the engine's restart finding matches the expectation
        rep = check_amber_in(write_in(text))
        check(f"[gate fires == {expect}] {name}", gate_fires(rep) == expect)
        # 3) on these minimal namelists OUR rule is the only possible FAIL, so
        #    has_fail must track the expectation too (catches spurious findings)
        check(f"[has_fail == {expect}] {name}", rep.has_fail == expect)

    print("\n(B) REGRESSION — real curated GREEN production mdins (no false-alarm)")
    pp = next((p / "project-prime" for p in HERE.parents
               if (p / "project-prime").is_dir()), None)
    if pp is None:
        print("  SKIP  project-prime not found alongside the vault")
    else:
        curated = ["golden-path", "happy-path-fixed-run", "smoke-test", "stage6-wire-test"]
        md_files, restart_files, false_alarms = [], [], []
        for d in curated:
            base = pp / d
            if not base.is_dir():
                continue
            for f in sorted(base.rglob("*.in")):
                text = f.read_text()
                if "&cntrl" not in text.lower():
                    continue            # cpptraj / sqm / leap scripts — not MD namelists
                md_files.append(f)
                m = re.search(r"(?i)\birest\s*=\s*(-?\d+)", cntrl_body(text))
                if m and int(m.group(1)) == 1:
                    restart_files.append(f)
                rep = check_amber_in(f)
                if gate_fires(rep):
                    false_alarms.append(str(f.relative_to(pp)))
                if gate_fires(rep) != oracle_fire(text):
                    check(f"engine == independent oracle on {f.relative_to(pp)}", False)
        check(f"found real MD namelists (got {len(md_files)})", len(md_files) >= 6)
        check(f"corpus exercises restart stages irest=1 (got {len(restart_files)})",
              len(restart_files) >= 3)
        check(f"0 false-alarms on real mdins (got {len(false_alarms)}: {false_alarms[:5]})",
              not false_alarms)

    print("\n(C) GROUND TRUTH — the exact namelist pmemd 26.0 rejected")
    # restart_irest1_ntx1_illegal.in is golden-path/prod.in with only ntx flipped
    # 5->1; pmemd aborted on it with "ntx and irest are inconsistent!" (see the
    # companion *_pmemd_abort.txt). Asserting the gate fires on these exact bytes
    # ties the gate to a failure AMBER itself produced — gate and test can't both
    # be wrong.
    fixture = HERE.parent / "fixtures" / "restart_irest1_ntx1_illegal.in"
    if not fixture.is_file():
        check("ground-truth fixture present", False)
    else:
        text = fixture.read_text()
        check("fixture really is irest=1, ntx=1", oracle_fire(text) is True)
        check("gate FAILs on the pmemd-rejected namelist", gate_fires(check_amber_in(fixture)))

    print(f"\n{'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
