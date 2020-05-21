#!/usr/bin/env python3
# -*- python -*-

"""
Salami: lightweight BSM NLO cross-sections, to go

Absolute cross-sections for BSM processes are an essential component,
along with analysis acceptances & efficiencies and collider luminosities,
of signal event-yield predictions in particle collider experiments.
Leading-order (LO) cross-sections can be calculated quickly, but next-to-LO
ones are hundreds of times slower to calculate: too slow for use in
large-scale parameter scan and fitting codes. Salami solves this problem
by rapid prediction of pre-trained NLO cross-sections as functions of the
SUSY/BSM spectrum.

TODO:
 - More careful treatment of negative masses (implies phases, not simply a modulus)
"""

from __future__ import print_function, division
__version__ = "0.3.1"

import numpy as np
from numpy import sqrt, log, exp

try:
    import tensorflow.compat.v1.logging as tf_log
    tf_log.set_verbosity(tf_log.ERROR)
    import os
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    # import warnings
    # warnings.filterwarnings('ignore')
except:
    pass


class SLHAFeatures:

    PNAMES = [
        #'i', 'm1','m2', #< only consider Prospino xsec_LO/NLO and errors as attrs in training
        'M1','M2','Mu','TanB',
        #'Xnn_L','Xnn_R','Xnc_L','Xnc_R','Xcc_L','Xcc_R', #< (n1,n2)-specific, accessed via methods
        'm_W', #< *really*?
        'm_h0','m_H0','m_A0','m_H_plus','m_g',
        'm_nino_1','m_nino_2','m_cino_1','m_nino_3','m_nino_4','m_cino_2',
        'm_d_L','m_u_L','m_s_L','m_c_L','m_t_1','m_b_1',
        'm_e_L', 'm_nue_L','m_mu_L','m_numu_L','m_tau_1','m_nu_tau_L',
        'm_d_R','m_u_R','m_s_R','m_c_R','m_t_2','m_b_2','m_e_R', 'm_mu_R','m_tau_2',
        'n11','n12','n13','n14','n21','n22','n23','n24',
        'n31','n32','n33','n34','n41','n42','n43','n44',
        'u11','u12','u21','u22','v11','v12','v21','v22',
        #'lo','nlo','K', 'relerrPDF', 'relerrME' #< TODO: add Prospino info as extra attrs in training
    ]


    def __getattr__(self, attr):
        "Map unknown attributes into the data dict. Intentionally fails messily with undefined dict key"
        return self.data[attr]


    def __init__(self, sdoc):
        """\
        Create a new SLHAFeatures object from a pyslha.Doc

        Note: if sdoc is a filename, the file will be automatically parsed with PySLHA.
        """

        # self.stdfnames = None
        self.stdfvals = None

        if type(sdoc) is str:
            import os.path
            if not os.path.isfile(sdoc):
                raise IOError("Missing SLHA data file: {}".format(sdoc))
            if os.path.getsize(sdoc) == 0:
                raise IOError("Empty SLHA data file: {}".format(sdoc))

            import pyslha
            sdoc = pyslha.read(sdoc)
        self.slha = sdoc

        masses = sdoc.blocks["MASS"]
        m_W        = abs(masses[24])

        # Higgsino mass terms
        m_h0       = abs(masses[25])
        m_H0       = abs(masses[35])
        m_A0       = abs(masses[36])
        m_H_plus   = abs(masses[37])

        # Gluino mass term
        m_g        = abs(masses[1000021])

        # Neutralino and chargino mass terms
        m_nino_1   = abs(masses[1000022])
        m_nino_2   = abs(masses[1000023])
        m_cino_1   = abs(masses[1000024])
        m_nino_3   = abs(masses[1000025])
        m_nino_4   = abs(masses[1000035])
        m_cino_2   = abs(masses[1000037])

        # squark and slepton masses
        m_d_L      = abs(masses[1000001])
        m_u_L      = abs(masses[1000002])
        m_s_L      = abs(masses[1000003])
        m_c_L      = abs(masses[1000004])
        m_t_1      = abs(masses[1000005])
        m_b_1      = abs(masses[1000006])
        m_e_L      = abs(masses[1000011])
        m_nue_L    = abs(masses[1000012])
        m_mu_L     = abs(masses[1000013])
        m_numu_L   = abs(masses[1000014])
        m_tau_1    = abs(masses[1000015])
        m_nu_tau_L = abs(masses[1000016])
        m_d_R      = abs(masses[2000001])
        m_u_R      = abs(masses[2000002])
        m_s_R      = abs(masses[2000003])
        m_c_R      = abs(masses[2000004])
        m_t_2      = abs(masses[2000005])
        m_b_2      = abs(masses[2000006])
        m_e_R      = abs(masses[2000011])
        m_mu_R     = abs(masses[2000013])
        m_tau_2    = abs(masses[2000015])

        # Neutralino matrix terms
        nmix = sdoc.blocks['NMIX']
        n11 = nmix[1,1]
        n12 = nmix[1,2]
        n13 = nmix[1,3]
        n14 = nmix[1,4]
        n21 = nmix[2,1]
        n22 = nmix[2,2]
        n23 = nmix[2,3]
        n24 = nmix[2,4]
        n31 = nmix[3,1]
        n32 = nmix[3,2]
        n33 = nmix[3,3]
        n34 = nmix[3,4]
        n41 = nmix[4,1]
        n42 = nmix[4,2]
        n43 = nmix[4,3]
        n44 = nmix[4,4]

        # Chargino matrix terms
        umix = sdoc.blocks['UMIX']
        u11 = umix[1,1]
        u12 = umix[1,2]
        u21 = umix[2,1]
        u22 = umix[2,2]

        vmix = sdoc.blocks['VMIX']
        v11 = vmix[1,1]
        v12 = vmix[1,2]
        v21 = vmix[2,1]
        v22 = vmix[2,2]

        # # Neutralino-Neutralino coupling terms
        # Xnn_L, Xnn_R = 0, 0
        # # TODO: what are n1, n2?
        # if n1 < 5 and n2 < 5:
        #       Xnn_L   = -0.5*nmix[n1,3]*nmix[n2,3] + 0.5*nmix[n1,4]*nmix[n2,4]
        #       Xnn_R   =  0.5*nmix[n1,3]*nmix[n2,3] - 0.5*nmix[n1,4]*nmix[n2,4]

        # # Chargino-Neutralino coupling terms
        # SQRT2 = math.sqrt(2)
        # INVSQRT2 = 1/SQRT2
        # Xnc_L, Xnc_R = 0, 0
        # if n1 < 5 and 4 < n2 < 7:
        #       Xnc_L = -INVSQRT2*nmix[n1,4]*vmix[(n2-4),2] + nmix[n1,2]*vmix[(n2-4),1]
        #       Xnc_R = -INVSQRT2*nmix[n1,3]*umix[(n2-4),2] + nmix[n1,2]*umix[(n2-4),1]
        # elif n1 < 5 and n2 > 6:
        #       Xnc_L = -INVSQRT2*nmix[n1,4]*vmix[(n2-6),2] + nmix[n1,2]*vmix[(n2-6),1]
        #       Xnc_R = -INVSQRT2*nmix[n1,3]*umix[(n2-6),2] + nmix[n1,2]*umix[(n2-6),1]

        # # Chargino-Chargino coupling terms. Note this does not include all the processes!!! The formula must be modified inorder to include all the processes.
        # # Currently some of the processes are not done by prospino. Only chi+1-chi-2 and chi+2-chi-2 processes are included.
        # Xcc_L, Xcc_R = 0, 0
        # if 9 > n1 > 4 and 9 > n2 > 4:
        #       Xcc_L = -v11*v21 - 0.5*v12*v22
        #       Xcc_R = -u11*u21 - 0.5*u12*u22

        # 4D parameters
        # TODO: is this essential? Specific to breaking-model...
        exts = sdoc.blocks['EXTPAR']
        M1    = exts[1]
        M2    = exts[2]
        Mu    = exts[23]
        try:
            TanB  = exts[25]
        except:
            TanB = sdoc.blocks['MINPAR'][3]

        ## Store
        # print(locals())
        lvars = locals()
        self.data = { k : lvars[k] for k in SLHAFeatures.PNAMES }
        self.nmix = nmix
        self.umix = umix
        self.vmix = vmix


    @property
    def m_q12(self):
        "Return average masses of L and R squarks from the first two generations, as an (L,R) pair"
        return [(self.m_d_L + self.m_u_L + self.m_s_L + self.m_c_L) / 4.,
                (self.m_d_R + self.m_u_R + self.m_s_R + self.m_c_R) / 4.]

    @property
    def m_l12(self):
        "Return average masses of L and R sleptons from the first two generations, as an (L,R) pair"
        return [(self.m_e_L + self.m_nue_L + self.m_mu_L + self.m_numu_L) / 4.,
                (self.m_e_R + self.m_mu_R) / 2.]

    def Xnn(self, n1, n2):
        "Neutralino-Neutralino coupling terms, returned as an (L,R) pair"
        Xnn_L, Xnn_R = 0, 0
        if n1 < 5 and n2 < 5:
            Xnn_L = -0.5*self.nmix[n1,3]*self.nmix[n2,3] + 0.5*self.nmix[n1,4]*self.nmix[n2,4]
            Xnn_R =  0.5*self.nmix[n1,3]*self.nmix[n2,3] - 0.5*self.nmix[n1,4]*self.nmix[n2,4]
        return Xnn_L, Xnn_R

    def Xnc(self, n1, n2):
        "Chargino-Neutralino coupling terms, returned as an (L,R) pair"
        SQRT2 = sqrt(2)
        INVSQRT2 = 1/SQRT2
        Xnc_L, Xnc_R = 0, 0
        if n1 < 5 and 4 < n2 <= 6:
            Xnc_L = -INVSQRT2*self.nmix[n1,4]*self.vmix[(n2-4),2] + self.nmix[n1,2]*self.vmix[(n2-4),1]
            Xnc_R = -INVSQRT2*self.nmix[n1,3]*self.umix[(n2-4),2] + self.nmix[n1,2]*self.umix[(n2-4),1]
        elif n1 < 5 and n2 > 6:
            Xnc_L = -INVSQRT2*self.nmix[n1,4]*self.vmix[(n2-6),2] + self.nmix[n1,2]*self.vmix[(n2-6),1]
            Xnc_R = -INVSQRT2*self.nmix[n1,3]*self.umix[(n2-6),2] + self.nmix[n1,2]*self.umix[(n2-6),1]
        return Xnc_L, Xnc_R

    def Xcc(self, n1, n2):
        """Chargino-Chargino coupling terms, returned as an (L,R) pair

        Currently some of the processes are not done by prospino. Only chi+1-chi-2 and chi+2-chi-2 processes are included.

        TODO: Note this does not include all the processes!!! The formula must be modified in order to include all the processes.
        """
        Xcc_L, Xcc_R = 0, 0
        if 4 < n1 < 9 and 4 < n2 < 9:
            Xcc_L = -self.v11*self.v21 - 0.5*self.v12*self.v22
            Xcc_R = -self.u11*self.u21 - 0.5*self.u12*self.u22
        return Xcc_L, Xcc_R


    def invalid(self):
        "Check the standard features for bad values"
        import math
        stdfs = self.stdfeatures()
        return any(math.isnan(d) for d in stdfs)
        # TODO: any other checks?


    @classmethod
    def stdfeaturenames(cls):
        "Return the list of standard SLHA feature names"
        # TODO: cache... but how, for a class method?
        #if self.stdfnames is None:
        rtn = SLHAFeatures.PNAMES + ["m_q12L", "m_q12R", "m_l12L", "m_l12R"]
        for i in range(1,5):
            for j in range(i,5):
                rtn += ["Xnn_L_{:d}{:d}".format(i, j), "Xnn_R_{:d}{:d}".format(i, j)]
        for i in range(1,5):
            for j in range(5,9):
                rtn += ["Xnc_L_{:d}{:d}".format(i, j-4), "Xnc_R_{:d}{:d}".format(i, j-4)]
        for i in range(5,9):
            for j in range(5,9):
                rtn += ["Xcc_L_{:d}{:d}".format(i-4, j-4), "Xcc_R_{:d}{:d}".format(i-4, j-4)]
        #self.stdfnames = rtn
        #return self.stdfnames
        return rtn


    def stdfeatures(self):
        "Return the list of standard SLHA feature values"
        if self.stdfvals is None:
            rtn = [getattr(self, p) for p in SLHAFeatures.PNAMES]
            rtn += self.m_q12 + self.m_l12
            for i in range(1,5):
                for j in range(i,5):
                    rtn += self.Xnn(i, j)
            for i in range(1,5):
                for j in range(5,9):
                    rtn += self.Xnc(i, j)
            for i in range(5,9):
                for j in range(5,9):
                    rtn += self.Xcc(i, j)
            self.stdfvals = rtn
        return self.stdfvals


class ProspinoData:
    """\
    Reader and processor of Prospino output data from (multiplexed) prospino.dat files

    TODO: provide accessors for asymm errors
    """

    def __init__(self):
        self._lo_nom = None
        self._deltalo_pdf = np.array([0.,0.])
        self._deltalo_me = np.array([0.,0.])
        self._relerrlo = 0.0
        self._nlo_nom = None
        self._deltanlo_pdf = np.array([0.,0.])
        self._deltanlo_me = np.array([0.,0.])
        self._relerrnlo = 0.0


    @classmethod
    def fromDatFile(cls, path_or_stream):
        if type(path_or_stream) is str:
            import os.path
            if not os.path.isfile(path_or_stream):
                raise IOError("Missing Prospino data file: {}".format(path_or_stream))
            if os.path.getsize(path_or_stream) == 0:
                raise IOError("Empty Prospino data file: {}".format(path_or_stream))

        ## Read using Pandas
        import pandas as pd
        try:
            pros = pd.read_csv(path_or_stream, sep=r"\s+", engine='python', skipfooter=1, header=None,
                               names=["proc", "id1", "id2", "energy", "dummy1", "scafac", "m1", "m2", "angle",
                                      "xsec_lo", "rel_err_lo", "xsec_nlo", "rel_err_nlo", "K", "xsec_lo_ms", "xsec_nlo_ms"])
            # print(pros)
            pros = pros.drop(columns="proc").apply(pd.to_numeric)

            rtn = ProspinoData()
            rtn._prosids = [pros["id1"][0], pros["id2"][0]]
            rtn._energy = pros["energy"][0]

            ## LO: separate odd and even columns and calculate errors
            # TODO: use _ms xsecs if non-zero / requested
            # TODO: handle alpha_s up/down variations
            lo = pros['xsec_lo']
            lo_nom = lo.values[0]
            rtn._lo_nom = lo_nom
            if lo.size > 1:
                lo_pdf_even = lo[2:-2:2].reset_index(drop=True)
                lo_pdf_odd = lo[1:-2:2].reset_index(drop=True)
                lo_me = lo[-2:].reset_index(drop=True)
                deltalo_pdf_even = abs(lo_pdf_even - lo_nom)
                deltalo_pdf_odd = abs(lo_pdf_odd - lo_nom)
                deltalo_pdf_avg = (deltalo_pdf_even + deltalo_pdf_odd)/2.
                deltalo_me = (lo_me - lo_nom).to_numpy()
                deltalo_pdf_avg_quad = (deltalo_pdf_avg**2).to_numpy().sum()**0.5
                rtn._deltalo_pdf = np.array([-deltalo_pdf_avg_quad, deltalo_pdf_avg_quad])
                rtn._deltalo_me = deltalo_me
                rtn._relerrlo = pros['rel_err_lo'].max()

            ## NLO: separate odd and even columns to calculate errors
            # TODO: use _ms xsecs if non-zero / requested
            # TODO: handle alpha_s up/down variations
            nlo = pros['xsec_nlo']
            nlo_nom = nlo.values[0]
            rtn._nlo_nom = nlo_nom
            if nlo.size > 1:
                nlo_pdf_even = nlo[2:-2:2].reset_index(drop=True)
                nlo_pdf_odd = nlo[1:-2:2].reset_index(drop=True)
                nlo_me = nlo[-2:].reset_index(drop=True)
                deltanlo_pdf_even = abs(nlo_pdf_even - nlo_nom)
                deltanlo_pdf_odd = abs(nlo_pdf_odd - nlo_nom)
                deltanlo_pdf_avg = (deltanlo_pdf_even + deltanlo_pdf_odd)/2.
                deltanlo_me = (nlo_me - nlo_nom).to_numpy()
                deltanlo_pdf_avg_quad = (deltanlo_pdf_avg**2).to_numpy().sum()**0.5
                rtn._deltanlo_pdf = np.array([-deltanlo_pdf_avg_quad, deltanlo_pdf_avg_quad])
                rtn._deltanlo_me = deltanlo_me
                rtn._relerrnlo = pros['rel_err_nlo'].max()
        except Exception as e:
            raise IOError("Error in parsing {}: {}".format(path_or_stream, e))

        return rtn


    @classmethod
    def fromDatStr(cls, datstr):
        import io
        return ProspinoData.fromDatFile(io.StringIO(datstr))


    @classmethod
    def fromSLHA(cls, path_or_sdoc):
        if type(path_or_sdoc) is str:
            import pyslha
            sdoc = pyslha.read(path_or_sdoc)
        else:
            sdoc = path_or_sdoc

        rtn = []
        prosblock = sdoc.blocks["PROSPINO_OUTPUT"]
        for ilist in prosblock.itemlists():
            pd = ProspinoData()
            try:
                #print(entry)
                id1, id2, energy, \
                    xsec_lo, relerr_lo_num,\
                    xsec_nlo, relerr_nlo_num, \
                    xsec_nlo_ms, \
                    xsec_nlo_ms_me05, xsec_nlo_ms_me20, \
                    xsecerr_nlo_ms_pdf, \
                    xsec_nlo_ms_aup, xsec_nlo_ms_adn = ilist
                pd._prosids = [ProspinoData.prosid(id1), ProspinoData.prosid(id2)]
                pd._energy = energy
                pd._lo_nom = xsec_lo/1000. #< fb->pb; TODO: this is NLO_MS/LO :-/
                pd._deltalo_pdf = np.array([0.,0.])/1000. #< fb->pb
                pd._deltalo_me = np.array([0.,0.])/1000. #< fb->pb
                pd._relerrlo = relerr_lo_num
                pd._nlo_nom = xsec_nlo_ms/1000. #< fb->pb
                pd._deltanlo_pdf = np.array([-xsecerr_nlo_ms_pdf, xsecerr_nlo_ms_pdf])/1000. #< fb->pb
                pd._deltanlo_me = np.array([xsec_nlo_ms_me05 - xsec_nlo_ms, xsec_nlo_ms_me20 - xsec_nlo_ms])/1000. #< fb->pb
                pd._relerrnlo = relerr_nlo_num
                rtn.append(pd)
            except Exception as e:
                print(e)
                pass
        return rtn


    # def size(self):
    #     return len(self.XXX)


    @classmethod
    def pdgid(cls, prosid):
        "Translate from PDG ID code to Prospino ID code (for EWinos)"
        return {1 : 1000022, 2 : 1000023, 3 : 1000025, 4 : 1000035, 5 : 1000024, 6 : 1000037, 7 : -1000024, 8 : -1000037}.get(prosid)

    @classmethod
    def prosid(cls, pdgid):
        "Translate from Prospino ID code to PDG ID code (for EWinos)"
        return {1000022 : 1, 1000023 : 2, 1000025 : 3, 1000035 : 4, 1000024 : 5, -1000024 : 7, 1000037 : 6, -1000037 : 8}.get(pdgid)

    def prosids(self):
        return self._prosids

    def pdgids(self):
        return [self.pdgid(i) for i in self._prosids]



    def energy(self):
        return self._energy



    def kfac(self): #, index=None):
        return self.xsec_nlo()/self.xsec_lo()



    def xsec_lo(self): #, index=None):
        return self._lo_nom


    # def xsecerr_lo(self):
    #     return sqrt(self.xsecerr_lo_me()**2 + self.xsecerr_lo_pdf()**2 + self.xsecerr_lo_num()**2)

    def xsecerr_lo_pdf(self):
        return self._deltalo_pdf

    def xsecerr_lo_me(self):
        return self._deltalo_me

    def xsecerr_lo_num(self):
        return self.relerr_lo_num() * self.xsec_lo()


    # def relerr_lo(self):
    #     return self.xsecerr_lo()/self.xsec_lo()

    def relerr_lo_pdf(self):
        return self.xsecerr_lo_pdf()/self.xsec_lo()

    def relerr_lo_me(self):
        return self.xsecerr_lo_me()/self.xsec_lo()

    def relerr_lo_num(self):
        return self._relerrlo


    # def pcterr_lo(self):
    #     return 100*self.relerr_lo()

    def pcterr_lo_pdf(self):
        return 100*self.relerr_lo_pdf()

    def pcterr_lo_me(self):
        return 100*self.relerr_lo_me()

    def pcterr_lo_num(self):
        return 100*self.relerr_lo_num()



    def xsec_nlo(self): #, index=None):
        return self._nlo_nom


    # def xsecerr_nlo(self):
    #     return sqrt(self.xsecerr_nlo_me()**2 + self.xsecerr_nlo_pdf()**2 + self.xsecerr_nlo_num()**2)

    def xsecerr_nlo_pdf(self):
        return self._deltanlo_pdf

    def xsecerr_nlo_me(self):
        return self._deltanlo_me

    def xsecerr_nlo_num(self):
        return self.relerr_nlo_num() * self.xsec_nlo()


    # def relerr_nlo(self):
    #     return self.xsecerr_nlo()/self.xsec_nlo()

    def relerr_nlo_pdf(self):
        return self.xsecerr_nlo_pdf()/self.xsec_nlo()

    def relerr_nlo_me(self):
        return self.xsecerr_nlo_me()/self.xsec_nlo()

    def relerr_nlo_num(self):
        return self._relerrnlo


    # def pcterr_nlo(self):
    #     return 100*self.relerr_nlo()

    def pcterr_nlo_pdf(self):
        return 100*self.relerr_nlo_pdf()

    def pcterr_nlo_me(self):
        return 100*self.relerr_nlo_me()

    def pcterr_nlo_num(self):
        return 100*self.relerr_nlo_num()


    def invalid(self, kmin=0.5, kmax=2):
        "Check the standard data output for bad values"
        import math
        stdd = self.stddata()
        # print(stdd)
        # print(type(stdd))
        # print([type(i) for i in stdd])
        if any(math.isnan(d) for d in stdd):
            return True
        if self.xsec_lo() <= 0 or self.xsec_nlo() <= 0:
            return True
        if kmin is not None and self.kfac() < kmin:
            return True
        if kmax is not None and self.kfac() > kmax:
            return True
        return False


    @classmethod
    def stddatanames(self):
        rtn = ["xsec_lo", "pcterr_lo_num", "xsec_nlo", "pcterr_nlo_num",
               "kfac", "pcterr_nlo_pdf_dn", "pcterr_nlo_pdf_up", "pcterr_nlo_me_dn", "pcterr_nlo_me_up"]
        return rtn

    def stddata(self):
        stdfnnames = self.stddatanames()[:-4] + ["pcterr_nlo_pdf", "pcterr_nlo_me"]
        unflat = [getattr(self, methodname)() for methodname in stdfnnames]
        rtn = []
        for u in unflat:
            if type(u) is list:
                rtn += u
            elif type(u) is np.ndarray:
                rtn += u.tolist()
            else:
                rtn.append(u)
        return rtn


    def __repr__(self):
        return "ProspinoData<{}@{:d}, lo,num%,nlo,num%,K,pdf%,me%={}>".format(self.prosids(), self.energy(), self.stddata())



class XsecLnScaler:
    """\
    Transform cross-section numbers into a positive, logarithmised measure
    """
    def __init__(self, offset):
        self.offset = offset

    def transform(self, xsec):
        return log(xsec) + self.offset

    def inverse_transform(self, xsec):
        return exp(xsec - self.offset)



def load_pickle(filename):
    "Load a scaler class from a given pickle file"
    import pickle
    with open(filename, "rb") as pf:
        obj = pickle.load(pf)
        return obj


class UnsupportedProcess(Exception):
    "Error raised when an unsupported process is requested"
    pass


class KPred:
    """\
    Predictor of K-factors via pre-trained neural nets, given an SLHA dataset and a LO cross-section
    """

    def __init__(self, energy, process):
        self.energy = energy
        self.process = process

        ## Determine and test the data path for this energy and process
        import os.path
        dirname = "E{}_P{}".format(self.energy, self.canonical_process)
        dirpath = os.path.join(os.path.dirname(__file__), dirname)
        if not os.path.exists(dirpath):
            raise UnsupportedProcess("Unsupported process " + self.process)

        ## Load scalers and model from data path
        from tensorflow.keras.models import load_model
        def getpath(x):
            return os.path.join(dirpath, x)
        self.model = load_model(getpath("kfactor_weights.hdf5"))
        try:
            tools = load_pickle(getpath("kfactor_objects.pkl"))
            self.feature_indices = tools["FEATURE_INDICES"].tolist()
            self.feature_indices.remove(149)
            self.feature_ranges = tools["FEATURE_RANGES"]
            self.feature_scaler = tools["FEATURE_SCALER"]
            self.loxsec_scaler = tools["LOXSEC_SCALER"]
        except FileNotFoundError as e:
            raise e

        # print(len(self.feature_indices), self.feature_ranges.shape)
        # print(self.model, self.feature_indices, self.feature_scaler, self.loxsec_scaler)


    @property
    def canonical_process(self):
        """The process, in canonical increasing-index order"""
        return "".join(sorted(self.process))

    def predict_kfac(self, slhadoc, xsec_lo, kmin=0, kmax=None, freeze_xpol=True):
        """\
        Predict a LO->NLO K-factor, given an SLHA dataset and a LO cross-section

        The optional kmin,kmax arguments permit truncation of the K-factor to
        within a user-supplied range, e.g. to suppress corrections thought too
        large to be physical. The returned value is max(min(k,kmax),kmin), if
        both kmin and kmax are non-null.

        The optional freeze_xpol parameter freezes NN predictions to their
        values at the boundaries of the sampled parameter space, to avoid bad
        extrapolations.
        """

        import numpy as np

        ## Build the raw features vector
        ln_xsec_lo = self.loxsec_scaler.transform(xsec_lo)
        params = SLHAFeatures(slhadoc)
        stdparams = np.array(params.stdfeatures())
        raw_features = stdparams[self.feature_indices]

        ## Check & freeze if extrapolating beyond trained feature boundaries
        # TODO: warn/record if outside bounds?
        if freeze_xpol:
            ## NB. feature_ranges pairs are in [max,min] order!
            features_bounded = np.fmax(raw_features, self.feature_ranges[:-1,1])
            features_bounded = np.fmin(raw_features, self.feature_ranges[:-1,0])

        ## Add the LO ln(xsec) as the trailing entry
        raw_features = np.concatenate((stdparams[self.feature_indices], [ln_xsec_lo]))

        ## Build the scaled feature vector expected by the trained neural net
        # TODO: embed this logic into the pickled feature selector & scaler
        scaled_features = self.feature_scaler.transform(np.atleast_2d(raw_features))

        ## Make and return the K-factor prediction (with min/max truncation)
        kpred = self.model.predict(scaled_features)[0,0]
        if kmin is not None:
            kpred = max(kpred, kmin)
        if kmax is not None:
            kpred = min(kpred, kmax)
        return kpred


    def predict_kfac_xsec(self, slhadoc, xsec_lo, kmin=0, kmax=None, freeze_xpol=True):
        "Predict a LO->NLO K-factor and the NLO cross-section, given an SLHA dataset and a LO cross-section"
        kpred = self.predict_kfac(slhadoc, xsec_lo, kmin, kmax, freeze_xpol)
        xsecpred = kpred * xsec_lo
        return kpred, xsecpred


    def predict_xsec(self, slhadoc, xsec_lo, kmin=0, kmax=None, freeze_xpol=True):
        "Predict the NLO cross-section, given an SLHA dataset and a LO cross-section"
        kpred = self.predict_kfac(slhadoc, xsec_lo, kmin, kmax, freeze_xpol)
        xsecpred = kpred * xsec_lo
        return xsecpred


class KPredConst:
    """\
    Dummy predictor of K-factors that just returns constant values
    """

    def __init__(self, kfix=1.2):
        self.k = kfix

    def predict_kfac(self, slhadoc, xsec_lo, kmin=0, kmax=None, freeze_xpol=None):
        "Return the dummy K-factor, given an SLHA dataset and a LO cross-section"
        if kmin is not None and self.k < kmin:
            return kmin
        if kmax is not None and self.k > kmax:
            return kmax
        return self.k

    def predict_kfac_xsec(self, slhadoc, xsec_lo, kmin=0, kmax=None, freeze_xpol=None):
        "Return the dummy K-factor and the corresponding dummy NLO cross-section, given an SLHA dataset and a LO cross-section"
        return self.k, self.predict_xsec(slhadoc, xsec_lo, kmin, kmax)

    def predict_xsec(self, slhadoc, xsec_lo, kmin=0, kmax=None, freeze_xpol=None):
        "Return the dummy NLO cross-section, given an SLHA dataset and a LO cross-section"
        return self.predict_kfac(slhadoc, xsec_lo, kmin, kmax) * xsec_lo


class KPreds:
    """\
    Predictor of K-factors via pre-trained neural nets, given an SLHA dataset and a LO cross-section
    """

    def __init__(self, energy, preload_processes=[]):
        """Initialize for a fixed collider energy, optionally eagerly loading some process interpolators"""
        self.energy = str(energy)
        self.kpreds = {}
        for proc in preload_processes:
            self.kpred(proc)

    def kpred(self, process):
        """Get the interpolator for a named process, loading and caching if necessary"""
        proc = str(process)
        if proc not in self.kpreds:
            ## Make the real or dummy predictor
            try:
                kp = KPred(str(self.energy), proc)
            except UnsupportedProcess:
                kp = KPredConst(1.0)
            ## Store under normal and reversed names
            rproc = "".join(reversed(proc))
            self.kpreds[proc] = kp
            self.kpreds[rproc] = kp #< no point in duplicate detection
        return self.kpreds[proc]

    def __getitem__(self, process):
        """Get the interpolator for a named process: syntactic wrapper for kpred()"""
        return self.kpred(process)

    def predict_kfac(self, process, slhadoc, xsec_lo, kmin=0, kmax=None, freeze_xpol=True):
        "Predict a LO->NLO K-factor, given an SLHA dataset and a LO cross-section"
        return self.kpred(process).predict_kfac(slhadoc, xsec_lo, kmin, kmax, freeze_xpol)

    def predict_kfac_xsec(self, process, slhadoc, xsec_lo, kmin=0, kmax=None, freeze_xpol=True):
        "Predict a LO->NLO K-factor and the NLO cross-section, given an SLHA dataset and a LO cross-section"
        return self.kpred(process).predict_kfac_xsec(slhadoc, xsec_lo, kmin, kmax, freeze_xpol)

    def predict_xsec(self, process, slhadoc, xsec_lo, kmin=0, kmax=None, freeze_xpol=True):
        "Predict the NLO cross-section, given an SLHA dataset and a LO cross-section"
        return self.kpred(process).predict_xsec(slhadoc, xsec_lo, kmin, kmax, freeze_xpol)
