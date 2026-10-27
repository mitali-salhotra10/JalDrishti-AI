# JalDrishti-AI: Earth Engine Terrain and SoilGrids Extraction Pipeline
# Author: JalDrishti-AI Engineering Team
# Workspace: Maharashtra Watershed Decision-Support Framework

import argparse
import sys
import time
import pandas as pd
import ee

GEE_PROJECT = 'jaldrishti-508107'
VILLAGE_ASSET = 'projects/jaldrishti-508107/assets/maharashtra_villages'
DRIVE_FOLDER = 'JalDrishti_AI'

SAMPLE_DISTRICTS = ['Latur', 'Pune', 'Nagpur', 'Nashik', 'Gadchiroli', 'Palghar', 'Solapur', 'Amravati']

def init_ee(project=GEE_PROJECT):
    try:
        ee.Initialize(project=project)
        print(f'[SUCCESS] Connected and authenticated to Earth Engine project: {project}')
    except Exception as e:
        print(f'[ERROR] Failed to initialize Earth Engine: {e}')
        print('Please run `earthengine authenticate` or verify cloud credentials.')
        sys.exit(1)

def get_terrain_clean_collection(village_fc, tile_scale=8):
    dem = ee.Image('USGS/SRTMGL1_003').select('elevation')
    slope = ee.Terrain.slope(dem).rename('slope_deg')
    terrain_composite = dem.rename('elevation_m').addBands(slope)

    terrain_reduced = terrain_composite.reduceRegions(
        collection=village_fc,
        reducer=ee.Reducer.mean(),
        scale=30,
        tileScale=tile_scale
    )

    def prepare_terrain(f):
        return ee.Feature(
            None,
            {
                'area_id': f.get('area_id'),
                'village': f.get('village'),
                'district': f.get('district'),
                'subdistric': f.get('subdistric'),
                'vlcode': f.get('vlcode'),
                'elevation_mean_m': f.get('elevation_m'),
                'slope_mean_deg': f.get('slope_deg')
            }
        )

    return terrain_reduced.map(prepare_terrain)

def get_soil_clean_collection(village_fc, tile_scale=8):
    sand = ee.Image('projects/soilgrids-isric/sand_mean')
    clay = ee.Image('projects/soilgrids-isric/clay_mean')
    silt = ee.Image('projects/soilgrids-isric/silt_mean')
    soc = ee.Image('projects/soilgrids-isric/soc_mean')

    soil_composite = (
        sand.select(['sand_0-5cm_mean', 'sand_5-15cm_mean'], ['sand_0_5cm', 'sand_5_15cm'])
        .addBands(clay.select(['clay_0-5cm_mean', 'clay_5-15cm_mean'], ['clay_0_5cm', 'clay_5_15cm']))
        .addBands(silt.select(['silt_0-5cm_mean', 'silt_5-15cm_mean'], ['silt_0_5cm', 'silt_5_15cm']))
        .addBands(soc.select(['soc_0-5cm_mean', 'soc_5-15cm_mean'], ['soc_0_5cm', 'soc_5_15cm']))
    )

    soil_reduced = soil_composite.reduceRegions(
        collection=village_fc,
        reducer=ee.Reducer.mean(),
        scale=250,
        tileScale=tile_scale
    )

    def prepare_soil(f):
        return ee.Feature(
            None,
            {
                'area_id': f.get('area_id'),
                'village': f.get('village'),
                'district': f.get('district'),
                'subdistric': f.get('subdistric'),
                'vlcode': f.get('vlcode'),
                'sand_0_5cm': f.get('sand_0_5cm'),
                'sand_5_15cm': f.get('sand_5_15cm'),
                'clay_0_5cm': f.get('clay_0_5cm'),
                'clay_5_15cm': f.get('clay_5_15cm'),
                'silt_0_5cm': f.get('silt_0_5cm'),
                'silt_5_15cm': f.get('silt_5_15cm'),
                'soc_0_5cm': f.get('soc_0_5cm'),
                'soc_5_15cm': f.get('soc_5_15cm')
            }
        )

    return soil_reduced.map(prepare_soil)

def run_sample_verification(villages_per_district=3):
    print('\n================================================================')
    print('  JALDRISHTI-AI: SOIL & TERRAIN EXTRACTION SAMPLE VERIFICATION  ')
    print('================================================================')
    init_ee()

    village_asset = ee.FeatureCollection(VILLAGE_ASSET)
    sample_fc = ee.FeatureCollection([])

    print(f'Sampling {villages_per_district} villages each from {len(SAMPLE_DISTRICTS)} agro-climatic districts...')
    for d in SAMPLE_DISTRICTS:
        d_villages = village_asset.filter(ee.Filter.eq('district', d)).limit(villages_per_district)
        sample_fc = sample_fc.merge(d_villages)

    sample_size = sample_fc.size().getInfo()
    print(f'[OK] Sample FeatureCollection ready: {sample_size} villages.')

    # 1. Terrain Sample
    print('\n[1/2] Executing SRTM Terrain Reducer (elevation_m, slope_deg)...')
    terrain_clean = get_terrain_clean_collection(sample_fc, tile_scale=4)
    t0 = time.time()
    terrain_res = terrain_clean.getInfo()
    t_terrain = time.time() - t0
    print(f'[OK] Terrain extraction finished in {t_terrain:.2f} seconds!')

    df_terrain = pd.DataFrame([f['properties'] for f in terrain_res['features']])
    print('\n--- Sample Terrain Summary ---')
    print(df_terrain[['area_id', 'village', 'district', 'elevation_mean_m', 'slope_mean_deg']].head(8).to_string())
    print(f'Elevation range: {df_terrain["elevation_mean_m"].min():.2f} m to {df_terrain["elevation_mean_m"].max():.2f} m')
    print(f'Slope range:     {df_terrain["slope_mean_deg"].min():.2f} deg to {df_terrain["slope_mean_deg"].max():.2f} deg')

    # 2. SoilGrids Sample
    print('\n[2/2] Executing ISRIC SoilGrids 250m Reducer (sand, clay, silt, soc)...')
    soil_clean = get_soil_clean_collection(sample_fc, tile_scale=4)
    t0 = time.time()
    soil_res = soil_clean.getInfo()
    t_soil = time.time() - t0
    print(f'[OK] SoilGrids extraction finished in {t_soil:.2f} seconds!')

    df_soil = pd.DataFrame([f['properties'] for f in soil_res['features']])
    df_soil['texture_sum_0_5cm'] = df_soil['sand_0_5cm'] + df_soil['clay_0_5cm'] + df_soil['silt_0_5cm']
    print('\n--- Sample SoilGrids Summary & Physical Sanity ---')
    print(df_soil[['area_id', 'village', 'district', 'sand_0_5cm', 'clay_0_5cm', 'silt_0_5cm', 'texture_sum_0_5cm']].head(8).to_string())
    
    avg_sum = df_soil['texture_sum_0_5cm'].mean()
    print(f'Mean Texture Sum (sand + clay + silt, expected 1000.0 g/kg): {avg_sum:.2f} g/kg')
    if abs(avg_sum - 1000.0) < 1.0:
        print('[PASS] Physical sanity verified: Soil texture components sum to 100.0% within measurement tolerance!')
    else:
        print(f'[WARN] Soil texture sum deviates from 1000 g/kg: {avg_sum}')

def start_batch_exports(folder=DRIVE_FOLDER):
    print('\n================================================================')
    print('  JALDRISHTI-AI: LAUNCHING GEE BATCH EXPORT TASKS (44,468 VILLAGES) ')
    print('================================================================')
    init_ee()

    village_asset = ee.FeatureCollection(VILLAGE_ASSET)
    total_count = village_asset.size().getInfo()
    print(f'Total villages in asset: {total_count:,}')

    # 1. Terrain Export Task
    print('\nPreparing Terrain Export Task...')
    terrain_clean = get_terrain_clean_collection(village_asset, tile_scale=8)
    task_terrain = ee.batch.Export.table.toDrive(
        collection=terrain_clean,
        description='JalDrishti_Maharashtra_Village_Terrain_v2',
        folder=folder,
        fileNamePrefix='maharashtra_village_terrain_v2',
        fileFormat='CSV',
        selectors=['area_id', 'village', 'district', 'subdistric', 'vlcode', 'elevation_mean_m', 'slope_mean_deg']
    )
    task_terrain.start()
    print(f'[LAUNCHED] Terrain Export Task ID: {task_terrain.id}')

    # 2. SoilGrids Export Task
    print('\nPreparing SoilGrids Export Task...')
    soil_clean = get_soil_clean_collection(village_asset, tile_scale=8)
    task_soil = ee.batch.Export.table.toDrive(
        collection=soil_clean,
        description='JalDrishti_Maharashtra_Village_SoilGrids_v2',
        folder=folder,
        fileNamePrefix='maharashtra_village_soilgrids_v2',
        fileFormat='CSV',
        selectors=[
            'area_id', 'village', 'district', 'subdistric', 'vlcode',
            'sand_0_5cm', 'sand_5_15cm',
            'clay_0_5cm', 'clay_5_15cm',
            'silt_0_5cm', 'silt_5_15cm',
            'soc_0_5cm', 'soc_5_15cm'
        ]
    )
    task_soil.start()
    print(f'[LAUNCHED] SoilGrids Export Task ID: {task_soil.id}')

    print(f'\nBoth export tasks submitted successfully to Google Drive folder "{folder}".')
    print('Monitor task status with `python export_village_terrain_soil_gee.py --check-status`.')

def check_task_status():
    print('\n================================================================')
    print('  JALDRISHTI-AI: GEE RECENT TASK STATUS                         ')
    print('================================================================')
    init_ee()

    tasks = ee.batch.Task.list()
    print(f'Retrieved {len(tasks)} recent tasks from Earth Engine:')
    found = False
    for t in tasks[:15]:
        desc = t.config.get('description', 'Unknown')
        state = t.state
        task_id = t.id
        print(f' - [{state:10s}] ID: {task_id} | Name: {desc}')
        found = True
    if not found:
        print('No tasks found.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JalDrishti-AI Terrain & SoilGrids GEE Pipeline')
    parser.add_argument('--sample', action='store_true', help='Run interactive sample verification (24 villages across 8 districts)')
    parser.add_argument('--start-tasks', action='store_true', help='Submit full batch export tasks for all 44,468 villages to Google Drive')
    parser.add_argument('--check-status', action='store_true', help='List recent GEE tasks and statuses')
    parser.add_argument('--folder', type=str, default=DRIVE_FOLDER, help='Google Drive destination folder')

    args = parser.parse_args()

    if args.sample:
        run_sample_verification()
    elif args.start_tasks:
        start_batch_exports(folder=args.folder)
    elif args.check_status:
        check_task_status()
    else:
        parser.print_help()
