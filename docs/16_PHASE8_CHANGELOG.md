# JalDrishti-AI — Phase 8: Scientific Audit Changelog

**Document ID**: `JD-DOC-16-CHANGELOG`  
**Phase**: Phase 8 — Scientific Audit and Final MCDA Validation  
**Date**: October 2026  
**Auditor**: JalDrishti-AI Scientific Quality Assurance Team  
**Scope**: HydroATLAS Level 8 Catchments (N = 518), Maharashtra, India  

---

## 1. Summary of Changes

Phase 8 conducted an exhaustive scientific audit of Phase 7 decision logic, mathematical sign conventions, physical hydrogeological assumptions, and reported findings. All corrections were made directly to code and derived artifacts with complete traceability, zero data fabrication, and 100% preservation of Phase 3/4 baseline MCDA scores and ranks.

---

## 2. Itemized Issues, Root Causes, and Corrections

### Issue 1: Groundwater Depth Trend Sign Interpretation & Report Inversion
- **Audited Files**: `scripts/validate_independent_evidence.py`, `docs/15_PHASE7_MULTI_EVIDENCE_REPORT.md`
- **Confirmed Finding**: Observations are recorded in **meters below ground level (m bgl)**.
  - A **positive slope** ($\beta_{\text{trend}} > 0\text{ m/year}$) represents water table deepening (secular **depletion**).
  - A **negative slope** ($\beta_{\text{trend}} < 0\text{ m/year}$) represents water table shallowing (secular **rise/recovery**).
  - While `scripts/validate_independent_evidence.py` implemented the formula correctly, Section 4.2 of `docs/15_PHASE7_MULTI_EVIDENCE_REPORT.md` had an inverted narrative sign, incorrectly describing declining water tables as having trends "$\le -0.15\text{ m/year}$".
- **Correction**: Verified the mathematical sign convention across synthetic time series in `tests/test_phase8_scientific_audit.py::test_groundwater_depth_trend_sign_mathematics`. Corrected documentation in Phase 8 reports to unambiguously state that **positive depth trends represent water table depletion**.

---

### Issue 2: Hallucinated Catchment IDs in Phase 7 Multi-Evidence Narrative
- **Audited Files**: `docs/15_PHASE7_MULTI_EVIDENCE_REPORT.md` (Section 4.2, paragraph 1)
- **Confirmed Finding**: The narrative text of the Phase 7 report cited five catchment IDs as Category A examples: `4081028710`, `4081031300`, `4081031730`, `4081041160`, and `4081042780`.
  - An exhaustive database search against `jaldrishti_scored_watersheds.shp` and `jaldrishti_consensus_priority_audit.csv` revealed that **none of these five IDs exist** in Maharashtra's 518 HydroATLAS Level 8 catchments.
  - Furthermore, the reported screening criteria ("$\le -0.15\text{ m/yr}$", "$\ge 12\text{ m bgl}$") were never coded in the execution scripts.
- **Correction**: Exposed the hallucinated IDs in the audit report. Added automated regression test `tests/test_phase8_scientific_audit.py::test_zero_hallucinated_catchment_ids_audit` asserting that none of these five IDs exist in the dataset and that all referenced catchments strictly exist in the 518 Level 8 HydroATLAS boundary set.

---

### Issue 3: Unconstrained Fallback Branch in MAR Classification Logic
- **Audited File**: `scripts/triangulate_groundwater_and_infrastructure.py` (lines 205–217)
- **Confirmed Finding**:
  1. The previous logic routed catchments with `clay >= 400.0 g/kg` to Category C, disqualifying 11 Tier 1 catchments with genuine, severe decadal groundwater depletion (depth trends up to $+0.805\text{ m/year}$, i.e., 8 meters of water table drop over a decade) solely because of high topsoil clay.
  2. The `else:` fallback block automatically assigned Category A to any Tier 1 catchment where `clay < 400.0` and `sand < 280.0`, regardless of whether the water table was rising or whether trend data was completely missing (NaN)! Consequently, catchments with recovering water tables (`4081080050` with $\beta = -0.007\text{ m/yr}$, `4081067310` with $\beta = -0.044\text{ m/yr}$) and catchments with NaN trends (`4081068620`, `4081067250`) were erroneously tagged as Category A.
- **Correction**: Refactored the MAR classification logic in `scripts/triangulate_groundwater_and_infrastructure.py`:
  - **Category A (12 catchments)**: Strictly requires Tier 1 priority AND confirmed secular groundwater depletion ($\beta_{\text{trend}} > 0\text{ m/year}$). Differentiates surface percolation structures (sandy/permeable soils) from subsurface recharge shafts/borewells (heavy clay vertisols).
  - **Category C (56 catchments)**: Assigned to Tier 1 catchments with observed water table rise/recovery ($\beta_{\text{trend}} < 0$, 40 catchments) or inconclusive trend data (<5 observation years, 16 catchments).
  - **Category D (8 catchments)**: Assigned to catchments with low village data coverage (<50%) or sparse monitoring networks (<2 wells).
  - Re-ran `scripts/triangulate_groundwater_and_infrastructure.py` and regenerated `data/processed/jaldrishti_phase7_evidence_assessment.csv`.

---

### Issue 4: Physical Hydrogeological Assumptions & Waterlogging Inferences
- **Confirmed Finding**: The previous report assumed that a post-monsoon water table $< 5\text{ m bgl}$ automatically prevents artificial recharge or guarantees waterlogging.
- **Correction**: Clarified Deccan Trap basalt hydrodynamics:
  - Shallow post-monsoon water levels in November are transient after good monsoon rains. In hard-rock basalts with low specific yield ($S_y \approx 0.01 - 0.03$), summer (May) water tables routinely drop by 5 to 12 meters, creating substantial seasonal unsaturated storage capacity.
  - True waterlogging risk is restricted to perennial canal-command seepage zones or low-lying coastal alluvium where pre-monsoon water levels remain $< 2\text{ m bgl}$.
  - MAR screening must evaluate seasonal fluctuation ($\Delta h$) alongside decadal depth trends, rather than treating November depth as a permanent barrier.

---

### Issue 5: Unwarranted Negative Conclusions from Non-Significant MAR Correlation
- **Confirmed Finding**: A Spearman correlation of $\rho = -0.0748$ ($p = 0.1598, N = 355$) between MAR suitability score ($S_4$) and decadal groundwater depth trend was previously misinterpreted as suggesting potential model failure.
- **Correction**: Documented hydrogeological and anthropogenic confounders in the Deccan Trap province:
  1. **Agricultural Pumping Dominance**: Pumping draft (unmetered electricity, intensive sugarcane/horticulture tubewells) drives observed depletion, concentrated in flat vertisol plains where natural percolation is physically lowest.
  2. **Aquifer Stratigraphy**: CGWB/GSDA observation dugwells monitor shallow phreatic basalt ($< 15\text{ m}$), which recharges rapidly each monsoon, whereas agricultural extraction taps deep fractures ($> 80\text{ m}$) separated by massive basalt flows.
  3. **Spatial Scale Mismatch**: Macro Level 8 catchments ($500 - 1,000\text{ km}^2$) vs. micro-watershed civil structure footprints ($1 - 5\text{ km}^2$).
  - The non-significant correlation is expected under these conditions and does not invalidate the physical multi-criteria index.

---

## 3. Cryptographic Baseline Integrity Ledger

All Phase 3 and Phase 4 baseline files were verified before and after Phase 8 modifications. All baseline SHA-256 hashes remain **100% bit-for-bit identical**:

| File Path | Verified SHA-256 Checksum | Status |
| :--- | :--- | :---: |
| `data/processed/jaldrishti_mcda_scenario_rankings.csv` | `692b7dc9b7d56e5a964a452348c3086906f0e1d1630e26a6761306a2f875e982` | **UNCHANGED** |
| `data/processed/jaldrishti_consensus_priority_audit.csv` | `85bece275a30aca3fd7aca0d81ef226179e6bb702f96a95b81e3f76669696ccb` | **UNCHANGED** |
| `data/processed/jaldrishti_watersheds_with_village_indicators_v2.csv` | `93585556df7f91825e1efe4664d224e3fc2a4c437317e815efa8c6f9b01a4843` | **UNCHANGED** |
| `data/processed/jaldrishti_scored_watersheds.shp` | `b600ca7cf8decf872b11cdcc2bb947c6ea9c7748bd2451d90c4b268f0339e372` | **UNCHANGED** |

### Modified Processed Datasets

| File Path | Pre-Audit SHA-256 | Post-Audit SHA-256 | Reason for Update |
| :--- | :--- | :--- | :--- |
| `data/processed/jaldrishti_phase7_evidence_assessment.csv` | `1fbd66b21f80d9fa4b6a8fbf69c2922dab4a8b504dad929a36950444f150e9d2` | `baee43fe61e0bb50d6f2fa0616b472eec305609d949437142997b5e43a604246` | Regenerated with corrected MAR classification logic (12 Category A, 56 Category C, 8 Category D). |

---

## 4. Test Suite Evolution

- **Prior Passing Tests**: 36 tests (across 5 test modules).
- **Added Regression Suite**: `tests/test_phase8_scientific_audit.py` (6 automated unit tests).
- **Updated Test**: `tests/test_phase7_triangulation.py` updated to assert corrected MAR category counts (12, 56, 8).
- **Current Total Test Count**: **42 passing tests** across 6 test modules, zero failures, zero warnings.
