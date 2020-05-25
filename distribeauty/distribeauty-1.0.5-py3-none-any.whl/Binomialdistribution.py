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
    
    
    TODO: Fill out all TODOs in the functions below
            
    """

    def __init__(self, prob=.5, size=20):

        self.p = prob
        self.n = size
         
 
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        super().__init__(self.mean, self.stdev)
        
        pass            
    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        self.mean = self.p * self.n
                
        return self.mean



    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """

        var = self.n * self.p * (1 - self.p)
        self.stdev = math.sqrt(var)
        return self.stdev
        
        
        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """        
   
        self.n = len(self.data)
        pos_trials = [i for i in self.data if i == 1]
        self.p = len(pos_trials)/self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n
        
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
            

        x_axis = [0, 1]
        y_axis = [self.data.count(0), self.data.count(1)]
        plt.bar(x_axis, y_axis)
        plt.xlabel('Trial')
        plt.ylabel('Distribution of Trials')
        plt.title('Bar Chart of Data')
        plt.show()
        
    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        n_fact = math.factorial(self.n)
        k_fact = math.factorial(k)
        diff_fact = math.factorial(self.n - k)
        n_choose_k = n_fact / (k_fact * diff_fact)
        pdf = n_choose_k * pow(self.p, k) * pow((1 - self.p), self.n - k)
        return pdf
          

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
    

        k = list(range(0, self.n + 1))
        pdfs = [self.pdf(i) for i in k]
        plt.plot(k, pdfs)
        plt.xlabel('Number of positive outcomes')
        plt.ylabel('Probability density function values')
        plt.title('Distribution of positive outcomes')
        
        return k, pdfs
                
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
            new_n = self.n + other.n
            new_distr = Binomial(self.p, new_n)
            return new_distr
        except AssertionError as error:
            raise
        

        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
  
        return "mean {}, standart deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
