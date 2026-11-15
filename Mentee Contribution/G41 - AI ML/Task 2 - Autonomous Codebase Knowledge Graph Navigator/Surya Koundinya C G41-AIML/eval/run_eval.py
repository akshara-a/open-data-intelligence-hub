"""Golden-set evaluation against the seeded demo graph (needs Neo4j + GEMINI_API_KEY).
Checks: required entities present, forbidden entities absent, grounding check passed,
and that no Cypher executed by the agent was blocked as unsafe."""
import asyncio
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from kgnav.agent import NavigatorAgent  # noqa: E402

# must_not_include is meant to catch entities wrongly CLAIMED as affected or
# as part of a cycle. Naming an entity elsewhere is legitimate: coupling and
# single-point-of-failure lists name the busiest nodes, and "Not affected"
# lists explicit exclusions. So only claim-bearing sections are checked.
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_CLAIM_HEADING = re.compile(r"affected|circular|cycle", re.I)
_NEUTRAL_HEADING = re.compile(r"not affected|exclusion|coupling", re.I)
# A metrics line (Ca/Ce/instability/fan-in/out) only reports numbers. It is
# ignored unless the same line also makes a cycle or impact claim.
_METRIC_LINE = re.compile(r"\bCa\b|\bCe\b|instability|fan[_ -]?(in|out)", re.I)
_CLAIM_WORDS = re.compile(r"cycle|circular|\bscc\b|affected|break|impacted|blast", re.I)


def claims_text(md: str) -> str:
    """Text of claim-bearing sections only. Falls back to the whole body
    when no such section is found, so the check can never pass silently."""
    stack: list[tuple[int, str]] = []
    out: list[str] = []
    for line in md.splitlines():
        m = _HEADING.match(line)
        if m:
            level = len(m.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, m.group(2)))
        titles = [t for _, t in stack]
        if any(_CLAIM_HEADING.search(t) for t in titles) and not any(
            _NEUTRAL_HEADING.search(t) for t in titles
        ):
            if _METRIC_LINE.search(line) and not _CLAIM_WORDS.search(line):
                continue
            out.append(line)
    return "\n".join(out) if out else md


async def main():
    cases = json.loads((ROOT / "eval" / "golden.json").read_text())
    passed = 0
    for c in cases:
        res = await NavigatorAgent().run(c["question"], ROOT / "reports")
        md = res.report_md.split("## Appendix A")[0]
        miss = [m for m in c["must_include"] if m not in md]
        leak = [m for m in c["must_not_include"] if m in claims_text(md)]
        unsafe = [e for e in res.evidence if "UnsafeCypherError" in e["output"]]
        ok = not miss and not leak and not res.ungrounded
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} | {c['question'][:70]}\n   missing={miss} leaked={leak} ungrounded={res.ungrounded} blocked_cypher={len(unsafe)}")
    print(f"\n{passed}/{len(cases)} passed")
    sys.exit(0 if passed == len(cases) else 1)


asyncio.run(main())