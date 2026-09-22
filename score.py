#!/usr/bin/env python3
"""
Call Proactivity & Expansion Signal Scorecard
Obludzyner & Co. | Post-sales advisory for B2B SaaS | https://obludzyner.com

This script does NOT read or score a transcript itself -- scoring a
conversation against a rubric is a judgment call an LLM makes while reading
it (see rubric.md), not a deterministic calculation. What this script does
is take the 5 dimension scores an LLM (or a human) has already assigned,
apply the shared banding logic, and render a consistent report and chart --
the same way diagnostic.py and rollup.py handle their own math. See
skill/SKILL.md or gpt/CUSTOM_GPT_INSTRUCTIONS.md for how the 5 scores get
produced from an actual transcript.

Zero dependencies. Python 3.8+.

Usage:
    python3 score.py --renewal 3 --risk 2 --expansion 3 --stakeholder 2 --nextstep 3 \
        --json --svg scorecard.svg
"""

import argparse
import json

DIMENSIONS = [
    ("renewal", "Renewal ownership"),
    ("risk", "Risk surfacing"),
    ("expansion", "Expansion probing"),
    ("stakeholder", "Stakeholder mapping"),
    ("nextstep", "Next-step ownership"),
]

MAX_PER_DIMENSION = 3
MAX_SCORE = MAX_PER_DIMENSION * len(DIMENSIONS)


def band_label(total, max_score=MAX_SCORE):
    pct = total / max_score
    if pct >= 0.85:
        return "Commercial"
    if pct >= 0.55:
        return "Developing"
    if pct >= 0.25:
        return "Reactive"
    return "Order-taking"


def compute(scores):
    """scores: dict with keys matching DIMENSIONS[i][0], values 0-3."""
    total = sum(scores[key] for key, _ in DIMENSIONS)
    return {
        "dimensions": [
            {"key": key, "label": label, "score": scores[key], "max": MAX_PER_DIMENSION}
            for key, label in DIMENSIONS
        ],
        "total_score": total,
        "max_score": MAX_SCORE,
        "band": band_label(total),
    }


def render_text(result, expansion_signals=None, risk_signals=None):
    lines = []
    lines.append("=" * 60)
    lines.append("CALL PROACTIVITY & EXPANSION SCORECARD")
    lines.append("=" * 60)
    lines.append(f"Commercial Proactivity Score: {result['total_score']} of {result['max_score']}  ->  {result['band']}")
    lines.append("")
    for d in result["dimensions"]:
        filled = "#" * d["score"] + "-" * (d["max"] - d["score"])
        lines.append(f"  {d['label']:<22} [{filled}] {d['score']}/{d['max']}")
    lines.append("")
    if expansion_signals:
        lines.append("EXPANSION OPPORTUNITIES DETECTED")
        for s in expansion_signals:
            lines.append(f"  - \"{s.get('quote','')}\"")
            lines.append(f"      -> {s.get('why','')}")
        lines.append("")
    if risk_signals:
        lines.append("RISK / CHURN SIGNALS DETECTED")
        for s in risk_signals:
            lines.append(f"  - \"{s.get('quote','')}\"")
            lines.append(f"      -> {s.get('why','')}")
        lines.append("")
    lines.append("=" * 60)
    lines.append("This is the open-source, directional version of the call")
    lines.append("scorecard used inside a SHIFT Method engagement.")
    lines.append("For a Revenue Audit built on your real calls and data:")
    lines.append("  https://obludzyner.com")
    lines.append("=" * 60)
    return "\n".join(lines)


def render_svg(result, path):
    def hbar_row(y, label, value, max_value, color):
        w = 0 if max_value == 0 else max(2, (value / max_value) * 260)
        return (
            f'<text x="0" y="{y-4}" font-size="12" font-family="monospace" fill="#0a1a33">{label}</text>'
            f'<rect x="0" y="{y}" width="260" height="14" fill="#eef1f6" />'
            f'<rect x="0" y="{y}" width="{w:.1f}" height="14" fill="{color}" />'
            f'<text x="{min(w,255)+8}" y="{y+11}" font-size="11" font-family="monospace" fill="#0a1a33">{value}/{MAX_PER_DIMENSION}</text>'
        )

    rows = []
    y = 60
    for d in result["dimensions"]:
        color = "#2f9e6e" if d["score"] == 3 else ("#d9a52f" if d["score"] >= 1 else "#d9542f")
        rows.append(hbar_row(y, d["label"], d["score"], MAX_PER_DIMENSION, color))
        y += 30

    total_h = y + 30
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 {total_h}" font-family="sans-serif">
<rect x="0" y="0" width="300" height="{total_h}" fill="#ffffff" />
<text x="0" y="20" font-size="13" font-family="monospace" fill="#5a6472">Score: {result['total_score']}/{result['max_score']}</text>
<text x="0" y="40" font-size="15" font-family="sans-serif" font-weight="bold" fill="#0a1a33">{result['band']}</text>
{''.join(rows)}
<text x="0" y="{total_h-10}" font-size="9" font-family="monospace" fill="#9aa5b1">Obludzyner &amp; Co. | obludzyner.com | open-source scorecard</text>
</svg>'''
    with open(path, "w") as f:
        f.write(svg)


def main():
    parser = argparse.ArgumentParser(description="Call Proactivity & Expansion Signal Scorecard (open-source)")
    for key, label in DIMENSIONS:
        parser.add_argument(f"--{key}", type=int, choices=[0, 1, 2, 3], required=True, help=label)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--svg", type=str, help="path to write an SVG chart to")
    parser.add_argument("--signals", type=str, help="path to a JSON file with {\"expansion\": [...], \"risk\": [...]} quote lists")
    args = parser.parse_args()

    scores = {key: getattr(args, key) for key, _ in DIMENSIONS}
    result = compute(scores)

    expansion_signals, risk_signals = None, None
    if args.signals:
        with open(args.signals) as f:
            data = json.load(f)
        expansion_signals = data.get("expansion")
        risk_signals = data.get("risk")

    if args.svg:
        render_svg(result, args.svg)

    if args.json:
        out = dict(result)
        if expansion_signals is not None:
            out["expansion_signals"] = expansion_signals
        if risk_signals is not None:
            out["risk_signals"] = risk_signals
        print(json.dumps(out, indent=2))
    else:
        print(render_text(result, expansion_signals, risk_signals))


if __name__ == "__main__":
    main()
