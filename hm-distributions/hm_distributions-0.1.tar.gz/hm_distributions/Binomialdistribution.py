import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


class Binomial(Distribution):
    """ Binomial distribution class for calculating and
    visualizing a Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials

    """

    #       A binomial distribution is defined by two variables:
    #           the probability of getting a positive outcome
    #           the number of trials

    #       If you know these two values, you can calculate the mean and the standard deviation
    #
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))

    #

    def __init__(self, prob=.4, size=20):

        Distribution.__init__(self, mu=0, sigma=1)
        self.p = prob
        self.n = size

    def calculate_mean(self):

        """Function to calculate the mean from p and n

        Args:
            None

        Returns:
            float: mean of the data set

        """

        mean = self.n * self.p
        self.mean = mean
        return (mean)

    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set

        """

        stdev = math.sqrt(self.n * self.p * (1 - self.p))
        self.stdev = stdev
        return (stdev)

    def read_data_file(self, file_name):

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
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()

    def replace_stats_with_data(self):

        """Function to calculate p and n from the data set

        Args:
            None

        Returns:
            float: the p value
            float: the n value

        """

        n = len(self.data)
        p = self.data.count(1) / n
        self.n = n
        self.p = p
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return (p, n)

    def plot_bar(self):
        """Function to output a bar plot for the data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """

        plt.bar(self.data)
        plt.title('category counts')
        plt.xlabel('category')
        plt.ylabel('count')

    def pdf(self, k):
        """Probability density function calculator for the binomial distribution

        Args:
            k (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """

        fac = math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n - k))
        pdf = fac * math.pow(self.p, k) * math.pow((1 - self.p), self.n - k)
        return (pdf)

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """

        pdf_list = []
        num = list(range(self.n + 1))
        for k in num:
            pdf_list.append(self.pdf(k))

        plt.bar(pdf_list)
        plt.title('pdf bar plot')
        plt.xlabel('number of successes')
        plt.ylabel('pdf')

        return (num, pdf_list)

    def __add__(self, other):

        """Function to add together two Binomial hm_distributions with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution

        """

        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        new = Binomial()
        new.p = self.p
        new.n = self.n + other.n
        return (new)

    def __repr__(self):

        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Gaussian

        """

        return ("mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n))
