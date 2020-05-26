import matplotlib.pyplot as plt
from scipy.stats import linregress
from Generalvoltammogram import Voltammogram

class Peaks(Voltammogram):
    def __init__(self, s_flat = 105, e_flat = 110, max_peak = 0,
                 min_peak = 0, peak_ref = 0):
            Voltammogram.__init__(self, s_flat, e_flat, max_peak, min_peak)
            self.peak_ref = peak_ref
            self.epp = 0
            self.enp = 0
            self.ppos = 0
            self.npos = 0
            self.bslope = 0
            self.y_flat = []
        
    def calculate_max(self):
            self.max = max(self.y_values)
            return self.max

    def calculate_min(self):
            self.min = min(self.y_values)
            return self.min

    def get_baseline_slope(self, inc = 2):
            start_scan = self.x_values.index(max(self.x_values))
            end_scan = self.y_values.index(self.min)
            slicer = (end_scan - start_scan)
            inc = int(slicer/10)
            slope_list = []
            for i in range(slicer-inc):
                x = self.x_values[start_scan+i:start_scan+i+inc]
                y = self.y_values[start_scan+i:start_scan+i+inc]
                res = linregress(x,y)
                if res.slope > 0:
                    slope_list.append(res.slope)
            self.bslope = min(slope_list)
            print(slope_list)
            return self.bslope
        
    def calculate_peak_ref(self):
            x_range = self.x_values
            y_range = self.y_values
            self.s_flat = self.x_values.index(max(self.x_values))
            
            m = self.bslope
            y = [m*x for x in x_range]
            b = y_range[self.s_flat]-y[self.s_flat]
            self.y_flat = y + b
            
            self.peak_ref = self.y_flat[y_range.index(min(y_range))]
            
            return self.peak_ref, self.y_flat
        
    def calculate_epp_enp(self):
            self.epp = self.max
            self.enp = self.min - self.peak_ref
            return self.epp, self.enp

    def get_pk_pos(self):
            self.ppos = self.x_values[self.y_values.index(self.max)]
            self.npos = self.x_values[self.y_values.index(self.min)]
            return self.ppos, self.npos

    def cv_plot(self):
            l_start = self.x_values[self.y_values.index(min(self.y_values))]
            
            plt.plot(self.x_values,self.y_values)
            plt.plot(self.x_values,self.y_flat,linewidth = 1, linestyle=('--'), color = 'k')
            plt.plot([l_start,l_start],[min(self.y_values),self.peak_ref], linestyle = ':', color = 'orange')

            text_center = [min(self.x_values), min(self.y_values)]
            plt.text(text_center[0], text_center[1],
                     "Ic = {:.2e} mA \nIa = {:.2e} mA\nEpp = {:.2e} mV \nEpp = {:.2e} mV \nΔEp = {:.2e} mV"
                     .format(self.epp, self.enp, self.ppos, self.npos, self.ppos-self.npos),
                     rotation=0, fontsize=8, verticalalignment = 'baseline', color = 'k')
            print(self.max)

            plt.title("Stretch Cyclic Voltammogram")
            plt.legend(['Average Current Density', 'Negative Peak Reference'])
            plt.xlabel("Electric Potential [mV]")
            plt.ylabel("Total Current [mA]")
            plt.show()
            
    def run_all(self):
            self.calculate_max()
            self.calculate_min()
            self.get_baseline_slope()
            self.calculate_epp_enp()
            self.get_pk_pos()
            self.calculate_peak_ref()
            self.cv_plot()
