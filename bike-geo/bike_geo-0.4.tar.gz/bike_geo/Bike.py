import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns

class Bike:

    def __init__(self, HTA, STA, BB_drop, CSL, SH, frame_stack, frame_reach):

        """ Bike class for calculating and visualizing the stack, reach, and chainstay to rear hub horizontal distance. The stack and               reach are adjusted from the input values to account for the position of the stem above the headtube. 
            Attributes:
                HTA (float) representing the head tube angle
                STA (float) representing the seat tube angle
                BB_drop (float) representing the vertical drop from hub centers to bottom bracket center
                CSL (float) representing chainstay length along chainstay from hub to bottom bracket
                SH (float) representing the distance from bottom bracket center to the top of the seat, not the vertical height
        """

        self.HTA = HTA
        self.STA = STA
        self.BB_drop = BB_drop
        self.CSL = CSL
        self.SH = SH
        self.frame_stack = frame_stack
        self.frame_reach = frame_reach

    def calculate_reach(self):

        """Function to calculate the reach at your seat height. The number is stored in the actual_reach attribute.

                Args:
                    None
                Returns:
                    float: the actual reach of your bike at your seat height

        """
        self.actual_stack = self.calculate_stack()
        added_stack = self.actual_stack - self.frame_stack
        lost_reach = added_stack/math.tan(math.radians(self.HTA))
        self.actual_reach = self.frame_stack - lost_reach

        return self.actual_reach

    def calculate_stack(self):	

        """Function to calculate the stack at your seat height. The number is stored in the actual_stack attribute.

                Args:
                    None

                Returns:
                    float: the actual stack of your bike at your seat height

        """
        self.actual_stack = self.SH * math.cos(math.radians(90 - self.STA))
        return self.actual_stack

    def calculate_chainstay_overhang(self):	

        """Function to calculate the horizontal offset from your seat to the bottom bracket center. The number is stored in the                    actual_chainstay_overhang attribute. The function also calculates the overhang of a seat positioned parallel with the top                of the head tube. The number is stored in the frame_chainstay_overhang attribute.

               Args:
                   None
               Returns:
                   float: the horizontal distance from seat to bottom bracket shell

        """
        #horizontal_CSL = math.sqrt(self.CSL**2 + self.BB_drop**2)

        self.frame_chainstay_overhang = self.frame_stack * math.tan(math.radians(90 - self.STA))

        self.actual_chainstay_overhang = self.actual_stack * math.tan(math.radians(90 - self.STA))

        return self.actual_chainstay_overhang

    def compare_bikes(self, other):	

        """Function to graphically compare the stack, reach, and seat-to-rear hub distance for two different bike objects.

                Args:
                    other (Bike): Bike instance
                Returns:
                    None

        """
        bike_properties = pd.DataFrame({'bike_1': [self.calculate_stack(), self.calculate_reach(), self.calculate_chainstay_overhang()], 'bike_2': [other.calculate_stack(), other.calculate_reach(), other.calculate_chainstay_overhang()]})
        sns.barplot(data = bike_properties)
        plt.title('Bike 1 vs Bike 2')
        plt.ylabel('value')
        plt.xlabel('measurement')
        plt.show()
