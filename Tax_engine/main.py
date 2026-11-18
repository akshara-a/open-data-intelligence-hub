"""Command-line entry point for the tax engine."""

import argparse
import sys
from pathlib import Path

from agents.supervisor import EngineError, run


def main(argv: list[str] | None = None) -> int:
    """Run the input pipeline and return a process exit code."""
    project_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Reconcile asset inputs and calculate limited 2025 US MACRS examples."
    )
    parser.add_argument("--data-dir", type=Path, default=project_dir / "data")
    parser.add_argument("--output-dir", type=Path, default=project_dir / "output")
    parser.add_argument(
        "--tax-year",
        type=int,
        choices=(2025,),
        default=2025,
        help="Tax year supported by the included educational rule set (2025 only).",
    )
    args = parser.parse_args(argv)

    try:
        result = run(args.data_dir, args.output_dir, tax_year=args.tax_year)
    except (EngineError, OSError) as exc:
        print(f"Tax engine failed: {exc}", file=sys.stderr)
        return 1

    print(f"Processed {result.asset_count} asset(s).")
    print(f"JSON export: {result.json_path}")
    print(f"Audit log: {result.audit_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
