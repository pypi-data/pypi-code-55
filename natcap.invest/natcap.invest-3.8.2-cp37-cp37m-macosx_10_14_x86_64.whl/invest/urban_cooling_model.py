"""Urban Cooling Model."""
import shutil
import tempfile
import math
import logging
import os
import pickle
import time

from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import pygeoprocessing
import taskgraph
import numpy
import shapely.wkb
import shapely.prepared
import rtree

from . import validation
from . import utils

LOGGER = logging.getLogger(__name__)
TARGET_NODATA = -1
_LOGGING_PERIOD = 5.0

ARGS_SPEC = {
    'model_name': 'Urban Cooling Model',
    'module': __name__,
    'userguide_html': 'urban_cooling_model.html',
    "args_with_spatial_overlap": {
        "spatial_keys": ["lulc_raster_path", "ref_eto_raster_path",
                         "aoi_vector_path", "building_vector_path"],
        "different_projections_ok": True,
    },
    "args": {
        "workspace_dir": validation.WORKSPACE_SPEC,
        "results_suffix": validation.SUFFIX_SPEC,
        "n_workers": validation.N_WORKERS_SPEC,
        "lulc_raster_path": {
            "name": "Land Use / Land Cover Raster",
            "type": "raster",
            "required": True,
            "validation_options": {
                "projected": True,
                "projection_units": "m",
            },
            "about": (
                "A GDAL-supported raster file containing integer values "
                "representing the LULC code for each cell.  The LULC code "
                "should be an integer.  The model will use the resolution of "
                "this layer to resample all outputs.  The resolution should "
                "be small enough to capture the effect of green areas in the "
                "landscape, although LULC categories can comprise a mix of "
                "vegetated and non-vegetated covers (e.g. 'residential', "
                "which may have 30% canopy cover."
            )
        },
        "ref_eto_raster_path": {
            "name": "Reference Evapotranspiration Raster",
            "type": "raster",
            "required": True,
            "about": (
                "A GDAL-supported raster file containing numeric values "
                "representing the evapotranspiration (in mm) for the period "
                "of interest."
            )
        },
        "aoi_vector_path": {
            "name": "Area of Interest Vector",
            "type": "vector",
            "required": True,
            "about": (
                "A GDAL-compatible vector delineating areas of interest "
                "(city or neighborhood boundaries).  Results will be "
                "aggregated within each feature in this vector."
            )
        },
        "biophysical_table_path": {
            "name": "Biophysical Table",
            "type": "csv",
            "required": True,
            "validation_options": {
                "required_fields": ["lucode", "kc", "green_area"],
            },
            "about": (
                "A CSV table containing model information corresponding "
                "to each of the land use classes in the LULC.  All classes "
                "in the land cover raster MUST have corresponding values "
                "in this table.  Each row is a land use/land cover class."
            ),
        },
        "green_area_cooling_distance": {
            "name": "Green area max cooling distance effect (m)",
            "type": "number",
            "required": True,
            "validation_options": {
                "expression": "value > 0",
            },
            "about": (
                "Distance (in m) over which large green areas (> 2 ha) "
                "will have a cooling effect."
            ),
        },
        "t_air_average_radius": {
            "name": "T_air moving average radius (m)",
            "type": "number",
            "required": True,
            "validation_options": {
                "expression": "value > 0"
            },
            "about": (
                "Radius of the averaging filter for turning T_air_nomix "
                "into T_air")
        },
        "t_ref": {
            "name": "Reference Air Temperature",
            "type": "number",
            "required": True,
            "about": (
                "Rural reference temperature (where the urban heat island"
                "effect is not observed) for the period of interest. This "
                "could be nighttime or daytime temperature, for a specific "
                "date or an average over several days. The results will be "
                "given for the same period of interest)"),
        },
        "uhi_max": {
            "name": "Magnitude of the UHI effect",
            "type": "number",
            "required": True,
            "about": (
                "The magnitude of the urban heat island effect, in degrees "
                "C.  Example: the difference between the rural reference "
                "temperature and the maximum temperature observed in the "
                "city."
            ),
        },
        "do_valuation": {
            "name": "Run Valuation Model",
            "type": "boolean",
            "required": True,
            "about": "Select to run the valuation model."
        },
        "avg_rel_humidity": {
            "name": "Average relative humidity (0-100%)",
            "type": "number",
            "required": "do_valuation",
            "validation_options": {
                "expression": "(value >= 0) and (value <= 100)",
            },
            "about": (
                "The average relative humidity (0-100%) over the time period "
                "of interest."
            ),
        },
        "building_vector_path": {
            "name": "Buildings vector",
            "type": "vector",
            "required": "do_valuation",
            "validation_options": {
                "required_fields": ["type"],
            },
            "about": (
                "A GDAL-compatible vector with built infrastructure "
                "footprints.  The attribute table must contain the column "
                "'type', with integers referencing the building type "
                "(e.g. 1=residential, 2=office, etc.) that match types in "
                "the energy consumption table."
            ),
        },
        "energy_consumption_table_path": {
            "name": "Energy consumption table",
            "type": "csv",
            "required": "do_valuation",
            "validation_options": {
                "required_fields": ["type", "consumption"],
            },
            "about": (
                "A CSV table containing information on energy consumption "
                "for various types of buildings, in kW/degC."
            ),
        },
        "cc_method": {
            "name": "Cooling capacity calculation method",
            "type": "option_string",
            "required": True,
            "validation_options": {
                "options": ['factors', 'intensity'],
            },
            "about": (
                'The method selected here determines the predictor used for '
                'air temperature.  If <b>"Weighted Factors"</b> is '
                'selected, the Cooling Capacity calculations will use the '
                'weighted factors for shade, albedo and ETI as a predictor '
                'for daytime temperatures. <br/>'
                'Alternatively, if <b>"Building Intensity"</b> is selected, '
                'building intensity will be used as a predictor for nighttime '
                'temperature instead of shade, albedo and ETI.'
            ),
        },
        "cc_weight_shade": {
            "name": "Cooling capacity: adjust shade weight",
            "type": "number",
            "required": False,
            "validation_options": {
                "expression": "value > 0",
            },
            "about": (
                "The relative weight to apply to shade when calculating the "
                "cooling index.  Default: 0.6"
            ),
        },
        "cc_weight_albedo": {
            "name": "Cooling capacity: adjust albedo weight",
            "type": "number",
            "required": False,
            "validation_options": {
                "expression": "value > 0",
            },
            "about": (
                "The relative weight to apply to albedo when calculating the "
                "cooling index.  Default: 0.2"
            ),
        },
        "cc_weight_eti": {
            "name": "Cooling capacity: adjust evapotranspiration weight",
            "type": "number",
            "required": False,
            "validation_options": {
                "expression": "value > 0",
            },
            "about": (
                "The relative weight to apply to ETI when calculating the "
                "cooling index.  Default: 0.2"
            )
        },
    }
}


def execute(args):
    """Urban Cooling Model.

    Args:
        args['workspace_dir'] (str): path to target output directory.
        args['results_suffix'] (string): (optional) string to append to any
            output file names
        args['t_ref'] (str/float): reference air temperature.
        args['lulc_raster_path'] (str): path to landcover raster.
        args['ref_eto_raster_path'] (str): path to evapotranspiration raster.
        args['aoi_vector_path'] (str): path to desired AOI.
        args['biophysical_table_path'] (str): table to map landcover codes to
            Shade, Kc, and Albedo values. Must contain the fields 'lucode',
            'kc', and 'green_area'.  If ``args['cc_method'] == 'factors'``,
            then this table must also contain the fields 'shade' and
            'albedo'.  If ``args['cc_method'] == 'intensity'``, then this
            table must also contain the field 'building_intensity'.
        args['green_area_cooling_distance'] (float): Distance (in m) over
            which large green areas (> 2 ha) will have a cooling effect.
        args['t_air_average_radius'] (float): radius of the averaging filter
            for turning T_air_nomix into T_air.
        args['uhi_max'] (float): Magnitude of the UHI effect.
        args['do_valuation'] (bool): if True, consider the valuation
            parameters for buildings.
        args['avg_rel_humidity'] (float): (optional, depends on
            'do_valuation') Average relative humidity (0-100%).
        args['building_vector_path']: (str) (optional, depends on
            'do_valuation') path to a vector of building footprints that
            contains at least the field 'type'.
        args['energy_consumption_table_path'] (str): (optional, depends on
            'do_valuation') path to a table that maps building types to
            energy consumption. Must contain at least the fields 'type' and
            'consumption'.
        args['cc_method'] (str): Either "intensity" or "factors".  If
            "intensity", then the "building_intensity" column must be
            present in the biophysical table.  If "factors", then
            ``args['cc_weight_shade']``, ``args['cc_weight_albedo']``,
            ``args['cc_weight_eti']`` may be set to alternative weights
            if desired.
        args['cc_weight_shade'] (str/float): floating point number
            representing the relative weight to apply to shade when
            calculating the cooling index. Default: 0.6
        args['cc_weight_albedo'] (str/float): floating point number
            representing the relative weight to apply to albedo when
            calculating the cooling index. Default: 0.2
        args['cc_weight_eti'] (str/float): floating point number
            representing the relative weight to apply to ETI when
            calculating the cooling index. Default: 0.2


    Returns:
        None.

    """
    LOGGER.info('Starting Urban Cooling Model')
    file_suffix = utils.make_suffix_string(args, 'results_suffix')
    intermediate_dir = os.path.join(
        args['workspace_dir'], 'intermediate')
    utils.make_directories([args['workspace_dir'], intermediate_dir])
    biophysical_lucode_map = utils.build_lookup_from_csv(
        args['biophysical_table_path'], 'lucode', to_lower=True,
        warn_if_missing=True)

    # cast to float and calculate relative weights
    # Use default weights for shade, albedo, eti if the user didn't provide
    # weights.
    cc_weight_shade_raw = float(args.get('cc_weight_shade', 0.6))
    cc_weight_albedo_raw = float(args.get('cc_weight_albedo', 0.2))
    cc_weight_eti_raw = float(args.get('cc_weight_eti', 0.2))
    t_ref_raw = float(args['t_ref'])
    uhi_max_raw = float(args['uhi_max'])
    cc_weight_sum = sum(
        (cc_weight_shade_raw, cc_weight_albedo_raw, cc_weight_eti_raw))
    cc_weight_shade = cc_weight_shade_raw / cc_weight_sum
    cc_weight_albedo = cc_weight_albedo_raw / cc_weight_sum
    cc_weight_eti = cc_weight_eti_raw / cc_weight_sum

    # Cast to a float upfront in case of casting errors.
    t_air_average_radius_raw = float(args['t_air_average_radius'])

    try:
        n_workers = int(args['n_workers'])
    except (KeyError, ValueError, TypeError):
        # KeyError when n_workers is not present in args.
        # ValueError when n_workers is an empty string.
        # TypeError when n_workers is None.
        n_workers = -1  # Synchronous mode.

    task_graph = taskgraph.TaskGraph(
        os.path.join(intermediate_dir, '_taskgraph_working_dir'), n_workers)

    # align all the input rasters.
    aligned_lulc_raster_path = os.path.join(
        intermediate_dir, 'lulc%s.tif' % file_suffix)
    aligned_ref_eto_raster_path = os.path.join(
        intermediate_dir, 'ref_eto%s.tif' % file_suffix)

    lulc_raster_info = pygeoprocessing.get_raster_info(
        args['lulc_raster_path'])
    # ensure raster has square pixels by picking the smallest dimension
    cell_size = numpy.min(numpy.abs(lulc_raster_info['pixel_size']))

    # Reproject and align inputs to the intersection of the AOI, ETO and LULC,
    # with target raster sizes matching those of the LULC.
    aligned_raster_path_list = [
        aligned_lulc_raster_path, aligned_ref_eto_raster_path]
    align_task = task_graph.add_task(
        func=pygeoprocessing.align_and_resize_raster_stack,
        args=([args['lulc_raster_path'], args['ref_eto_raster_path']],
              aligned_raster_path_list,
              ['mode', 'cubicspline'],
              (cell_size, -cell_size),
              'intersection'),
        kwargs={
            'base_vector_path_list': [args['aoi_vector_path']],
            'raster_align_index': 1,
            'target_sr_wkt': lulc_raster_info['projection']},
        target_path_list=aligned_raster_path_list,
        task_name='align rasters')

    task_path_prop_map = {}
    reclassification_props = ('kc', 'green_area')
    if args['cc_method'] == 'factors':
        reclassification_props += ('shade', 'albedo')
    else:
        reclassification_props += ('building_intensity',)

    for prop in reclassification_props:
        prop_map = dict(
            (lucode, x[prop])
            for lucode, x in biophysical_lucode_map.items())

        prop_raster_path = os.path.join(
            intermediate_dir, '%s%s.tif' % (prop, file_suffix))
        prop_task = task_graph.add_task(
            func=pygeoprocessing.reclassify_raster,
            args=(
                (aligned_lulc_raster_path, 1), prop_map, prop_raster_path,
                gdal.GDT_Float32, TARGET_NODATA),
            kwargs={'values_required': True},
            target_path_list=[prop_raster_path],
            dependent_task_list=[align_task],
            task_name='reclassify to %s' % prop)
        task_path_prop_map[prop] = (prop_task, prop_raster_path)

    green_area_decay_kernel_distance = int(numpy.round(
        float(args['green_area_cooling_distance']) / cell_size))
    cc_park_raster_path = os.path.join(
        intermediate_dir, 'cc_park%s.tif' % file_suffix)
    cc_park_task = task_graph.add_task(
        func=convolve_2d_by_exponential,
        args=(
            green_area_decay_kernel_distance,
            task_path_prop_map['green_area'][1],
            cc_park_raster_path),
        target_path_list=[cc_park_raster_path],
        dependent_task_list=[
            task_path_prop_map['green_area'][0]],
        task_name='calculate T air')

    # Calculate the area of greenspace within a search radius of each pixel.
    area_kernel_path = os.path.join(
        intermediate_dir, 'area_kernel%s.tif' % file_suffix)
    area_kernel_task = task_graph.add_task(
        func=flat_disk_kernel,
        args=(green_area_decay_kernel_distance, area_kernel_path),
        target_path_list=[area_kernel_path],
        task_name='area kernel')

    green_area_sum_raster_path = os.path.join(
        intermediate_dir, 'green_area_sum%s.tif' % file_suffix)
    green_area_sum_task = task_graph.add_task(
        func=pygeoprocessing.convolve_2d,
        args=(
            (task_path_prop_map['green_area'][1], 1),  # green area path
            (area_kernel_path, 1),
            green_area_sum_raster_path),
        kwargs={
            'working_dir': intermediate_dir,
            'ignore_nodata': True},
        target_path_list=[green_area_sum_raster_path],
        dependent_task_list=[
            task_path_prop_map['green_area'][0],  # reclassed green area task
            area_kernel_task],
        task_name='calculate green area')

    align_task.join()

    cc_raster_path = os.path.join(
        intermediate_dir, 'cc%s.tif' % file_suffix)
    if args['cc_method'] == 'factors':
        LOGGER.info('Calculating Cooling Coefficient from factors')
        # Evapotranspiration index (Equation #1)
        ref_eto_raster = gdal.OpenEx(aligned_ref_eto_raster_path,
                                     gdal.OF_RASTER)
        ref_eto_band = ref_eto_raster.GetRasterBand(1)
        _, ref_eto_max, _, _ = ref_eto_band.GetStatistics(0, 1)
        ref_eto_max = numpy.round(ref_eto_max, decimals=9)
        ref_eto_band = None
        ref_eto_raster = None

        eto_nodata = pygeoprocessing.get_raster_info(
            args['ref_eto_raster_path'])['nodata'][0]
        eti_raster_path = os.path.join(
            intermediate_dir, 'eti%s.tif' % file_suffix)
        eti_task = task_graph.add_task(
            func=pygeoprocessing.raster_calculator,
            args=(
                [(task_path_prop_map['kc'][1], 1), (TARGET_NODATA, 'raw'),
                 (aligned_ref_eto_raster_path, 1), (eto_nodata, 'raw'),
                 (ref_eto_max, 'raw'), (TARGET_NODATA, 'raw')],
                calc_eti_op, eti_raster_path, gdal.GDT_Float32, TARGET_NODATA),
            target_path_list=[eti_raster_path],
            dependent_task_list=[task_path_prop_map['kc'][0]],
            task_name='calculate eti')

        # Cooling Capacity calculations (Equation #2)
        cc_task = task_graph.add_task(
            func=pygeoprocessing.raster_calculator,
            args=([(task_path_prop_map['shade'][1], 1),
                   (task_path_prop_map['albedo'][1], 1),
                   (eti_raster_path, 1),
                   (cc_weight_shade, 'raw'),
                   (cc_weight_albedo, 'raw'),
                   (cc_weight_eti, 'raw')],
                  calc_cc_op_factors, cc_raster_path,
                  gdal.GDT_Float32, TARGET_NODATA),
            target_path_list=[cc_raster_path],
            dependent_task_list=[
                task_path_prop_map['shade'][0],
                task_path_prop_map['albedo'][0],
                eti_task],
            task_name='calculate cc index (weighted factors)')
    else:
        # args['cc_method'] must be 'intensity', so we use a modified CC
        # function.
        LOGGER.info('Calculating Cooling Coefficient using '
                    'building intensity')
        cc_task = task_graph.add_task(
            func=pygeoprocessing.raster_calculator,
            args=([(task_path_prop_map['building_intensity'][1], 1)],
                  calc_cc_op_intensity, cc_raster_path,
                  gdal.GDT_Float32, TARGET_NODATA),
            target_path_list=[cc_raster_path],
            dependent_task_list=[
                task_path_prop_map['building_intensity'][0]],
            task_name='calculate cc index (intensity)')

    # Compute Heat Mitigation (HM) index.
    #
    # convert 2 hectares to number of pixels
    green_area_threshold = 2e4 / cell_size**2
    hm_raster_path = os.path.join(
        args['workspace_dir'], 'hm%s.tif' % file_suffix)
    hm_task = task_graph.add_task(
        func=pygeoprocessing.raster_calculator,
        args=([
            (cc_raster_path, 1),
            (green_area_sum_raster_path, 1),
            (cc_park_raster_path, 1),
            (green_area_threshold, 'raw'),
            ], hm_op, hm_raster_path, gdal.GDT_Float32, TARGET_NODATA),
        target_path_list=[hm_raster_path],
        dependent_task_list=[cc_task, green_area_sum_task, cc_park_task],
        task_name='calculate HM index')

    t_air_nomix_raster_path = os.path.join(
        intermediate_dir, 'T_air_nomix%s.tif' % file_suffix)
    t_air_nomix_task = task_graph.add_task(
        func=pygeoprocessing.raster_calculator,
        args=([(t_ref_raw, 'raw'),
               (hm_raster_path, 1),
               (uhi_max_raw, 'raw')],
              calc_t_air_nomix_op, t_air_nomix_raster_path, gdal.GDT_Float32,
              TARGET_NODATA),
        target_path_list=[t_air_nomix_raster_path],
        dependent_task_list=[hm_task, align_task],
        task_name='calculate T air nomix')

    decay_kernel_distance = int(numpy.round(
        t_air_average_radius_raw / cell_size))
    t_air_raster_path = os.path.join(
        intermediate_dir, 'T_air%s.tif' % file_suffix)
    t_air_task = task_graph.add_task(
        func=convolve_2d_by_exponential,
        args=(
            decay_kernel_distance,
            t_air_nomix_raster_path,
            t_air_raster_path),
        target_path_list=[t_air_raster_path],
        dependent_task_list=[t_air_nomix_task],
        task_name='calculate T air')

    intermediate_aoi_vector_path = os.path.join(
        intermediate_dir, 'reprojected_aoi%s.shp' % file_suffix)
    intermediate_uhi_result_vector_task = task_graph.add_task(
        func=pygeoprocessing.reproject_vector,
        args=(
            args['aoi_vector_path'], lulc_raster_info['projection'],
            intermediate_aoi_vector_path),
        kwargs={'driver_name': 'ESRI Shapefile'},
        target_path_list=[intermediate_aoi_vector_path],
        task_name='reproject and label aoi')

    cc_aoi_stats_pickle_path = os.path.join(
        intermediate_dir, 'cc_ref_aoi_stats.pickle')
    _ = task_graph.add_task(
        func=pickle_zonal_stats,
        args=(
            intermediate_aoi_vector_path,
            cc_raster_path, cc_aoi_stats_pickle_path),
        target_path_list=[cc_aoi_stats_pickle_path],
        dependent_task_list=[cc_task, intermediate_uhi_result_vector_task],
        task_name='pickle cc ref stats')

    t_air_aoi_stats_pickle_path = os.path.join(
        intermediate_dir, 't_air_aoi_stats.pickle')
    _ = task_graph.add_task(
        func=pickle_zonal_stats,
        args=(
            intermediate_aoi_vector_path,
            t_air_raster_path, t_air_aoi_stats_pickle_path),
        target_path_list=[t_air_aoi_stats_pickle_path],
        dependent_task_list=[t_air_task, intermediate_uhi_result_vector_task],
        task_name='pickle t-air over stats over AOI')

    wbgt_stats_pickle_path = None
    light_loss_stats_pickle_path = None
    heavy_loss_stats_pickle_path = None
    energy_consumption_vector_path = None
    if bool(args['do_valuation']):
        LOGGER.info('Starting valuation')
        # work productivity
        wbgt_raster_path = os.path.join(
            intermediate_dir, 'wbgt%s.tif' % file_suffix)
        wbgt_task = task_graph.add_task(
            func=calculate_wbgt,
            args=(
                float(args['avg_rel_humidity']), t_air_raster_path,
                wbgt_raster_path),
            target_path_list=[wbgt_raster_path],
            dependent_task_list=[t_air_task],
            task_name='vapor pressure')

        light_work_loss_raster_path = os.path.join(
            intermediate_dir,
            'light_work_loss_percent%s.tif' % file_suffix)
        heavy_work_loss_raster_path = os.path.join(
            intermediate_dir,
            'heavy_work_loss_percent%s.tif' % file_suffix)

        loss_task_path_map = {}
        for loss_type, temp_map, loss_raster_path in [
                # Breaks here are described in the UG chapter and are the
                # result of a literature review.
                ('light', [31.5, 32.0, 32.5], light_work_loss_raster_path),
                ('heavy', [27.5, 29.5, 31.5], heavy_work_loss_raster_path)]:
            work_loss_task = task_graph.add_task(
                func=map_work_loss,
                args=(temp_map, wbgt_raster_path, loss_raster_path),
                target_path_list=[loss_raster_path],
                dependent_task_list=[wbgt_task],
                task_name='work loss: %s' % os.path.basename(loss_raster_path))
            loss_task_path_map[loss_type] = (work_loss_task, loss_raster_path)

        intermediate_building_vector_path = os.path.join(
            intermediate_dir,
            'reprojected_buildings%s.shp' % file_suffix)
        intermediate_building_vector_task = task_graph.add_task(
            func=pygeoprocessing.reproject_vector,
            args=(
                args['building_vector_path'], lulc_raster_info['projection'],
                intermediate_building_vector_path),
            kwargs={'driver_name': 'ESRI Shapefile'},
            target_path_list=[intermediate_building_vector_path],
            task_name='reproject building vector')

        # zonal stats over buildings for t_air
        t_air_stats_pickle_path = os.path.join(
            intermediate_dir, 't_air_stats.pickle')
        pickle_t_air_task = task_graph.add_task(
            func=pickle_zonal_stats,
            args=(
                intermediate_building_vector_path,
                t_air_raster_path, t_air_stats_pickle_path),
            target_path_list=[t_air_stats_pickle_path],
            dependent_task_list=[
                t_air_task, intermediate_building_vector_task],
            task_name='pickle t-air stats over buildings')

        energy_consumption_vector_path = os.path.join(
            args['workspace_dir'], 'buildings_with_stats%s.shp' % file_suffix)
        _ = task_graph.add_task(
            func=calculate_energy_savings,
            args=(
                t_air_stats_pickle_path, t_ref_raw,
                uhi_max_raw, args['energy_consumption_table_path'],
                intermediate_building_vector_path,
                energy_consumption_vector_path),
            target_path_list=[energy_consumption_vector_path],
            dependent_task_list=[
                pickle_t_air_task, intermediate_building_vector_task],
            task_name='calculate energy savings task')

        # pickle WBGT
        wbgt_stats_pickle_path = os.path.join(
            intermediate_dir, 'wbgt_stats.pickle')
        _ = task_graph.add_task(
            func=pickle_zonal_stats,
            args=(
                intermediate_aoi_vector_path,
                wbgt_raster_path, wbgt_stats_pickle_path),
            target_path_list=[wbgt_stats_pickle_path],
            dependent_task_list=[
                wbgt_task, intermediate_uhi_result_vector_task],
            task_name='pickle WBgt stats')
        # pickle light loss
        light_loss_stats_pickle_path = os.path.join(
            intermediate_dir, 'light_loss_stats.pickle')
        _ = task_graph.add_task(
            func=pickle_zonal_stats,
            args=(
                intermediate_aoi_vector_path,
                loss_task_path_map['light'][1], light_loss_stats_pickle_path),
            target_path_list=[light_loss_stats_pickle_path],
            dependent_task_list=[
                loss_task_path_map['light'][0],
                intermediate_uhi_result_vector_task],
            task_name='pickle light_loss stats')

        heavy_loss_stats_pickle_path = os.path.join(
            intermediate_dir, 'heavy_loss_stats.pickle')
        _ = task_graph.add_task(
            func=pickle_zonal_stats,
            args=(
                intermediate_aoi_vector_path,
                loss_task_path_map['heavy'][1], heavy_loss_stats_pickle_path),
            target_path_list=[heavy_loss_stats_pickle_path],
            dependent_task_list=[
                loss_task_path_map['heavy'][0],
                intermediate_uhi_result_vector_task],
            task_name='pickle heavy_loss stats')

    # final reporting can't be done until everything else is complete so
    # stop here
    task_graph.join()

    target_uhi_vector_path = os.path.join(
        args['workspace_dir'], 'uhi_results%s.shp' % file_suffix)
    _ = task_graph.add_task(
        func=calculate_uhi_result_vector,
        args=(
            intermediate_aoi_vector_path,
            t_ref_raw, t_air_aoi_stats_pickle_path,
            cc_aoi_stats_pickle_path,
            wbgt_stats_pickle_path,
            light_loss_stats_pickle_path,
            heavy_loss_stats_pickle_path,
            energy_consumption_vector_path,
            target_uhi_vector_path),
        target_path_list=[target_uhi_vector_path],
        task_name='calculate uhi results')

    task_graph.close()
    task_graph.join()
    LOGGER.info('Urban Cooling Model complete.')


def calculate_uhi_result_vector(
        base_aoi_path, t_ref_val, t_air_stats_pickle_path,
        cc_stats_pickle_path,
        wbgt_stats_pickle_path,
        light_loss_stats_pickle_path,
        heavy_loss_stats_pickle_path,
        energy_consumption_vector_path, target_uhi_vector_path):
    """Summarize UHI results.

    Output vector will have fields with attributes summarizing:
        * average cc value
        * average temperature value
        * average temperature anomaly
        * avoided energy consumption

    Args:
        base_aoi_path (str): path to AOI vector.
        t_ref_val (float): reference temperature.
        wbgt_stats_pickle_path (str): path to pickled zonal stats for wbgt.
            Can be None if no valuation occurred.
        light_loss_stats_pickle_path (str): path to pickled zonal stats for
            light work loss. Can be None if no valuation occurred.
        heavy_loss_stats_pickle_path (str): path to pickled zonal stats for
            heavy work loss. Can be None if no valuation occurred.
        energy_consumption_vector_path (str): path to vector that contains
            building footprints with the field 'energy_sav'. Can be None
            if no valuation occurred.
        target_uhi_vector_path (str): path to UHI vector created for result.
            Will contain the fields:
                * avg_cc
                * avg_tmp_an
                * avd_eng_cn
                * average WBGT
                * average light loss work
                * average heavy loss work

    Returns:
        None.

    """
    LOGGER.info(
        "Calculate UHI summary results %s", os.path.basename(
            target_uhi_vector_path))

    LOGGER.info("Loading t_air_stats")
    with open(t_air_stats_pickle_path, 'rb') as t_air_stats_pickle_file:
        t_air_stats = pickle.load(t_air_stats_pickle_file)
    LOGGER.info("Loading cc_stats")
    with open(cc_stats_pickle_path, 'rb') as cc_stats_pickle_file:
        cc_stats = pickle.load(cc_stats_pickle_file)

    wbgt_stats = None
    if wbgt_stats_pickle_path:
        LOGGER.info("Loading wbgt_stats")
        with open(wbgt_stats_pickle_path, 'rb') as wbgt_stats_pickle_file:
            wbgt_stats = pickle.load(wbgt_stats_pickle_file)

    light_loss_stats = None
    if light_loss_stats_pickle_path:
        LOGGER.info("Loading light_loss_stats")
        with open(light_loss_stats_pickle_path, 'rb') as (
                light_loss_stats_pickle_file):
            light_loss_stats = pickle.load(light_loss_stats_pickle_file)

    heavy_loss_stats = None
    if heavy_loss_stats_pickle_path:
        LOGGER.info("Loading heavy_loss_stats")
        with open(heavy_loss_stats_pickle_path, 'rb') as (
                heavy_loss_stats_pickle_file):
            heavy_loss_stats = pickle.load(heavy_loss_stats_pickle_file)

    base_aoi_vector = gdal.OpenEx(base_aoi_path, gdal.OF_VECTOR)
    shapefile_driver = gdal.GetDriverByName('ESRI Shapefile')
    try:
        # Can't make a shapefile on top of an existing one
        os.remove(target_uhi_vector_path)
    except FileNotFoundError:
        pass

    LOGGER.info("Creating %s", os.path.basename(target_uhi_vector_path))
    shapefile_driver.CreateCopy(
        target_uhi_vector_path, base_aoi_vector)
    base_aoi_vector = None
    target_uhi_vector = gdal.OpenEx(
        target_uhi_vector_path, gdal.OF_VECTOR | gdal.GA_Update)
    target_uhi_layer = target_uhi_vector.GetLayer()

    for field_id in [
            'avg_cc', 'avg_tmp_v', 'avg_tmp_an', 'avd_eng_cn', 'avg_wbgt_v',
            'avg_ltls_v', 'avg_hvls_v']:
        target_uhi_layer.CreateField(ogr.FieldDefn(field_id, ogr.OFTReal))

    # I don't really like having two of the same conditions (one here and one
    # in the for feature in target_uhi_layer loop), but if the user has
    # multiple AOI features, we shouldn't have to rebuild the buildings spatial
    # index every time.
    if energy_consumption_vector_path:
        energy_consumption_vector = gdal.OpenEx(
            energy_consumption_vector_path, gdal.OF_VECTOR)
        energy_consumption_layer = energy_consumption_vector.GetLayer()

        LOGGER.info('Parsing building footprint geometry')
        building_shapely_polygon_lookup = dict(
            (poly_feat.GetFID(),
             shapely.wkb.loads(poly_feat.GetGeometryRef().ExportToWkb()))
            for poly_feat in energy_consumption_layer)

        LOGGER.info("Constructing building footprint spatial index")
        poly_rtree_index = rtree.index.Index(
            [(poly_fid, poly.bounds, None)
             for poly_fid, poly in
             building_shapely_polygon_lookup.items()])

    target_uhi_layer.StartTransaction()
    for feature in target_uhi_layer:
        feature_id = feature.GetFID()
        if feature_id in cc_stats and cc_stats[feature_id]['count'] > 0:
            mean_cc = (
                cc_stats[feature_id]['sum'] / cc_stats[feature_id]['count'])
            feature.SetField('avg_cc', mean_cc)
        mean_t_air = None
        if feature_id in t_air_stats and t_air_stats[feature_id]['count'] > 0:
            mean_t_air = (
                t_air_stats[feature_id]['sum'] /
                t_air_stats[feature_id]['count'])
            feature.SetField('avg_tmp_v', mean_t_air)

        if mean_t_air:
            feature.SetField(
                'avg_tmp_an', mean_t_air-t_ref_val)

        if wbgt_stats and feature_id in wbgt_stats and (
                wbgt_stats[feature_id]['count'] > 0):
            wbgt = (
                wbgt_stats[feature_id]['sum'] /
                wbgt_stats[feature_id]['count'])
            feature.SetField('avg_wbgt_v', wbgt)

        if light_loss_stats and feature_id in light_loss_stats and (
                light_loss_stats[feature_id]['count'] > 0):
            light_loss = (
                light_loss_stats[feature_id]['sum'] /
                light_loss_stats[feature_id]['count'])
            LOGGER.debug("Average light loss: %s", light_loss)
            feature.SetField('avg_ltls_v', float(light_loss))

        if heavy_loss_stats and feature_id in heavy_loss_stats and (
                heavy_loss_stats[feature_id]['count'] > 0):
            heavy_loss = (
                heavy_loss_stats[feature_id]['sum'] /
                heavy_loss_stats[feature_id]['count'])
            LOGGER.debug("Average heavy loss: %s", heavy_loss)
            feature.SetField('avg_hvls_v', float(heavy_loss))

        if energy_consumption_vector_path:
            aoi_geometry = feature.GetGeometryRef()
            aoi_shapely_geometry = shapely.wkb.loads(
                aoi_geometry.ExportToWkb())
            aoi_shapely_geometry_prep = shapely.prepared.prep(
                aoi_shapely_geometry)
            avd_eng_cn = 0.0
            for building_id in poly_rtree_index.intersection(
                    aoi_shapely_geometry.bounds):
                if aoi_shapely_geometry_prep.intersects(
                        building_shapely_polygon_lookup[building_id]):
                    energy_consumption_value = (
                        energy_consumption_layer.GetFeature(
                            building_id).GetField('energy_sav'))
                    if energy_consumption_value:
                        # this step lets us skip values that might be in
                        # nodata ranges that we can't help.
                        avd_eng_cn += float(
                            energy_consumption_value)
            feature.SetField('avd_eng_cn', avd_eng_cn)

        target_uhi_layer.SetFeature(feature)
    target_uhi_layer.CommitTransaction()


def calculate_energy_savings(
        t_air_stats_pickle_path, t_ref_raw, uhi_max,
        energy_consumption_table_path, base_building_vector_path,
        target_building_vector_path):
    """Calculate energy savings.

    Energy savings is calculated from equations 8 or 9 in the User's Guide
    (depending on whether a cost has been provided in the energy consumption
    table).

    Args:
        t_air_stats_pickle_path (str): path to t_air zonal stats indexed by
            FID.
        t_ref_raw (float): single value for Tref.
        uhi_max (float): UHI max parameter from documentation.
        energy_consumption_table_path (str): path to energy consumption table
            that contains at least the columns 'type', and 'consumption'.  If
            the table also contains a 'cost' column, the output energy
            savings field will be multiplied by the floating-point cost
            provided in the 'cost' column.
        base_building_vector_path (str): path to existing vector to copy for
            the target vector that contains at least the field 'type'.
        target_building_vector_path (str): path to target vector that
            will contain the additional field 'energy_sav' calculated as
            ``consumption.increase(b) * ((T_(air,MAX)  - T_(air,i)))``.

    Return:
        None.

    """
    LOGGER.info(
        "Calculate energy savings for %s", target_building_vector_path)
    LOGGER.info("Loading t_air_stats")
    with open(t_air_stats_pickle_path, 'rb') as t_air_stats_pickle_file:
        t_air_stats = pickle.load(t_air_stats_pickle_file)

    base_building_vector = gdal.OpenEx(
        base_building_vector_path, gdal.OF_VECTOR)
    shapefile_driver = gdal.GetDriverByName('ESRI Shapefile')
    LOGGER.info("Creating %s", os.path.basename(target_building_vector_path))
    try:
        # can't make a shapefile on top of an existing one
        os.remove(target_building_vector_path)
    except OSError:
        pass
    shapefile_driver.CreateCopy(
        target_building_vector_path, base_building_vector)
    base_building_vector = None
    target_building_vector = gdal.OpenEx(
        target_building_vector_path, gdal.OF_VECTOR | gdal.GA_Update)
    target_building_layer = target_building_vector.GetLayer()
    target_building_layer.CreateField(
        ogr.FieldDefn('energy_sav', ogr.OFTReal))
    target_building_layer.CreateField(
        ogr.FieldDefn('mean_t_air', ogr.OFTReal))

    # Find the index of the 'type' column in a case-insensitive way.
    # We can assume that the field exists because we're checking for it in
    # validation as defined in ARGS_SPEC.
    fieldnames = [field.GetName().lower()
                  for field in target_building_layer.schema]
    type_field_index = fieldnames.index('type')

    energy_consumption_table = utils.build_lookup_from_csv(
        energy_consumption_table_path, 'type', to_lower=True,
        warn_if_missing=True)

    target_building_layer.StartTransaction()
    last_time = time.time()
    for target_index, target_feature in enumerate(target_building_layer):
        last_time = _invoke_timed_callback(
            last_time, lambda: LOGGER.info(
                "energy savings approximately %.1f%% complete ",
                100.0 * float(target_index + 1) /
                target_building_layer.GetFeatureCount()),
            _LOGGING_PERIOD)

        feature_id = target_feature.GetFID()
        t_air_mean = None
        if feature_id in t_air_stats:
            pixel_count = float(t_air_stats[feature_id]['count'])
            if pixel_count > 0:
                t_air_mean = float(
                    t_air_stats[feature_id]['sum'] / pixel_count)
                target_feature.SetField('mean_t_air', t_air_mean)

        # Building type should be an integer and has to match the building
        # types in the energy consumption table.
        target_type = target_feature.GetField(int(type_field_index))
        if target_type not in energy_consumption_table:
            target_building_layer.CommitTransaction()
            target_building_layer = None
            target_building_vector = None
            raise ValueError(
                "Encountered a building 'type' of: '%s' in "
                "FID: %d in the building vector layer that has no "
                "corresponding entry in the energy consumption table "
                "at %s" % (
                    target_type, target_feature.GetFID(),
                    energy_consumption_table_path))

        consumption_increase = float(
            energy_consumption_table[target_type]['consumption'])

        # Load building cost if we can, but don't adjust the value if the cost
        # column is not there.
        # NOTE: if the user has an empty column value but the 'cost' column
        # exists, this will raise an error.
        try:
            building_cost = float(
                energy_consumption_table[target_type]['cost'])
        except KeyError:
            # KeyError when cost column not present.
            building_cost = 1.0

        # Calculate Equation 7: Energy Savings.
        # We'll only calculate energy savings if there were polygons with valid
        # stats that could be aggregated from t_air_mean.
        if t_air_mean:
            savings = (
                consumption_increase * (
                    t_ref_raw - t_air_mean + uhi_max) * building_cost)
            target_feature.SetField('energy_sav', savings)

        target_building_layer.SetFeature(target_feature)
    target_building_layer.CommitTransaction()
    target_building_layer.SyncToDisk()


def pickle_zonal_stats(
        base_vector_path, base_raster_path, target_pickle_path):
    """Calculate Zonal Stats for a vector/raster pair and pickle result.

    Args:
        base_vector_path (str): path to vector file
        base_raster_path (str): path to raster file to aggregate over.
        target_pickle_path (str): path to desired target pickle file that will
            be a pickle of the pygeoprocessing.zonal_stats function.

    Returns:
        None.

    """
    LOGGER.info('Taking zonal statistics of %s over %s',
                base_vector_path, base_raster_path)
    zonal_stats = pygeoprocessing.zonal_statistics(
        (base_raster_path, 1), base_vector_path,
        polygons_might_overlap=True)
    with open(target_pickle_path, 'wb') as pickle_file:
        pickle.dump(zonal_stats, pickle_file)


def calc_t_air_nomix_op(t_ref_val, hm_array, uhi_max):
    """Calculate air temperature T_(air,i)=T_ref+(1-HM_i)*UHI_max.

    Args:
        t_ref_val (float): The user-defined reference air temperature in
            degrees Celsius.
        hm_array (numpy.ndarray): The calculated Heat Mitigation index from
            equation 5 in the User's Guide.
        uhi_max (float): The user-defined maximum UHI magnitude.

    Returns:
        A numpy array with the same dimensions as ``hm_array`` with the
        calculated T_air_nomix values.

    """
    result = numpy.empty(hm_array.shape, dtype=numpy.float32)
    result[:] = TARGET_NODATA
    valid_mask = ~numpy.isclose(hm_array, TARGET_NODATA)
    result[valid_mask] = t_ref_val + (1-hm_array[valid_mask]) * uhi_max
    return result


def calc_cc_op_factors(
        shade_array, albedo_array, eti_array, cc_weight_shade,
        cc_weight_albedo, cc_weight_eti):
    """Calculate the cooling capacity index using weighted factors.

    Args:
        shade_array (numpy.ndarray): array of shade index values 0..1
        albedo_array (numpy.ndarray): array of albedo index values 0..1
        eti_array (numpy.ndarray): array of evapotransipration index values
            0..1
        cc_weight_shade (float): 0..1 weight to apply to shade
        cc_weight_albedo (float): 0..1 weight to apply to albedo
        cc_weight_eti (float): 0..1 weight to apply to eti

    Returns:
         CC_i = ((cc_weight_shade * shade) +
                 (cc_weight_albedo * albedo) +
                 (cc_weight_eti * ETI))

    """
    result = numpy.empty(shade_array.shape, dtype=numpy.float32)
    result[:] = TARGET_NODATA
    valid_mask = ~(
        numpy.isclose(shade_array, TARGET_NODATA) |
        numpy.isclose(albedo_array, TARGET_NODATA) |
        numpy.isclose(eti_array, TARGET_NODATA))
    result[valid_mask] = (
        cc_weight_shade*shade_array[valid_mask] +
        cc_weight_albedo*albedo_array[valid_mask] +
        cc_weight_eti*eti_array[valid_mask])
    return result


def calc_cc_op_intensity(intensity_array):
    """Calculate the cooling capacity index using building intensity.

    Args:
        intensity_array (numpy.ndarray): array of intensity values.

    Returns:
        A numpy array of ``1 - intensity_array``.

    """
    result = numpy.empty(intensity_array.shape, dtype=numpy.float32)
    result[:] = TARGET_NODATA
    valid_mask = ~numpy.isclose(intensity_array, TARGET_NODATA)
    result[valid_mask] = 1.0 - intensity_array[valid_mask]
    return result


def calc_eti_op(
        kc_array, kc_nodata, et0_array, et0_nodata, et_max, target_nodata):
    """Calculate ETI = (K_c * ET_0) / ET_max."""
    result = numpy.empty(kc_array.shape, dtype=numpy.float32)
    result[:] = target_nodata
    valid_mask = ~(
        numpy.isclose(kc_array, kc_nodata) |
        numpy.isclose(et0_array, et0_nodata))
    result[valid_mask] = (
        kc_array[valid_mask] * et0_array[valid_mask] / et_max)
    return result


def calculate_wbgt(
        avg_rel_humidity, t_air_raster_path, target_vapor_pressure_path):
    """Raster calculator op to calculate wet bulb globe temperature.

    Args:
        avg_rel_humidity (float): number between 0-100.
        t_air_raster_path (string): path to T air raster.
        target_vapor_pressure_path (string): path to target vapor pressure
            raster.

    Returns:
        WBGT_i  = 0.567 * T_(air,i)  + 0.393 * e_i  + 3.94

        where e_i:
            e_i  = RH/100*6.105*exp(17.27*T_air/(237.7+T_air))

    """
    LOGGER.info('Calculating WBGT')
    t_air_nodata = pygeoprocessing.get_raster_info(
        t_air_raster_path)['nodata'][0]

    def wbgt_op(avg_rel_humidity, t_air_array):
        wbgt = numpy.empty(t_air_array.shape, dtype=numpy.float32)
        valid_mask = ~numpy.isclose(t_air_array, t_air_nodata)
        wbgt[:] = TARGET_NODATA
        t_air_valid = t_air_array[valid_mask]
        e_i = (
            (avg_rel_humidity / 100.0) * 6.105 * numpy.exp(
                17.27 * (t_air_valid / (237.7 + t_air_valid))))
        wbgt[valid_mask] = 0.567 * t_air_valid + 0.393 * e_i + 3.94
        return wbgt

    pygeoprocessing.raster_calculator(
        [(avg_rel_humidity, 'raw'), (t_air_raster_path, 1)],
        wbgt_op, target_vapor_pressure_path, gdal.GDT_Float32,
        TARGET_NODATA)


def flat_disk_kernel(max_distance, kernel_filepath):
    """Create a flat disk  kernel.

    The raster created will be a tiled GeoTiff, with 256x256 memory blocks.

    Args:
        max_distance (int): The distance (in pixels) of the
            kernel's radius.
        kernel_filepath (string): The path to the file on disk where this
            kernel should be stored.  If this file exists, it will be
            overwritten.

    Returns:
        None

    """
    LOGGER.info('Creating a disk kernel of distance %s at %s',
                max_distance, kernel_filepath)
    kernel_size = int(numpy.round(max_distance * 2 + 1))

    driver = gdal.GetDriverByName('GTiff')
    kernel_dataset = driver.Create(
        kernel_filepath.encode('utf-8'), kernel_size, kernel_size, 1,
        gdal.GDT_Byte, options=[
            'BIGTIFF=IF_SAFER', 'TILED=YES', 'BLOCKXSIZE=256',
            'BLOCKYSIZE=256'])

    # Make some kind of geotransform and SRS. It doesn't matter what, but
    # having one will make GIS libraries behave better if it's all defined
    kernel_dataset.SetGeoTransform([0, 1, 0, 0, 0, -1])
    srs = osr.SpatialReference()
    srs.SetWellKnownGeogCS('WGS84')
    kernel_dataset.SetProjection(srs.ExportToWkt())

    kernel_band = kernel_dataset.GetRasterBand(1)
    kernel_band.SetNoDataValue(255)

    cols_per_block, rows_per_block = kernel_band.GetBlockSize()

    n_cols = kernel_dataset.RasterXSize
    n_rows = kernel_dataset.RasterYSize

    n_col_blocks = int(math.ceil(n_cols / float(cols_per_block)))
    n_row_blocks = int(math.ceil(n_rows / float(rows_per_block)))

    for row_block_index in range(n_row_blocks):
        row_offset = row_block_index * rows_per_block
        row_block_width = n_rows - row_offset
        if row_block_width > rows_per_block:
            row_block_width = rows_per_block

        for col_block_index in range(n_col_blocks):
            col_offset = col_block_index * cols_per_block
            col_block_width = n_cols - col_offset
            if col_block_width > cols_per_block:
                col_block_width = cols_per_block

            # Numpy creates index rasters as ints by default, which sometimes
            # creates problems on 32-bit builds when we try to add Int32
            # matrices to float64 matrices.
            row_indices, col_indices = numpy.indices((row_block_width,
                                                      col_block_width),
                                                     dtype=numpy.float)

            row_indices += numpy.float(row_offset - max_distance)
            col_indices += numpy.float(col_offset - max_distance)

            kernel_index_distances = numpy.hypot(
                row_indices, col_indices)
            kernel = kernel_index_distances < max_distance

            kernel_band.WriteArray(kernel, xoff=col_offset,
                                   yoff=row_offset)

    # Need to flush the kernel's cache to disk before opening up a new Dataset
    # object in interblocks()
    kernel_dataset.FlushCache()


def hm_op(cc_array, green_area_sum, cc_park_array, green_area_threshold):
    """Calculate HM.

        cc_array (numpy.ndarray): this is the raw cooling index mapped from
            landcover values.
        green_area_sum (numpy.ndarray): this is the sum of green space pixels
            pixels within the user defined area for green space.
        cc_park_array (numpy.ndarray): this is the exponentially decayed
            cooling index due to proximity of green space.
        green_area_threshold (float): a value used to determine how much
            area is required to trigger a green area overwrite.

    Returns:
        cc_array if green area < green_area_threshold or cc_park < cc array,
        otherwise cc_park array is returned.

    """
    result = numpy.empty(cc_array.shape, dtype=numpy.float32)
    result[:] = TARGET_NODATA
    valid_mask = ~(numpy.isclose(cc_array, TARGET_NODATA) &
                   numpy.isclose(cc_park_array, TARGET_NODATA))
    cc_mask = ((cc_array >= cc_park_array) |
               (green_area_sum < green_area_threshold))
    result[cc_mask & valid_mask] = cc_array[cc_mask & valid_mask]
    result[~cc_mask & valid_mask] = cc_park_array[~cc_mask & valid_mask]
    return result


def map_work_loss(
        work_temp_threshold_array, temperature_raster_path,
        work_loss_raster_path):
    """Map work loss due to temperature.

    Args:
        work_temp_threshold_array (list): list of 3 sorted floats indicating
            the thresholds for 25, 50, and 75% work loss.
        temperature_raster_path (string): path to temperature raster in the
            same units as `work_temp_threshold_array`.
        work_loss_raster_path (string): path to target raster that maps per
            pixel work loss percent.

    Returns:
        None.

    """
    LOGGER.info('Calculating work loss using thresholds: %s',
                work_temp_threshold_array)
    byte_target_nodata = 255

    def classify_to_percent_op(temperature_array):
        result = numpy.empty(temperature_array.shape)
        result[:] = byte_target_nodata
        valid_mask = ~numpy.isclose(temperature_array, TARGET_NODATA)
        result[
            valid_mask &
            (temperature_array < work_temp_threshold_array[0])] = 0
        result[
            valid_mask &
            (temperature_array >= work_temp_threshold_array[0]) &
            (temperature_array < work_temp_threshold_array[1])] = 25
        result[
            valid_mask &
            (temperature_array >= work_temp_threshold_array[1]) &
            (temperature_array < work_temp_threshold_array[2])] = 50
        result[
            valid_mask &
            (temperature_array >= work_temp_threshold_array[2])] = 75
        return result

    pygeoprocessing.raster_calculator(
        [(temperature_raster_path, 1)], classify_to_percent_op,
        work_loss_raster_path, gdal.GDT_Byte,
        nodata_target=byte_target_nodata)


def _invoke_timed_callback(
        reference_time, callback_lambda, callback_period):
    """Invoke callback if a certain amount of time has passed.

    This is a convenience function to standardize update callbacks from the
    module.

    Args:
        reference_time (float): time to base `callback_period` length from.
        callback_lambda (lambda): function to invoke if difference between
            current time and `reference_time` has exceeded `callback_period`.
        callback_period (float): time in seconds to pass until
            `callback_lambda` is invoked.

    Returns:
        `reference_time` if `callback_lambda` not invoked, otherwise the time
        when `callback_lambda` was invoked.

    """
    current_time = time.time()
    if current_time - reference_time > callback_period:
        callback_lambda()
        return current_time
    return reference_time


def convolve_2d_by_exponential(
        decay_kernel_distance, signal_raster_path,
        target_convolve_raster_path):
    """Convolve signal by an exponential decay of a given radius.

    Args:
        decay_kernel_distance (float): radius of 1/e cutoff of decay kernel
            raster in pixels.
        signal_rater_path (str): path to single band signal raster.
        target_convolve_raster_path (str): path to convolved raster.

    Returns:
        None.

    """
    LOGGER.info("Starting a convolution over %s with a decay "
                "distance of %s", signal_raster_path, decay_kernel_distance)
    temporary_working_dir = tempfile.mkdtemp(
        dir=os.path.dirname(target_convolve_raster_path))
    exponential_kernel_path = os.path.join(
        temporary_working_dir, 'exponential_decay_kernel.tif')
    utils.exponential_decay_kernel_raster(
        decay_kernel_distance, exponential_kernel_path)
    pygeoprocessing.convolve_2d(
        (signal_raster_path, 1), (exponential_kernel_path, 1),
        target_convolve_raster_path, working_dir=temporary_working_dir,
        ignore_nodata=True)
    shutil.rmtree(temporary_working_dir)


@validation.invest_validator
def validate(args, limit_to=None):
    """Validate args to ensure they conform to `execute`'s contract.

    Args:
        args (dict): dictionary of key(str)/value pairs where keys and
            values are specified in `execute` docstring.
        limit_to (str): (optional) if not None indicates that validation
            should only occur on the args[limit_to] value. The intent that
            individual key validation could be significantly less expensive
            than validating the entire `args` dictionary.

    Returns:
        list of ([invalid key_a, invalid_keyb, ...], 'warning/error message')
            tuples. Where an entry indicates that the invalid keys caused
            the error message in the second part of the tuple. This should
            be an empty list if validation succeeds.

    """
    validation_warnings = validation.validate(
        args, ARGS_SPEC['args'], ARGS_SPEC['args_with_spatial_overlap'])

    invalid_keys = validation.get_invalid_keys(validation_warnings)
    if ('biophysical_table_path' not in invalid_keys and
            'cc_method' not in invalid_keys):
        if args['cc_method'] == 'factors':
            extra_biophysical_keys = ['shade', 'albedo']
        else:
            # args['cc_method'] must be 'intensity'.
            # If args['cc_method'] isn't one of these two allowed values
            # ('intensity' or 'factors'), it'll be caught by
            # validation.validate due to the allowed values stated in
            # ARGS_SPEC.
            extra_biophysical_keys = ['building_intensity']

        required_keys = (
            extra_biophysical_keys +
            ARGS_SPEC['args']['biophysical_table_path'][
                'validation_options']['required_fields'][:])
        error_msg = validation.check_csv(
            args['biophysical_table_path'], required_fields=required_keys)
        if error_msg:
            validation_warnings.append((['biophysical_table_path'], error_msg))

    return validation_warnings
