# Forwarding wrapper for scripts/export_village_terrain_soil_gee.py
import sys
from pathlib import Path

scripts_dir = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(scripts_dir))

if __name__ == "__main__":
    import export_village_terrain_soil_gee
    export_village_terrain_soil_gee.main()
