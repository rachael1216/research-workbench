#!/usr/bin/env python3
"""Create a minimal study record without overwriting an existing project."""
import argparse
from pathlib import Path
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--domain", choices=["ai", "neuroscience", "cognition", "psychology"], required=True)
    args = parser.parse_args()
    args.path.mkdir(parents=True, exist_ok=False)
    for name in ("sources", "theory", "experiments", "analysis", "paper"):
        (args.path / name).mkdir()
    (args.path / "study.json").write_text(json.dumps({"domain": args.domain, "status": "planned", "question": None,
        "primary_claim": None, "independent_unit": None, "primary_endpoint": None,
        "budget": None, "data": None, "environment": None}, indent=2) + "\n", encoding="utf-8")
    (args.path / "experiments/protocol.md").write_text("# Experiment protocol — PLANNED\n\nQuestion:\n\nCompeting explanations:\n\nControls:\n\nIndependent unit and endpoint:\n\nSample size / precision rationale:\n\nSplit and analysis:\n\nBudget and stop rules:\n\nEnvironment and smoke command:\n\nDeviations:\n", encoding="utf-8")
    (args.path / "sources/search-log.jsonl").touch()
    print(f"Created planned study: {args.path.resolve()}; no experiments executed.")


if __name__ == "__main__":
    main()
