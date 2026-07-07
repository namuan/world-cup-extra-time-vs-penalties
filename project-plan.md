# End-to-end implementation plan

## Research question

In men's FIFA World Cups where teams played full extra time and penalty shootouts
were available, excluding the golden-goal World Cups (**1998** and **2002**):

1. How many knockout matches that reached extra time were decided during extra
   time?
2. How many were still tied after extra time and went to penalty kicks?

## Scope

**Included tournaments**

| Era                             | Years                        |
| ------------------------------- | ---------------------------- |
| Pre-golden-goal with penalties  | 1982, 1986, 1990, 1994       |
| Post-golden-goal with penalties | 2006, 2010, 2014, 2018, 2022 |

**Excluded**

- 1930 to 1978 — no penalty shootout system.
- 1998 and 2002 — golden goal was active.
- Qualification matches.
- Group-stage matches.

## Project structure

```text
world-cup-penalties/
├── data/
│   ├── raw/                    # Downloaded RSSSF HTML pages
│   │   ├── rsssf/
│   │   │   ├── world_cup_1982.html
│   │   │   ├── world_cup_1986.html
│   │   │   ├── world_cup_1990.html
│   │   │   ├── world_cup_1994.html
│   │   │   ├── world_cup_2006.html
│   │   │   ├── world_cup_2010.html
│   │   │   ├── world_cup_2014.html
│   │   │   ├── world_cup_2018.html
│   │   │   └── world_cup_2022.html
│   │   └── source_inventory.csv
│   ├── interim/                # Intermediate cleaned tables (optional)
│   └── processed/
│       └── extra_time_matches.csv  # Curated analysis dataset
├── notebooks/                  # Exploratory notebooks (optional)
├── reports/
│   └── full-extra-time-vs-penalties.md  # Final report output
├── src/world_cup_penalties/
│   ├── __init__.py
│   ├── config.py               # Constants: included years, paths
│   ├── collect.py              # Download RSSSF pages + write inventory
│   ├── clean.py                # Placeholder (manual curation used)
│   ├── classify.py             # Outcome classification logic
│   ├── analyze.py              # Counts, percentages, summary tables
│   └── report.py               # Generate final markdown report
├── tests/
│   └── test_classify.py        # Unit tests for classification
├── pyproject.toml
├── README.md
└── project-plan.md             # This file
```

---

## STATUS: What is done and what remains

| #   | Phase                      | Status | Output                                                  |
| --- | -------------------------- | ------ | ------------------------------------------------------- |
| 1   | Project setup              | Done   | `pyproject.toml`, `uv.lock`, directories                |
| 2   | Data collection            | Done   | 9 RSSSF HTML files + `source_inventory.csv`             |
| 3   | Data extraction & cleaning | Done   | Manual curation into `extra_time_matches.csv`           |
| 4   | Match filtering            | Done   | 46 rows, verified years, all tied at 90'                |
| 5   | Outcome classification     | Done   | `classify.py` + 3 unit tests passing                    |
| 6   | Validation                 | Done   | 18 dataset tests + 3 classify tests all passing         |
| 7   | Analysis                   | Done   | `analyze.py` with 4 breakdowns                          |
| 8   | Final report               | Done   | `report.py` → `reports/full-extra-time-vs-penalties.md` |

---

## Remaining work: step-by-step

### Step 1 — Implement analysis (`analyze.py`)

**What it does:** Reads the processed CSV and produces the tables/numbers
needed to answer the research question.

**Exact outputs:**

1. Overall count: total extra-time matches, count decided in extra time,
   count that went to penalties, with percentages.
2. Era split: same counts for 1982-1994 and 2006-2022 separately.
3. Per-tournament counts: a table with one row per year.
4. Per-stage counts: round of 16, quarter-final, semi-final, final, third-place.

**How to run it:**

```bash
uv run python -m world_cup_penalties.analyze
```

**What it prints to stdout:**

```text
=== Overall ===
Total extra-time matches: 46
Decided in extra time:   16  (34.8%)
Went to penalties:       30  (65.2%)

=== By era ===
                Total   ET-decided   Penalties   %-ET   %-Pens
1982-1994         18          7           11    38.9%   61.1%
2006-2022         28          9           19    32.1%   67.9%

=== By tournament ===
... (per-year table)

=== By stage ===
... (per-stage table)
```

**Implementation notes:**

- Read `data/processed/extra_time_matches.csv` with pandas.
- Group by `outcome_type` for overall counts.
- Add an `era` column: `1982-1994` or `2006-2022`.
- Group by `era` and `outcome_type`.
- Group by `year` and `outcome_type`.
- Group by `stage` and `outcome_type`.
- Print all tables to stdout.

---

### Step 2 — Add validation tests ✅ DONE

`tests/test_dataset.py` has 18 comprehensive tests covering:

- File presence and readability.
- Required columns.
- Year filters (no golden-goal years, no pre-penalty years, all in scope).
- Score consistency (all tied at 90').
- Outcome type validity and coverage.
- Penalty score integrity (present when needed, absent when not).
- Winner consistency with AET/penalty scores.
- Source columns filled.
- Known historical matches present with correct classification.
- No duplicate rows.

Run with:

```bash
uv run pytest   # 21 passed (3 classify + 18 dataset)
```

---

### Step 3 — Implement report generation (`report.py`)

**What it does:** Generates the final markdown research report at
`reports/full-extra-time-vs-penalties.md`.

**How to run it:**

```bash
uv run python -m world_cup_penalties.report
```

**Report structure (section by section):**

```markdown
# Men's FIFA World Cup: full extra time vs penalty shootouts

## Short answer

[Two-sentence summary of key numbers]

## Scope and exclusions

- Included: 1982-1994, 2006-2022
- Excluded: pre-1982 (no penalties), 1998 and 2002 (golden goal)
- Only men's World Cup knockout matches

## Data sources

- Primary: RSSSF (urls listed)
- Verification: Wikipedia tournament pages

## Methodology

[How matches were identified, classified, and validated]

## Overall results

| Outcome               | Count  | Percentage |
| --------------------- | ------ | ---------- |
| Decided in extra time | 16     | 34.8%      |
| Went to penalties     | 30     | 65.2%      |
| **Total**             | **46** | **100%**   |

## Results by era

[Table for 1982-1994 vs 2006-2022]

## Results by tournament

[Per-year table]

## Results by stage

[Per-stage table]

## Match-level appendix

[Full table of all 46 matches]

## Limitations

- Manual curation; cross-check against FIFA not yet complete
- RSSSF encoding issues for some older tournaments
- Third-place matches included
```

**Implementation notes:**

- Reuse analysis logic from `analyze.py` (import shared functions).
- Write the markdown file to `REPORTS_DIR / "full-extra-time-vs-penalties.md"`.
- Include the full match list as a markdown table.

---

### Step 3 — Run the full pipeline end-to-end

```bash
uv sync
uv run python -m world_cup_penalties.collect   # download RSSSF pages
uv run python -m world_cup_penalties.analyze    # print analysis to stdout
uv run python -m world_cup_penalties.report     # generate markdown report
uv run pytest                                   # all tests pass
uv run ruff check .                             # lint passes
```

---

### Step 4 — Cross-check against a second source (manual verification)

For each of the 46 matches, verify against Wikipedia tournament pages that:

- The score after 90 minutes is correct.
- The score after extra time is correct.
- The penalty score is correct.
- The outcome classification matches.

Mark any discrepancies in the `notes` column of the CSV.

---

## Reproducible commands

```bash
uv sync
uv run python -m world_cup_penalties.collect
uv run python -m world_cup_penalties.analyze
uv run python -m world_cup_penalties.report
uv run pytest
uv run ruff check .
```

After running these, the final report is at:

```text
reports/full-extra-time-vs-penalties.md
```
