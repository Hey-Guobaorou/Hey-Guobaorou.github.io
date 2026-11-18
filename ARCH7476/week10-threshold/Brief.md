# PeopleComfort A3 | Full peer reproduction brief

## Purpose and experimental design

A planner must place twelve seats across a cooler zone Z1 and warmer zone Z2 before knowing who will arrive. The reference D0 has 9/3 seats. D0-D6 cover all seven feasible integer splits with at most nine seats per zone. The hypothetical reading room has Z1 air and radiant temperatures of 23.5 °C and Z2 values of 27.5 °C. Both zones have 50% humidity and 0.1 m/s air speed. P1 is 1.0 met/0.5 clo, P2 is 1.2 met/0.5 clo, and P3 is 1.2 met/0.8 clo. All can enter both zones. The program finds the lowest-loss feasible assignment after the user mix is known.

S0=8/2/2, S1=2/8/2 and S2=2/2/8 are development mixes in P1/P2/P3 order. They select the layout. H0-H9 are ten additional constructed mixes for examining that frozen selection. H9 has only eight occupants. For each person, exceedance is `max(0, abs(PMV) - 0.5)`. A design's loss is mean exceedance across occupants. For any one mix, regret is that design's loss minus the lowest loss among all seven designs in the same mix. In S0, D0 loss 0.1953 minus D6 loss 0.0199 gives D0 regret 0.1754. D4 (7/5) minimizes the largest regret across S0-S2 at 0.1052, compared with D1 at 0.1139.

Freeze D4, then compare H0-H9 maximum regrets. D0 scores 0.2104749 and D4 0.1403166. Their relative reduction is 33.3333%, exceeding the exploratory 20% minimum. The 81-condition grid combines three values of each of four factors. Common air and radiant temperature offset `t` is −0.5/0/+0.5 °C in both zones. Opposing offset `g` is −0.5/0/+0.5 °C, subtracted in Z1 and added in Z2. Clothing offset `c` is −0.1/0/+0.1 clo for all profiles. The PMV screening boundary is 0.4/0.5/0.6. S, H and D counts remain fixed. PMV, allocation, loss and regret are recalculated in every condition.

One condition passes if fixed D4's maximum H0-H9 regret is at most fixed D0's maximum plus 0.01. At least 75% of 81 conditions, or 61, must pass. Only 54 pass. The action in this constructed case is to retain 9/3 pending site evidence. The 20%, 0.01 and 75% are exploratory project judgments, and 54/81 is grid coverage rather than a real-world probability.

## Software and source version

Use Windows PowerShell, Git, Python 3.11+ and Node.js 18+. The original run used Python 3.12.12 and Node v24.11.1. The A3 input and calculation were frozen at commit `e097a70664d19c0fbf78a2655350e94f48dc8126` (`a3-submission`). The revised report source is at commit `20f6d1c24a586200f8b2c129035a60992ac0f43c`. Both have the same A3 input. Use the revised commit below for report reproduction. CBE source is bundled at commit `e809c965dd6eb2e785bf4851de2149c7a1d3c299`.

### 1. Check your tools

```powershell
Get-Command git, python, node | Select-Object Name, Source
git --version
python --version
node --version
```

If any command fails, install that tool before proceeding. Use the same Python executable for every later step.

### 2. Clone and create a clean Python environment

```powershell
$reviewRoot = Join-Path $env:USERPROFILE 'Documents\PeopleComfort_A3_peer_review'
New-Item -ItemType Directory -Force -Path $reviewRoot | Out-Null
Set-Location $reviewRoot
git clone https://github.com/Hey-Guobaorou/peoplecomfort.git
Set-Location (Join-Path $reviewRoot 'peoplecomfort')
git checkout 20f6d1c24a586200f8b2c129035a60992ac0f43c
git rev-parse HEAD
git rev-parse 'a3-submission^{commit}'
python -m venv .venv
$python = Join-Path (Get-Location) '.venv\Scripts\python.exe'
& $python -m pip install --upgrade pip
& $python -m pip install -e .
& $python -m pip install numpy matplotlib reportlab pillow
```

The two `git rev-parse` commands should print the revised and frozen commits listed above. The package has no third-party Python dependency for its core calculation. Plotting and PDF generation require the packages installed in the last line. Node runs the bundled CBE thermal calculator.

### 3. Rerun the A3 analysis

Run these from the `peoplecomfort` repository root:

```powershell
& $python verification/smoke_check.py
& $python -m unittest discover -s tests -v
& $python coursework/analyze_extended.py
& $python run.py analyze --project examples/extended-a3/project.json --out rerun-extended
```

The smoke check must print `PASS`, input hash `bc361fcd1a90f8c77f7e780289ab56f989b883e550ba6968464d771aa18f5210`, `cells=91`, and `winner=D4`. Tests end with `OK`. The analysis writes `coursework/extended_results.json`, `extended_matrix.csv`, and three `figure_extended_*.png` figures. The CLI writes the full output and run manifest to `rerun-extended`. The 91 nominal comparison rows equal seven designs times 13 mixes.

### 4. Independently inspect the numbers in PowerShell

```powershell
$summary = Get-Content coursework/extended_results.json -Raw | ConvertFrom-Json
$matrix = Import-Csv coursework/extended_matrix.csv
$summary.development_winner
$summary.baseline_winner
$summary.development_max_regret.D4
$summary.holdout_max_regret.D0
$summary.holdout_max_regret.D4
$summary.relative_improvement_vs_existing
$summary.stress_noninferiority_count
$summary.stress_total
$summary.action_rule_passed
$matrix.Count
$matrix | Where-Object { $_.scenario -eq 'S0' -and $_.design -in @('D0','D6') } | Format-Table scenario,design,loss,regret
```

Expect D4, D6, 0.1052374, 0.2104749, 0.1403166, 0.3333333, 54, 81, False, and 91 in that order. The S0 rows support the manual subtraction 0.1953 − 0.0199 = 0.1754. Use unrounded values in the JSON for percentages.

```powershell
$project = Get-Content examples/extended-a3/project.json -Raw | ConvertFrom-Json
$project.uncertainty | Format-List
$project.design_action_rule | Format-List
[math]::Ceiling($summary.stress_total * $project.design_action_rule.stress_noninferiority_fraction)
$summary.stress_noninferiority_count / $summary.stress_total
```

The last two lines should return 61 and approximately 0.6667. Inspect the four lists under `uncertainty` and three action thresholds in `design_action_rule`. For a complete row-level audit of all 81 conditions, use the programmatic `analyze(project, True)` result. Each `uncertainty` record gives the four offsets, world-specific development winners and `holdout_regret_by_design` for all seven layouts. The 81 values are recalculated, not averaged into one regret.

### 5. Check an independent PMV implementation and rebuild the PDF

```powershell
& $python -m pip install -r verification/requirements.txt
& $python verification/independent_pmv_check.py
& $python coursework/build_pdf.py
```

The independent check uses `pythermalcomfort==4.8.1` for six nominal profile-zone cases. Expect maximum absolute PMV difference near 0.001497 and PPD difference near 0.0458 percentage points. It writes `verification/independent_pmv_comparison.json`. PDF generation writes `coursework/A3_research_report.pdf`. Chart or pagination bytes may vary with library versions, so inspect numerical labels and tables rather than expecting identical file hashes.

### 6. Check the public tool interactively

Open [PeopleComfort](https://hey-guobaorou.github.io/ARCH7476/peoplecomfort.html) and choose **Reset example**. Confirm 2 zones, 3 profiles, 7 designs and 13 scenarios. Under **Decision comparison**, expect D4 and holdout maximum regret 0.1403. In the thermal ledger expect P1/Z1 PMV near −0.951. Change only Z1 air temperature `ta` from 23.5 to 25, press Tab, and wait for **PMV and results updated**. Expect P1/Z1 near −0.664, selected D3 and holdout maximum regret near 0.0560. Reset and confirm D4 returns. Record the input values beside any result you report.

### 7. Rebuild and use the peer threshold flipbook

The [public flipbook](https://hey-guobaorou.github.io/ARCH7476/week10-threshold/flipbook.html) contains the threshold sweep. Rebuild its files from the A3 engine using the separate site repository and the `draw.py` script supplied with this brief:

```powershell
Set-Location $reviewRoot
git clone https://github.com/Hey-Guobaorou/Hey-Guobaorou.github.io.git
$peerDir = Join-Path $reviewRoot 'Hey-Guobaorou.github.io\ARCH7476\week10-threshold'
$env:PEOPLECOMFORT_REPO = Join-Path $reviewRoot 'peoplecomfort'
& $python (Join-Path $peerDir 'draw.py')
& $python (Join-Path $peerDir 'draw_coverage.py')
Start-Process (Join-Path $peerDir 'flipbook.html')
```

`draw.py` regenerates `options.csv`, `epsilon.csv`, `temperature_check.csv`, `threshold.png` and `flipbook.html`. `draw_coverage.py` writes `coverage_strip.png` and `.svg`. Keep Minimum gain at 20% and Allowed excess regret at 0.01. At 75% coverage there is no eligible alternative and the action is Keep D0. At exactly two thirds, D4 is eligible and on the Pareto front. At 50%, D1 and D4 are eligible but D4 dominates D1. The flipbook reuses the A3 holdout outcomes for a retrospective classroom exercise, so its Pareto selection is exploratory.

## Reviewer record

| Item | Peer observation |
|---|---|
| Reviewer, date, Python, Node and Git versions | |
| Checkout commit and A3 input hash | |
| Smoke check and unit-test outcomes | |
| Manual S0 D0 regret | |
| D4 development score and D0/D4 holdout maxima | |
| Nominal gain, stress pass count and required count | |
| First confusing instruction or exact error message | |
| Accepted, revised, rejected or pending claim | |
| One improvement needed for independent rerun | |

The constructed room, user mixes and action gates test a method. A real layout decision requires local thermal, occupancy, access and actual seat-choice evidence.

## Brief 1 | Should two seats move?

**Reader and action.** A reading-room planner has 30 seconds to decide whether the 9/3 reference should move to 7/5 under the stated rule. Title the chart “Keep 9/3: the 7/5 candidate falls short of the coverage gate.” Draw one horizontal bar on a 0-81 count axis. Label D4 (7/5) directly at 54. Draw the threshold line at 61 and identify the side that passes. Keep enough space between the endpoint and line for their difference to be visible. Use no legend. A qualifying world satisfies D4 maximum holdout regret ≤ D0 maximum holdout regret + 0.01. Caption: 33.3% nominal improvement clears 20%; 54/81 misses 75%, so retain D0. These are grid counts. Uncertainty includes clothing, two temperature shifts and screening band. A hand sketch needs only a dark bar and one coloured line.

**Round 2 prompt used for the code drawing.** Draw one decision figure for an architecture audience using only Brief 1. Put the threshold inside the plot, label options directly, use the takeaway as title, and request missing numbers rather than inventing them. Return Python/matplotlib code. Source and executed output: draw.py and threshold.png. Known-case check: ceil(0.75 × 81) = 61; 54 < 61. For a data redraw use the D4 row in options.csv.

## Brief 2 | When does the Pareto set change?

**Reader and action.** A method reviewer should find the first coverage requirement that excludes D4. Hold the improvement floor at 20% and allowed excess regret at 0.01. On a strip chart place coverage requirements at 50%, exactly two thirds, 70%, 75% and 100%. Directly label the surviving Pareto set at each setting. The sets are {D4}, {D4}, empty, empty and empty. Draw the boundary at exactly two thirds, with equality on the passing side. Title: “7/5 survives through 54 of 81; any higher coverage requirement removes it.” D1 reaches 51/81. Both D1 and D4 are feasible at 50%, but D4 dominates D1. Use flipbook.html for the reverse-ring exercise and change each of the other two controls separately. The tables list all survivors, the nondominated subset and the action. An empty set returns the reference layout as a fallback.

## Why these objectives and constraints?

Choose the layout on S0-S2 by minimizing maximum regret: this limits the cost of a poor choice when user-mix probabilities are unknown. Equal total seats, zone maxima, access and complete assignment are hard physical constraints. In A3 the chosen layout is frozen before H0-H9 evaluation. Improvement over D0 on H0-H9 is a minimum benefit required to justify change. Excess regret tolerance bounds the disadvantage allowed in a perturbed world; coverage sets the minimum fraction of worlds meeting that bound. They answer separate planner questions, so one large benefit cannot cancel failure of the other gate.

For the **new retrospective Pareto exercise**, compare all seven on (lower development regret, higher holdout gain, higher coverage at the selected tolerance). Remove a feasible design only if another is at least as good on all three and strictly better on one. Feasibility includes equality. Pick the feasible minimum development regret. This exploratory reuse of the holdouts illustrates rule sensitivity; it cannot independently validate a newly selected layout. The flipbook contains 125 combinations. D0 is a reference even when a positive benefit floor excludes it from the feasible set.

## Continuous change, category crossing and provenance

The [ASHRAE addendum](https://www.ashrae.org/file%20library/technical%20resources/standards%20and%20guidelines/standards%20addenda/55_2020_h_20221230.pdf) presents a continuous PMV–PPD curve; the [CBE tool](https://comfort.cbe.berkeley.edu/) displays a comfort zone bounded by PMV ±0.5. Borrowed: thermal model and screening convention. Project choice: quantify severity with max(0, abs(PMV) - 0.5) and flag only abs(PMV) > 0.5. The severity changes continuously with PMV; the flag changes category only at the boundary. Moving P1 from −0.951 to +0.530 reduces severity from 0.451 to 0.030 while both placements remain flagged. PPD itself varies smoothly and rises toward either thermal extreme.

Borrowed method: [Mavrotas (2009)](https://doi.org/10.1016/j.amc.2009.03.037) formalizes optimizing one criterion while bounding others. Our seven-design enumeration applies that principle directly. Our contributions are the seat-allocation comparison, choice of severity and regret metrics, exploratory action rule and this threshold sweep. The 20% benefit floor, 0.01 disadvantage allowance and 75% coverage requirement are project judgments. The literature supports distinguishing model response from classification; it supplies no empirical calibration of these three action cutoffs.

## Robustness and limits

The frozen 81 conditions form a balanced factorial grid. Keeping D4, D0 and the tolerance fixed, condition on the common air/radiant temperature offset: at −0.5 °C, 27/27 pass; at 0 °C, 18/27 pass; at +0.5 °C, 9/27 pass. The other three dimensions span the same 27 combinations within each group. The 75% coverage criterion passes only in the coolest group. See temperature_check.csv. Equal weighting is a modelling choice.

Weather-year, hourly and solar-angle robustness remains untested. The input contains two static indoor environments and no site, dated weather series, occupied-hour schedule, facade geometry or solar-to-indoor radiant model. To run that comparison: fix a site, geometry, HVAC and occupancy schedule; derive hourly Z1/Z2 air and radiant temperatures for each weather year; compare identical occupied windows at full hourly resolution and systematically thinned time steps with different start phases. If direct solar exposure matters, refine sun-position sampling and recompute radiant temperature. For each sampling plan freeze designs and rules, rebuild losses, then report Pareto membership and gate crossings. Record which year or schedule first changes the action. The temperature slices above are sensitivity evidence only.

