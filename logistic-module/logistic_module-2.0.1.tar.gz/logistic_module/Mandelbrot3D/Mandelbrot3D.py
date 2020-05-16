import numpy as np
import plotly
import plotly.graph_objects as go

class Mand_3D:
    
    """Class containing two functions to plot the Mandelbrot set in 3D and one to make it interactive :  
        
         1) Create square area observed formed by X and Y axis
         
         2) Matrix of elevation value of the Mandelbrot set in 2D as Z parameter
         
         3) Use the two later points to make an interactive vizualisation of the Mandelbrot set"""
    
    
    def __init__(self,n,M,L,dx,dy):
        
        """Initialization of the parameters of the class  
          
        :param n: Number of iteration of the Mandelbrot equation  
        :type n: int  
          
        :param M: Number of pixels
        :type M: int  
        
        :param L: Length of the square area observed  
        :type L: float  
        
        :param dx: Shift of the square area origin along the x axis compared to (0,0)  
        :type dx: float  
        
        :param dy: Shift of the square area origin along the y axis compared to (0,0)  
        :type dy: float
        """
        
        self.n = n
        self.M = M
        self.L = L
        self.dx = dx
        self.dy = dy


    def init_param():

        """ Initialize the parameters for the modelization with asked input :    
         
         :return:  - n : number of iteration of the Mandelbrot equation    
                   - M : number of pixels  
         :rtype: int,int  """

        n = int(input("Enter a value for n :"))
        M = int(input("Enter a value for M :"))

        return n,M
    
    
    def grid(self):
        
        """Set the square area observed : 
        
            - Define two numpy arrays X and Y with the following characteristics : 
            
              - Index of the middle element : dx/dy respectively
              - length 2*L
              - M elements
              
           :return: A grid formed by X and Y  
           :rtype: Numpy grid """
        
                
        x = np.linspace(-self.L+self.dx,self.L+self.dx,self.M)    
        y = np.linspace(-self.L+self.dy,self.L+self.dy,self.M)
        X,Y = np.meshgrid(x,y)
        
        return X,Y
    
 
    def mand(self):
        
        """Set the matrix of elevation values :  
         
            1) Initialize the elements of the Mandelbrot equation
            2) Compute n iteration of the Mandelbrot equation on a (M,M) shaped 2D-array  
            3) Apply an elevation function on this 2D-array
            4) Filter the element where we apply the elevation function
            
           :return: The elevated 2D Mandelbrot set as a 2D-array  
           :rtype: Numpy 2D-array  """
        
        X,Y = self.grid()
        C = X + 1j*Y   
        Z = C
        
        for k in range(1,(self.n)+1):     
            ZZ = Z**2 + C
            Z = ZZ
            
        W = np.e**(-np.abs(Z)) - 0.625
        W[W>0] = W[W>0]*0.0001
        
        return W

    
    def interact(self):
    
        """ Make an interactive vizualisation of the Mandelbrot set in 3D with plotly  
            
            :return: 3D figure of the Mandelbrot set     
            :rtype: Interactive object"""

        fig = go.Figure(data = [go.Surface(z=self.mand(), x=self.grid()[0], y=self.grid()[1],                                   
                                           colorscale = 'Reds', 
                                           showscale = False,
                                           connectgaps = False,
                                           hoverinfo = "none",
                                           contours = dict(x = dict(highlight = False),
                                                           y = dict(highlight = False),
                                                           z = dict(highlight = False))), 

                                go.Surface(z=-self.mand(), x=self.grid()[0], y=self.grid()[1],
                                           colorscale = 'Reds',
                                           reversescale = True,
                                           showscale = False,
                                           connectgaps = False,
                                           hoverinfo = "none",
                                           showlegend = False,
                                           contours = dict(x = dict(highlight = False),
                                                           y = dict(highlight = False),
                                                           z = dict(highlight = False)))],                       
                
                                layout = go.Layout(title='Mandelbrot 3D interactive visualization',
                                                   width = 600,
                                                   height = 600,
                                                   hovermode= 'closest',
                                                   template = "plotly_dark",
                                                   scene = dict(xaxis = dict(visible = False),
                                                                yaxis = dict(visible = False),
                                                                zaxis = dict(visible = False),
                                                                hovermode = False,
                                                                camera = dict(eye=dict(x=0, y=-0.8, z=2.5) ))))
    
        return fig

