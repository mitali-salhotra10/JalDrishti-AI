# Forwarding wrapper for src/jaldrishti/spatial_aggregation.py
import sys
from pathlib import Path

src_dir = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(src_dir))

if __name__ == "__main__":
    from jaldrishti.spatial_aggregation import run_spatial_aggregation, argparse
    parser = argparse.ArgumentParser(description="JalDrishti-AI Area-Weighted Spatial Aggregation")
    parser.add_argument("--root", type=str, default=None, help="Project root directory")
    parser.add_argument("--version", type=str, default="v2", help="Aggregation version tag (e.g. v1, v2)")
    args = parser.parse_args()
    root_path = Path(args.root) if args.root else None
    run_spatial_aggregation(project_root=root_path, version=args.version)
