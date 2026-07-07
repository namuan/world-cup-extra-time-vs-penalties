"""Project-wide constants and path configuration."""

from pathlib import Path

# Project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Data directories
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RSSSF_DIR = RAW_DIR / "rsssf"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Reports
REPORTS_DIR = PROJECT_ROOT / "reports"

# Inventory file
INVENTORY_PATH = RAW_DIR / "source_inventory.csv"

# Processed dataset
PROCESSED_CSV = PROCESSED_DIR / "extra_time_matches.csv"

# Tournaments included in the study
INCLUDED_YEARS = [1982, 1986, 1990, 1994, 2006, 2010, 2014, 2018, 2022]

# Excluded years
EXCLUDED_GOLDEN_GOAL = [1998, 2002]
EXCLUDED_NO_PENALTIES = list(range(1930, 1979, 4))  # 1930 through 1978

# Era groupings
ERA_GROUPS: dict[str, list[int]] = {
    "1982-1994": [1982, 1986, 1990, 1994],
    "2006-2022": [2006, 2010, 2014, 2018, 2022],
}

# Outcome types
OUTCOME_EXTRA_TIME = "extra_time"
OUTCOME_PENALTIES = "penalties"
OUTCOME_LABELS = {
    OUTCOME_EXTRA_TIME: "Decided in extra time",
    OUTCOME_PENALTIES: "Went to penalties",
}

# RSSSF URLs for each included World Cup
RSSSF_URLS: dict[int, str] = {
    1982: "https://www.rsssf.org/tables/82full.html",
    1986: "https://www.rsssf.org/tables/86full.html",
    1990: "https://www.rsssf.org/tables/90full.html",
    1994: "https://www.rsssf.org/tables/94full.html",
    2006: "https://www.rsssf.org/tables/2006f.html",
    2010: "https://www.rsssf.org/tables/2010f.html",
    2014: "https://www.rsssf.org/tables/2014full.html",
    2018: "https://www.rsssf.org/tables/2018full.html",
    2022: "https://www.rsssf.org/tables/2022f.html",
}

# Stages in order for display
STAGE_ORDER = [
    "Round of 16",
    "Quarter-final",
    "Semi-final",
    "Third place",
    "Final",
]
