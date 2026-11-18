# PeopleComfort | Threshold studio handoff

[Open the peer flipbook](https://hey-guobaorou.github.io/ARCH7476/week10-threshold/flipbook.html) · [Check the design totals](options.csv) · [Download the full threshold grid](epsilon.csv)

**Peer check.** Keep minimum gain at 20% and tolerance at 0.01. Change minimum coverage from 75% to exactly two thirds (displayed as 66.7%). Record the feasible designs, Pareto set and decision at both settings. Check D4 against its count of 54 in options.csv and the corresponding rows in epsilon.csv.

## The design decision

A reading-room planner must place twelve identical seats before knowing who will arrive. The reference layout D0 puts nine seats in the cooler zone Z1 and three in the warmer zone Z2. The proposed change D4 moves two seats into Z2, giving 7/5. Each zone can hold at most nine seats, so seven integer splits are possible. The question for the planner is whether the expected benefit of changing the layout holds up when the room, clothing or screening assumptions change.

The broader research topic is spatial planning under changing user composition, including population ageing. This prototype represents people through activity and clothing. Applying it to older readers would require local observations of activities, clothing, access needs and seat choice. The room and all user mixes here are constructed.

## What the model assumes

| Input | Nominal case | Why it matters |
|---|---|---|
| Thermal zones | Air temperature and mean radiant temperature are both 23.5 °C in Z1 and 27.5 °C in Z2. Relative humidity is 50% and air speed 0.1 m/s in both zones. | Two seats in different zones can produce different thermal exposure for the same reader. |
| Reader profiles | P1: 1.0 met / 0.5 clo. P2: 1.2 met / 0.5 clo. P3: 1.2 met / 0.8 clo. Met measures activity and clo measures clothing insulation. | P1 and P2 isolate an activity difference; P2 and P3 isolate a clothing difference. |
| Access and operation | All three profiles can use both zones. Once users arrive, the solver finds the feasible assignment with the lowest mean loss. Capacity and environment stay fixed during assignment. | Scores describe what managed seating can achieve. Actual seat choice requires observation. |
| User mixes | Develop on S0 = 8/2/2, S1 = 2/8/2 and S2 = 2/2/8, in P1/P2/P3 order. Evaluate the chosen split on ten additional mixes H0–H9. Six fall within the development envelope, three extend beyond it, and one has eight occupants. | Selection and evaluation have distinct roles. The ten holdouts are constructed stress cases. |

## How to read loss and regret

PMV estimates average thermal sensation for a stated environment, activity and clothing level. Zero is neutral. At the nominal screening limit of 0.5, each occupied seat contributes max(0, abs(PMV) − 0.5). For example P1 has PMV −0.951 in Z1 and +0.530 in Z2. Moving that reader reduces the exceedance from 0.451 to 0.030, although both seats still flag the reader. A layout's **loss** is the mean exceedance across the people present after allocation.

**Regret** measures the extra loss incurred by choosing a particular layout when another layout would have served the same mix better. Subtract the lowest loss among all seven layouts for that mix from the chosen layout's loss. In S0 the reference D0 scores 0.1953 and the best layout D6 scores 0.0199. D0 therefore has regret 0.1754. D6 has zero regret in S0 even though its loss is positive.

For each layout take its largest regret across S0–S2. The layout with the smallest such maximum is D4 (7/5). Freeze that choice. Across H0–H9 its maximum regret is 0.1403 against 0.2105 for D0, a 33.3% reduction using full precision. The comparison concerns the magnitude of modelled exposure; for the same allocations, flagged headcount is unchanged in six holdouts and increases in four.

## How the 81 test conditions are built

A **user mix** specifies who arrives. A **grid condition** specifies the environment, clothing adjustment and scoring boundary under which every layout and user mix is recalculated. The grid takes every combination of the following levels once. Each factor has a central value plus a lower and higher value to explore sensitivity around the nominal case. The ranges are exploratory project choices; no frequency distribution or instrument calibration was used.

| Factor | Three levels | Exact operation in one condition |
|---|---|---|
| Common temperature shift, t | −0.5, 0, +0.5 °C | Add t to both zones' air and radiant temperatures. Tests a cooler or warmer room overall. |
| Opposing zone shift, g | −0.5, 0, +0.5 °C | Subtract g in Z1 and add g in Z2. The warm-minus-cool contrast becomes 3, 4 or 5 °C respectively. |
| Common clothing shift, c | −0.1, 0, +0.1 clo | Add c to all three profiles' clothing values. Activity, humidity and air speed stay fixed. |
| PMV screening limit, tau | 0.4, 0.5, 0.6 | Apply max(0, abs(PMV) − tau). This changes how exposure is scored. |

For example, choose t = +0.5, g = +0.5, c = −0.1 and tau = 0.6. Z1 becomes 23.5 + 0.5 − 0.5 = 23.5 °C and Z2 becomes 27.5 + 0.5 + 0.5 = 28.5 °C. Clothing becomes 0.4, 0.4 and 0.7 clo. Compute PMV with those inputs, apply the 0.6 limit and solve the allocations again. Crossing the three levels of all four factors gives 3 × 3 × 3 × 3 = **81 conditions**, including the nominal condition.

## What one pass means, and why the line is at 61

1. Within one grid condition, calculate the seven layout losses in each holdout mix. Recompute the best loss separately in each mix under that same condition.
2. Subtract each mix's best loss to get regret. For each frozen layout, take its maximum regret across the ten holdouts. The worst mix may differ between layouts.
3. Count one pass if D4's maximum is at most D0's maximum **plus 0.01**. Here 0.01 is an absolute tolerance in regret units. Equality passes. A pass can include a small disadvantage for D4.
4. The action rule requires both a **20% reduction** under nominal inputs and passes in **at least 75%** of the grid. The first test compares 33.3% with 20%. The second requires the smallest whole count reaching 75% of 81: **61**. The observed count is **54**, seven short. The recommended action in this constructed case is to keep 9/3 pending site evidence.

These three settings have separate meanings: tau defines individual exposure, 0.01 defines an acceptable layout disadvantage, and 75% defines the required coverage. Grid coverage describes sensitivity to the selected levels. It does not estimate the chance of success in an actual building.

Bring A3_matrix.csv as the nominal design-by-mix output. The two drawing briefs below use the same setup.

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

## Course tool trial and reproduction

[Threshold Explorer](https://caadfutures2025.hku.hk/ARCH7476/site_tools/threshold-explorer.html): with default facade data, moving only the solar gain ceiling from 48 to 38.9 kept Hybrid first (88 vs 85). At 38, Deep fins led (85 vs 75). This was a separate classroom demonstration. The seating flipbook uses PeopleComfort values.

Open flipbook.html offline. For recalculation install matplotlib and Node.js, clone https://github.com/Hey-Guobaorou/peoplecomfort at e097a70664d19c0fbf78a2655350e94f48dc8126 and point r in draw.py at the checkout. Run python draw.py. Source numbers: A3_matrix.csv, options.csv and epsilon.csv. The public report is https://hey-guobaorou.github.io/ARCH7476/a3-peoplecomfort-research.html.
