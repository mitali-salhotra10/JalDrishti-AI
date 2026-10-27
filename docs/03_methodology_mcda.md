# 3. Methodology and MCDA

## End-to-end workflow

### 1. Define the decision question

Specify whether the goal is watershed prioritisation or suitability for
a named intervention. These are different analytical tasks.

### 2. Acquire and document data

Known source families: - CHIRPS rainfall for historical rainfall
analysis; - Dynamic World 2023 for land-cover summaries; - SRTM for
terrain; - WWF HydroATLAS Level 8 for basin identifiers and
hydro-environmental attributes.

The notebook should record exact asset IDs, versions, date ranges,
filters, reducers, scale, CRS, and export settings.

### 3. Clean and validate

Standardise field names and units; parse years; check duplicate IDs,
nulls, impossible values, geographic coverage, class coverage, and
quality flags. Never silently convert missing values to zero.

### 4. Engineer indicators

Known indicators include rainfall mean, annual variability, monsoon mean
and variability, wettest/driest years, land-cover percentages, annual
precipitation at basin scale, runoff, elevation, and slope. Verify the
formulas and units in code.

### 5. Integrate spatially

District rainfall/LULC tables and HydroATLAS basin records represent
different spatial units. Do not join them by row order or directly by
district name. If district inputs must be transferred to basins, use a
documented spatial overlay, zonal calculation, or area-weighted method.
Explain partial overlaps and coverage.

### 6. Normalise indicators

A min--max transform is one possible method:

`x_norm = (x - min(x)) / (max(x) - min(x))`

For an indicator where lower values are assumed to indicate greater
concern, the transformed value may be inverted:

`x_inverse = 1 - x_norm`

This is sensitive to outliers and the chosen dataset extent. Handle a
zero denominator explicitly. Document missing-value treatment and the
normalisation bounds.

### 7. Weight and combine

A weighted sum is:

`Score_j = sum(weight_i * normalised_indicator_ij)`

For a conventional weighted sum, weights should be non-negative and sum
to 1. State the rationale and direction of every indicator. Equal
weights are an assumption, not automatically an objective choice.

### 8. Rank and map

Retain raw values, normalised values, component contributions, final
score, and stable IDs. Use a clear legend and caveat. Check geometry,
CRS, feature counts, and exported attributes.

### 9. Validate

Test sensitivity to weights and normalisation; compare results with
independent water-stress or watershed evidence; ask hydrologists, GIS
specialists, and local planners to review assumptions; field-check
candidate areas; and evaluate outcomes when reliable intervention data
exists.

## Current preliminary score --- exact known formula

The demonstration score used: -
`slope_screen_norm = minmax(slp_dg_sav_deg)` -
`low_rainfall_screen_norm = 1 - minmax(pre_mm_syr)` -
`preliminary_screen_score = (0.5 * slope_screen_norm + 0.5 * low_rainfall_screen_norm) * 100`

A `screen_rank` field was also produced. Confirm exact tie-handling and
ranking direction from the code.

Interpretation: within the dataset used for normalisation, higher slope
and lower annual precipitation increase the score. This is a prototype
screening proxy, not a validated final MCDA model, probability,
forecast, or engineering suitability score.

## Why it is preliminary

-   only two indicators are used;
-   equal weights are not validated;
-   min--max results depend on observed extremes;
-   indicator directions are assumptions;
-   geology, soil infiltration, drainage geometry, site conditions,
    access, environmental constraints, cost, and field evidence are not
    included;
-   source quality flags and uncertainty need further review.

## Potential future indicator families

  -------------------------------------------------------------------------
  Family                  Examples                Caution
  ----------------------- ----------------------- -------------------------
  Rainfall                annual/monsoon mean,    Period and spatial
                          CV, deficit magnitude,  resolution matter
                          dry-year frequency      

  Terrain                 slope, flow             Scale and derivation
                          accumulation, drainage  matter
                          density                 

  Land cover              water, vegetation,      Classification/coverage
                          crops, built-up, bare   uncertainty
                          ground                  

  Hydrology               runoff, stream network, A long-term mean is not a
                          catchment area          full flow regime

  Soil/geology            infiltration,           Requires suitable scale
                          permeability,           and validation
                          lithology, aquifer      
                          properties              

  Demand/exposure         population, irrigation, Needs clear planning
                          drought exposure        rationale

  Feasibility             protected areas,        Often
                          settlements, access,    intervention-specific
                          engineering constraints 
  -------------------------------------------------------------------------

## Avoid double counting and false precision

Rainfall variables can be correlated. Land-cover percentages are
compositional. Correlated indicators may overweight the same concept.
Check redundancy, missingness, direction, and whether each criterion
represents need, opportunity, or feasibility.

The results depend on the spatial units used (modifiable areal unit
problem). District averages hide local variation; basin-level outputs
may still be too coarse for selecting a specific site. Map scale must
not imply more certainty than the input data supports.
