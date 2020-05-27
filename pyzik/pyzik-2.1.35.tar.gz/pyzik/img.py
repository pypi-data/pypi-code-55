# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 17:30:21 2020

@author: jazzn
"""

import numpy as np
from PIL import Image,ImageFilter 
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class Img:
    def __init__(self,file,rad=0):
        img = Image.open(file)
        print(f"{file} :\tFormat={img.format}\tSize={img.size}\tMode={img.mode}")
        if rad != 0:
            rad = 4 if rad>4 else rad
            img = img.filter(ImageFilter.GaussianBlur(radius = rad))
        self.array = np.array(img)
    
    def image2D(self,band='L'):
        if band == "L":
            tab_n, color_sc = self.array[:,:,0]*0.299 + self.array[:,:,1]*0.587 + self.array[:,:,2]*0.114,None
        elif band in "RGB":
            tab_n,color_sc = self.array[:,:,"RGB".index(band)],{'R':'reds','G':'greens','B':'blues'}[band]
        elif band =='normal':
            tab_n, color_sc = self.array,None
        elif band == 'all':
            tab_n, color_sc = np.vstack((self.array[:,:,0]*0.299 + self.array[:,:,1]*0.587 + self.array[:,:,2]*0.114,self.array[:,:,0],self.array[:,:,1],self.array[:,:,2])), None
        fig = px.imshow(tab_n,color_continuous_scale=color_sc)
        fig.update_layout(autosize=True,width=800, height=800,margin=dict(l=10, r=10, b=10, t=10)
                          ,title="image ",xaxis_title="x (px)",yaxis_title="y (px)")
        return fig.show()
    
    def image3D(self,band='L'):
        if band == "L":
            tab_n = self.array[:,:,0]*0.299 + self.array[:,:,1]*0.587 + self.array[:,:,2]*0.114
        elif band in "RGB":
            tab_n = self.array[:,:,"RGB".index(band)]
        img_df = pd.DataFrame(data=tab_n[1:,1:],index=tab_n[1:,0],columns=tab_n[0,1:])  
        fig = go.Figure(data=[go.Surface(z=img_df.values)])
        fig.update_layout(autosize=True,width=800, height=800,margin=dict(l=10, r=10, b=10, t=10))
        return fig.show()
    
    def lumni(self,band='L',**d):
        ymax,xmax,_ = self.array.shape
        y = d.get("y",-1)
        x = d.get("x",-1)
        if band == "L":
            tab_n = self.array[:,:,0]*0.299 + self.array[:,:,1]*0.587 + self.array[:,:,2]*0.114
        elif band in "RGB":
            tab_n = self.array[:,:,"RGB".index(band)]
        assert x>=0 or y>=0,"x or y not defined"
        if y>=0:
            x = np.arange(0,xmax)
            fig = px.line(x=x,y=tab_n[y,:])
            fig.update_layout(title = f"Luminosité le long du trait de coupe y={y} px - filtre={band}",xaxis_title="x (px)",yaxis_title="Luminosité")
            return fig.show()
        if x>=0:
            y = np.arange(0,ymax)
            fig = px.line(x=y,y=tab_n[:,x])
            fig.update_layout(title = f"Luminosité le long du trait de coupe x={x} px - filtre={band}",xaxis_title="y (px)",yaxis_title="Luminosité")
            return fig.show()