PeopleComfort | Threshold brief (v0.2.0)

**Files:** `options.csv` · `epsilon.csv` · `A3_matrix.csv` · [flipbook](https://hey-guobaorou.github.io/ARCH7476/week10-threshold/flipbook.html)
Shared setup
------------

Twelve identical seats are split between a cooler zone Z1 (23.5 °C) and a warmer zone Z2 (27.5 °C). The current layout is D0 = 9/3. The planner must choose before knowing who arrives. Readers are described by activity and clothing only (P1 1.0 met/0.5 clo, P2 1.2/0.5, P3 1.2/0.8). All rooms and mixes are constructed.

**Loss** is the mean of max(0, |PMV| − 0.5) over people present. **Regret** is a layout's loss minus the lowest loss among the seven layouts for the same mix. Layouts are chosen by minimizing maximum regret on three development mixes (S0–S2), then frozen and tested on ten holdout mixes (H0–H9).

| Design | Z1/Z2   | Max regret, H0–H9 | Gain vs D0 |
| ------ | ------- | ----------------- | ---------- |
| D0     | 9/3     | 0.2105            | reference  |
| D3     | 8/4     | 0.1754            | 16.7%      |
| **D4** | **7/5** | **0.1403**        | **33.3%**  |
| D1     | 6/6     | 0.1432            | 32.0%      |
| D5     | 5/7     | 0.1910            | 9.3%       |
| D6     | 4/8     | 0.2387            | −13.4%     |
| D2     | 3/9     | 0.2864            | −36.1%     |

**The 81 grid conditions** = common temperature shift (−0.5/0/+0.5 °C) × opposing zone shift (−0.5/0/+0.5 °C) × clothing shift (−0.1/0/+0.1 clo) × screening limit tau (0.4/0.5/0.6). They are equal-weighted sensitivity points, not probabilities.

**One pass:** in one condition, D4's max holdout regret ≤ D0's + 0.01 (equality passes).

**Action rule:** change layout only if gain ≥ 20% **and** passes ≥ 75% of 81 conditions, i.e. ≥ **61**. D4 has gain 33.3% and **54** passes (66.7%, 7 short), so **keep 9/3**.

**Where the thresholds come from:** tau = 0.5 and the PMV model are borrowed (ASHRAE/CBE). The 20%, 0.01 and 75% cutoffs are my own judgments, set during revision and **not preregistered**. No literature calibrates them.

* * *

Brief 1 | Should two seats move?
--------------------------------

| Field         | Content                                                                                                                                                                                                                                   |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Decision**  | Move the 9/3 reference to 7/5, or keep it?                                                                                                                                                                                                |
| **Data**      | D4 passes **54** of 81 conditions. Required: **61**.                                                                                                                                                                                      |
| **Threshold** | 61 = ceil(0.75 × 81). Source: my judgment (post hoc). It flips if the requirement drops to 2/3 (54/81).                                                                                                                                   |
| **Audience**  | Reading-room planner, 30 seconds                                                                                                                                                                                                          |
| **Must show** | One horizontal bar on a 0–81 axis, D4 (7/5) labelled directly at 54, the threshold line at 61 with the passing side marked, a visible gap between them, no legend. Title: "Keep 9/3: the 7/5 candidate falls short of the coverage gate." |

_Caption:_ 33.3% gain clears 20%; 54/81 misses 75%, so retain D0.  
_Do not confuse_ 54 (pass count) with 23 (the number of conditions where D4 is the single best layout).  
_Caveats:_ the 33.3% is driven by two P1-heavy extremes (H6, H8); D4 is worse than D0 in 4 of 10 holdouts. Raising tolerance to 0.02 still gives 54/81.  
_Hand sketch:_ one dark bar and one coloured line.
Brief 2 | When does the Pareto set change?
------------------------------------------

| Field         | Content                                                                                                                                                                                |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Decision**  | At what coverage requirement does D4 stop being recommended?                                                                                                                           |
| **Data**      | Gain floor 20% and tolerance 0.01 fixed. Coverage settings: 50%, 66.7% (= 54/81), 70%, 75%, 100%. Surviving Pareto sets: {D4}, {D4}, ∅, ∅, ∅.                                          |
| **Threshold** | Boundary at exactly 2/3, equality passes. Source: my judgment (post hoc). At 70% the requirement is 57, three more than 54.                                                            |
| **Audience**  | Method reviewer                                                                                                                                                                        |
| **Must show** | A strip chart with the five settings, the surviving set labelled at each, and the boundary at 2/3. Title: "7/5 survives through 54 of 81; any higher coverage requirement removes it." |

_Notes:_ at 50%, D1 (51/81) and D4 are both feasible, but D4 dominates D1. An empty set falls back to D0. Pareto axes: lower development regret, higher holdout gain, higher coverage.

* * *

**Peer check (flipbook):** keep gain 20% and tolerance 0.01, switch coverage from 75% to 66.7%, and record the feasible set, Pareto set and decision at both settings. 
