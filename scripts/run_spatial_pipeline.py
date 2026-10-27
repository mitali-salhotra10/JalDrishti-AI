#!/usr/bin/env python3
"""
CLI runner for the JalDrishti-AI spatial aggregation pipeline.
Executes area-weighted overlay translating 44,468 village polygons onto 518 HydroATLAS catchments.
"""

import sys
from pathlib import Path

# Add src to python path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from jaldrishti.spatial_aggregation import run_spatial_aggregation

if __name__ == "__main__":
    run_spatial_aggregation()
