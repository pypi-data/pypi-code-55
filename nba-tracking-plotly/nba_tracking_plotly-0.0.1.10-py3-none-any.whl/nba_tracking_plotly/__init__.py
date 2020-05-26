import plotly.graph_objects as go
from PIL import Image
import pandas as pd
import numpy as np
import os
from numpy import genfromtxt
import pkg_resources

def get_frame(team1_x_values, team1_y_values, team2_x_values, team2_y_values, ball_x_values, ball_y_values):
    frame = go.Frame(data=[
        go.Scatter(x=team1_x_values, y=team1_y_values, mode='markers', marker=dict(color="blue"), text=list(range(1,6))), 
        go.Scatter(x=team2_x_values, y=team2_y_values, mode='markers', marker=dict(color="green"), text=list(range(6,11))),
        go.Scatter(x=ball_x_values, y=ball_y_values, mode='markers', marker=dict(color="orange"))
    ])
    return frame
    
def plot_given_frames(frames, frame_duration=40, transition_duration=0):
    fig = go.Figure(
        data=[go.Scatter(x=frames[0]['data'][0]['x'], y=frames[0]['data'][0]['y'], mode='markers', marker=dict(color="blue"), text=list(range(1,6))),
              go.Scatter(x=frames[0]['data'][1]['x'], y=frames[0]['data'][1]['y'], mode='markers', marker=dict(color="green"), text=list(range(6,11))),
              go.Scatter(x=frames[0]['data'][2]['x'], y=frames[0]['data'][2]['y'], mode='markers', marker=dict(color="orange"))],
        layout=go.Layout(
            xaxis=dict(range=[0, 94], autorange=False),
            yaxis=dict(range=[0, 50], autorange=False),
            title="Live Court",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None, {'frame': {'duration':frame_duration, 'redraw': False},
                                'fromcurrent':True, 'transition':{'duration':transition_duration, 'easing':'linear'}}])])]),
        frames=frames
    )
    
    fig.update_traces(textposition='top center')


    fig.add_layout_image(
            dict(
                xref="x",
                yref="y",
                x=0,
                y=50,
                sizex=94,
                sizey=50,
                sizing="stretch",
                opacity=1,
                layer="below")
    )

    fig.update_layout(template="plotly_white", width=800, height=500, grid=None)
    fig.show()
    
def get_frames_from_dir(direct):
    
    arrs = pd.DataFrame()
    for filename in os.listdir(direct):
        if filename.endswith(".csv"): 
            person = filename.split('.')[0]
            if person == 'ball':
                person = '0'
            personarr = genfromtxt(os.path.join(direct,filename), delimiter=',')
            arrs[person+'x'] = personarr[:,0]
            arrs[person+'y'] = personarr[:,1]
            
    frames = []
    for i, row in arrs.iterrows():
        team1_x_values = []
        team1_y_values = []
        team2_x_values = []
        team2_y_values = []
        ball_x_values = []
        ball_y_values = []
            
        for x in range(1,6):
            team1_x_values.append(row[str(x)+'x'])
            team1_y_values.append(row[str(x)+'y'])
        for x in range(6,11):
            team2_x_values.append(row[str(x)+'x'])
            team2_y_values.append(row[str(x)+'y'])
            
        ball_x_values.append(row['0x'])
        ball_y_values.append(row['0y'])
        
        frame = get_frame(team1_x_values, 
                  team1_y_values, 
                  team2_x_values, 
                  team2_y_values, 
                  ball_x_values,
                  ball_y_values)
        frames.append(frame)
    plot_given_frames(frames)