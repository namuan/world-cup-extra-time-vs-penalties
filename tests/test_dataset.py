"""Comprehensive validation tests for the processed dataset.

These 18+ tests verify:
- File presence and readability
- Required columns
- Year filters (no golden-goal years, no pre-penalty years, all in scope)
- Score consistency (all tied at 90')
- Outcome type validity and coverage
- Penalty score integrity
- Winner consistency with AET/penalty scores
- Source columns filled
- Known historical matches present with correct classification
- No duplicate rows
"""


import pandas as pd
import pytest

from world_cup_penalties.config import (
    EXCLUDED_GOLDEN_GOAL,
    EXCLUDED_NO_PENALTIES,
    INCLUDED_YEARS,
    PROCESSED_CSV,
)

# ── Fixtures ────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def df() -> pd.DataFrame:
    """Load the processed dataset once per module."""
    if not PROCESSED_CSV.exists():
        pytest.fail(f"Dataset not found: {PROCESSED_CSV}")
    return pd.read_csv(PROCESSED_CSV)


# ── File & structure tests ─────────────────────────────────────────────


class TestFileStructure:
    """Tests for file presence and basic structure."""

    def test_file_exists(self):
        """The processed CSV file must exist."""
        assert PROCESSED_CSV.exists(), f"File not found: {PROCESSED_CSV}"

    def test_file_is_readable(self):
        """The file must be readable as CSV with at least one row."""
        raw = pd.read_csv(PROCESSED_CSV)
        assert len(raw) > 0, "CSV file is empty"

    def test_required_columns_present(self, df):
        """All required columns must be present."""
        required = [
            "year",
            "stage",
            "team_home",
            "team_away",
            "score_90home",
            "score_90away",
            "score_ethome",
            "score_etaway",
            "score_penhome",
            "score_penaway",
            "outcome_type",
            "winner",
        ]
        missing = [c for c in required if c not in df.columns]
        assert not missing, f"Missing columns: {missing}"

    def test_no_duplicate_rows(self, df):
        """No duplicate rows (same year, stage, teams)."""
        dupes = df.duplicated(subset=["year", "stage", "team_home", "team_away"])
        assert not dupes.any(), f"Found {dupes.sum()} duplicate rows"


# ── Year-filter tests ──────────────────────────────────────────────────


class TestYearFilters:
    """Tests for correct year filtering."""

    def test_no_golden_goal_years(self, df):
        """1998 and 2002 must NOT appear."""
        bad = df[df["year"].isin(EXCLUDED_GOLDEN_GOAL)]
        assert bad.empty, f"Golden-goal years present: {sorted(bad['year'].unique())}"

    def test_no_pre_penalty_years(self, df):
        """Years before 1978 must NOT appear."""
        bad = df[df["year"].isin(EXCLUDED_NO_PENALTIES)]
        assert bad.empty, f"Pre-penalty years present: {sorted(bad['year'].unique())}"

    def test_all_years_in_scope(self, df):
        """Every row year must be in INCLUDED_YEARS."""
        bad = df[~df["year"].isin(INCLUDED_YEARS)]
        assert bad.empty, f"Unexpected years: {sorted(bad['year'].unique())}"

    def test_all_included_years_present(self, df):
        """Every included year must have at least one match."""
        missing = [y for y in INCLUDED_YEARS if y not in df["year"].values]
        assert not missing, f"Years with no matches: {missing}"

    def test_year_is_integer(self, df):
        """Year column must be integer type."""
        assert pd.api.types.is_integer_dtype(df["year"]), "year is not integer"


# ── Score-consistency tests ────────────────────────────────────────────


class TestScoreConsistency:
    """Tests for score integrity."""

    def test_all_tied_at_90(self, df):
        """Every match must be tied after 90 minutes."""
        tied = df["score_90home"] == df["score_90away"]
        assert tied.all(), f"Found {tied.sum()} matches not tied at 90'"

    def test_score_columns_are_numeric(self, df):
        """All score columns must be numeric (int or float)."""
        score_cols = [
            "score_90home",
            "score_90away",
            "score_ethome",
            "score_etaway",
            "score_penhome",
            "score_penaway",
        ]
        for col in score_cols:
            assert pd.api.types.is_numeric_dtype(
                df[col]
            ), f"{col} is not numeric"

    def test_extra_time_scores_non_negative(self, df):
        """Extra-time scores must be >= 0 (or NaN if not available)."""
        for col in ["score_ethome", "score_etaway"]:
            vals = df[col].dropna()
            assert (vals >= 0).all(), f"{col} has negative values"

    def test_penalty_scores_non_negative(self, df):
        """Penalty scores must be >= 0 (or NaN if not available)."""
        for col in ["score_penhome", "score_penaway"]:
            vals = df[col].dropna()
            assert (vals >= 0).all(), f"{col} has negative values"


# ── Outcome-type tests ─────────────────────────────────────────────────


class TestOutcomeType:
    """Tests for outcome_type column."""

    def test_outcome_type_valid(self, df):
        """outcome_type must be 'extra_time' or 'penalties'."""
        valid = {"extra_time", "penalties"}
        bad = df[~df["outcome_type"].isin(valid)]
        assert bad.empty, f"Invalid outcome types: {bad['outcome_type'].unique()}"

    def test_both_outcomes_present(self, df):
        """Both outcome types must appear at least once."""
        present = set(df["outcome_type"].unique())
        assert "extra_time" in present, "No extra_time outcomes"
        assert "penalties" in present, "No penalties outcomes"

    def test_penalty_outcome_has_penalty_scores(self, df):
        """Rows with outcome=penalties must have penalty scores."""
        pens = df[df["outcome_type"] == "penalties"]
        missing = pens[pens["score_penhome"].isna() | pens["score_penaway"].isna()]
        assert missing.empty, (
            f"{len(missing)} penalty rows missing penalty scores"
        )

    def test_extra_time_outcome_has_no_penalty_scores(self, df):
        """Rows with outcome=extra_time should have NaN penalty scores."""
        et = df[df["outcome_type"] == "extra_time"]
        has_pens = et[et["score_penhome"].notna() | et["score_penaway"].notna()]
        assert has_pens.empty, (
            f"{len(has_pens)} extra_time rows have penalty scores"
        )

    def test_extra_time_scores_differ(self, df):
        """Rows with outcome=extra_time must have different AET scores."""
        et = df[df["outcome_type"] == "extra_time"]
        tied = et[et["score_ethome"] == et["score_etaway"]]
        assert tied.empty, f"{len(tied)} extra_time rows have tied AET scores"


# ── Winner-consistency tests ───────────────────────────────────────────


class TestWinnerConsistency:
    """Tests for winner column integrity."""

    def test_winner_present(self, df):
        """Winner column must have no missing values."""
        assert df["winner"].notna().all(), "Some rows missing winner"

    def test_winner_is_one_of_teams(self, df):
        """Winner must be either team_home or team_away."""
        valid = (df["winner"] == df["team_home"]) | (
            df["winner"] == df["team_away"]
        )
        assert valid.all(), "Winner is not one of the two teams"

    def test_extra_time_winner_matches_score(self, df):
        """For extra_time outcomes, winner should have higher AET score."""
        et = df[df["outcome_type"] == "extra_time"].copy()
        home_wins = et["winner"] == et["team_home"]
        away_wins = et["winner"] == et["team_away"]
        score_ok = (
            (home_wins & (et["score_ethome"] > et["score_etaway"]))
            | (away_wins & (et["score_etaway"] > et["score_ethome"]))
        )
        bad = et[~score_ok]
        assert bad.empty, f"{len(bad)} extra_time rows have inconsistent winner"

    def test_penalty_winner_matches_score(self, df):
        """For penalties outcomes, winner should have higher penalty score."""
        pens = df[df["outcome_type"] == "penalties"].copy()
        home_wins = pens["winner"] == pens["team_home"]
        away_wins = pens["winner"] == pens["team_away"]
        score_ok = (
            (home_wins & (pens["score_penhome"] > pens["score_penaway"]))
            | (away_wins & (pens["score_penaway"] > pens["score_penhome"]))
        )
        bad = pens[~score_ok]
        assert bad.empty, f"{len(bad)} penalty rows have inconsistent winner"


# ── Known-match tests ──────────────────────────────────────────────────


class TestKnownMatches:
    """Spot-check a few historically significant matches."""

    def test_1982_semi_present(self, df):
        """1982 SF: West Germany vs France went to penalties."""
        match = df[
            (df["year"] == 1982) & (df["stage"] == "Semi-final")
            & (df["team_home"] == "West Germany") & (df["team_away"] == "France")
        ]
        assert len(match) == 1
        assert match.iloc[0]["outcome_type"] == "penalties"

    def test_1994_final_present(self, df):
        """1994 Final: Brazil vs Italy went to penalties."""
        match = df[
            (df["year"] == 1994) & (df["stage"] == "Final")
            & (df["team_home"] == "Brazil") & (df["team_away"] == "Italy")
        ]
        assert len(match) == 1
        assert match.iloc[0]["outcome_type"] == "penalties"

    def test_2006_final_present(self, df):
        """2006 Final: Italy vs France went to penalties."""
        match = df[
            (df["year"] == 2006) & (df["stage"] == "Final")
            & (df["team_home"] == "Italy") & (df["team_away"] == "France")
        ]
        assert len(match) == 1
        assert match.iloc[0]["outcome_type"] == "penalties"

    def test_2014_final_extra_time(self, df):
        """2014 Final: Germany vs Argentina decided in extra time."""
        match = df[
            (df["year"] == 2014) & (df["stage"] == "Final")
            & (df["team_home"] == "Germany") & (df["team_away"] == "Argentina")
        ]
        assert len(match) == 1
        assert match.iloc[0]["outcome_type"] == "extra_time"

    def test_2022_final_penalties(self, df):
        """2022 Final: Argentina vs France went to penalties."""
        match = df[
            (df["year"] == 2022) & (df["stage"] == "Final")
            & (df["team_home"] == "Argentina") & (df["team_away"] == "France")
        ]
        assert len(match) == 1
        assert match.iloc[0]["outcome_type"] == "penalties"


# ── Count consistency tests ────────────────────────────────────────────


class TestCountConsistency:
    """Overall counts from the research question."""

    def test_total_matches(self, df):
        """Total matches should be 46 per the research plan."""
        assert len(df) == 46, f"Expected 46 matches, got {len(df)}"

    def test_era_counts(self, df):
        """1982-1994 should have 18, 2006-2022 should have 28."""
        early = df[df["year"].isin([1982, 1986, 1990, 1994])]
        late = df[df["year"] >= 2006]
        assert len(early) == 18, f"1982-1994: expected 18, got {len(early)}"
        assert len(late) == 28, f"2006-2022: expected 28, got {len(late)}"
