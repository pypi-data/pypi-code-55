import plotly
import plotly.graph_objects as go
import warnings 

from .Mandelbrot3D import Mand_3D

warnings.filterwarnings("ignore")


def animation(mand):

        """ Animate the rotation of the Mandelbrot set in 3D.  
            Show the bijection between Mandelbrot set and bifurcation diagram.  
            Use the Mand_3D class from Mandelbrot3D.  

            :param mand: 3D figure of the Mandelbrot set  
            :type mand: plotly.graph_objs._figure.Figure  
            
            :return: Rotation of the Mandelbrot set in 3D   
            :rtype: Animation 3D"""

        anim = mand.interact() 

        updatemenus=[dict(type='buttons',
                  showactive=True,
                  y=1,
                  x=0.8,
                  xanchor='left',
                  yanchor='bottom',
                  pad=dict(t=45, r=10),
                  buttons=[dict(label='Play',
                                 method='animate',
                                 args=[None, dict(frame=dict(duration=5, redraw=True), 
                                                             transition=dict(duration=0, easing='linear'),
                                                             fromcurrent=True,
                                                             mode='immediate'
                                                            )])])]


        anim.update_layout(updatemenus=updatemenus, title = 'Mandelbrot 3D rotation')
        anim.update_traces(go.Surface(contours = dict(y = dict(highlight = False,
                                                                    show = True,
                                                                    start = -2,
                                                                    end = 2,
                                                                    size = 1,
                                                                    color = "yellow"))))


        frames = []

        xt = 0
        yt = -0.8
        zt = 2.5

        for t in range(10):
            xt = xt
            yt = yt - 0.08
            zt = zt - 0.1
            frames.append(go.Frame(layout=dict(scene_camera_eye=dict(x=xt,y=yt,z=zt))))
    
        anim.frames=frames

        return anim