""" Module Pressure

    v0 :    c. sooriyakumaran 2019

This module is used to load pressure data from the different types of Scanivalve pressure scanners. It contains
functions to compute different pressure coefficients, calibrate probes, and

This module contains the following functions:

    *  - returns the
    *
"""
# standard library
import os
import sys
import logging
import time
from dataclasses import dataclass
from dataclasses import field

# third-party site packages
import numpy as np
import matplotlib.pyplot as plt

# Custom Package files
import aiolos_fluid_dynamics.units as units
from aiolos_commissioning_tools import __version__
from aiolos_code_instrumentation.timer import timer
from aiolos_commissioning_tools.tunnel_conditions import wind_speed_from_pitot, wind_speed_algorithm

from aiolos_fluid_dynamics import fluid_dynamics_relationships as fluids
from aiolos_plotting import plot_pressures

log = logging.getLogger(__name__)

# Pressure measurement equipment (use SN as unique identifier)
ZOC334 = 334
ZOC335 = 335
ZOC732 = 732
DSA9214 = 9214
DSA10015 = 10015

pressure_scanner_types = {
    ZOC334:     'ZOC33x64',
    ZOC335:     'ZOC33x64',
    ZOC732:     'ZOC33x64',
    DSA9214:    'DSA3217x16',
    DSA10015:   'DSA3217x16'
}

pressure_scanner_names = {
    ZOC334:     'ZOC334',
    ZOC335:     'ZOC335',
    ZOC732:     'ZOC732',
    DSA9214:    'DSA3217',
    DSA10015:   'DSA3217'
}

pressure_scanner_ranges = {
    ZOC334:  10 * units.INCHES_H2O,  # 2488.4 Pa = 10 inches water
    ZOC335:  10 * units.INCHES_H2O,  # 2488.4 Pa = 10 inches water
    ZOC732:  20 * units.INCHES_H2O,  # 4976.8 Pa = 20 inches water
    DSA9214: 20 * units.INCHES_H2O,  # 4976.8 Pa = 20 inches water
    DSA10015:20 * units.INCHES_H2O   # 4976.8 Pa = 20 inches water
}

# pressure probes
AEROPROBE = 10
CEA = 20
UNITEDSENSOR = 30
AIRFLOW = 40

pressure_probe_ids = {
    'AEROPROBE': AEROPROBE,
    'CEA': CEA,
    'UNITEDSENSOR': UNITEDSENSOR,
    'United Sensor USNH-A-70': UNITEDSENSOR,
    'United Sensor USNH-A-633': UNITEDSENSOR,
    'AIRFLOW': AIRFLOW
}

pressure_probe_names = {
                        AEROPROBE: 'AEROPROBE',
                        CEA: 'CEA',
                        UNITEDSENSOR: 'UNITEDSENSOR',
                        AIRFLOW: 'AIRFLOW'}

pressure_probe_correction = {AEROPROBE: 1.0,
                             UNITEDSENSOR: 1.0,
                             AIRFLOW:  0.997
                             }


def add_scanner(scanner_id, scanner_name, scanner_range, scanner_type):
    pressure_scanner_names[scanner_id] = scanner_name
    pressure_scanner_names[scanner_name] = scanner_id
    pressure_scanner_ranges[scanner_id] = scanner_range
    pressure_scanner_types[scanner_id] = scanner_type


def add_probe(probe_id, probe_name):
    pressure_probe_names[probe_id] = probe_name
    pressure_probe_names[probe_name] = probe_id


@dataclass
class PneumaticProbe:
    id: int
    pitch: np.float64 = field(repr=False, default='')
    yaw: np.float64 = field(repr=False, default='')
    cal_file: str = field(repr=False, default='')
    correction: float = field(init=False)
    name: str = field(init=False)

    def __post_init__(self):
        try:
            self.name = pressure_probe_names[self.id]
            self.correction = pressure_probe_correction[self.id]
        except KeyError as err:
            log.error(err)


@dataclass
class PressureScanner:
    id: int
    ref: int = field(default=0)
    name: str = field(init=False)
    range: float = field(init=False)
    type: str = field(init=False)

    def __post_init__(self):
        try:
            self.name = pressure_scanner_names[self.id]
            self.range = pressure_scanner_ranges[self.id]
            self.type = pressure_scanner_types[self.id]
        except KeyError as err:
            err_msg = 'scanner id [%s] not defined. use add_scanner() method to set new scanner properties.' % err
            log.error(err_msg)
            raise err


@dataclass
class ScannerData:

    run_id: int
    scanner_id: int
    port_count: int
    frame_count: int
    ref: int
    scanner_name: str
    file_name: str = field(repr=False)
    pressure: np.ndarray = field(repr=False)
    temperature: np.ndarray = field(repr=False)
    port: np.ndarray = field(repr=False)
    frame: np.ndarray = field(repr=False)

    def plot_data(self, channels=[], subplots=8, save_path='', show_plots=True):
        plot_pressures.plot_channels(self, channels=channels, subplots=subplots, save_path=save_path, show_plots=show_plots)

    def plot_mean_data(self, channels=[], show_plots=True):
        plot_pressures.plot_mean_pressures(self, channels=channels, show_plots=show_plots)

@dataclass
class ScannerConnections:
    """
    pressure scanner port connections

    p can be any size.
        i.e. for boundary layer rakes p.size = 60
             for flow angles probe p.size = 4
    """
    ref: int
    pc1: int = field(default=0)
    pc2: int = field(default=0)
    pc3: int = field(default=0)
    pt: int = field(default=0)
    ps: int = field(default=0)
    p: np.ndarray = field(default='')


@dataclass
class BoundaryLayerData:
    run_id: int
    Ue: np.float64
    boundary_layer_thickness: np.float64
    displacement_thickness: np.float64
    momentum_thickness: np.float64
    shape_factor: np.float64
    z: np.ndarray = field(repr=False)
    po: np.ndarray = field(repr=False)
    ps: np.float64 = field(repr=False)
    u: np.ndarray = field(repr=False)

    def plot_data(self, show_plots=True):
        plot_pressures.plot_boundary_layer_data(self, show_plots=show_plots)


@dataclass
class AxialStaticPressureGradientData:
    run_id: int
    u_ref: np.float64
    x: np.ndarray = field(repr=False)
    u: np.ndarray = field(repr=False)
    q: np.ndarray = field(repr=False)
    cps: np.ndarray = field(repr=False)
    cpo: np.ndarray = field(repr=False)

    def plot_data(self, show_plots=True):
        fig, axs = plot_pressures.plot_axial_data(self, show_plots=show_plots)
        return fig, axs


@dataclass
class Traverse:
    """
    start:      x-location at the start of the run
    end:        x-location at the end of the run
    nsamples:   number of samples per data point (set = 1.0 if the run was continuous)

    """
    start: np.float64
    end: np.float64
    nsamples: int
    x_ref: np.float64


class BoundaryLayerRake:
    """
    this object requires an input parameter filename which contains a mapping between scanner port number and height. Note that scanner ports need not be sequential,
    they will not be used as indexes. If the connection mapping is not in meters, specify units with the parameter z_units.
    """
    def __init__(self, filename, z_units='m'):
        self.filename = filename
        self.units = z_units

        self.port, self.z = np.loadtxt(filename, dtype=None, delimiter='\t', unpack=True)
        self.z = self.z * units.__getattribute__(z_units.upper())

        self.port_count = np.shape(self.port)[0]
        self.max_z = np.max(self.z)
        self.min_Z = np.min(self.z)

    def __repr__(self):

        return '%s(filename=%r, port_count=%s, %r mm < z < %r mm' % \
               (self.__class__.__qualname__, self.filename, self.port_count, self.min_Z / units.MM, self.max_z / units.MM)


def load_scanner_data(data_file, scanner_id, reference_port=0, run_id=0):

    """

    :param data_file:       <str> path to data file containing pressure data
    :param scanner_id:      <int> serial number of the pressure scanner used. this will generate a local PressureScanner object.
    :param reference_port:  <int> the port/channel number which is monitoring the reference for drift. set to 0 if no port is connected to the reference port.
    :param run_id:          <int> a unique identifier useful for parallel processing.
    :return:

            SannerData object
    """
    _ = timer.Timer()

    scanner = PressureScanner(id=scanner_id, ref=reference_port)
    log.debug('Loading data file %s from %s' % (os.path.basename(data_file), scanner.__repr__()))

    if scanner.type == 'ZOC33x64':
        try:
            scanner_group, scanner_frame, scanner_module, scanner_port, scanner_data = np.loadtxt(data_file, unpack=True)
        except ValueError as err:
            log.warning(err)
            try:
                scanner_group, scanner_frame, scanner_module, scanner_port, scanner_data = np.loadtxt(data_file, delimiter=',', unpack=True)
            except (ValueError, IOError, FileNotFoundError) as err:
                log.error(err)
                log.error('could not load run %i [%s]' % (run_id, os.path.basename(data_file)))
                raise err
            else:
                log.warning('FIXED: Pressure data was "," delimited')

        frame_count = int(np.max(scanner_frame))  # number of frames (i.e. number of data samples)
        port_count = len(scanner_data)//frame_count  # port number is not sequential - calculate total number of ports
        log.debug('no. of frames = %03i, no. of ports = %02i' % (frame_count, port_count))

        temperature_data    = np.zeros(shape=(frame_count, port_count), dtype=np.float64)  # temperature is not output from the DSM
        pressure_data       = np.ndarray(shape=(frame_count, port_count), dtype=np.float64)
        frame_num           = np.ndarray(shape=(frame_count, ), dtype=int)
        port_num            = np.ndarray(shape=(port_count, ), dtype=int)

        for f in range(frame_count):
            for p in range(port_count):
                frame_num[f]        = scanner_frame[p + f*port_count]
                port_num[p]         = scanner_port[p + f*port_count]
                pressure_data[f, p] = scanner_data[p + f*port_count]

    elif scanner.type == "DSA3217x16":
        try:
            scanner_data = np.loadtxt(data_file, delimiter=',')

        except (ValueError, IOError, FileNotFoundError) as err:
            log.error(err)
            log.error('could not load run %i [%s]' % (run_id, os.path.basename(data_file)))
            raise err

        # number of channels, and data frames recorded
        frame_count = np.shape(scanner_data)[0]  # DSA outputs one row per frame
        port_count = 16  # fixed for DSA units
        log.debug('no. of frames = %03i, no. of ports = %02i' % (frame_count, port_count))

        temperature_data    = np.ndarray(shape=(frame_count, port_count), dtype=np.float64)
        pressure_data       = np.ndarray(shape=(frame_count, port_count), dtype=np.float64)
        frame_num           = np.ndarray(shape=(frame_count, ), dtype=int)
        port_num            = np.ndarray(shape=(port_count, ), dtype=int)

        for f in range(frame_count):
            for p in range(port_count):
                port_num[p]             = p+1  # DSA will always output all channels and we want to index from 1
                frame_num[f]            = scanner_data[f, 0] + 1 # keep frame numbering consistent with DSM outputs (i.e. index from 1)
                pressure_data[f, p]     = scanner_data[f, port_num[p]]
                temperature_data[f, p]  = scanner_data[f, port_num[p]+port_count]

    else:
        err_msg = "%s not a valid pressure scanner type. add new type with add_scanner() method" % scanner.__repr__()
        log.error(err_msg)
        raise ValueError(err_msg)

    if not reference_port == 0:
        # use reference_port to offset pressure data from other channels
        pressure_data[:, :] = pressure_data[:, :] - pressure_data[:, port_num == reference_port]

    uncertainty     = np.ndarray(shape=(port_count,))
    uncertainty_fs  = np.ndarray(shape=(port_count,))
    average         = np.ndarray(shape=(port_count,))

    for p in range(port_count):
        average[p] = np.mean(pressure_data[:, p], dtype=np.float64)
        uncertainty[p] = np.std(pressure_data[:, p]/average[p]) if np.abs(average[p]) > 0 else 0
        uncertainty_fs[p] = np.std(pressure_data[:, p]/scanner.range)
        log.debug('sigma(p) = %.4f %% (%.4f %% FS) on port %02i where mean(p) = %.4f Pa' % (uncertainty[p] * 100, uncertainty_fs[p] * 100, port_num[p], average[p]))

    max_uncertainty = np.max(uncertainty)
    max_fs = uncertainty_fs[np.where(uncertainty == max_uncertainty)[0]]
    max_port = port_num[np.where(uncertainty == max_uncertainty)[0]]
    max_avg = average[np.where(uncertainty == max_uncertainty)[0]]

    min_uncertainty = np.min(uncertainty[np.where(uncertainty > 0.0)])
    min_fs = uncertainty_fs[np.where(uncertainty == min_uncertainty)[0]]
    min_port = port_num[np.where(uncertainty == min_uncertainty)[0]]
    min_avg = average[np.where(uncertainty == min_uncertainty)[0]]

    mean_uncertainty = np.mean(uncertainty)

    log.debug('max sigma(p) = %.4f %% (%.4f %% FS) on port %02i where mean(p) = %.4f Pa' % (max_uncertainty*100, max_fs*100, max_port, max_avg))
    log.debug('min sigma(p) = %.4f %% (%.4f %% FS) on port %02i where mean(p) = %.4f Pa' % (min_uncertainty*100, min_fs*100, min_port, min_avg))
    log.debug('mean sigma(p) = %.4f %% ' % (mean_uncertainty*100))

    return ScannerData(
        run_id=run_id, scanner_id=scanner.id, scanner_name=scanner.name, port_count=port_count, frame_count=frame_count,
        pressure=pressure_data, temperature=temperature_data, port=port_num, frame=frame_num, ref=reference_port, file_name=data_file
    )


def calibrate_4_hole(pressure, alpha, beta, probe_id=1):
    """

    :param pressure:    <2D array<float>> size(numruns, 6) pressure data for each port + po $ ps
    :param alpha:       <1D array<float>> flow pitch angle data
    :param beta:        <1D array<float>> flow yaw angle data
    :param probe_id:    <int> probe ID
    :return:
            f
    """
    pass


def generate_probe_calibration_func(calibration_file, file_units='rad'):
    """

    :param calibration_file:    <str> path to file containing the calibration data
    :param file_units:          <str> == deg or degrees : specifies that the calibration file is in units of degrees
    :return:
        alpha:      <func> returns pitch angle of the flow relative to the probe axis
        beta:       <func> returns yaw angle of the flow relative to the probe axis

    notes:
        ws : wind speed [m/s]
        ao : probe pitch offset angle during calibration
        ma : probe sensitivity in pitch
        bo : probe yaw offset angle during calibration
        mb : probe sensitivity in yaw

    calibration file format
        whitespace separated columns of ws  ao  ma  bo  mb
        one row for each wind speed calibrated
    """
    ws, ao, ma, bo, mb = np.loadtxt(calibration_file, unpack=True)

    if file_units.lower() == 'deg' or file_units.lower() == 'degrees':
        bo = np.deg2rad(bo)         # bo [rad] => bo [°] * pi [rad] / 180 [°]
        ao = np.deg2rad(ao)         # ao [rad] => ao [°] * pi [rad] / 180 [°]

        ma = np.rad2deg(ma)         # ma [/rad]=> ma [/°] * 180 [°] / pi [rad]
        mb = np.rad2deg(mb)         # mb [/rad]=> mb [/°] * 180 [°] / pi [rad]

    def alpha(cp, u):
        m = np.interp(u, ws, ma)    # linear interpolation between wind speeds in calibration
        b = np.interp(u, ws, ao)    # linear interpolation between wind speeds in calibration
        return cp / m - b           # returns alpha in [rad]

    def beta(cp, u):
        m = np.interp(u, ws, mb)    # linear interpolation between wind speeds in calibration
        b = np.interp(u, ws, bo)    # linear interpolation between wind speeds in calibration
        return cp / m - b           # returns beta in [rad]

    return alpha, beta


def process_boundary_layer_data(run_id, scanner_data, tunnel_data, scanner_channels, rake, probe):

    # rows or axis = 0 is the raw samples form the scanner
    # cols or axis = 1 is the port number

    # process scanner data: the .squeeze() method removes the second dimension of size 1.
    # i.e. ps.shape=(scanner_data.frame_count,) not (scanner_data.frame_count, 1)

    pc1 = scanner_data.pressure[:, scanner_data.port == scanner_channels.pc1].mean()
    pc2 = scanner_data.pressure[:, scanner_data.port == scanner_channels.pc2].mean()
    pc3 = scanner_data.pressure[:, scanner_data.port == scanner_channels.pc3].mean()
    pt  = scanner_data.pressure[:, scanner_data.port == scanner_channels.pt].mean()
    ps  = scanner_data.pressure[:, scanner_data.port == scanner_channels.ps].mean()

    # allocate arrays for the rake pitot tubes and heights.
    po = np.ndarray(shape=scanner_channels.p.shape, dtype=np.float64)
    z  = np.ndarray(shape=scanner_channels.p.shape, dtype=np.float64)

    for i, port in enumerate(scanner_channels.p):
        po[i] = scanner_data.pressure[:, scanner_data.port == port].mean()
        z[i]  = rake.z[rake.port == port]

    # sort the rake Pitot pressures, and heights
    po = po[z.argsort(axis=0)]
    z  = z[z.argsort(axis=0)]

    # todo: find a better way to handle units - i.e. convert while loading data in load_tunnel_data()
    # process tunnel data
    pabs = np.mean(tunnel_data.pabs) * units.KPA
    total_temperature = units.celcius_to_kelvin(np.mean(tunnel_data.total_temperature))
    dew_point_temperature = units.celcius_to_kelvin(np.mean(tunnel_data.dewpoint))

    # calculate wind speed
    u = wind_speed_from_pitot(po, ps, pabs, probe.correction, total_temperature, dew_point_temperature)
    u_e = wind_speed_from_pitot(pt, ps, pabs, probe.correction, total_temperature, dew_point_temperature)

    # calculate boundary layer parameters
    boundary_layer_thickness = fluids.boundary_layer_thickness(z, u, u_e)
    displacement_thickness = fluids.dispacement_thickness(z, u, u_e)
    momentum_thickness = fluids.momentum_thickness(z, u, u_e)
    shape_factor = displacement_thickness / momentum_thickness

    return BoundaryLayerData(
        run_id=run_id, z=z, po=po, ps=ps, u=u, Ue=u_e, boundary_layer_thickness=boundary_layer_thickness,
        displacement_thickness=displacement_thickness,  momentum_thickness=momentum_thickness, shape_factor=shape_factor
    )


# todo: this is the only function in this module that requires wind speed calibration. How else could the reference velocity be determined?
def process_aspg_data(run_id, scanner_data, tunnel_data, scanner_channels, probe, traverse, fkp, fkq):
    """
        This function computes the local total and static pressure coefficients for an axial
        static pressure gradient test.

    :param run_id:
    :param scanner_data:
    :param tunnel_data:
    :param scanner_channels:
    :param probe:
    :param traverse:
    :return:
    """
    #
    log.debug("processing ASPG data for run %i" % run_id)
    # initially define x based on the total file since if the file is truncated because the number of samples for
    # each point result in all points being used, we don't want to skew the x data.
    x = np.linspace(traverse.start, traverse.end, scanner_data.frame_count)
    x_ref = x[x<=traverse.x_ref][0]
    # traversr.nsamples = number of samples per point == 1 for continuous runs
    # scanner_data.frame_count = number of points per data file
    # npoints = scanner_data.frame_count / traverse.nsamples

    npoints = np.int64(np.floor(scanner_data.frame_count / traverse.nsamples))

    po = np.array([np.mean(scanner_data.pressure[point*traverse.nsamples:(point+1)*traverse.nsamples, scanner_data.port == scanner_channels.pt]) for point in range(npoints)])
    ps = np.array([np.mean(scanner_data.pressure[point*traverse.nsamples:(point+1)*traverse.nsamples, scanner_data.port == scanner_channels.ps]) for point in range(npoints)])
    x = np.array([np.mean(x[point*traverse.nsamples:(point+1)*traverse.nsamples]) for point in range(npoints)])

    # process tunnel data
    dp = np.mean(scanner_data.pressure[:, scanner_data.port == scanner_channels.pc1] - scanner_data.pressure[:, scanner_data.port == scanner_channels.pc2])/units.PSF # todo remove unit conversion
    pabs = np.mean(tunnel_data.pabs) * units.KPA
    p_ref = fkp(dp)*dp
    Po_ref = fkq(dp)*dp + p_ref

    total_temperature = units.celcius_to_kelvin(np.mean(tunnel_data.total_temperature))
    dew_point_temperature = units.celcius_to_kelvin(np.mean(tunnel_data.dewpoint))

    # calculate wind speed
    u = wind_speed_from_pitot(po, ps, pabs, probe.correction, total_temperature, dew_point_temperature)
    u_ref = wind_speed_algorithm(dp=dp, absolute_pressure=pabs, total_temperature=total_temperature, dew_point=dew_point_temperature, fkp=fkp, fkq=fkq)

    q_ref = fluids.dynamic_pressure(p=pabs+p_ref, M=fluids.Mach_number(Po=pabs + Po_ref, p=pabs+p_ref))

    cps_ref = (ps[x == x_ref] - p_ref) / q_ref
    cps = ((ps - p_ref) / q_ref)  - cps_ref
    cpo = (po - ps) / q_ref

    return AxialStaticPressureGradientData(
        run_id=run_id, x=x, cps=cps, cpo=cpo, q=q_ref, u=u, u_ref=u_ref
    )


def main():
    """ Main function to call when this module is executed directly on a list of input data files"""
    log.setLevel(logging.DEBUG)

    fmt = logging.Formatter('%(asctime)s <%(levelname)s> [%(module)s.%(funcName)s]: %(message)s')
    strm_handler = logging.StreamHandler()
    strm_handler.setLevel(logging.DEBUG)
    strm_handler.setFormatter(fmt)

    log.addHandler(strm_handler)

    log.debug("%s -v%i.%i.%i module %s -v%s with test case(s) %s" %
              (sys.executable, sys.version_info[0], sys.version_info[1], sys.version_info[2],
               os.path.basename(sys.argv[0]), __version__, ', '.join(sys.argv[1:])))

    probe = PneumaticProbe(id=AEROPROBE)

    scanner = PressureScanner(id=ZOC334, ref=0)
    #scanner = PressureScanner(id=DSA9214, ref=2)

    log.debug('Default %s ' % probe.__repr__())
    log.debug('Default %s ' % scanner.__repr__())

    for arg in sys.argv[1:]:
        data = load_scanner_data(arg, scanner.id, reference_port=scanner.ref)
        p_average = np.ndarray(shape=(len(data.pressure[0]),))
        if data.port_count < 8:
            max_plots = data.port_count
        else:
            max_plots = 8
        if data.port_count < 100:  # TODO add functionality to print 10 at a time
            for p in range(data.port_count):
                if p % max_plots == 0:
                    # show only 8 traces per figure
                    fig, ax = plt.subplots(max_plots, 1, figsize=(10,5), sharex=True)
                p_average[p] = np.mean(data.pressure[:,p])
                ax[p % max_plots].plot(data.pressure[:, p], linewidth=0.5, color='C0')
                ax[p % max_plots].axhline(p_average[p]+np.std(data.pressure[:, p]), linestyle='--', color='C1', linewidth=0.5)
                ax[p % max_plots].axhline(p_average[p]-np.std(data.pressure[:, p]), linestyle='--', color='C1', linewidth=0.5)
                ax[p % max_plots].set_ylabel('%02i' % data.port[p])
            plt.show()
        else:
            log.debug('Too many ports to plot')


if __name__ == "__main__":
    start_time = time.time()
    main()
    print('[completed in %.2f seconds]' % (time.time() - start_time))
    input('Press <Enter> to exit')