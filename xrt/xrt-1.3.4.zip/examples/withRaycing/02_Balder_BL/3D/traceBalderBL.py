# -*- coding: utf-8 -*-
__author__ = "Konstantin Klementiev"
__date__ = "08 Mar 2016"

import os, sys; sys.path.append(os.path.join('..', '..', '..', '..'))  # analysis:ignore
#import math
import xrt.plotter as xrtp
import xrt.runner as xrtr
import BalderBL

showIn3D = True
BalderBL.showIn3D = showIn3D

def add_plot(plots, plot, prefix, suffix):
    plots.append(plot)
    fileName = '{0}{1:02d}{2}{3}'.format(
        prefix, len(plots), plot.title, suffix)
    if not plot.fluxKind.startswith('power'):
        plot.fluxFormatStr = '%.1p'
    plot.saveName = [fileName + '.png', ]
#    plot.persistentName = fileName + '.pickle'


def define_plots(beamLine, prefix, suffix):
    dE = eMaxRays - eMinRays
    if dE < eTune / 20.:
        fwhmFormatStrE = '%.2f'
        offsetE = eTune
    else:
        fwhmFormatStrE = None
        offsetE = 0
    plots = []

    plot = xrtp.XYCPlot(
        'beamFSM0', (1,),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=None),
        yaxis=xrtp.XYCAxis(r'$z$', 'mm', limits=None),
        caxis='category', ePos=0, title=beamLine.fsm0.name)
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamFilter1local1', (1,),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-7, 7]),
        yaxis=xrtp.XYCAxis(r'$y$', 'mm'),
        ePos=1, title='Filter1 footprint1 I')
    plot.caxis.fwhmFormatStr = fwhmFormatStrE
    plot.fluxFormatStr = '%.2e'
    plot.caxis.limits = [0, eMaxRays]
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamFilter1local1', (1,),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-7, 7]),
        yaxis=xrtp.XYCAxis(r'$y$', 'mm'),
        fluxKind='power', ePos=1, title='Filter1 footprint1 P',
        contourLevels=[0.85, 0.95], contourColors=['b', 'r'],
        contourFmt=r'%.1f W/mm$^2$')
    plot.caxis.fwhmFormatStr = fwhmFormatStrE
    plot.fluxFormatStr = '%.0f'
    plot.caxis.limits = [0, eMaxRays]
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamFilter1local2', (1,),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-7, 7]),
        yaxis=xrtp.XYCAxis(r'$y$', 'mm'),
        fluxKind='power', ePos=1, title='Filter1 footprint2 P',
        contourLevels=[0.85, 0.95], contourColors=['b', 'r'],
        contourFmt=r'%.1f W/mm$^2$')
    plot.caxis.fwhmFormatStr = fwhmFormatStrE
    plot.fluxFormatStr = '%.0f'
    plot.caxis.limits = [0, eMaxRays]
    add_plot(plots, plot, prefix, suffix)

    if hasattr(beamLine, 'filter2'):
        plot = xrtp.XYCPlot(
            'beamFilter2local1', (1,),
            xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-7, 7]),
            yaxis=xrtp.XYCAxis(r'$y$', 'mm'),
            ePos=1, title='Filter2 footprint1 I')
        plot.caxis.fwhmFormatStr = fwhmFormatStrE
        plot.fluxFormatStr = '%.2e'
        plot.caxis.limits = [0, eMaxRays]
        add_plot(plots, plot, prefix, suffix)

        plot = xrtp.XYCPlot(
            'beamFilter2local1', (1,),
            xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-7, 7]),
            yaxis=xrtp.XYCAxis(r'$y$', 'mm'),
            fluxKind='power', ePos=1, title='Filter2 footprint1 P')
        plot.caxis.fwhmFormatStr = fwhmFormatStrE
        plot.fluxFormatStr = '%.0f'
        plot.caxis.limits = [0, eMaxRays]
        add_plot(plots, plot, prefix, suffix)

        plot = xrtp.XYCPlot(
            'beamFilter2local2', (1,),
            xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-7, 7]),
            yaxis=xrtp.XYCAxis(r'$y$', 'mm'),
            fluxKind='power', ePos=1, title='Filter2 footprint2 P',
            contourLevels=[0.85, 0.95], contourColors=['b', 'r'],
            contourFmt=r'%.1f W/mm$^2$')
        plot.caxis.fwhmFormatStr = fwhmFormatStrE
        plot.fluxFormatStr = '%.0f'
        plot.caxis.limits = [0, eMaxRays]
        add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamVCMlocal', (1, 2, 3), aspect='auto',
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-16, 16]),
        yaxis=xrtp.XYCAxis(r'$y$', 'mm', limits=[-660, 660]),
        fluxKind='power', title='VCM footprint P',  # oe=beamLine.vcm,
        contourLevels=[0.85, 0.95], contourColors=['b', 'r'],
        contourFmt=r'%.3f W/mm$^2$')
    plot.caxis.fwhmFormatStr = fwhmFormatStrE
    plot.fluxFormatStr = '%.0f'
    plot.xaxis.fwhmFormatStr = '%.1f'
    plot.yaxis.fwhmFormatStr = '%.0f'
    plot.caxis.limits = [0, eMaxRays]
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamDCMlocal1', (1, 2, 4), aspect='auto',
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-12, 12]),
        yaxis=xrtp.XYCAxis(r'$y$', 'mm', limits=[-32, 32]),
        caxis='category', title='Xtal1_footprint C', oe=beamLine.dcm)
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamDCMlocal1', (1,), aspect='auto',
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-12, 12]),
        yaxis=xrtp.XYCAxis(r'$y$', 'mm', limits=[-32, 32]),
        fluxKind='power', title='Xtal1_footprint P', oe=beamLine.dcm,
        contourLevels=[0.85, 0.95], contourColors=['b', 'r'],
        contourFmt=r'%.1f W/mm$^2$')
    plot.fluxFormatStr = '%.0f'
    plot.caxis.fwhmFormatStr = fwhmFormatStrE
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamDCMlocal2', (1, 2, 4, -2), aspect='auto',
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-12, 12]),
        yaxis=xrtp.XYCAxis(r'$y$', 'mm', limits=[-92, 92]),
        caxis='category', title='Xtal2_footprint', oe=beamLine.dcm,
        raycingParam=2)
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamDCMlocal2', (1, 4), aspect='auto',
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-12, 12]),
        yaxis=xrtp.XYCAxis(r'$y$', 'mm', limits=[-92, 92]),
        ePos=1, title='Xtal2_footprintE', oe=beamLine.dcm, raycingParam=2)
    plot.fluxFormatStr = '%.2e'
    plot.caxis.fwhmFormatStr = fwhmFormatStrE
    plot.caxis.offset = offsetE
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamBSBlocklocal',
        (1, 2, beamLine.BSBlock.lostNum),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-15, 15]),
        yaxis=xrtp.XYCAxis(r'$z$', 'mm', limits=[20, 50]),
        caxis='category', title=beamLine.BSBlock.name, oe=beamLine.BSBlock)
    add_plot(plots, plot, prefix, suffix)

    op = beamLine.slitAfterDCM.opening
    cz = (op[2] + op[3]) / 2
    plot = xrtp.XYCPlot(
        'beamSlitAfterDCMlocal', (1, 2, beamLine.slitAfterDCM.lostNum),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-8, 8]),
        yaxis=xrtp.XYCAxis(r'$z$', 'mm', limits=[cz-8, cz+8]),
        caxis='category', title=beamLine.slitAfterDCM.name,
        oe=beamLine.slitAfterDCM)
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamVFMlocal', (1, 2, 3), aspect='auto',
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-12, 12]),
        yaxis=xrtp.XYCAxis(r'$y$', 'mm', limits=[-710, 710]),
        caxis='category', title='VFM_footprint', oe=beamLine.vfm)
    add_plot(plots, plot, prefix, suffix)

    op = beamLine.slitAfterVFM.opening
    cz = (op[2] + op[3]) / 2
    plot = xrtp.XYCPlot(
        'beamSlitAfterVFMlocal', (1, 2, beamLine.slitAfterVFM.lostNum),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-8, 8]),
        yaxis=xrtp.XYCAxis(r'$z$', 'mm', limits=[cz-8, cz+8]),
        caxis='category', title=beamLine.slitAfterVFM.name,
        oe=beamLine.slitAfterVFM)
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamPSLocal', (1, 2, 4, beamLine.ohPS.lostNum),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-10, 10]),
        yaxis=xrtp.XYCAxis(r'$z$', 'mm', limits=[30, 50]),
        caxis='category', title=beamLine.ohPS.name, oe=beamLine.ohPS)
    add_plot(plots, plot, prefix, suffix)
#
    op = beamLine.slitEH.opening
    cz = (op[2] + op[3]) / 2
    dx = (op[1] - op[0]) / 2
    plot = xrtp.XYCPlot(
        'beamSlitEHLocal', (1, 2, beamLine.slitEH.lostNum),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-dx, dx]),
        yaxis=xrtp.XYCAxis(r'$z$', 'mm', limits=[cz-dx, cz+dx]),
        caxis='category', title=beamLine.slitEH.name, oe=beamLine.slitEH)
    add_plot(plots, plot, prefix, suffix)

#    dz = max(0.1, beamLine.spotSizeH*0.55)
    dz = 2
    plot = xrtp.XYCPlot(
        'beamFSMSample', (1, 2),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-dz, dz],
                           fwhmFormatStr='%1.3f'),
        yaxis=xrtp.XYCAxis(r'$z$', 'mm', limits=[cz-dz, cz+dz],
                           fwhmFormatStr='%1.3f'),
        caxis='category', title=beamLine.fsmSample.name)
    add_plot(plots, plot, prefix, suffix)

    plot = xrtp.XYCPlot(
        'beamFSMSample', (1,),
        xaxis=xrtp.XYCAxis(r'$x$', 'mm', limits=[-dz, dz],
                           fwhmFormatStr='%1.3f'),
        yaxis=xrtp.XYCAxis(r'$z$', 'mm', limits=[cz-dz, cz+dz],
                           fwhmFormatStr='%1.3f'),
        ePos=1, title=beamLine.fsmSample.name+'E')
    plot.fluxFormatStr = '%.2e'
    plot.caxis.fwhmFormatStr = fwhmFormatStrE
    plot.caxis.offset = offsetE
    add_plot(plots, plot, prefix, suffix)

    return plots


def main(pitch, fixedExit, hkl, stripe, eMinRays, eMaxRays, eTune, vfmR,
         prefix):
    myBalder = BalderBL.build_beamline(1e5, hkl, stripe, eMinRays, eMaxRays)
    BalderBL.align_beamline(
        myBalder, pitch=pitch, energy=eTune, fixedExit=fixedExit, vfmR=vfmR)
    suffix = ''
#= touch the beam with the EH slit: ===========================================
# note that for using `touch_beam` the beams must exist, therefore you should
# run the source shrinkage above or `run_process` below this line.
#    BalderBL.run_process(myBalder)
#    myBalder.slitEH.touch_beam(myBalder.beams['beamVFMglobal'])

    if showIn3D:
        myBalder.glow(centerAt='VFM')
        return

    plots = define_plots(myBalder, prefix, suffix)
    xrtr.run_ray_tracing(plots, repeats=1, beamLine=myBalder, processes=4)
#    myBalder.glow()


#this is necessary to use multiprocessing in Windows, otherwise the new Python
#contexts cannot be initialized:
if __name__ == '__main__':

#    pitchNo = '00'; pitch = 2.0e-3; fixedExit = 20.86
#    pitchNo = '02'; pitch = 1.0e-3; fixedExit = 31.43
#    pitchNo = '03'; pitch = 1.5e-3; fixedExit = 26.14
#    pitchNo = '04'; pitch = 3.0e-3; fixedExit = 10.2
    pitchNo = '05'
    pitch = 2.2e-3
    fixedExit = 18.6

    vfmR = 'auto'

    stripe = 'Ir'
    eTune = 20000
    eMinRays, eMaxRays = eTune-5, eTune+5
    hkl = (1, 1, 1)
    estr = '07-10keV-focused'

    prefix = '{0}-{1}mrad-{2}-'.format(pitchNo, pitch*1e3, estr)
    main(pitch, fixedExit, hkl, stripe, eMinRays, eMaxRays, eTune, vfmR,
         prefix)
