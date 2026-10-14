#!/usr/bin/env python

"""
Verify that every artefact promised by docs/PROMISES-COVERAGE.md
actually exists in the repository. Fails (exit ≠ 0) on any missing
entry so the CFP stays honest.

Usage::

    python3 scripts/check-promises-coverage.py
    python3 scripts/check-promises-coverage.py --strict
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (path_relative_to_root, human_label)
REQUIRED_PATHS: list[tuple[str, str]] = [
    ("scripts/green-api-auto-discover.py",   "Analyzer entry-point"),
    ("scripts/architecture_rules.py",         "Architecture rules AR01-AR05"),
    ("scripts/adr_rules.py",                  "ADR verification module"),
    ("scripts/creedengo-detect-stack.py",     "Multi-stack detection"),
    ("scripts/start.sh",                      "CLI entry-point"),
    ("green-score-threshold.json",            "Threshold gate config"),
    ("Axa Summit Workshop CFP.md",            "Workshop CFP"),
    ("docs/WORKSHOP-ROADMAP.md",              "Workshop roadmap"),
    ("docs/PROMISES-COVERAGE.md",             "Coverage matrix"),
    ("docs/CI-INTEGRATION.md",                "CI integration snippets"),
    ("templates/ci/green-score.yml",          "GitHub Actions workflow"),
    ("templates/adr/README.md",               "ADR templates catalogue"),
    ("samples/java-spring/pom.xml",           "Sample Java Spring Boot"),
    ("samples/python-fastapi/app.py",         "Sample Python FastAPI"),
    ("samples/csharp-aspnet/Program.cs",      "Sample C# ASP.NET Core"),
    ("samples/k8s/hpa.yaml",                  "Sample k8s HPA (AR04)"),
]

# 10 ADR templates (0001-0010)
REQUIRED_PATHS += [
    (f"templates/adr/00{n:02d}-*.md", f"ADR {n:04d}") for n in range(1, 11)
]


def main() -> int:
    strict = "--strict" in sys.argv
    missing: list[tuple[str, str]] = []
    print("🔎 Promises coverage check")
    print("=" * 60)
    for rel, label in REQUIRED_PATHS:
        p = ROOT / rel
        if "*" in rel:
            # glob under parent dir
            parent = ROOT / str(Path(rel).parent)
            pattern = Path(rel).name
            hits = list(parent.glob(pattern)) if parent.is_dir() else []
            ok = bool(hits)
        else:
            ok = p.exists()
        icon = "✅" if ok else "❌"
        print(f"  {icon} {label:35s} {rel}")
        if not ok:
            missing.append((rel, label))
    print("=" * 60)
    if missing:
        print(f"❌ {len(missing)} missing artefact(s):")
        for rel, label in missing:
            print(f"   - {label} ({rel})")
        return 1 if strict else 0
    print("✅ Toutes les promesses du CFP sont matérialisées.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

