from __future__ import division
import logging

import argparse
import datetime
from dateutil.parser import parse
import utils
import pickle
import json
import numpy as np
import hydroengine as hyd
import tqdm
import os


def main(argc):

    init_date = argc.init_date

    pp = utils.RasterParameterIO(argc.precip, masked=True)
    pp_affine = pp.transform
    pp_nodata = pp.nodata
    pp_data = pp.array.clip(min=0)

    tmin = utils.RasterParameterIO(argc.tmin, masked=True)
    tmin_affine = tmin.transform
    tmin_nodata = tmin.nodata
    tmin_data = tmin.array
    tmin_data[tmin_data != tmin_nodata] -= 273.15

    tmax = utils.RasterParameterIO(argc.tmax, masked=True)
    tmax_affine = tmax.transform
    tmax_nodata = tmax.nodata
    tmax_data = tmax.array
    tmax_data[tmax_data != tmax_nodata] -= 273.15

    hbv_pars = {}
    with open(argc.params) as json_file:
        pars = json.load(json_file)
        for key, value in pars.items():
            hbv_pars[key] = utils.RasterParameterIO(value, 1).array

    # Create base raster as template to write tiff outputs
    # base_map = utils.RasterParameterIO()

    # retrieve latitude of cells
    lon, lat = tmax_affine * np.indices(tmin_data[0, :, :].shape)[[1,0],:,:]

    # retrieve adjacency matrix
    graph = utils.ParseNetwork(argc.network_file)
    adj_net = graph.conn_matrix
    num_links = len(adj_net.index)

    # initiate hydrologic engine with empty storages
    swe = np.zeros_like(pp_data[0, :, :])
    pond = np.zeros_like(pp_data[0, :, :])
    sm = np.zeros_like(pp_data[0, :, :])
    soils = []
    Q = np.zeros(num_links)
    qold = np.zeros(num_links)

    # if restart flag on, initiate hydrologic engine and rewrite variables using pickled states from previous run
    if argc.restart:
        try:
            swe = pickle.load(open(os.path.join(argc.restart_if,'swe.pickled'), 'rb'))
            # swe = np.zeros_like(pp_data[0, :, :])
            pond = pickle.load(open(os.path.join(argc.restart_if,'pond.pickled'), 'rb'))
            sm = pickle.load(open(os.path.join(argc.restart_if,'sm.pickled'), 'rb'))
            soils = pickle.load(open(os.path.join(argc.restart_if,'soils.pickled'), 'rb'))
            Q = pickle.load(open(os.path.join(argc.restart_if,'streamflows.pickled'), 'rb'))
            qold = pickle.load(open(os.path.join(argc.restart_if, 'lateral_inflows.pickled'), 'rb'))
        except IOError as e:
            print("Unable to find initialization file %s. Initializing variable with empty storage" % e.filename)
        except pickle.PickleError as e:
            print("Unable to read file %s. Initializing variable with empty storage" % e.filename)



    """
    Creates the rainfall-runoff model object, the routing object and the model coupling objects
    """
    rr = hyd.HBV(86400, swe, pond, sm, soils, **hbv_pars)
    mc = hyd.Routing(adj_net, rr.dt)

    # creates mock coupler
    simulated_water_users = utils.coupling.StrawFarmCoupling(num_links)
    irr_ids = arr_land_use = 0
    if argc.econengine is not None:
        print("Economic module activated, generating water users and coupling objects... ")
        # Open water user object
        with open(argc.econengine[0]) as json_farms:
            farms = json.load(json_farms)

        # Open scenarios object
        with open(argc.econengine[1]) as json_scenarios:
            scenarios = json.load(json_scenarios)

        # retrieve the list of farms in the json input
        lst_farms = farms['farms']

        # Building the model coupling object and set up the farmer users
        coupler = utils.coupling.HydroEconCoupling(mc, lst_farms, pp_data[0, :, :], pp_affine)
        coupler.setup_farmer_user(argc.water_user_shapes[0], argc.water_user_shapes[1])

        print("Simulating water users... ")
        # simulates all users with loaded scenarios
        simulated_water_users = coupler.simulate_all_users(scenarios, argc.path_kf_info)

        arr_land_use = utils.RasterParameterIO(argc.fn_lu_raster)
        arr_land_use = np.squeeze(arr_land_use.array)
        irr_ids = tuple(argc.lu_irr_ids)

    ro_ts = []
    Q_ts = []
    up_res = []
    low_res = []
    diversions = []
    #qold = np.zeros(num_links)
    e = np.array(graph.get_parameter('e'))
    ks = np.array(graph.get_parameter('ks'))

    total_ts = pp_data.shape[0]

    if argc.num_time_steps_run is not None:
        total_ts = argc.num_time_steps_run

    with tqdm.tqdm(total=total_ts, unit='days') as pbar:

        for i in np.arange(total_ts):

            cur_date = (parse(init_date) + i * datetime.timedelta(seconds=rr.dt)).strftime("%Y%m%d")

            water_diversion, water_diversion_table, water_diversion_table_rates = \
                simulated_water_users.retrieve_water_diversion_per_node(cur_date)
            suppl_irr = simulated_water_users.retrieve_supplemental_irrigation_map(arr_land_use,
                                                                                   irr_ids,
                                                                                   water_diversion_table)

            # Calculate potential evapotranspiration
            pet = hyd.hamon_pe((tmin_data[i, :, :] + tmax_data[i, :, :]) * 0.5, lat, i)
            runoff, soils = rr.run_time_step(pp_data[i, :, :] + suppl_irr, tmax_data[i, :, :], tmin_data[i, :, :],
                                             pet, argc.basin_shp, affine=pp_affine, nodata=pp_nodata)
            # runoff[1] = runoff[-1] = 0

            qnew = np.array(runoff)
            water_diversion = water_diversion / rr.dt

            Q = mc.muskingum_routing(Q, ks, e, qnew, qold, water_diversion)
            qold = qnew #np.array(runoff)  # np.insert(runoff, 3, 0)

            ro_ts.append(runoff)
            Q_ts.append(Q)
            # retrieve the upper and lower reservoir information from array soils objects
            upr = np.array([i[1].upper_reservoir for i in soils])
            lowr = np.array([i[1].lower_reservoir for i in soils])
            up_res.append(upr)
            low_res.append(lowr)
            try:
                diversions.append(water_diversion.values)
            except AttributeError:
                diversions.append([0])

            # write to drive the states for the current time step

            latlon = np.array((lat.ravel(), lon.ravel()))
            rr.write_current_states(cur_date, ".tif", pp.write_array_to_geotiff, argc.hydro_maps_of)
            pbar.update()

        rr.pickle_current_states('./')
        # pickle current streamflows
        pickle.dump(Q, open(os.path.join(argc.restart_if, "streamflows.pickled"), "wb"))
        pickle.dump(qold, open(os.path.join(argc.restart_if, "lateral_inflows.pickled"), "wb"))
        utils.WriteOutputTimeSeries(adj_net, init_date, fname=os.path.join(argc.hydro_ts_of, r'streamflows.json')).write_json(Q_ts)
        utils.WriteOutputTimeSeries(adj_net, init_date, fname=os.path.join(argc.hydro_ts_of, r'upper_soil.json')).write_json(up_res)
        utils.WriteOutputTimeSeries(adj_net, init_date, fname=os.path.join(argc.hydro_ts_of, r'groundwater.json')).write_json(low_res)

        if argc.econengine is not None:
            print("Writing water users objects to drive... ")
            utils.WriteOutputTimeSeries(adj_net, init_date,
                                        fname=os.path.join(argc.hydro_ts_of, r'diversions.json')).write_json(diversions)
            # Open water user object
            simulated_water_users.save_farm_list_json(os.path.join(argc.econ_results_of, "Farm_data_out.json"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hydrologic engine')
    parser.add_argument('init_date', help='Simulation start date (mm/dd/yy)')
    parser.add_argument('-num_time_steps_run', help='Length of simulation (days). '
                                                    'If None (default), simulate all days on precipitation record',
                        required=False, type=int, default=None)
    parser.add_argument('precip', help='NetCDF file with daily precipitation (mm/day)')
    parser.add_argument('tmin', help='NetCDF file with minimum daily temperature (K)')
    parser.add_argument('tmax', help='file with maximum daily temperature(K)')
    parser.add_argument('params', help='json dictionary with names of parameter files (see documentation)')

    parser.add_argument('network_file', help='stream network, shapefile or geojson format')
    parser.add_argument('basin_shp', help='shapefile with subcatchments for each node')

    parser.add_argument('--restart', dest='restart', action='store_true')
    parser.add_argument('-hydro_maps_of', help='path to map results from hydrologic model', default='.')
    parser.add_argument('-hydro_ts_of', help='path to time series results from hydrologic model', default='.')
    parser.add_argument('-restart_if', help='path to restart pickle files', default='.')

    parser.add_argument('-econengine', required=False, default=None, nargs=2,
                        metavar=('fn_farm_data_json', 'fn_scenario_data_json'),
                        help="Activates the economic engine of agricultural production. ")

    parser.add_argument('--water_user_shapes', metavar=('fn_shapes', 'ID_field'), nargs=2, type=str,
                        help="filename of water user shapes (shp, geojson, etc) "
                        "and name of field to be used as user ID")

    parser.add_argument('--fn_lu_raster', type=str, help='filename of land use raster')
    parser.add_argument('--lu_irr_ids', nargs='+', type=int, help='sequence of integers identifying irrigation'
                                                                  ' land uses in fn_lu_raster')
    parser.add_argument('-econ_results_of', help='path to results from economic model', default='.')
    parser.add_argument('-path_kf_info', help='activate stochastic econ with path to kf_info files', default=None)

    # if __debug__:
        #     args = parser.parse_args("08/31/2012 precip_F2012-09-01_T2013-08-31.nc tempmin_F2012-09-01_T2013-08-31.nc"
        #             " tempmax_F2012-09-01_T2013-08-31.nc"
        #             " param_files_test.json rivout.shp subsout.shp "
        #             "-econengine Farms.json Scenario.json Counties.geojson ORIG_FID LCType_mt.tif (12,14)".split())
    # else:
    #     args = parser.parse_args()
    args = parser.parse_args()
    if args.econengine and (args.water_user_shapes is None or args.fn_lu_raster is None or args.lu_irr_ids is None):
        parser.error("Options --fn_water_user_shapes --fn_lu_raster, --lu_irr_ids "
                     "are required if -econengine argument is present")

    logging.basicConfig(filename='non_standard_output.log', level=logging.WARNING)

    main(args)
