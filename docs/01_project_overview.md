# 1. Project Overview

## What are we building?

JalDrishti-AI is a **GIS-based watershed decision-support framework**.
It is intended to bring environmental data into a repeatable workflow so
planners can compare watersheds, understand why some rank higher under
defined criteria, visualise the results, and identify areas needing
further investigation.

The product is not just a map. It consists of: - a documented data
pipeline; - clean and traceable environmental indicators; - a
transparent prioritisation/scoring method; - GIS-ready outputs and
visualisations; - quality checks, uncertainty notes, and a path to
validation.

## Geographic scope

The long-term vision is relevant to India. **Maharashtra is the initial
implementation/study phase**, because the current rainfall and
land-cover analysis focuses on Maharashtra. Do not describe Maharashtra
as the only intended geography unless the owner changes the scope.

The current watershed records use WWF HydroATLAS Level 8 basin
geography. Basins are hydrological units, not administrative districts.
A district can overlap multiple basins and a basin can cross district
boundaries.

## Two different decisions --- never conflate them

### Watershed prioritisation

"Where should planners investigate conservation needs first?" This is a
broad screening question informed by rainfall, terrain, land cover,
runoff context, and other evidence.

### Structure/site suitability

"Where is a particular intervention technically appropriate?" This
requires intervention-specific hydrology, drainage geometry, soil
infiltration, geology, foundation conditions, land access, environmental
constraints, engineering design, and field verification.

A high-priority watershed is **not automatically suitable** for a check
dam, percolation tank, recharge structure, or other intervention. The
current score must not be presented as a check-dam suitability score.

## Why "AI"?

The demonstrated work to date is principally GIS, environmental data
processing, indicator engineering, and preliminary MCDA-style screening.
The current record does not establish that a trained machine-learning
model or deployed predictive AI service exists. Unless later code proves
otherwise, describe the current build as a GIS-based
decision-support/MCDA framework with possible AI-assisted
extensions---not a validated AI predictor.

## Intended outputs

-   district rainfall indicator tables;
-   2023 district land-cover summaries;
-   prepared basin indicator tables;
-   score tables with raw inputs and component scores;
-   GIS-compatible vector layers;
-   static maps/SVGs for reporting;
-   documented metadata, assumptions, and quality flags;
-   eventually, a validated prioritisation workflow.

## Current maturity

The project is in data preparation and preliminary prototyping. Data
tables have been saved and a preliminary score layer was exported to
Google Drive. The full MCDA model, spatial integration of district and
basin data, independent validation, field verification, and production
deployment are not confirmed complete.


