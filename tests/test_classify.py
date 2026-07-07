"""Unit tests for world_cup_penalties.classify."""

import pytest

from world_cup_penalties.classify import classify_outcome, determine_winner
from world_cup_penalties.config import OUTCOME_EXTRA_TIME, OUTCOME_PENALTIES


class TestClassifyOutcome:
    """Tests for classify_outcome()."""

    def test_extra_time_home_wins(self):
        """Match decided in extra time (home scores winner)."""
        assert classify_outcome(2, 1, None, None) == OUTCOME_EXTRA_TIME

    def test_extra_time_away_wins(self):
        """Match decided in extra time (away scores winner)."""
        assert classify_outcome(1, 2, None, None) == OUTCOME_EXTRA_TIME

    def test_penalty_shootout(self):
        """Match tied after extra time, goes to penalties."""
        assert classify_outcome(0, 0, 5, 4) == OUTCOME_PENALTIES

    def test_penalty_shootout_only_pen_home(self):
        """Penalty score only for home team."""
        assert classify_outcome(1, 1, 3, None) == OUTCOME_PENALTIES

    def test_penalty_shootout_only_pen_away(self):
        """Penalty score only for away team."""
        assert classify_outcome(1, 1, None, 5) == OUTCOME_PENALTIES

    def test_invalid_no_scores(self):
        """Raises ValueError when no scores are provided."""
        with pytest.raises(ValueError):
            classify_outcome(None, None, None, None)

    def test_invalid_tied_aet_no_pens(self):
        """Raises ValueError when tied after ET with no penalty scores."""
        with pytest.raises(ValueError):
            classify_outcome(1, 1, None, None)


class TestDetermineWinner:
    """Tests for determine_winner()."""

    def test_winner_extra_time_home(self):
        """Home team wins in extra time."""
        assert determine_winner(3, 1, None, None, "Brazil", "Chile") == "Brazil"

    def test_winner_extra_time_away(self):
        """Away team wins in extra time."""
        assert determine_winner(1, 2, None, None, "Italy", "France") == "France"

    def test_winner_penalties_home(self):
        """Home team wins on penalties."""
        assert determine_winner(0, 0, 4, 2, "Germany", "Argentina") == "Germany"

    def test_winner_penalties_away(self):
        """Away team wins on penalties."""
        assert determine_winner(1, 1, 3, 5, "England", "Portugal") == "Portugal"
