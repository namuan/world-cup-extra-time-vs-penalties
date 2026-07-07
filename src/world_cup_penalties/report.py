"""Generate the final markdown research report.

Writes ``reports/full-extra-time-vs-penalties.md``.
"""



from world_cup_penalties.analyze import (
    add_era_column,
    by_era,
    by_stage,
    by_tournament,
    load_data,
    overall_counts,
)
from world_cup_penalties.config import (
    OUTCOME_LABELS,
    REPORTS_DIR,
    RSSSF_URLS,
)


def _fmt_pct(value: float) -> str:
    return f"{value:.1f}%"


def _era_label(year: int) -> str:
    if year <= 1994:
        return "1982-1994"
    return "2006-2022"


def generate_report() -> str:
    """Generate the full markdown report as a string."""
    df = load_data()
    overall = overall_counts(df)

    lines: list[str] = []

    # ── Title ──────────────────────────────────────────────────────────
    lines.append("# Men's FIFA World Cup: full extra time vs penalty shootouts\n")

    # ── Short answer ───────────────────────────────────────────────────
    lines.append("## Short answer\n")
    et_label = OUTCOME_LABELS["extra_time"]
    pen_label = OUTCOME_LABELS["penalties"]
    lines.append(
        f"Of the **{overall['total']}** knockout matches in men's World Cups "
        f"that reached extra time between 1982–1994 and 2006–2022, "
        f"**{overall['extra_time']}** ({_fmt_pct(overall['extra_time_pct'])}) "
        f"were {et_label.lower()} while "
        f"**{overall['penalties']}** ({_fmt_pct(overall['penalties_pct'])}) "
        f"{pen_label.lower()}.\n"
    )
    lines.append(
        "In other words, nearly two-thirds of all extra-time knockout matches "
        "ended in a penalty shootout rather than being settled during "
        "the additional 30 minutes.\n"
    )

    # ── Scope and exclusions ───────────────────────────────────────────
    lines.append("## Scope and exclusions\n")
    lines.append("**Included tournaments:**")
    lines.append("- 1982, 1986, 1990, 1994 (pre-golden-goal era with penalties)")
    lines.append("- 2006, 2010, 2014, 2018, 2022 (post-golden-goal era with penalties)")
    lines.append("")
    lines.append("**Excluded:**")
    lines.append("- 1930 to 1978 — no penalty shootout system")
    lines.append("- 1998 and 2002 — golden goal was active")
    lines.append("- Qualification matches")
    lines.append("- Group-stage matches\n")

    # ── Data sources ───────────────────────────────────────────────────
    lines.append("## Data sources\n")
    lines.append("Match results were sourced from the Rec.Sport.Soccer Statistics "
                 "Foundation (RSSSF) for each tournament:")
    lines.append("")
    for year in sorted(RSSSF_URLS):
        lines.append(f"- [{year}]({RSSSF_URLS[year]})")
    lines.append("")
    lines.append("Key matches were cross-checked against individual Wikipedia "
                 "tournament pages for verification.\n")

    # ── Methodology ────────────────────────────────────────────────────
    lines.append("## Methodology\n")
    lines.append("1. **Identify candidate matches:** All knockout-stage matches "
                 "in the included tournaments were reviewed.")
    lines.append("2. **Filter for extra time:** Only matches that were tied "
                 "after 90 minutes (regulation) were retained.")
    lines.append("3. **Classify outcome:** Each match was classified as either "
                 "`extra_time` (a goal was scored during the 30-minute extra "
                 "time period) or `penalties` (the match remained tied after "
                 "extra time and proceeded to a penalty shootout).")
    lines.append("4. **Validate:** Data was cross-checked against Wikipedia "
                 "and all rows were programmatically validated (see "
                 "`tests/test_dataset.py`).\n")

    # ── Overall results ────────────────────────────────────────────────
    lines.append("## Overall results\n")
    lines.append("| Outcome | Count | Percentage |")
    lines.append("| ------ | ----: | :--------: |")
    lines.append(
        f"| {et_label} | {overall['extra_time']} | "
        f"{_fmt_pct(overall['extra_time_pct'])} |"
    )
    lines.append(
        f"| {pen_label} | {overall['penalties']} | "
        f"{_fmt_pct(overall['penalties_pct'])} |"
    )
    lines.append(
        f"| **Total** | **{overall['total']}** | **100%** |\n"
    )

    # ── Results by era ─────────────────────────────────────────────────
    lines.append("## Results by era\n")
    era_df = by_era(df)
    lines.append(era_df.to_markdown() + "\n")

    # ── Results by tournament ──────────────────────────────────────────
    lines.append("## Results by tournament\n")
    tourn_df = by_tournament(df)
    lines.append(tourn_df.to_markdown() + "\n")

    # ── Results by stage ───────────────────────────────────────────────
    lines.append("## Results by stage\n")
    stage_df = by_stage(df)
    lines.append(stage_df.to_markdown() + "\n")

    # ── Match-level appendix ───────────────────────────────────────────
    lines.append("## Match-level appendix\n")
    display_df = df.copy()
    display_df = add_era_column(display_df)
    display_df = display_df.rename(
        columns={
            "year": "Year",
            "stage": "Stage",
            "team_home": "Home",
            "team_away": "Away",
            "score_90home": "90'H",
            "score_90away": "90'A",
            "score_ethome": "AET H",
            "score_etaway": "AET A",
            "score_penhome": "Pens H",
            "score_penaway": "Pens A",
            "outcome_type": "Outcome",
            "winner": "Winner",
        }
    )
    display_cols = [
        "Year", "Stage", "Home", "Away",
        "90'H", "90'A", "AET H", "AET A", "Pens H", "Pens A",
        "Outcome", "Winner",
    ]
    lines.append(display_df[display_cols].to_markdown(index=False) + "\n")

    # ── Limitations ────────────────────────────────────────────────────
    lines.append("## Limitations\n")
    lines.append("- **Manual curation:** The dataset was compiled manually "
                 "from RSSSF pages; some encoding issues exist for older "
                 "tournaments (1982–1994).")
    lines.append("- **Third-place matches:** One third-place match (1986, "
                 "France vs Belgium) reached extra time and is included "
                 "in the dataset.")
    lines.append("- **Cross-check:** A full cross-check against FIFA's own "
                 "records has not yet been completed.")
    lines.append("- **Small sample:** With 46 matches spread across 9 "
                 "tournaments, per-tournament and per-stage breakdowns "
                 "should be interpreted cautiously.\n")

    return "\n".join(lines)


def main() -> None:
    """Generate and write the report."""
    report = generate_report()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "full-extra-time-vs-penalties.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"Report written → {report_path}")


if __name__ == "__main__":
    main()
