# 2. Problem Statement, Proposed Solution, and Requirements

## Problem statement

Water-conservation planning requires comparing areas with different
rainfall patterns, terrain, land cover, runoff behaviour, and local
physical conditions. These data often come from separate sources, time
periods, resolutions, and spatial units. Without a consistent and
documented workflow, rankings can be difficult to reproduce, explain, or
update.

**Problem statement:** Develop a transparent and reproducible GIS-based
decision-support workflow that consolidates rainfall, land-cover,
terrain, and watershed attributes into comparable indicators, enabling
planners to screen and prioritise watersheds for further
water-conservation investigation while documenting uncertainty and the
need for technical and field validation.

This is a screening and decision-support problem. It is not a claim that
data alone can select a final construction site.

## Practical problems being addressed

1.  Averages can hide rainfall variability and dry years.
2.  Land cover can influence hydrological processes, but satellite
    classes are imperfect proxies.
3.  Slope affects flow and erosion but cannot alone establish structure
    feasibility.
4.  Data sources differ in resolution, coverage, units, and geographic
    boundaries.
5.  Rankings can look authoritative despite weak weights or missing
    validation.
6.  A map can hide data gaps, uncertainty, and scale effects.

## Proposed solution

1.  Acquire and document data sources.
2.  Clean and standardise source tables and geospatial layers.
3.  Calculate indicators at appropriate spatial and temporal units.
4.  assess missingness, coverage, duplicates, outliers, and source
    flags.
5.  integrate layers using defensible spatial operations.
6.  define explicit indicator directions, normalisation, weights, and
    missing-data rules.
7.  create a score table that retains raw indicators and score
    contributions.
8.  export GIS layers and maps with clear legends and caveats.
9.  validate rankings with independent evidence, experts, and field
    checks.
10. version assumptions and outputs so the workflow can be repeated.

## Objectives

-   Create a traceable data foundation.
-   Characterise rainfall averages and variability.
-   Summarise land-cover composition and coverage.
-   Prepare basin-level attributes for analysis.
-   Test a transparent screening score.
-   Export spatial results for GIS inspection.
-   Establish a defensible route toward MCDA and validation.

## Functional requirements

The eventual pipeline should load documented sources, validate schemas
and identifiers, calculate indicators, retain review flags, spatially
integrate data only where justified, normalise values, check weights,
preserve score components, export tables and GIS files, and report
data-quality issues.

## Non-functional requirements

-   **Reproducibility:** rerun from a clean kernel.
-   **Traceability:** source, date, unit, formula, and transformation
    for each field.
-   **Explainability:** rankings can be decomposed into contributions.
-   **Spatial correctness:** district and basin units are not treated as
    equivalent.
-   **Data integrity:** preserve raw values and quality flags.
-   **Portability:** configure paths once rather than hard-coding them
    in every cell.
-   **Conservative interpretation:** screening is not engineering
    approval.

## Success criteria

For the prototype: data preparation is repeatable; schemas and units are
understood; joins are defensible; score logic is transparent; and GIS
exports can be inspected.

For a validated version: add documented sensitivity analysis,
independent comparison, expert review, field verification, and evidence
that the ranking helps the intended decision. Do not invent performance
targets before they are defined and measured.

## Out of scope unless implemented separately

Guaranteed groundwater recharge, guaranteed water savings, final
structure design, construction approval, parcel-level legal clearance, a
trained predictive AI model, and a live production app are not
established as completed.
