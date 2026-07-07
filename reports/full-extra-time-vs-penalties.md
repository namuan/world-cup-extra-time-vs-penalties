# Men's FIFA World Cup: full extra time vs penalty shootouts

## Short answer

Of the **46** knockout matches in men's World Cups that reached extra time between 1982–1994 and 2006–2022, **16** (34.8%) were decided in extra time while **30** (65.2%) went to penalties.

In other words, nearly two-thirds of all extra-time knockout matches ended in a penalty shootout rather than being settled during the additional 30 minutes.

## Scope and exclusions

**Included tournaments:**

- 1982, 1986, 1990, 1994 (pre-golden-goal era with penalties)
- 2006, 2010, 2014, 2018, 2022 (post-golden-goal era with penalties)

**Excluded:**

- 1930 to 1978 — no penalty shootout system
- 1998 and 2002 — golden goal was active
- Qualification matches
- Group-stage matches

## Data sources

Match results were sourced from the Rec.Sport.Soccer Statistics Foundation (RSSSF) for each tournament:

- [1982](https://www.rsssf.org/tables/82full.html)
- [1986](https://www.rsssf.org/tables/86full.html)
- [1990](https://www.rsssf.org/tables/90full.html)
- [1994](https://www.rsssf.org/tables/94full.html)
- [2006](https://www.rsssf.org/tables/2006f.html)
- [2010](https://www.rsssf.org/tables/2010f.html)
- [2014](https://www.rsssf.org/tables/2014full.html)
- [2018](https://www.rsssf.org/tables/2018full.html)
- [2022](https://www.rsssf.org/tables/2022f.html)

Key matches were cross-checked against individual Wikipedia tournament pages for verification.

## Methodology

1. **Identify candidate matches:** All knockout-stage matches in the included tournaments were reviewed.
2. **Filter for extra time:** Only matches that were tied after 90 minutes (regulation) were retained.
3. **Classify outcome:** Each match was classified as either `extra_time` (a goal was scored during the 30-minute extra time period) or `penalties` (the match remained tied after extra time and proceeded to a penalty shootout).
4. **Validate:** Data was cross-checked against Wikipedia and all rows were programmatically validated (see `tests/test_dataset.py`).

## Overall results

| Outcome               |  Count | Percentage |
| --------------------- | -----: | :--------: |
| Decided in extra time |     16 |   34.8%    |
| Went to penalties     |     30 |   65.2%    |
| **Total**             | **46** |  **100%**  |

## Results by era

| era       | Total | ET-decided | Penalties | %-ET | %-Pens |
| :-------- | ----: | ---------: | --------: | ---: | -----: |
| 1982-1994 |    18 |          7 |        11 | 38.9 |   61.1 |
| 2006-2022 |    28 |          9 |        19 | 32.1 |   67.9 |

## Results by tournament

| year | Total | ET-decided | Penalties | %-ET | %-Pens |
| ---: | ----: | ---------: | --------: | ---: | -----: |
| 1982 |     1 |          0 |         1 |    0 |    100 |
| 1986 |     5 |          2 |         3 |   40 |     60 |
| 1990 |     8 |          4 |         4 |   50 |     50 |
| 1994 |     4 |          1 |         3 |   25 |     75 |
| 2006 |     6 |          2 |         4 | 33.3 |   66.7 |
| 2010 |     4 |          2 |         2 |   50 |     50 |
| 2014 |     8 |          4 |         4 |   50 |     50 |
| 2018 |     5 |          1 |         4 |   20 |     80 |
| 2022 |     5 |          0 |         5 |    0 |    100 |

## Results by stage

| stage         | Total | ET-decided | Penalties | %-ET | %-Pens |
| :------------ | ----: | ---------: | --------: | ---: | -----: |
| Round of 16   |    21 |         10 |        11 | 47.6 |   52.4 |
| Quarter-final |    13 |          1 |        12 |  7.7 |   92.3 |
| Semi-final    |     6 |          2 |         4 | 33.3 |   66.7 |
| Third place   |     1 |          1 |         0 |  100 |      0 |
| Final         |     5 |          2 |         3 |   40 |     60 |

## Match-level appendix

| Year | Stage         | Home                | Away        | 90'H | 90'A | AET H | AET A | Pens H | Pens A | Outcome    | Winner              |
| ---: | :------------ | :------------------ | :---------- | ---: | ---: | ----: | ----: | -----: | -----: | :--------- | :------------------ |
| 1982 | Semi-final    | West Germany        | France      |    3 |    3 |     3 |     3 |      5 |      4 | penalties  | West Germany        |
| 1986 | Round of 16   | Soviet Union        | Belgium     |    2 |    2 |     3 |     4 |    nan |    nan | extra_time | Belgium             |
| 1986 | Quarter-final | Brazil              | France      |    1 |    1 |     1 |     1 |      3 |      4 | penalties  | France              |
| 1986 | Quarter-final | West Germany        | Mexico      |    0 |    0 |     0 |     0 |      4 |      1 | penalties  | West Germany        |
| 1986 | Quarter-final | Spain               | Belgium     |    1 |    1 |     1 |     1 |      4 |      5 | penalties  | Belgium             |
| 1986 | Third place   | France              | Belgium     |    2 |    2 |     4 |     2 |    nan |    nan | extra_time | France              |
| 1990 | Round of 16   | Cameroon            | Colombia    |    0 |    0 |     2 |     1 |    nan |    nan | extra_time | Cameroon            |
| 1990 | Round of 16   | Spain               | Yugoslavia  |    1 |    1 |     1 |     2 |    nan |    nan | extra_time | Yugoslavia          |
| 1990 | Round of 16   | England             | Belgium     |    0 |    0 |     1 |     0 |    nan |    nan | extra_time | England             |
| 1990 | Round of 16   | Republic of Ireland | Romania     |    0 |    0 |     0 |     0 |      5 |      4 | penalties  | Republic of Ireland |
| 1990 | Quarter-final | Argentina           | Yugoslavia  |    0 |    0 |     0 |     0 |      3 |      2 | penalties  | Argentina           |
| 1990 | Quarter-final | England             | Cameroon    |    2 |    2 |     3 |     2 |    nan |    nan | extra_time | England             |
| 1990 | Semi-final    | Italy               | Argentina   |    1 |    1 |     1 |     1 |      3 |      4 | penalties  | Argentina           |
| 1990 | Semi-final    | West Germany        | England     |    1 |    1 |     1 |     1 |      4 |      3 | penalties  | West Germany        |
| 1994 | Round of 16   | Nigeria             | Italy       |    1 |    1 |     1 |     2 |    nan |    nan | extra_time | Italy               |
| 1994 | Round of 16   | Mexico              | Bulgaria    |    1 |    1 |     1 |     1 |      1 |      3 | penalties  | Bulgaria            |
| 1994 | Quarter-final | Romania             | Sweden      |    2 |    2 |     2 |     2 |      4 |      5 | penalties  | Sweden              |
| 1994 | Final         | Brazil              | Italy       |    0 |    0 |     0 |     0 |      3 |      2 | penalties  | Brazil              |
| 2006 | Round of 16   | Argentina           | Mexico      |    1 |    1 |     2 |     1 |    nan |    nan | extra_time | Argentina           |
| 2006 | Round of 16   | Switzerland         | Ukraine     |    0 |    0 |     0 |     0 |      0 |      3 | penalties  | Ukraine             |
| 2006 | Quarter-final | Germany             | Argentina   |    1 |    1 |     1 |     1 |      4 |      2 | penalties  | Germany             |
| 2006 | Quarter-final | England             | Portugal    |    0 |    0 |     0 |     0 |      1 |      3 | penalties  | Portugal            |
| 2006 | Semi-final    | Germany             | Italy       |    0 |    0 |     0 |     2 |    nan |    nan | extra_time | Italy               |
| 2006 | Final         | Italy               | France      |    1 |    1 |     1 |     1 |      5 |      3 | penalties  | Italy               |
| 2010 | Round of 16   | USA                 | Ghana       |    1 |    1 |     1 |     2 |    nan |    nan | extra_time | Ghana               |
| 2010 | Round of 16   | Paraguay            | Japan       |    0 |    0 |     0 |     0 |      5 |      3 | penalties  | Paraguay            |
| 2010 | Quarter-final | Uruguay             | Ghana       |    1 |    1 |     1 |     1 |      4 |      2 | penalties  | Uruguay             |
| 2010 | Final         | Spain               | Netherlands |    0 |    0 |     1 |     0 |    nan |    nan | extra_time | Spain               |
| 2014 | Round of 16   | Brazil              | Chile       |    1 |    1 |     1 |     1 |      3 |      2 | penalties  | Brazil              |
| 2014 | Round of 16   | Germany             | Algeria     |    0 |    0 |     2 |     1 |    nan |    nan | extra_time | Germany             |
| 2014 | Round of 16   | Argentina           | Switzerland |    0 |    0 |     1 |     0 |    nan |    nan | extra_time | Argentina           |
| 2014 | Round of 16   | Belgium             | USA         |    0 |    0 |     2 |     1 |    nan |    nan | extra_time | Belgium             |
| 2014 | Round of 16   | Costa Rica          | Greece      |    1 |    1 |     1 |     1 |      5 |      3 | penalties  | Costa Rica          |
| 2014 | Quarter-final | Netherlands         | Costa Rica  |    0 |    0 |     0 |     0 |      4 |      3 | penalties  | Netherlands         |
| 2014 | Semi-final    | Argentina           | Netherlands |    0 |    0 |     0 |     0 |      4 |      2 | penalties  | Argentina           |
| 2014 | Final         | Germany             | Argentina   |    0 |    0 |     1 |     0 |    nan |    nan | extra_time | Germany             |
| 2018 | Round of 16   | Russia              | Spain       |    1 |    1 |     1 |     1 |      4 |      3 | penalties  | Russia              |
| 2018 | Round of 16   | Croatia             | Denmark     |    1 |    1 |     1 |     1 |      3 |      2 | penalties  | Croatia             |
| 2018 | Round of 16   | Colombia            | England     |    1 |    1 |     1 |     1 |      3 |      4 | penalties  | England             |
| 2018 | Quarter-final | Russia              | Croatia     |    2 |    2 |     2 |     2 |      3 |      4 | penalties  | Croatia             |
| 2018 | Semi-final    | Croatia             | England     |    1 |    1 |     2 |     1 |    nan |    nan | extra_time | Croatia             |
| 2022 | Round of 16   | Japan               | Croatia     |    1 |    1 |     1 |     1 |      1 |      3 | penalties  | Croatia             |
| 2022 | Round of 16   | Morocco             | Spain       |    0 |    0 |     0 |     0 |      3 |      0 | penalties  | Morocco             |
| 2022 | Quarter-final | Croatia             | Brazil      |    1 |    1 |     1 |     1 |      4 |      2 | penalties  | Croatia             |
| 2022 | Quarter-final | Netherlands         | Argentina   |    2 |    2 |     2 |     2 |      3 |      4 | penalties  | Argentina           |
| 2022 | Final         | Argentina           | France      |    3 |    3 |     3 |     3 |      4 |      2 | penalties  | Argentina           |

## Limitations

- **Manual curation:** The dataset was compiled manually from RSSSF pages; some encoding issues exist for older tournaments (1982–1994).
- **Third-place matches:** One third-place match (1986, France vs Belgium) reached extra time and is included in the dataset.
- **Cross-check:** A full cross-check against FIFA's own records has not yet been completed.
- **Small sample:** With 46 matches spread across 9 tournaments, per-tournament and per-stage breakdowns should be interpreted cautiously.
