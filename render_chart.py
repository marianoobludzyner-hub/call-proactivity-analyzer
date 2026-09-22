#!/usr/bin/env python3
"""
Dashboard renderer for the Call Proactivity & Expansion Signal Analyzer.
Obludzyner & Co. | https://obludzyner.com

OPTIONAL. score.py has zero dependencies and computes the real scorecard.
This script turns its JSON output into the polished dashboard PNG shown
in the README. It requires matplotlib:

    pip install matplotlib
    python3 score.py --renewal 3 --risk 2 --expansion 3 --stakeholder 2 --nextstep 3 \
        --signals examples/sample_signals.json --json > result.json
    python3 render_chart.py result.json examples/sample_dashboard.png
"""

import json
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
SURFACE = "#fcfcfb"
GRIDLINE = "#e1e0d9"

GOOD = "#0ca30c"
WARNING = "#fab219"
SERIOUS = "#ec835a"
CRITICAL = "#d03b3b"
BLUE = "#2a78d6"

BAND_COLOR = {"Commercial": GOOD, "Developing": WARNING, "Reactive": SERIOUS, "Order-taking": CRITICAL}


def score_color(v):
    return {0: CRITICAL, 1: SERIOUS, 2: WARNING, 3: GOOD}[v]


plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["text.color"] = INK


def render(result, out_path):
    dims = result["dimensions"]
    total = result["total_score"]
    max_score = result["max_score"]
    band = result["band"]
    band_color = BAND_COLOR.get(band, INK_MUTED)
    expansion = result.get("expansion_signals") or []
    risk = result.get("risk_signals") or []

    # each signal card needs room for a wrapped quote (up to 2 lines) + a
    # wrapped reason (up to 2 lines) -- estimate rows generously so nothing
    # collides with the card edge or the next section
    exp_rows = max(len(expansion), 1)
    risk_rows = max(len(risk), 1)
    fig_h = 7.3 + 0.95 * (exp_rows + risk_rows)

    fig = plt.figure(figsize=(8.6, fig_h), dpi=200)
    fig.patch.set_facecolor(SURFACE)

    gs = fig.add_gridspec(
        4, 1, left=0.08, right=0.94, top=1 - (0.5 / fig_h), bottom=0.3 / fig_h,
        height_ratios=[1.5, 1.9, 0.35 + 0.95 * exp_rows, 0.35 + 0.95 * risk_rows],
        hspace=0.5,
    )

    fig.text(0.08, 1 - (0.28 / fig_h), "OBLUDZYNER & CO.  -  OPEN-SOURCE CALL PROACTIVITY ANALYZER",
              fontsize=9.5, color=INK_MUTED, fontweight="bold", ha="left")

    # -- hero: score, then band badge on its own row (never collides with
    # the score digits, regardless of how many digits the score has) --------
    ax_hero = fig.add_subplot(gs[0])
    ax_hero.axis("off")
    ax_hero.text(0, 0.86, "COMMERCIAL PROACTIVITY SCORE", fontsize=11, color=INK_MUTED,
                  fontweight="bold", transform=ax_hero.transAxes)
    ax_hero.text(0, 0.42, f"{total}/{max_score}", fontsize=52, color=INK, fontweight="bold",
                  transform=ax_hero.transAxes, va="center")
    ax_hero.add_patch(FancyBboxPatch((0.0, 0.03), 0.24, 0.20, boxstyle="round,pad=0.02,rounding_size=0.09",
                                       linewidth=0, facecolor=band_color, transform=ax_hero.transAxes))
    ax_hero.text(0.12, 0.13, band.upper(), fontsize=14, color="#ffffff", fontweight="bold",
                  ha="center", va="center", transform=ax_hero.transAxes)

    # -- 5-dimension bars ----------------------------------------------------
    ax_dim = fig.add_subplot(gs[1])
    ax_dim.set_title("5-dimension scorecard", loc="left", fontsize=13, fontweight="bold", color=INK, pad=14)
    n = len(dims)
    ys = list(range(n))[::-1]
    seg_w, seg_gap = 1.0, 0.14
    for y, d in zip(ys, dims):
        for i in range(3):
            c = score_color(d["score"]) if i < d["score"] else GRIDLINE
            ax_dim.add_patch(FancyBboxPatch(
                (i * (seg_w + seg_gap), y - 0.28), seg_w, 0.56,
                boxstyle="round,pad=0,rounding_size=0.14", linewidth=0, facecolor=c,
            ))
        ax_dim.text(-0.25, y, d["label"], ha="right", va="center", fontsize=11, color=INK_SECONDARY)
        ax_dim.text(3 * (seg_w + seg_gap) + 0.15, y, f"{d['score']}/{d['max']}", ha="left", va="center",
                     fontsize=11, fontweight="bold", color=score_color(d["score"]))
    ax_dim.set_xlim(-3.2, 3 * (seg_w + seg_gap) + 1.1)
    ax_dim.set_ylim(-0.7, n - 0.3)
    ax_dim.axis("off")

    # -- signal cards --------------------------------------------------------
    # Wrap text to a real multi-line block sized to the card's actual pixel
    # width, rather than a longer single line that silently runs off the
    # canvas -- 46 chars is calibrated for this card width at this font size.
    def wrap(text, width=46, max_lines=2):
        lines = textwrap.wrap(text, width=width) or [""]
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            lines[-1] = lines[-1].rstrip() + "..."
        return lines

    def signal_panel(ax, title, tag_color, signals):
        ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color=INK, pad=14)
        ax.axis("off")
        ax.set_xlim(0, 1)
        rows = signals if signals else [None]
        row_h = 1.0 / len(rows)
        for i, s in enumerate(rows):
            y1 = 1.0 - row_h * i
            y0 = y1 - row_h * 0.88
            ax.add_patch(FancyBboxPatch((0, y0), 1.0, y1 - y0, boxstyle="round,pad=0.006,rounding_size=0.03",
                                          linewidth=0, facecolor="#f4f3ef", transform=ax.transAxes))
            ax.add_patch(FancyBboxPatch((0.012, y0 + (y1 - y0) * 0.10), 0.012, (y1 - y0) * 0.80,
                                          boxstyle="round,pad=0,rounding_size=0.006",
                                          linewidth=0, facecolor=tag_color, transform=ax.transAxes))
            if s is None:
                ax.text(0.04, (y0 + y1) / 2, "None detected in this call.", fontsize=10.5,
                         color=INK_MUTED, va="center", transform=ax.transAxes, style="italic")
                continue
            quote_lines = wrap(f"\u201c{s.get('quote','')}\u201d", width=52, max_lines=2)
            why_lines = wrap(s.get("why", ""), width=58, max_lines=2)
            ax.text(0.04, y1 - (y1 - y0) * 0.14, "\n".join(quote_lines), fontsize=9.5, color=INK,
                     va="top", linespacing=1.5, transform=ax.transAxes)
            why_top = y0 + (y1 - y0) * (0.46 if len(quote_lines) > 1 else 0.60)
            ax.text(0.04, why_top, "\n".join(why_lines), fontsize=9, color=INK_SECONDARY,
                     va="top", linespacing=1.5, transform=ax.transAxes)
        ax.set_ylim(0, 1)

    ax_exp = fig.add_subplot(gs[2])
    signal_panel(ax_exp, f"Expansion opportunities detected ({len(expansion)})", BLUE, expansion)

    ax_risk = fig.add_subplot(gs[3])
    signal_panel(ax_risk, f"Risk / churn signals detected ({len(risk)})", CRITICAL, risk)

    fig.text(0.08, 0.10 / fig_h, "Open-source, directional version. obludzyner.com  -  Book a Revenue Audit for your real numbers.",
              fontsize=9, color=INK_MUTED)

    fig.savefig(out_path, facecolor=SURFACE)
    print(f"Wrote {out_path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 render_chart.py result.json out.png", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1]) as f:
        result = json.load(f)
    render(result, sys.argv[2])


if __name__ == "__main__":
    main()
