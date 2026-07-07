"""Analysis of extra-time outcomes across included World Cups.

Produces four breakdowns:
1. Overall counts & percentages
2. By era (1982-1994 vs 2006-2022)
3. By tournament (per year)
4. By stage (Round of 16, Quarter-final, Semi-final, Third place, Final)
"""

import pandas as pd

from world_cup_penalties.config import (
    ERA_GROUPS,
    OUTCOME_LABELS,
    PROCESSED_CSV,
    STAGE_ORDER,
)


def load_data() -> pd.DataFrame:
    """Load the curated extra-time matches dataset."""
    df = pd.read_csv(PROCESSED_CSV)
    return df


def add_era_column(df: pd.DataFrame) -> pd.DataFrame:
    """Add an ``era`` column based on the ``year`` column."""
    def _era(year: int) -> str:
        for label, years in ERA_GROUPS.items():
            if year in years:
                return label
        raise ValueError(f"Year {year} is not in any defined era")

    df = df.copy()
    df["era"] = df["year"].apply(_era)
    return df


def overall_counts(df: pd.DataFrame) -> dict:
    """Return overall counts and percentages."""
    total = len(df)
    counts = df["outcome_type"].value_counts()
    et_count = counts.get("extra_time", 0)
    pen_count = counts.get("penalties", 0)

    return {
        "total": total,
        "extra_time": et_count,
        "penalties": pen_count,
        "extra_time_pct": round(et_count / total * 100, 1) if total else 0.0,
        "penalties_pct": round(pen_count / total * 100, 1) if total else 0.0,
    }


def by_era(df: pd.DataFrame) -> pd.DataFrame:
    """Return a summary table grouped by era."""
    df = add_era_column(df)
    # Use ordered categories for display
    era_order = list(ERA_GROUPS.keys())

    summary = (
        df.groupby(["era", "outcome_type"])
        .size()
        .unstack(fill_value=0)
        .reindex(era_order)
    )

    summary["Total"] = summary.sum(axis=1)
    summary["%-ET"] = (summary.get("extra_time", 0) / summary["Total"] * 100).round(1)
    summary["%-Pens"] = (summary.get("penalties", 0) / summary["Total"] * 100).round(1)

    # Rename columns for display
    summary = summary.rename(
        columns={
            "extra_time": "ET-decided",
            "penalties": "Penalties",
        }
    )

    return summary[["Total", "ET-decided", "Penalties", "%-ET", "%-Pens"]]


def by_tournament(df: pd.DataFrame) -> pd.DataFrame:
    """Return a summary table grouped by year (tournament)."""
    summary = (
        df.groupby(["year", "outcome_type"])
        .size()
        .unstack(fill_value=0)
    )

    summary["Total"] = summary.sum(axis=1)
    summary["%-ET"] = (summary.get("extra_time", 0) / summary["Total"] * 100).round(1)
    summary["%-Pens"] = (summary.get("penalties", 0) / summary["Total"] * 100).round(1)

    summary = summary.rename(
        columns={
            "extra_time": "ET-decided",
            "penalties": "Penalties",
        }
    )

    return summary[["Total", "ET-decided", "Penalties", "%-ET", "%-Pens"]]


def by_stage(df: pd.DataFrame) -> pd.DataFrame:
    """Return a summary table grouped by knockout stage."""
    summary = (
        df.groupby(["stage", "outcome_type"])
        .size()
        .unstack(fill_value=0)
    )

    # Reindex to standard stage order, keeping only stages that appear
    stage_order = [s for s in STAGE_ORDER if s in summary.index]

    summary["Total"] = summary.sum(axis=1)
    summary["%-ET"] = (summary.get("extra_time", 0) / summary["Total"] * 100).round(1)
    summary["%-Pens"] = (summary.get("penalties", 0) / summary["Total"] * 100).round(1)

    summary = summary.rename(
        columns={
            "extra_time": "ET-decided",
            "penalties": "Penalties",
        }
    )

    return summary.loc[stage_order, ["Total", "ET-decided", "Penalties", "%-ET", "%-Pens"]]


def print_overall(results: dict) -> None:
    """Print the overall summary."""
    print("=== Overall ===")
    print(f"Total extra-time matches: {results['total']}")
    et_label = OUTCOME_LABELS["extra_time"]
    pen_label = OUTCOME_LABELS["penalties"]
    print(f"{et_label}: {results['extra_time']:>5}  ({results['extra_time_pct']}%)")
    print(f"{pen_label}: {results['penalties']:>5}  ({results['penalties_pct']}%)")
    print()


def print_era_table(summary: pd.DataFrame) -> None:
    """Print the era breakdown table."""
    print("=== By era ===")
    print(summary.to_string())
    print()


def print_tournament_table(summary: pd.DataFrame) -> None:
    """Print the per-tournament table."""
    print("=== By tournament ===")
    print(summary.to_string())
    print()


def print_stage_table(summary: pd.DataFrame) -> None:
    """Print the per-stage table."""
    print("=== By stage ===")
    print(summary.to_string())
    print()


def main() -> None:
    """Run all analyses and print results to stdout."""
    df = load_data()
    results = overall_counts(df)
    print_overall(results)
    print_era_table(by_era(df))
    print_tournament_table(by_tournament(df))
    print_stage_table(by_stage(df))


if __name__ == "__main__":
    main()
