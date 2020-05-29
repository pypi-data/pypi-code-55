import math
import matplotlib.pyplot as plt
import numpy as np
from .Generaldistribution import Distribution


class Gaussian(Distribution):
    """ Gaussian distribution class for calculating and
    visualizing a Gaussian distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats extracted from the data file

    """

    def __init__(self, mu=0, sigma=1):

        Distribution.__init__(self, mu, sigma)

    def calculate_mean(self):

        """Method to calculate the mean of the data set.

        Args:
            None

        Returns:
            float: mean of the data set

        """
        avg = np.mean(self.data)
        self.mean = avg
        return (self.mean)

    def calculate_stdev(self, sample=True):

        """Method to calculate the standard deviation of the data set.

        Args:
            sample (bool): whether the data represents a sample or population

        Returns:
            float: standard deviation of the data set

        """

        arr = np.array(self.data)
        mean = self.calculate_mean()
        deviation = arr - mean
        squared = np.square(deviation)
        sum_sqs = np.sum(squared)
        if sample is True:
            std_dev = np.sqrt(sum_sqs / (len(self.data) - 1))
            self.stdev = std_dev
            return std_dev
        else:
            std_dev = np.sqrt(sum_sqs / len(self.data))
            self.stdev = std_dev
            return std_dev

    def read_data_file(self, file_name, sample=True):

        """Method to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.
        After reading in the file, the mean and standard deviation are calculated

        Args:
            file_name (string): name of a file to read from

        Returns:
            None

        """

        # This code opens a data file and appends the data to a list called data_list
        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                data_list.append(int(line))
                line = file.readline()
        file.close()

        self.data = data_list

    def plot_histogram(self):
        """Method to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """

        plt.figure(figsize=(10, 6))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

    def pdf(self, x):
        """Probability density function calculator for the gaussian distribution.

        Args:
            x (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """

        dev_sqd = np.square((x - self.mean) / self.stdev)
        exponent = np.exp(-0.5 * dev_sqd)
        denom = self.stdev * np.sqrt(2 * math.pi)
        result = exponent / denom
        return (result)

    def plot_histogram_pdf(self, n_spaces=50):

        """Method to plot the normalized histogram of the data and a plot of the
        probability density function along the same range

        Args:
            n_spaces (int): number of data points

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """

        mu = self.mean
        sigma = self.stdev

        min_range = min(self.data)
        max_range = max(self.data)

        # calculates the interval between x values
        interval = 1.0 * (max_range - min_range) / n_spaces

        x = []
        y = []

        # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval * i
            x.append(tmp)
            y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2, sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y

    def __add__(self, other):
        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = np.sqrt(np.square(self.stdev) + np.square(other.stdev))
        return (result)

    def __repr__(self):
        return "mean {}, standard deviation {}".format(self.mean, self.stdev)
