
"""Command-line interface for KG Navigator."""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path


def _exception_group_message(group: ExceptionGroup) -> str:
    """Flatten nested exception groups into readable error messages."""

    messages = []

    def collect(exc):
        if isinstance(exc, BaseExceptionGroup):
            for nested in exc.exceptions:
                collect(nested)
        else:
            message = str(exc).strip()
            if message:
                messages.append(
                    f"{type(exc).__name__}: {message}"
                )

    collect(group)

    return "\n".join(dict.fromkeys(messages)) or str(group)


def main():
    parser = argparse.ArgumentParser(
        prog="kgnav",
        description="Autonomous Codebase Knowledge Graph Navigator",
    )

    sub = parser.add_subparsers(
        dest="cmd",
        required=True,
    )

    ask_parser = sub.add_parser(
        "ask",
        help="Ask an architecture / blast-radius question",
    )

    ask_parser.add_argument("question")
    ask_parser.add_argument("--out-dir", default="reports")
    ask_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show agent steps on stderr",
    )
    ask_parser.add_argument(
        "--print",
        dest="show",
        action="store_true",
        help="Also print the report",
    )

    resume_parser = sub.add_parser(
        "resume",
        help="Re-run ONLY the report step from a saved evidence checkpoint",
    )

    resume_parser.add_argument(
        "checkpoint",
        nargs="?",
        help="checkpoint .json (default: newest in reports/.checkpoints)",
    )
    resume_parser.add_argument("--out-dir", default="reports")
    resume_parser.add_argument("-v", "--verbose", action="store_true")
    resume_parser.add_argument(
        "--print",
        dest="show",
        action="store_true",
    )

    sub.add_parser(
        "seed",
        help="Seed the demo graph into Neo4j",
    )

    sub.add_parser(
        "doctor",
        help="Check Gemini key, model IDs and Neo4j connectivity",
    )

    args = parser.parse_args()

    if args.cmd == "doctor":
        from .doctor import run
        sys.exit(run())

    if args.cmd == "seed":
        import runpy

        runpy.run_path(
            str(
                Path(__file__).resolve().parents[2]
                / "scripts"
                / "seed_graph.py"
            ),
            run_name="__main__",
        )
        return

    from .agent import (
        InvestigationFailedError,
        NavigatorAgent,
        TargetNotFoundError,
    )

    try:
        agent = NavigatorAgent(verbose=args.verbose)

        if args.cmd == "resume":
            checkpoint = args.checkpoint

            if not checkpoint:
                checkpoint_dir = Path(
                    args.out_dir,
                    ".checkpoints",
                )

                found = sorted(
                    checkpoint_dir.glob("*.json"),
                    key=lambda path: path.stat().st_mtime,
                )

                if not found:
                    print(
                        "ERROR: No checkpoints found in "
                        + str(checkpoint_dir),
                        file=sys.stderr,
                    )
                    sys.exit(2)

                checkpoint = found[-1]

            result = asyncio.run(
                agent.resume(
                    checkpoint,
                    args.out_dir,
                )
            )

        else:
            result = asyncio.run(
                agent.run(
                    args.question,
                    args.out_dir,
                )
            )

    except TargetNotFoundError as exc:
        print(
            "\nKG Navigator — Target validation failed",
            file=sys.stderr,
        )
        print(
            "Status: TARGET NOT FOUND",
            file=sys.stderr,
        )

        if exc.requested_target:
            print(
                f"Requested target: {exc.requested_target}",
                file=sys.stderr,
            )

        print(
            "Graph verification: No exact matching node was found.",
            file=sys.stderr,
        )

        if exc.suggestions:
            print(
                "Possible matches (not selected automatically): "
                + ", ".join(exc.suggestions),
                file=sys.stderr,
            )

        print(
            "Impact analysis: NOT EXECUTED",
            file=sys.stderr,
        )
        print(
            "Report: NOT GENERATED",
            file=sys.stderr,
        )
        print(
            "\nPlease retry using an exact graph node name.",
            file=sys.stderr,
        )

        sys.exit(2)

    except InvestigationFailedError as exc:
        if os.getenv("KGNAV_DEBUG"):
            raise

        print(
            f"\nINVESTIGATION ERROR: {exc}",
            file=sys.stderr,
        )
        print(
            "No report was generated because the required "
            "graph investigation could not be completed.",
            file=sys.stderr,
        )
        sys.exit(2)

    except ExceptionGroup as exc:
        if os.getenv("KGNAV_DEBUG"):
            raise

        print(
            "\nINVESTIGATION ERROR:",
            file=sys.stderr,
        )
        print(
            _exception_group_message(exc),
            file=sys.stderr,
        )
        print(
            "The investigation did not complete successfully. "
            "No verified report should be used.",
            file=sys.stderr,
        )
        sys.exit(2)

    except RuntimeError as exc:
        if os.getenv("KGNAV_DEBUG"):
            raise

        print(
            f"\nERROR: {exc}",
            file=sys.stderr,
        )
        sys.exit(2)

    if args.show:
        print(result.report_md)

    print(
        f"\nReport written to {result.path}",
        file=sys.stderr,
    )

    if result.ungrounded:
        print(
            "WARNING: unverified identifiers: "
            f"{result.ungrounded}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
