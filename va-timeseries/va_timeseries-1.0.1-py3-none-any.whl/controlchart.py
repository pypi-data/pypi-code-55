from .rulesets import *
from .segment import *
from .general import *
import math

class controlchart: 
    # https://en.wikipedia.org/wiki/Shewhart_individuals_control_chart
    
    def __init__(self, baseline_sample_size = 8):
        self.period_series = []
        self.value_series = []
        self.segments = []
        self.mR_series = []
        self.rules = rulesets(self)
        self.baseline_sample_size = baseline_sample_size

    def load_from_pandas(self, df, period_column, value_column):
        import pandas
        self.load_from_arrays(df[period_column].tolist(), df[value_column].tolist())

    def load_from_arrays(self, period_series, value_series):
        self.mR_series = []
        self.period_series = [str(interval) for interval in period_series]
        self.value_series = value_series
        self.value_series = fillna(self.value_series, math.nan)
        self.segments = self.segment_data()
        self.mR_series = [abs(self.value_series[i+1]-self.value_series[i]) for i in range(len(self.value_series)-1)]

    # when <baseline_sample_size> samples fall the same side of the mean, recalculate the 
    # mean and standard deviations
    def segment_data(self):
        # not big enough to have more than one segment
        if (len(self.value_series) < (2 * self.baseline_sample_size)):
            pass

        # <baseline_sample_size> of 0 (or less) mean don't segment the data
        if self.baseline_sample_size < 1:
            self.baseline_sample_size = len(self.value_series)

        boundaries = []
        last_boundary = 0

        current_mean = mean(self.value_series[0:self.baseline_sample_size])
        for start in range(len(self.value_series) - self.baseline_sample_size + 1):
            # don't start a new segment close to the last
            if (start - self.baseline_sample_size) > last_boundary:
                cummulative_sum = 0
                for index in range(self.baseline_sample_size):
                    delta = self.value_series[start + index] - current_mean
                    # avoid divide by 0
                    if delta == 0:
                        side = 0
                    else:
                        side = delta / abs(delta)
                    cummulative_sum = cummulative_sum + side
                if abs(cummulative_sum) == self.baseline_sample_size:
                    boundaries.append((last_boundary, start))
                    last_boundary = start
                    current_mean = mean(self.value_series[start + 1:(start + self.baseline_sample_size)])
        # add everything else to the last segment
        boundaries.append((last_boundary, len(self.value_series)))

        # create segments out of the boundaries
        segments = []
        for boundary in boundaries:
            start, end = boundary
            segments.append(segment(self, start, end, self.baseline_sample_size))
        return segments

    # summary information
    def describe(self):
        description = 'Population' + '\n'
        description = description + '======================' + '\n'
        description = description + 'Number of Samples = ' + str(len(self.value_series)) + '\n'
        description = description + 'Population Mean = ' + '{:.3f}'.format(mean(self.value_series)) + '\n'
        description = description + 'Population Maximum = ' + str(max(self.value_series)) + '\n'
        description = description + 'Population Minimum = ' + str(min(self.value_series)) + '\n'
        description = description + 'Number of Segments = ' + str(len(self.segments)) + '\n'
        print (description)

    # collate the bin information from each of the segments
    def individuals_bins(self):
        bins = []
        for segment in self.segments:
            bins = bins + segment.individuals_bins()
        return bins

    # collate the direction information from the segments
    def individuals_direction(self):
        directions = []
        for segment in self.segments:
            directions = directions + segment.individuals_direction()
        return directions

    def individuals_sigma_line(self, number):
        sigma_line = []
        for segment in self.segments:
            sigma_line = sigma_line + segment.individuals_sigma_line(number)
        return sigma_line

    def moving_range_sigma_line(self, number):
        sigma_line = []
        for segment in self.segments:
            sigma_line = sigma_line + segment.moving_range_sigma_line(number)
        return sigma_line

    def plot(self, title="Process Behavior Chart", x_label="Period", i_label="X", mr_label="mR", file='', show_SD = False):        
        from matplotlib import pyplot as plt
        LARGE_FONT = 15
        plt.rc('font', size=LARGE_FONT)
        plt.figure(figsize=(20, 12))
        plt.title("Title")  

        # individuals
        ax = plt.subplot(211)
        plt.plot(self.period_series, self.value_series, marker='o', markersize=2, color='#6666CC')

        plt.plot(self.period_series, self.individuals_sigma_line(3), color='r', linestyle='--')
        plt.plot(self.period_series, self.individuals_sigma_line(0), color='g', linestyle='--')
        plt.plot(self.period_series, self.individuals_sigma_line(-3), color='r', linestyle='--')

        # include the SD lines on the plot
        if show_SD:
            plt.plot(self.period_series, self.individuals_sigma_line(2), color='r', linestyle=':')
            plt.plot(self.period_series, self.individuals_sigma_line(1), color='r', linestyle=':')
            plt.plot(self.period_series, self.individuals_sigma_line(-1), color='r', linestyle=':')
            plt.plot(self.period_series, self.individuals_sigma_line(-2), color='r', linestyle=':')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.title("Individuals")  
        plt.xlabel(x_label)
        plt.ylabel(i_label)
        ax.set_xticks(ax.get_xticks()[::self.baseline_sample_size])

        # moving range
        ax = plt.subplot(212)

        plt.plot(self.period_series[:-1], self.mR_series, marker='o', markersize=2, color='#6666CC')
        plt.plot(self.period_series, self.moving_range_sigma_line(3), color='r', linestyle='--')
        plt.plot(self.period_series, self.moving_range_sigma_line(0), color='g', linestyle='--')
        plt.plot(self.period_series, self.moving_range_sigma_line(-3), color='r', linestyle='--')

        # include the SD lines on the plot
        if show_SD:
            plt.plot(self.period_series, self.moving_range_sigma_line(2), color='r', linestyle=':')
            plt.plot(self.period_series, self.moving_range_sigma_line(1), color='r', linestyle=':')
            plt.plot(self.period_series, self.moving_range_sigma_line(-1), color='r', linestyle=':')
            plt.plot(self.period_series, self.moving_range_sigma_line(-2), color='r', linestyle=':')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.title("Moving Range")  
        plt.xlabel(x_label)
        plt.ylabel(mr_label)
        ax.set_xticks(ax.get_xticks()[::self.baseline_sample_size])

        # save the plot to a file
        if (len(file) > 0):
            plt.savefig(file, format='svg')
