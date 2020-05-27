import os
import numpy as np
import matplotlib.pyplot as plt

import logging

import aiolos_fluid_dynamics.units as units

log  = logging.getLogger(__name__)


def plot_channels(scanner_data, channels=[], subplots=8, save_path='', show_plots=True):
    """
    this will plot the raw data from each of the pressure scanner channels in the channels array. if the
    array is empty, all channels will be plotted. each figure will contain the number of subplots accord-
    ing to the value of the subplots parameter. Image files can be saved by specifying a path in the
    save_path parameter (if more than one figure if generated, multiple files will automatically be saved).

    :param scanner_data:  <ScannerData> object containing the pressure scanner data for one run
    :param channels:      <list of np.array> list of channels to plot, if empty all will be plotted
    :param subplots:      <int> number of subplots per figure. default = 8 yields 8 plots for 64 channel scanners.
    :param save_path:     <str> path to save plots
    :return:
        None
    """
    save_plots = False

    if np.shape(channels)[0] == 0:
        channels = scanner_data.port

    if np.shape(channels)[0] <= subplots:
        subplots = np.shape(channels)[0]

    if save_path != '':
        save_plots = True
        ext = save_path.split('.')[-1]
        path = save_path.split('.')[0]
        dirname = os.path.dirname(save_path)

    for i in np.arange(np.shape(channels)[0]):
        if i % subplots == 0:
            fig, ax = plt.subplots(subplots, 1, figsize=(10, 5), sharex='col')
            ax[-1].set_xlabel('Frame No.')
        p = scanner_data.pressure[:, scanner_data.port == channels[i]]
        ax[i % subplots].set_ylabel('%02i' % scanner_data.port[scanner_data.port == channels[i]])
        ax[i % subplots].plot(p, linewidth=0.5, color='C0')
        ax[i % subplots].axhline(p.mean()+p.std(), linestyle='--', color='C1', linewidth=0.5)
        ax[i % subplots].axhline(p.mean()-p.std(), linestyle='--', color='C1', linewidth=0.5)

        if save_plots and i != 0 and scanner_data.port[scanner_data.port == channels[i]] % subplots == 0:
            fname='%s-%03i-of-%03i.%s' % (path, np.ceil(i/subplots), np.ceil(np.shape(channels)[0]/subplots), ext)
            try:
                plt.savefig(fname=fname, dpi=600, bbox='tight')
            except FileNotFoundError as err:
                log.warning(err)
                os.mkdir(dirname)
                plt.savefig(fname=fname, dpi=600, bbox='tight')
    if show_plots:
        plt.show()


def plot_mean_pressures(scanner_data, channels=[], show_plots=True):

    """
    this function will generate a plot of the average pressures in the pressure scanner data. The channels listed
    in the array channels will be plotted. If the array is empty all channels will be plotted.

    :param scanner_data:  <ScannerData> object containing the pressure scanner data for one run
    :param channels:      <list of np.array> list of channels to plot, if empty all will be plotted
    :return:
            fig, ax     returns the figure and axes handles of the plots generated.
    """

    # todo: add saving funtionality

    if np.shape(channels)[0] == 0:
        channels = scanner_data.port

    averages = scanner_data.pressure.mean(axis=0)
    fig, ax = plt.subplots(1,1, figsize=(10,5))
    ax.set_ylabel('Pressure in [Pa]')
    ax.set_xlabel('Scanner Channel No. ')
    ax.set_xlim(np.min(channels)-1, np.max(channels)+1)
    ax.text(scanner_data.ref/(np.max(channels) - np.min(channels) + 2), 0.5,
            'Reference Port', horizontalalignment='center', verticalalignment='top', transform=ax.transAxes, rotation='vertical',
            bbox={'facecolor': 'white', 'pad': 5, 'alpha': 0.8, 'edgecolor': 'white'})

    ax.axvline(scanner_data.ref, linestyle='--', linewidth=0.5, color='C1')
    for i in np.arange(np.shape(channels)[0]):
        ax.plot(scanner_data.port[scanner_data.port == channels[i]], averages[scanner_data.port == channels[i]], '+', color='C0')

    if show_plots:
        plt.show()
    return fig, ax


def plot_boundary_layer_data(bl_data, show_plots=True):
    """

    :param bl_data: <BoundaryLayerData> Dataclass object containing the boundary layer data for one run
    :return:
            fig, ax     returns the figure and axes handles of the plots generated.
    """

    # todo: add saving functionality

    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex='col', gridspec_kw={'height_ratios': [3, 1]})

    u_ue = bl_data.u / bl_data.Ue
    z = bl_data.z / units.MM
    delta = bl_data.boundary_layer_thickness / units.MM
    delstar = bl_data.displacement_thickness / units.MM
    ue_kph = bl_data.Ue / units.KPH

    axs[1].set_xlabel('$u/U_{e}$')
    axs[1].set_ylim(0, 1.5*delta)
    axs[0].text(0.1, 0.9,
                'Run No. %4i\n\t$U_{e}$ = %.4f kph' % (bl_data.run_id, ue_kph),
                horizontalalignment='left', verticalalignment='center', transform=axs[0].transAxes,
                bbox={'facecolor': 'white', 'pad': 1, 'alpha': 0.8, 'edgecolor': 'white'})

    for ax in axs:
        ax.plot(u_ue, z, 'o', markersize='0.5')
        ax.axhline(delta, linestyle='--', linewidth=0.5, color='C1')
        ax.axhline(delstar, linestyle='--', linewidth=0.5, color='C1')
        ax.set_ylabel('height, z (mm)')
        ax.text(0.2, (delta-ax.get_ylim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0]),
                '$\u03B4$ = $%.4f$ $mm$' % delta, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
                bbox={'facecolor': 'white', 'pad': 1, 'alpha': 0.8, 'edgecolor': 'white'})
        ax.text(0.2, (delstar-ax.get_ylim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0]),
                '$\u03B4^{*}$ = $%.4f$ $mm$' % delstar, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
                bbox={'facecolor': 'white', 'pad': 1, 'alpha': 0.8, 'edgecolor': 'white'})
    if show_plots:
        plt.show()
    return fig, axs


def plot_axial_data(axial_data, show_plots=True):
    fig, axs = plt.subplots(1, 1, figsize=(10, 5))

    axs.plot(axial_data.x, axial_data.cps)
    if show_plots:
        plt.show()
    return fig, axs
