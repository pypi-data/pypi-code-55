from .general import *

class segment: 
    
    def __init__(self, movingrange, segment_start, segment_end, samples = 8):
        self.mR_series = []
        self.samples = samples
        self.start = segment_start
        self.end = segment_end
        self.mr = movingrange
        self.value_series = movingrange.value_series[segment_start:segment_end]
        self.mR_series = [abs(self.value_series[i+1]-self.value_series[i]) for i in range(len(self.value_series)-1)]

    def moving_range_mean(self):
        return mean(self.mR_series[0:self.samples])

    def moving_range_sigma(self):
        # mean x 3.267 = mean + 3 x sigma => sigma = (mean x 2.267) / 3
        mr_mean = self.moving_range_mean()
        sigma = (mr_mean * 2.267) / 3
        return sigma

    def moving_range_standard_deviation(self, number = 1):
        mr_mean = self.moving_range_mean()
        sigma = self.moving_range_sigma()
        std_dev = mr_mean + (sigma * number)
        if std_dev < 0:
            std_dev = 0
        return std_dev

    # puts mRs into a bin corresponding to their displacement from the mean in standard deviations
    def moving_range_bins(self):
        bins = []
        mr_mean = self.moving_range_mean()
        sigma = self.moving_range_sigma()
        for value in range(len(self.mR_series)):
            if sigma == 0:
                bin = 0
            else:
                bin = binner((self.value_series[value] - i_mean) / sigma)
            bins.append(bin)
        return bins

    # returns an array with items of 1 (increase), 0 (stable) or -1 (reduction)
    def moving_range_direction(self):
        directions = []
        for i in range(len(self.mR_series) - 1):
            delta = self.mR_series[i + 1] - self.mR_series[i]
            if delta == 0:
                direction = 0
            else:
                direction = delta / abs(delta)
            directions.append(direction)
        return directions

    def moving_range_sigma_line(self, number = 1):
        value = self.moving_range_standard_deviation(number)
        return [value] * len(self.value_series)

    def individuals_mean(self):
        return mean(self.value_series[0:self.samples])

    def individuals_sigma(self):
        mr_mean = self.moving_range_mean()
        sigma = (2.66 * mr_mean) / 3
        return sigma

    def individuals_standard_deviation(self, number = 1):
        i_mean = self.individuals_mean()
        sigma = self.individuals_sigma()
        std_dev = i_mean + (sigma * number)
        return std_dev

    # puts observations into a bin corresponding to their displacement from the mean in standard deviations
    def individuals_bins(self):
        bins = []
        i_mean = self.individuals_mean()
        sigma = self.individuals_sigma()
        for value in range(len(self.value_series)):
            if sigma == 0:
                bin = 0
            else:
                bin = binner((self.value_series[value] - i_mean) / sigma)
            bins.append(bin)
        return bins

    # returns an array with items of 1 (increase), 0 (stable) or -1 (reduction)
    def individuals_direction(self):
        directions = []
        for i in range(len(self.value_series) - 1):
            delta = self.value_series[i + 1] - self.value_series[i]
            if delta == 0:
                direction = 0
            else:
                direction = delta / abs(delta)
            directions.append(direction)
        return directions

    def describe(self):
        i_mean = self.individuals_mean()
        sigma = self.individuals_sigma()
        bins = self.individuals_bins()

        description = 'Segment' + '\n'
        description = description + '===========================' + '\n'
        description = description + 'Number of Samples = ' + str(len(self.value_series)) + '\n'
        description = description + 'Start Position = ' + str(self.start) + '\n'
        description = description + 'End Position = ' + str(self.end) + '\n'
        description = description + 'Segment Minimum = ' + str(min(self.value_series)) + '\n'
        description = description + 'Segment Maximum = ' + str(max(self.value_series)) + '\n'
        description = description + '---------------------------' + '\n'
        description = description + 'Segment Mean = ' + '{:.3f}'.format(i_mean) + '\n'
        description = description + 'Items Above Mean = ' + str(len(matches(bins, lambda t: t > 0))) + '\n'
        description = description + 'Items Below Mean = ' + str(len(matches(bins, lambda t: t < 0))) + '\n'
        description = description + 'Average Change = ' + '{:.3f}'.format(mean(self.mR_series)) + '\n'
        # longest run of increase
        # longest run of decrease
        description = description + '---------------------------' + '\n'
        description = description + 'Sigma(X) = ' + '{:.3f}'.format(sigma) + '\n'
        description = description + ' 3+ Sigma = (' + str(len(matches(bins, lambda t: t > 3))) + ' items)\n'
        description = description + ' 3  Sigma = ' + '{:.3f}'.format(self.individuals_standard_deviation(3)) + ' (' + str(len(matches(bins, lambda t: t == 3))) + ' items)\n'
        description = description + ' 2  Sigma = ' + '{:.3f}'.format(self.individuals_standard_deviation(2)) + ' (' + str(len(matches(bins, lambda t: t == 2))) + ' items)\n'
        description = description + ' 1  Sigma = ' + '{:.3f}'.format(self.individuals_standard_deviation(1)) + ' (' + str(len(matches(bins, lambda t: t == 1))) + ' items)\n'
        description = description + ' 0  Sigma = ' + '{:.3f}'.format(self.individuals_standard_deviation(0)) + ' (' + str(len(matches(self.value_series, lambda t: t == i_mean))) + ' items)\n'
        description = description + '-1  Sigma = ' + '{:.3f}'.format(self.individuals_standard_deviation(-1)) + ' (' + str(len(matches(bins, lambda t: t == -1))) + ' items)\n'
        description = description + '-2  Sigma = ' + '{:.3f}'.format(self.individuals_standard_deviation(-2)) + ' (' + str(len(matches(bins, lambda t: t == -2))) + ' items)\n'
        description = description + '-3  Sigma = ' + '{:.3f}'.format(self.individuals_standard_deviation(-3)) + ' (' + str(len(matches(bins, lambda t: t == -3))) + ' items)\n'
        description = description + '-3+ Sigma = (' + str(len(matches(bins, lambda t: t < -3))) + ' items)\n'
        print (description)

    def individuals_sigma_line(self, number = 1):
        value = self.individuals_standard_deviation(number)
        return [value] * len(self.value_series)

def binner(number):
    result = number // 1
    if result >= 0:
        result = result + 1
    return result
