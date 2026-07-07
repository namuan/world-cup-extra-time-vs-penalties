"""Outcome classification logic for extra-time matches.

Determines whether a knockout match that reached extra time was
decided during extra time or went to a penalty shootout.
"""

from world_cup_penalties.config import (
    OUTCOME_EXTRA_TIME,
    OUTCOME_PENALTIES,
)


def classify_outcome(
    score_aet_home: int | None,
    score_aet_away: int | None,
    score_pen_home: int | None,
    score_pen_away: int | None,
) -> str:
    """Classify a match outcome based on extra-time and penalty scores.

    Parameters
    ----------
    score_aet_home : int | None
        Home team goals at end of extra time (or None if not available).
    score_aet_away : int | None
        Away team goals at end of extra time.
    score_pen_home : int | None
        Home team penalty shootout goals (None if no shootout).
    score_pen_away : int | None
        Away team penalty shootout goals.

    Returns
    -------
    str
        ``"extra_time"`` if the match was decided during extra time,
        ``"penalties"`` if it went to a penalty shootout.

    Raises
    ------
    ValueError
        If the input combination is logically impossible (e.g., both
        extra-time and penalty scores are None, or the scores imply
        a tie after extra time with no shootout).

    Examples
    --------
    >>> classify_outcome(0, 0, 4, 2)
    'penalties'
    >>> classify_outcome(2, 1, None, None)
    'extra_time'
    """
    # If penalty scores are present, it went to a shootout
    if score_pen_home is not None or score_pen_away is not None:
        return OUTCOME_PENALTIES

    # If extra-time scores are present and different, decided in ET
    if score_aet_home is not None and score_aet_away is not None:
        if score_aet_home != score_aet_away:
            return OUTCOME_EXTRA_TIME

    # If we get here something is wrong
    msg = (
        f"Cannot classify: AET=({score_aet_home},{score_aet_away}), "
        f"PEN=({score_pen_home},{score_pen_away})"
    )
    raise ValueError(msg)


def determine_winner(
    score_aet_home: int | None,
    score_aet_away: int | None,
    score_pen_home: int | None,
    score_pen_away: int | None,
    team_home: str,
    team_away: str,
) -> str:
    """Determine the winning team after extra time / penalties.

    Parameters
    ----------
    score_aet_home, score_aet_away : int | None
        Goals at end of extra time.
    score_pen_home, score_pen_away : int | None
        Penalty shootout goals.
    team_home, team_away : str
        Names of the two teams.

    Returns
    -------
    str
        Name of the winning team.
    """
    outcome = classify_outcome(
        score_aet_home, score_aet_away, score_pen_home, score_pen_away
    )

    if outcome == OUTCOME_EXTRA_TIME:
        if score_aet_home is not None and score_aet_away is not None:
            if score_aet_home > score_aet_away:
                return team_home
            return team_away

    if outcome == OUTCOME_PENALTIES:
        if score_pen_home is not None and score_pen_away is not None:
            if score_pen_home > score_pen_away:
                return team_home
            return team_away

    msg = f"Cannot determine winner for {team_home} vs {team_away}"
    raise ValueError(msg)
