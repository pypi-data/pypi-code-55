import matplotlib.pyplot as plt
import math
from distkit.general import *


class Gaussian(Distribution):
    """ Gaussian distribution class for calculating and
    visualizing a Gaussian distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        std (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats extracted from the data file """

    def __init__(self, mu=0, sigma=1):
        Distribution.__init__(self, mu, sigma)

    def calculate_mean(self):
        """ Function to calculate the mean of the data set.

        Args:
            None
        Returns:
            float: mean of the data set """

        self.mean = float(sum(self.data) / len(self.data))
        return self.mean

    def calculate_stdev(self, sample=True):
        """ Function to calculate the standard deviation of the data set.

        Args:
            sample (bool): whether the data represents a sample or population
        Returns:
            float: standard deviation of the data set """

        if sample:
            n = len(self.data) - 1
        else:
            n = len(self.data)

        var = sum([(i - self.mean) ** 2 for i in self.data])
        self.std = math.sqrt(var / n)

        return self.std

    def read_data_file(self, file_name, sample=True):
        """ Function to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.
        After reading in the file, the mean and standard deviation are calculated

        Args:
            file_name (string): name of a file to read from
        Returns:
            None """

        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(line)
                file.readline()
        file.close()

        self.data = data_list
        self.mean = self.calculate_mean()
        self.std = self.calculate_stdev(sample)

    def plot_histogram(self):
        """ Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None
        Returns:
            None """

        plt.hist(self.data)
        plt.title('Histogram of Data')
        plt.xlabel('Data')
        plt.ylabel('Frequency')

    def pdf(self, x):
        """Probability density function calculator for the gaussian distribution.

        Args:
            x (float): point for calculating the probability density function
        Returns:
            float: probability density function output
        """

        return (1.0 / math.sqrt(2 * math.pi) * math.pow(self.std, 2)) * math.e ** (
                -math.pow(x - self.mean, 2) / (2 * math.pow(self.std, 2)))

    def plot_histogram_pdf(self, n_spaces=25):
        """ Function to plot the normalized histogram of the data and a plot of the
        probability density function along the same range

        Args:
            n_spaces (int): number of data points
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot """

        mu = self.mean
        sigma = self.std
        min_range = min(self.data)
        max_range = max(self.data)

        # calculates the interval between x values
        interval = 1.0 * (max_range - min_range) / n_spaces

        x, y = [], []

        for i in range(n_spaces):
            tmp = min_range + interval * i
            x.append(tmp)
            y.append(self.pdf(tmp))

            # make the plots
            fig, axes = plt.subplots(2, sharex=True)
            fig.subplots_adjust(hspace=.5)
            axes[0].hist(self.data, density=True)
            axes[0].title('Normed Histogram of Data')
            axes[0].ylabel('Density')

            axes[1].plot(x, y)
            axes[1].title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
            axes[0].ylabel('Density')
            plt.show()

            return x, y

    def __add__(self, other):
        """ Function to add together two Gaussian distributions

        Args:
            other (Gaussian): Gaussian instance
        Returns:
            Gaussian: Gaussian distribution """

        result = Gaussian()
        result.mean = self.mean + other.mean
        result.std = math.sqrt(self.std ** 2 + other.std ** 2)

        return result

    def __repr__(self):
        """Function to output the characteristics of the Gaussian instance

        Args:
            None
        Returns:
            string: characteristics of the Gaussian """

        return "mean {}, standard deviation {}".format(self.mean, self.std)
