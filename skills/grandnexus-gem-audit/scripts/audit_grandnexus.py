#!/usr/bin/env python3
"""Run safe, read-only health checks against a GrandNexus checkout."""
from __future__ import annotations
import argparse, importlib.util, json, pathlib, subprocess, sys

def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    return {"command": " ".join(cmd), "returncode": p.returncode,
            "stdout": p.stdout[-12000:], "stderr": p.stderr[-6000:]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=pathlib.Path)
    ap.add_argument("--report", type=pathlib.Path)
    args = ap.parse_args()
    root = args.root.resolve()
    if not (root / "grandnexus").is_dir():
        raise SystemExit(f"Not a GrandNexus root: {root}")
    report = {"root": str(root), "files": {}, "tools": {}, "checks": []}
    for rel in ["README.md", "STATUS.md", "requirements.txt", "tools/smoke_test.py", "tests_lab"]:
        report["files"][rel] = (root / rel).exists()
    for name in ["hypothesis", "clingo", "rdflib", "networkx", "psutil", "yaml", "torch"]:
        report["tools"][name] = bool(importlib.util.find_spec(name))
    smoke = root / "tools/smoke_test.py"
    if smoke.exists():
        report["checks"].append(run([sys.executable, str(smoke)], root))
    tests = sorted((root / "tests_lab").glob("test_*.py"))
    for test in tests:
        result = run([sys.executable, str(test)], root)
        report["checks"].append(result)
    diff = root / "tools/diff_engines.py"
    programs = root / "tests_lab/programmes_nx"
    if report["tools"]["clingo"] and diff.exists() and programs.is_dir():
        report["checks"].append(run([sys.executable, str(diff), str(programs)], root))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    passed = sum(x["returncode"] == 0 for x in report["checks"])
    failed = len(report["checks"]) - passed
    print(json.dumps({"root": str(root), "checks": len(report["checks"]), "passed": passed, "failed": failed, "report": str(args.report) if args.report else None}, ensure_ascii=False))
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
