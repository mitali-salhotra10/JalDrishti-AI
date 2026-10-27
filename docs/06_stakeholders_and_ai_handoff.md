# 6. Stakeholders and Instructions for the Next AI/Developer

## Intended stakeholders

These are relevant stakeholder groups; their participation is not
claimed unless it has actually occurred.

  ------------------------------------------------------------------------
  Stakeholder              Potential role          Information needed
  ------------------------ ----------------------- -----------------------
  State/district           Planning and review     Transparent maps,
  water-resource                                   assumptions, indicators
  departments                                      

  Watershed development    Identify areas for      Basin summaries and
  agencies                 further assessment      screening rationale

  Hydrologists/water       Review hydrological     Raw attributes,
  engineers                logic and feasibility   methods, uncertainty

  GIS/remote-sensing       Build and validate      CRS, resolution,
  analysts                 spatial layers          lineage, reproducible
                                                   code

  Soil/geology specialists Review infiltration,    Suitable thematic data
                           lithology, aquifer      and site evidence
                           context                 

  Local government/village Supply local context    Understandable maps and
  institutions             and priorities          transparent methods

  Communities and water    Share seasonal and      Clear explanations and
  users                    access-related          opportunity to correct
                           knowledge               assumptions

  NGOs/implementers        Plan field assessment   Candidate areas,
                           and implementation      constraints, monitoring
                                                   needs

  Researchers/reviewers    Test methodology        Reproducible formulas
                                                   and sensitivity
                                                   analysis

  Funders/evaluators       Assess rationale and    Evidence, limitations,
                           outcomes                measurable indicators

  Landowners/authorities   Confirm access and      Site-level consultation
                           permissions             and official clearance
  ------------------------------------------------------------------------

## Appropriate use cases now

-   Compare basins under the current illustrative formula.
-   Examine rainfall variability among districts.
-   Compare district land-cover composition.
-   Find records with missing values or review flags.
-   Decide where more detailed analysis or field assessment may be
    useful.

## Questions the current system cannot answer on its own

-   How much groundwater recharge a site will produce.
-   Whether a particular check dam will succeed.
-   How many households will receive reliable water.
-   Whether land is legally available or a site is environmentally
    permitted.
-   Whether an engineering design is safe or economically optimal.

## Rules for the next AI tool

1.  Inspect the actual project directory before assuming file state.
2.  Use saved CSVs as durable state; do not assume notebook variables
    survived a kernel reset.
3.  Do not claim local file access unless the environment actually
    provides it.
4.  Do not claim the export is downloaded because the remote task
    completed.
5.  If asked for the next Jupyter cell, provide the next concrete cell
    rather than another broad explanation.
6.  Do not redo expensive data acquisition without a reason.
7.  Never join district records to basin records by row order.
8.  Do not drop quality-flagged records without investigating flag
    semantics.
9.  Keep watershed prioritisation distinct from structure suitability.
10. Keep the score labelled preliminary until validation is documented.
11. Preserve raw inputs, stable IDs, score components, and provenance.
12. Do not invent validation metrics, fieldwork, stakeholder
    participation, or model performance.
13. Verify generated artifact paths before sharing links.

## First notebook cell

``` python
from pathlib import Path
import pandas as pd

DATA_DIR = Path(r"C:\Users\MITALI SALHOTRA\JalDrishti-AI")
print("Project directory exists:", DATA_DIR.exists())
for path in sorted(DATA_DIR.iterdir()):
    print(("DIR " if path.is_dir() else "FILE"), path.name)
```

Then load existing tables only after confirming their presence:

``` python
required = {
    "rainfall": "jaldrishti_rainfall_indicators_2018_2025_clean.csv",
    "lulc": "jaldrishti_lulc_2023_all_36_districts.csv",
    "district_combined": "jaldrishti_district_rainfall_lulc_analysis.csv",
    "hydroatlas": "jaldrishti_hydroatlas_indicators_prepared.csv",
    "watershed_inputs": "jaldrishti_watershed_mcda_inputs.csv",
    "screening": "jaldrishti_watershed_preliminary_screening.csv",
}
tables = {}
for name, filename in required.items():
    path = DATA_DIR / filename
    if not path.exists():
        print("MISSING:", path)
        continue
    tables[name] = pd.read_csv(path)
    print(name, tables[name].shape, tables[name].columns.tolist())
```

## Progress reporting format

For each major step, report: files read/written; row counts; validation
checks; assumptions; unresolved issues; and the next exact action. Code
execution alone does not prove an output is correct.

## Priority order

1.  Verify local export files.
2.  Validate geometry, CRS, row count, and score values.
3.  Create the SVG from verified geospatial data.
4.  Audit the preliminary formula and quality flags.
5.  Investigate the 518-versus-522 basin-count difference.
6.  Define and implement the full MCDA model.
7.  Add defensible spatial overlays if district attributes are required
    at basin scale.
8.  Perform sensitivity analysis and expert/field validation.
9.  Consider productionisation or predictive AI extensions only after
    the analytical foundation is defensible.
