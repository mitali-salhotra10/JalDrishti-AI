# JalDrishti-AI Notebooks

This directory contains Jupyter notebooks documenting the exploratory, analytical, and validation stages of the project.

## Notebook Inventory & Recommended Order

| Notebook | Purpose & Status | Execution Notes |
| :--- | :--- | :--- |
| **`JalDrishti_Watershed_Analysis_Continued.ipynb`** | **Primary Analytical Notebook** (Active & Fully Executed). Contains shapefile validation, preliminary score recalculation, root-cause diagnosis of soil/terrain blockers, live multi-district sample verification, spatial aggregation diagnostics, and 3-panel comparative cartography. | Fully reproducible using local Python environment and local datasets. Earth Engine sample verification runs live via authenticated GEE API. |
| **`JalDrishti_Data_Validation_Step1_Cleaned.ipynb`** | **Historical Validation Notebook** (Reference). Working copy of initial district-level CHIRPS rainfall, Dynamic World LULC, and preliminary HydroATLAS screening. | Retained for auditability. Contains historical execution outputs up to Cell 308. |
| **`Sentinel-2_Maharstra.ipynb`** | **Archival Extraction Notebook** (Audit Reference). Sourced from development history; contains Cells 60 and 82–84 audited in Document 08 and Document 09. | Retained to document original Earth Engine reducer setup and bug evidence. |

## Running the Notebooks

1. Activate your Python environment:
   ```bash
   pip install -r requirements.txt
   ```
2. Start Jupyter:
   ```bash
   jupyter lab
   ```
3. Open `notebooks/JalDrishti_Watershed_Analysis_Continued.ipynb` and run all cells. Dynamic path resolution automatically detects the project root and accesses `data/` and `outputs/`.
