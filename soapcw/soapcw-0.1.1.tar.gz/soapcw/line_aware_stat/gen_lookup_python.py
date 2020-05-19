import scipy.stats as st
import numpy as np
from scipy.integrate import quad
#import numba as nb
#--------------------------------------------------------------------------------
# Gaussian Numerically finding the integral by integrating over SNR^2, where the variance depends on the standard deviation
#------------------------------------------------------------------------------------


class LineAwareStatistic:

    def __init__(self, powers, k = 2, N = 48, pvs = 1, pvl = 5, ratio =1,approx=True):

        if len(np.shape(powers)) == 1:
            self.signoiseline,self.signoise,self.sigline,self.sig,self.noise,self.line = self.gen_lookup_one_det(powers,approx=approx,pvs=pvs,pvl=pvl,ratio=ratio)
        elif np.shape(powers)[0] == 2:
            self.signoiseline,self.signoise,self.sigline,self.sig,self.noise,self.line = self.gen_lookup_two_det(powers[0],powers[1],approx=approx,pvs=pvs,pvl=pvl,ratio=ratio)
            
    def chi2_sig(self,lamb,gs,k,N,pv):
        """
        returns the likelihood of two powers multiplied by the prior on the snr**2
        args
        -------
        lamb: float
            snr^2
        g1: float
            SFT power in detector 1
        g2: float
            SFT power in detector 2
        k: int
            number of degrees of freedom
        N: int
            Number of summed SFTS
        pv: float
            width of exponetial distribution of prior
        returns
        ---------
        func*prior: float
        likelihood multiplied by prior
        """
        if len(np.shape(gs)) == 0:
            func = st.ncx2.pdf(gs,df=N*k,nc=lamb,loc=0,scale=1)
        else:
            func = np.prod([st.ncx2.pdf(i,df=N*k,nc=lamb,loc=0,scale=1) for i in gs],axis=0)
        wid = 1./pv
        return func*wid*np.exp(-wid*lamb)


    def chi2_line(self,lamb,gs,k,N,pv):
        """
        returns the likelihood of two powers multiplied by the prior on the snr**2
        works for 1 or 2 detectors only

        args
        -------
        lamb: float
        snr^2
        g1: float
        SFT power in detector 1
        g2: float
        SFT power in detector 2
        k: int
        number of degrees of freedom
        N: int
        Number of summed SFTS
        pv: float
        width of exponetial distribution of prior
        returns
        ---------
        func*prior: float
        likelihood multiplied by prior
        """
        if len(np.shape(gs)) == 0:
            func = st.ncx2.pdf(gs,df=N*k,nc=lamb,loc=0,scale=1)
        else:
            func = 1./len(gs)*(st.chi2.pdf(gs[0],df=N*k,loc=0,scale=1)*st.ncx2.pdf(gs[1],df=N*k,nc=lamb,loc=0,scale=1) + st.ncx2.pdf(gs[0],df=N*k,nc=lamb,loc=0,scale=1)*st.chi2.pdf(gs[1],df=N*k,loc=0,scale=1))
        wid = 1./pv
        return func*wid*np.exp(-wid*lamb)
    
    
    def chi2_noise(self,gs,k,N):
        if len(np.shape(gs)) == 0:
            func = st.chi2.pdf(gs,df=N*k,loc=0,scale=1)
        else:
            func = np.prod([st.chi2.pdf(i,df=N*k,loc=0,scale=1) for i in gs],axis=0)
        return func


    def two_det(self,g1,g2,k,N,pvs=10,pvl=10,ratio=1., approx=True):
        """
        integrate likelihood and prior to get evidence for powers g1 and g2
        args
        -------
        approx: bool
            choose to approximate the integral with trapz or full integration
        """
        if approx:
            l = np.linspace(0,100,500)
            sig_int = np.trapz(np.nan_to_num(self.chi2_sig(l,[g1,g2],k,N,pvs)),l)
            line_int = np.trapz(np.nan_to_num(self.chi2_line(l,[g1,g2],k,N,pvl)),l)
        else:
            sig_int, sig_err = quad(self.chi2_sig,0,np.inf, args = ([g1,g2],k,N,pvs))
            line_int, line_err = quad(self.chi2_line,0,np.inf, args = ([g1,g2],k,N,pvl))

        siglinenoise = sig_int/(ratio*line_int + self.chi2_noise([g1,g2],k,N))
        signoise = sig_int/(self.chi2_noise([g1,g2],k,N))
        sigline = sig_int/line_int
        
        return siglinenoise,signoise,sigline,sig_int,self.chi2_noise([g1,g2],k,N),line_int

    def one_det(self,g1,k,N,pvs=10,pvl=10,ratio=1., approx=True):
        """
        integrate likelihood and prior to get evidence for powers g1 and g2
        args
        -------
        approx: bool
            choose to approximate the integral with trapz or full integration
        """

        if approx:
            l = np.linspace(0,100,500)
            sig_int = np.trapz(np.nan_to_num(self.chi2_sig(l,g1,k,N,pvs)),l)
            line_int = np.trapz(np.nan_to_num(self.chi2_line(l,g1,k,N,pvl)),l)
        else:
            sig_int, sig_err = quad(self.chi2_sig,0,np.inf, args = (g1,k,N,pvs))
            line_int, line_err = quad(self.chi2_line,0,np.inf, args = (g1,k,N,pvl))

        siglinenoise = sig_int/(ratio*line_int + self.chi2_noise(g1,k,N))
        signoise = sig_int/(self.chi2_noise(g1,k,N))
        sigline = sig_int/line_int
        
        return siglinenoise,signoise,sigline,sig_int,self.chi2_noise(g1,k,N),line_int

    
    def gen_lookup_one_det(self,powers,approx=True,pvs=10,pvl=10,ratio=1):
        """
        calculate lookup table for values of x in the detector
        args
        -----------
        powers: array, list
            list of spectrogram powers to calcualte statistic at
        returns
        ---------
        signoiseline: log(sig/(noise+line))
        signoise: log(sig/(noise))
        sigline: log(sig/(line))
        sig: log(sig)
        noise: log(noise)
        line: log(line)
        """

        signoiseline = np.zeros((len(powers)))
        signoise = np.zeros((len(powers)))
        sigline = np.zeros((len(powers)))
        sig = np.zeros((len(powers)))
        noise = np.zeros((len(powers)))
        line = np.zeros((len(powers)))
        
        for i in range(len(powers)):
            ig = self.one_det(powers[i],2.,48.,pvs,pvl,ratio,approx=approx)
            signoiseline[i] = ig[0]
            signoise[i] = ig[1]
            sigline[i] = ig[2]
            sig[i] = ig[3]
            noise[i] = ig[4]
            line[i] = ig[4]
                    
        return signoiseline,signoise,sigline,sig,noise,line

    def gen_lookup_two_det(self,powers1,powers2,approx=True,pvs=10,pvl=10,ratio=1):
        """
        calculate lookup table for values of x and y in each detector
        args
        ----------
        powers1: array, list
            list of spectrogram powers to calcualte statistic at in det1
        powers2: array, list
            list of spectrogram powers to calcualte statistic at in det2


        returns
        ---------
        signoiseline: log(sig/(noise+line))
        signoise: log(sig/(noise))
        sigline: log(sig/(line))
        sig: log(sig)
        noise: log(noise)
        line: log(line)
        """

        signoiseline = np.zeros((len(powers1),len(powers2)))
        signoise = np.zeros((len(powers1),len(powers2)))
        sigline = np.zeros((len(powers1),len(powers2)))
        sig = np.zeros((len(powers1),len(powers2)))
        noise = np.zeros((len(powers1),len(powers2)))
        line = np.zeros((len(powers1),len(powers2)))
        
        for i in range(len(powers1)):
            for j in range(len(powers2)):
                ig = self.two_det(powers1[i],powers2[j],2.,48.,pvs,pvl,ratio,approx=approx)
                signoiseline[i,j] = ig[0]
                signoise[i,j] = ig[1]
                sigline[i,j] = ig[2]
                sig[i,j] = ig[3]
                noise[i,j] = ig[4]
                line[i,j] = ig[4]
                    
        return signoiseline,signoise,sigline,sig,noise,line



#------------------------------------
# Line aware statistic with consistent amplitude
# --------------------------------------


class LineAwareAmpStatistic:

    def __init__(self):
        pass

    def chi2_sig_amp(self,lamb,g1,g2,k,N,pv,logfrac):
        """
        function to generate the signal probability as a function of the power in each detector. includes a factor which includes the noise disrtibution and duty cycle for each of the detectors. works for 2 detectors.
        args
        ---------
        lamb: float
            factor proportional to the SNR
        g1: float
            SFT power in detector 1
        g2: float
            SFT power in detector 2
        k: int
            number of degrees of freedom for chi2 distribution
        N: int
            number of summed SFTs 
        pv: float
            width of the exponentional distribution used for the prior on lamb
        logfrac: float
            ratio of the detectors duty cycle and psd, \frac{S_2 f_1}{S_1 f_2}
        returns
        ----------
        prob: float
            probability of these two powers being a signal given the detector powers, duty cycles and noise psd
        """
        if logfrac>=0:
            func = st.ncx2.pdf(g1,df=N*k,nc=lamb,loc=0,scale=1)*st.ncx2.pdf(g2,df=N*k,nc=lamb*(10**(logfrac)),loc=0,scale=1)
        else:
            func = st.ncx2.pdf(g1,df=N*k,nc=lamb*(10**(-logfrac)),loc=0,scale=1)*st.ncx2.pdf(g2,df=N*k,nc=lamb,loc=0,scale=1)
        return func*st.expon.pdf(lamb,loc=0,scale=pv)

    def chi2_line_amp(lamb,g1,g2,k,N,pv,logfrac):
        """
        function to generate the line probability as a function of the power in each detector. includes a factor which includes the noise disrtibution and duty cycle for each of the detectors. works for 2 detectors.
        args
        ---------
        lamb: float
            factor proportional to the SNR
        g1: float
            SFT power in detector 1
        g2: float
            SFT power in detector 2
        k: int
            number of degrees of freedom for chi2 distribution
        N: int
            number of summed SFTs 
        pv: float
            width of the exponentional distribution used for the prior on lamb
        logfrac: float
            ratio of the detectors duty cycle and psd, \frac{S_2 f_1}{S_1 f_2}
        returns
        ----------
        prob: float
            probability of these two powers being a noise line given the detector powers, duty cycles and noise psd
        """
        if logfrac >= 0:
            func = st.chi2.pdf(g1,df=N*k,loc=0,scale=1)*st.ncx2.pdf(g2,df=N*k,nc=lamb*10**(logfrac),loc=0,scale=1) + st.ncx2.pdf(g1,df=N*k,nc=lamb,loc=0,scale=1)*st.chi2.pdf(g2,df=N*k,loc=0,scale=1)
        else:
            func = st.chi2.pdf(g1,df=N*k,loc=0,scale=1)*st.ncx2.pdf(g2,df=N*k,nc=lamb,loc=0,scale=1) + st.ncx2.pdf(g1,df=N*k,nc=lamb*10**(-logfrac),loc=0,scale=1)*st.chi2.pdf(g2,df=N*k,loc=0,scale=1)
        return 0.5*func*st.expon.pdf(lamb,loc=0,scale=pv)

    def chi2_noise_amp(g1,g2,k,N):
        """
        function to generate the noise probability as a function of the power in each detector.
        args
        ---------
        g1: float
            SFT power in detector 1
        g2: float
            SFT power in detector 2
        k: int
            number of degrees of freedom for chi2 distribution
        N: int
            number of summed SFTs 
        returns
        ----------
        prob: float
            probability of these two powers being noise given the detector powers
        """
        func = st.chi2.pdf(g1,df=N*k,loc=0,scale=1)*st.chi2.pdf(g2,df=N*k,loc=0,scale=1)
        return func
    
    def line_aware_amp(g1,g2,logfrac,k,N,pvs=10,pvl=10,ratio=1.):
        """
        marginalises over the "SNR" for both the noise and line case and combines into an odds ratio(using quad)
        args
        ---------
        g1: float
            SFT power in detector 1
        g2: float
            SFT power in detector 2
        k: int
            number of degrees of freedom for chi2 distribution
        N: int
            number of summed SFTs 
        pvs: float
            width of the exponentional distribution used for the prior on lamb in the signal case
        pvl: float
            width of the exponentional distribution used for the prior on lamb in the line case
        logfrac: float
            ratio of the detectors duty cycle and psd, \frac{S_2 f_1}{S_1 f_2}
        ratio: float
            ratio of the prior on the line model to the gaussian noise model, \frac{M_{N}}{M_{G}}
        returns
        ----------
        bsgl1: float
            log odds ratio of all three models \frac{M_{S}}{M_{L} + M_{G}}
        bsgl2: float
            log odds ratio of signal and gaussian noise models \frac{M_{S}}{M_{G}}
        bsgl3: float
            log odds ratio of signal and line models \frac{M_{S}}{M_{L}}
        sig_int: float
            log likelihood of signal model
        noise_func: float
            log likelihood of gaussian noise model
        line_int: float
            log likelihood of line model
        """
        sig_int, sig_err = quad(chi2_sig_amp,0,np.inf, args = (g1,g2,k,N,pvs,logfrac))
        line_int, line_err = quad(chi2_line_amp,0,np.inf, args = (g1,g2,k,N,pvl,logfrac))
        bsgl1 = sig_int/(ratio*line_int + chi2_noise_amp(g1,g2,k,N))
        bsgl2 = sig_int/(chi2_noise_amp(g1,g2,k,N))
        bsgl3 = sig_int/line_int
        return np.log(bsgl1),np.log(bsgl2),np.log(bsgl3),np.log(sig_int),np.log(chi2_noise_amp(g1,g2,k,N)),np.log(line_int)

    def line_aware_amp_approx(g1,g2,logfrac,k,N,pvs=1,pvl=1,ratio=1.):
        """
        marginalises over the "SNR" for both the noise and line case and combines into an odds ratio (approximate using trapz)
        args
        ---------
        g1: float
            SFT power in detector 1
        g2: float
            SFT power in detector 2
        k: int
            number of degrees of freedom for chi2 distribution
        N: int
            number of summed SFTs 
        pvs: float
            width of the exponentional distribution used for the prior on lamb in the signal case
        pvl: float
            width of the exponentional distribution used for the prior on lamb in the line case
        logfrac: float
            ratio of the detectors duty cycle and psd, \frac{S_2 f_1}{S_1 f_2}
        ratio: float
            ratio of the prior on the line model to the gaussian noise model, \frac{M_{N}}{M_{G}}
        returns
        ----------
        bsgl1: float
            log odds ratio of all three models \frac{M_{S}}{M_{L} + M_{G}}
        bsgl2: float
            log odds ratio of signal and gaussian noise models \frac{M_{S}}{M_{G}}
        bsgl3: float
            log odds ratio of signal and line models \frac{M_{S}}{M_{L}}
        sig_int: float
            log likelihood of signal model
        noise_func: float
            log likelihood of gaussian noise model
        line_int: float
            log likelihood of line model
        """
        l = np.linspace(0,100,200)
        sig_int = np.trapz(np.nan_to_num(chi2_sig_amp(l,g1,g2,k,N,pvs,logfrac)),l)
        line_int = np.trapz(np.nan_to_num(chi2_line_amp(l,g1,g2,k,N,pvl,logfrac)),l)
        bsgl1 = sig_int/(ratio*line_int + chi2_noise_amp(g1,g2,k,N))
        bsgl2 = sig_int/(chi2_noise_amp(g1,g2,k,N))
        bsgl3 = sig_int/line_int
        return np.log(bsgl1),np.log(bsgl2),np.log(bsgl3),np.log(sig_int),np.log(chi2_noise_amp(g1,g2,k,N)),np.log(line_int)

    def line_aware_amp_cpp(g1,g2,logfrac,k,N,pvs=1,pvl=1,ratio=1.):
        """
        marginalises over the "SNR" for both the noise and line case and combines into an odds ratio (approximate using trapz)
        args
        ---------
        g1: float
            SFT power in detector 1
        g2: float
            SFT power in detector 2
        k: int
            number of degrees of freedom for chi2 distribution
        N: int
            number of summed SFTs 
        pvs: float
            width of the exponentional distribution used for the prior on lamb in the signal case
        pvl: float
            width of the exponentional distribution used for the prior on lamb in the line case
        logfrac: float
            ratio of the detectors duty cycle and psd, \frac{S_2 f_1}{S_1 f_2}
        ratio: float
            ratio of the prior on the line model to the gaussian noise model, \frac{M_{N}}{M_{G}}
        returns
        ----------
        bsgl1: float
            log odds ratio of all three models \frac{M_{S}}{M_{L} + M_{G}}
        bsgl2: float
            log odds ratio of signal and gaussian noise models \frac{M_{S}}{M_{G}}
        bsgl3: float
            log odds ratio of signal and line models \frac{M_{S}}{M_{L}}
        sig_int: float
            log likelihood of signal model
        noise_func: float
            log likelihood of gaussian noise model
        line_int: float
            log likelihood of line model
        """
        sig_int = integrals.Integral([g1],g2,logfrac,k,N,pvs,"signal")
        line_int = integrals.Integral([g1],g2,logfrac,k,N,pvl,"line")
        bsgl1 = sig_int/(ratio*line_int + chi2_noise_amp(g1,g2,k,N))
        bsgl2 = sig_int/(chi2_noise_amp(g1,g2,k,N))
        bsgl3 = sig_int/line_int
        return np.log(bsgl1),np.log(bsgl2),np.log(bsgl3),np.log(sig_int),np.log(chi2_noise_amp(g1,g2,k,N)),np.log(line_int)

    
    def gen_lookup_line_aware_amp(x,y,n1,int_type = 'chi2',approx=True,pvs=1,pvl=1,ratio=1):
        """
        calculates the odds ratio in ch_integrals_approx_noise for given values of power and ratio.
        args
        --------
        x: array
            array of the SFT power in detector 1
        y: array
            array of SFT power in detector 2
        n1: array
            array of the ratios of the duty cycle and noise psds, \frac{f_{1} S_{2}}{f_{2} S_{1}}
        int_type: string
            which statistic to use ("chi2" only option for now)
        approx: bool
            choose whether to use trapz or quad to complete integrals
        pvs: float
            width on prior for signal model
        pvl: float
            width on prior for line model
        ratio: float
            ratio of the priors on the line and signal models
        returns
        ----------
        val: array
            array of odd ratio with 3 models
        val1: array
            array of odd ratio with signal/noise model
        val2: array
            array of odd ratio with signal/line model
        val3: array
            array of signal likelihoods
        val4: array
            array of noise likelihoods
        val: array
            array of line likelihoods
        """
        val = np.zeros((len(x),len(y),len(n1)))
        val1 = np.zeros((len(x),len(y),len(n1)))
        val2 = np.zeros((len(x),len(y),len(n1)))
        val3 = np.zeros((len(x),len(y),len(n1)))
        val4 = np.zeros((len(x),len(y),len(n1)))
        val5 = np.zeros((len(x),len(y),len(n1)))
        for i in range(len(x)):
            for j in range(len(y)):
                for k in range(len(n1)):
                    if approx:
                        ig = line_aware_amp_approx(x[i],y[j],n1[k],2.,48.,pvs,pvl,ratio)
                    else:
                        ig = line_aware_amp_cpp(x[i],y[j],n1[k],2.,48.,pvs,pvl,ratio)
                    val[i,j,k] = ig[0]
                    val1[i,j,k] = ig[1]
                    val2[i,j,k] = ig[2]
                    val3[i,j,k] = ig[3]
                    val4[i,j,k] = ig[4]
                    val5[i,j,k] = ig[5]
        return val,val1,val2,val3,val4,val5
            
    def gen_lookup_line_aware_amp_cpp(g1,g2,logfrac,pvs,pvl,ratio):
        """
        calculates the odds ratio in ch_integrals_approx_noise for given values of power and ratio.
        args
        --------
        g1: array
            array of the SFT power in detector 1
        g1: array
            array of SFT power in detector 2
        logfrac: array
            array of the ratios of the duty cycle and noise psds, \frac{f_{1} S_{2}}{f_{2} S_{1}}
        pvs: float
            width on prior for signal model
        pvl: float
            width on prior for line model
        ratio: float
            ratio of the priors on the line and signal models
        returns
        ----------
        val: array
            array of odd ratio with 3 models
        val1: array
            array of signal likelihoods
        val2: array
            array of line likelihoods
        val3: array
            array of noise likelihoods
        """
        return np.log(integrals.Integral(list(g1),list(g2),list(logfrac),2,48,pvs,pvl,ratio))
