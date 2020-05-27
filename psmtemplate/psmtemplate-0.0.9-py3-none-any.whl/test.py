import sys
import os
from psmtemplate import PSMA4
import ntpath
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import tkinter as tk
from tkinter import filedialog
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')
import math

#@title
# Material and section parameters
Es = 200000 # Steel modulus (MPa)
fck = 40 # Characterestic concrete compressive stnregth (MPa)
fcm = 48 # Mean concrete compressive stnregth (MPa)
Ecm = 35220 # Concrete modulus (MPa)
fctm = 3.5 # Mean concrete axial tensile strength (MPa)

# Crack spacing
k1 = 0.8 # Bond property coefficient
k3 = 3.40 # k3 Coefficient
k4 = 0.425 # k4 Coefficient

# Use RILEM Crack Width? 0 for NO, 1 for YES
RILEM = 0
RILEM_L = 35 # Length of steel fibres (mm)
RILEM_D = 0.55 # Diameter of steel fibres (mm)
RILEM_K1 = 1.6 # Plain bars

# Strain
strain_ratio = 5.68 # Ratio of Es/Ecm, alpha e
kt = 0.4 # load duration factor

# Concrete cover
# Defined as the clear cover to the transverse bar rather than the minimum cover
cover_top = 72 # (mm)
cover_bot = 72 # (mm)

# Dictionary to reference increment letter to Load Case
Load_Cases = {'A':'S2A','B':'S2B','C':'S3A','D':'S3B','E':'S9'}

# Dictionary to assign Zones and reo parameters to beam IDs
x1 = range(0,138)
x2 = range(138,282)
x3 = range(282,426)
zone = {}
dia_top = {}
spc_top = {}
dia_bot = {}
spc_bot = {}
liner_t = {}

for n in x1:
    zone[n] = 'Upper Wall'
    dia_top[n] = 16
    spc_top[n] = 150
    dia_bot[n] = 16
    spc_bot[n] = 150
    liner_t[n] = 700
for n in x2:
    zone[n] = 'Arch'
    dia_top[n] = 16
    spc_top[n] = 150
    dia_bot[n] = 24
    spc_bot[n] = 150
    liner_t[n] = 700
for n in x3:
    zone[n] = 'Lower Wall'
    dia_top[n] = 16
    spc_top[n] = 150
    dia_bot[n] = 16
    spc_bot[n] = 150
    liner_t[n] = 700

#@title 


import re
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import math
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

pd.options.display.float_format = '{:20,.2f}'.format

# Import structural actions from Strand7, assign beam and node numbers
column_names = ['ID','Shear Force 1','Bending Moment 1','Shear Force 2','Bending Moment 2','Axial Force','Torque','Axial Strain','Curvature 1','Curvature 2','Twist']
csv = pd.read_csv(r"C:\Users\Jianan Jiang\Documents\GitHub\Shotcrete\shotcrete-master\shotcrete\Strand7.csv", header=None)
No_cols = csv.shape[1]

df = pd.DataFrame(data=csv.values,columns=column_names[0:No_cols])
beams = []
nodes1 = []
nodes2 = []
inc_letters = []

for line in df['ID'].values:
    beam = re.findall('Beam +\d{1,10}', line)[0]
    beam_num = re.findall('\d{1,10}',beam)
    beams.append(beam_num[0])
    node = re.findall(' +\d{1,10}: +\d{1,10}',line)[0]
    node_num = re.findall('\d{1,10}',node)
    nodes1.append(node_num[0])
    nodes2.append(node_num[1])
    inc_letter = re.search(r"\[([A-Za-z0-9_]+)\]", line)
    inc_letter2 = re.search('[a-zA-Z]',inc_letter[0])
    inc_letters.append(inc_letter2[0])

df['Beam'] = beams
df['Node 1'] = nodes1
df['Node 2'] = nodes2
df['Increment Letter'] = inc_letters

zones = []
dia_tops = []
spc_tops = []
dia_bots = []
spc_bots = []
liner_ts = []

for i in df['Beam'].values:
    n = int(i)
    zones.append(zone[n])
    dia_tops.append(dia_top[n])
    spc_tops.append(spc_top[n])
    dia_bots.append(dia_bot[n])
    spc_bots.append(spc_bot[n])
    liner_ts.append(liner_t[n])

df['Zone'] = zones
df['Reo Diameter Top'] = dia_tops
df['Reo Spacing Top'] = spc_tops
df['Reo Diameter Bot'] = dia_bots
df['Reo Spacing Bot'] = spc_bots
df['Liner Thickness'] = liner_ts

# Calculate "MATLAB INPUTS"
df['d top'] = df['Reo Diameter Top']*0.5 + cover_top
df['d bot'] = df['Reo Diameter Bot']*0.5 + cover_bot
df['Ast top'] = math.pi * df['Reo Diameter Top']**2/4*1000/df['Reo Spacing Top']
df['Ast bot'] = math.pi * df['Reo Diameter Bot']**2/4*1000/df['Reo Spacing Bot']

# Start crack width calculations (from Crackwidths_plate_AR_20161117 - Author: Alex Rogan)
M = df['Bending Moment 2']*10**9
N = df['Axial Force']*10**6
A_stt = df['Ast top']
A_stb = df['Ast bot']
d_top = df['d top']
d_bot = df['d bot']
Depth = df['Liner Thickness']

f_c = fck
E_st = Es
E_c = 22*((f_c+8)/10)**0.3*1000

n = len(df)

d_N_ = []
e_t_ = []
e_b_ = []
e_stt_ = []
e_stb_ = []
case_ = []
g_ = []

for i in range(0,n):
    if M[i]>=0: #sagging 
        #Case 1
        a=1000*E_c*N[i]
        b=(-1500*Depth[i]*E_c*N[i]-3000*E_c*M[i])
        c=(3*A_stb[i]*Depth[i]*E_st*N[i]-6*A_stb[i]*E_st*N[i]*d_bot[i]-3*A_stt[i]*Depth[i]*E_st*N[i]+6*A_stt[i]*E_st*N[i]*d_top[i]-6*A_stb[i]*E_st*M[i]-6*A_stt[i]*E_st*M[i])
        d=-3*A_stb[i]*Depth[i]**2*E_st*N[i]+9*A_stb[i]*Depth[i]*E_st*N[i]*d_bot[i]-6*A_stb[i]*E_st*N[i]*d_bot[i]**2+3*A_stt[i]*Depth[i]*E_st*N[i]*d_top[i]-6*A_stt[i]*E_st*N[i]*d_top[i]**2+6*A_stb[i]*Depth[i]*E_st*M[i]-6*A_stb[i]*E_st*M[i]*d_bot[i]+6*A_stt[i]*E_st*M[i]*d_top[i]
        
        coeff = [a,b,c,d]
        g = np.roots(coeff)        
        g_i = g[np.imag(g)==0]
        g = np.real(g_i)
        
        if len(g)==3:
           g=g[2]
        
        g = g.item(0)
        d_N=g
        e_t=-N[i]/(-E_st*(d_N-Depth[i]+d_bot[i])*A_stb[i]/d_N-E_st*(d_N-d_top[i])*A_stt[i]/d_N-500*E_c*d_N)
        e_b=-e_t*(-d_N+Depth[i])/d_N
        e_stt=e_t*(d_N-d_top[i])/d_N
        e_stb=-e_t*(-d_N+Depth[i]-d_bot[i])/d_N
        case=1
        
        #Case 3
        if d_N < 0 or d_N > Depth[i] and N[i] < 0:
          d_N=(1/3)*(3*A_stb[i]*Depth[i]**2*E_st*N[i]-9*A_stb[i]*Depth[i]*E_st*N[i]*d_bot[i]+6*A_stb[i]*E_st*N[i]*d_bot[i]**2-3*A_stt[i]*Depth[i]*E_st*N[i]*d_top[i]+6*A_stt[i]*E_st*N[i]*d_top[i]**2+500*Depth[i]**3*E_c*N[i]-6*A_stb[i]*Depth[i]*E_st*M[i]+6*A_stb[i]*E_st*M[i]*d_bot[i]-6*A_stt[i]*E_st*M[i]*d_top[i]-3000*Depth[i]**2*E_c*M[i])/(A_stb[i]*Depth[i]*E_st*N[i]-2*A_stb[i]*E_st*N[i]*d_bot[i]-A_stt[i]*Depth[i]*E_st*N[i]+2*A_stt[i]*E_st*N[i]*d_top[i]-2*A_stb[i]*E_st*M[i]-2*A_stt[i]*E_st*M[i]-2000*Depth[i]*E_c*M[i])
          e_t = -N[i]/(-E_st*(d_N-Depth[i]+d_bot[i])*A_stb[i]/d_N-E_st*(d_N-d_top[i])*A_stt[i]/d_N-500*E_c*(1-(d_N-Depth[i])/d_N)*Depth[i]-1000*E_c*(d_N-Depth[i])*Depth[i]/d_N)
          e_b=e_t*(d_N-Depth[i])/d_N
          e_stt=e_t*(d_N-d_top[i])/d_N
          e_stb=e_t*(d_N-Depth[i]+d_bot[i])/d_N
          case=3
          
         # Case 5
        else:
            if d_N < 0 or d_N > Depth[i] and N[i] >= 0:
                d_N = (A_stb[i]*Depth[i]**2*N[i]-3*A_stb[i]*Depth[i]*N[i]*d_bot[i]+2*A_stb[i]*N[i]*d_bot[i]**2-A_stt[i]*Depth[i]*N[i]*d_top[i]+2*A_stt[i]*N[i]*d_top[i]**2-2*A_stb[i]*Depth[i]*M[i]+2*A_stb[i]*M[i]*d_bot[i]-2*A_stt[i]*M[i]*d_top[i])/(A_stb[i]*Depth[i]*N[i]-2*A_stb[i]*N[i]*d_bot[i]-A_stt[i]*Depth[i]*N[i]+2*A_stt[i]*N[i]*d_top[i]-2*A_stb[i]*M[i]-2*A_stt[i]*M[i])
                e_t=(1/2)*(A_stb[i]*Depth[i]**2*N[i]-3*A_stb[i]*Depth[i]*N[i]*d_bot[i]+2*A_stb[i]*N[i]*d_bot[i]**2-A_stt[i]*Depth[i]*N[i]*d_top[i]+2*A_stt[i]*N[i]*d_top[i]**2-2*A_stb[i]*Depth[i]*M[i]+2*A_stb[i]*M[i]*d_bot[i]-2*A_stt[i]*M[i]*d_top[i])/((Depth[i]**2-2*Depth[i]*d_bot[i]-2*Depth[i]*d_top[i]+d_bot[i]**2+2*d_bot[i]*d_top[i]+d_top[i]**2)*A_stt[i]*A_stb[i]*E_st)
                e_b=e_t*(d_N-Depth[i])/d_N
                e_stt=e_t*(d_N-d_top[i])/d_N
                e_stb=e_t*(d_N-Depth[i]+d_bot[i])/d_N
                case=5
        
    #Case 2
    if M[i] < 0:
            
        #Case 2
        a=1000*E_c*N[i]
        b=-1500*Depth[i]*E_c*N[i]-3000*E_c*M[i]
        c=(-3*A_stb[i]*Depth[i]*E_st*N[i]+6*A_stb[i]*E_st*N[i]*d_bot[i]+3*A_stt[i]*Depth[i]*E_st*N[i]-6*A_stt[i]*E_st*N[i]*d_top[i]+6*A_stb[i]*E_st*M[i]+6*A_stt[i]*E_st*M[i]+6000*Depth[i]*E_c*M[i])
        d=3*A_stb[i]*Depth[i]**2*E_st*N[i]-9*A_stb[i]*Depth[i]*E_st*N[i]*d_bot[i]+6*A_stb[i]*E_st*N[i]*d_bot[i]**2-3*A_stt[i]*Depth[i]*E_st*N[i]*d_top[i]+6*A_stt[i]*E_st*N[i]*d_top[i]**2+500*Depth[i]**3*E_c*N[i]-6*A_stb[i]*Depth[i]*E_st*M[i]+6*A_stb[i]*E_st*M[i]*d_bot[i]-6*A_stt[i]*E_st*M[i]*d_top[i]-3000*Depth[i]**2*E_c*M[i]

        coeff = [a,b,c,d]
        g = np.roots(coeff)        
        g_i = g[np.imag(g)==0]
        g = np.real(g_i)
        
        if len(g)==3:
           g=g[2]
        
        g = g.item(0)
        d_N=g
        e_t=-N[i]/(E_st*(Depth[i]-d_N-d_bot[i])*A_stb[i]/d_N-E_st*(d_N-d_top[i])*A_stt[i]/d_N+500*E_c*(Depth[i]-d_N)**2/d_N)
        e_b=-e_t*(-d_N+Depth[i])/d_N
        e_stt=e_t*(d_N-d_top[i])/d_N
        e_stb=-e_t*(-d_N+Depth[i]-d_bot[i])/d_N
        case=2
   
        #Case 4
        if (d_N < 0 or d_N > Depth[i]) and N[i] < 0:
            d_N=(1/3)*(3*A_stb[i]*Depth[i]*E_st*N[i]*d_bot[i]-6*A_stb[i]*E_st*N[i]*d_bot[i]**2-3*A_stt[i]*Depth[i]**2*E_st*N[i]+9*A_stt[i]*Depth[i]*E_st*N[i]*d_top[i]-6*A_stt[i]*E_st*N[i]*d_top[i]**2-500*Depth[i]**3*E_c*N[i]-6*A_stb[i]*E_st*M[i]*d_bot[i]-6*A_stt[i]*Depth[i]*E_st*M[i]+6*A_stt[i]*E_st*M[i]*d_top[i]-3000*Depth[i]**2*E_c*M[i])/(A_stb[i]*Depth[i]*E_st*N[i]-2*A_stb[i]*E_st*N[i]*d_bot[i]-A_stt[i]*Depth[i]*E_st*N[i]+2*A_stt[i]*E_st*N[i]*d_top[i]-2*A_stb[i]*E_st*M[i]-2*A_stt[i]*E_st*M[i]-2000*Depth[i]*E_c*M[i])    
            e_b=-N[i]/(-E_st*(d_N-d_bot[i])*A_stb[i]/d_N-E_st*(d_N-Depth[i]+d_top[i])*A_stt[i]/d_N-500*E_c*(1-(d_N-Depth[i])/d_N)*Depth[i]-1000*E_c*(d_N-Depth[i])*Depth[i]/d_N)
            e_t=e_b*(d_N-Depth[i])/d_N
            e_stt=e_b*(d_N-Depth[i]+d_top[i])/d_N
            e_stb=e_b*(d_N-d_bot[i])/d_N
            case=4
            
     #Case 6
        else:
            if d_N < 0 or d_N > Depth[i] and N[i] >= 0:
                d_N=(A_stb[i]*Depth[i]*N[i]*d_bot[i]-2*A_stb[i]*N[i]*d_bot[i]**2-A_stt[i]*Depth[i]**2*N[i]+3*A_stt[i]*Depth[i]*N[i]*d_top[i]-2*A_stt[i]*N[i]*d_top[i]**2-2*A_stb[i]*M[i]*d_bot[i]-2*A_stt[i]*Depth[i]*M[i]+2*A_stt[i]*M[i]*d_top[i])/(A_stb[i]*Depth[i]*N[i]-2*A_stb[i]*N[i]*d_bot[i]-A_stt[i]*Depth[i]*N[i]+2*A_stt[i]*N[i]*d_top[i]-2*A_stb[i]*M[i]-2*A_stt[i]*M[i])
                e_b=-(1/2)*(A_stb[i]*Depth[i]*N[i]*d_bot[i]-2*A_stb[i]*N[i]*d_bot[i]**2-A_stt[i]*Depth[i]**2*N[i]+3*A_stt[i]*Depth[i]*N[i]*d_top[i]-2*A_stt[i]*N[i]*d_top[i]**2-2*A_stb[i]*M[i]*d_bot[i]-2*A_stt[i]*Depth[i]*M[i]+2*A_stt[i]*M[i]*d_top[i])/((Depth[i]**2-2*Depth[i]*d_bot[i]-2*Depth[i]*d_top[i]+d_bot[i]**2+2*d_bot[i]*d_top[i]+d_top[i]**2)*A_stt[i]*A_stb[i]*E_st)
                e_t=e_b*(d_N-Depth[i])/d_N
                e_stt=e_b*(d_N-Depth[i]+d_top[i])/d_N
                e_stb=e_b*(d_N-d_bot[i])/d_N
                case=6
    
    d_N_.append(d_N)
    e_t_.append(e_t)
    e_b_.append(e_b)
    e_stt_.append(e_stt)
    e_stb_.append(e_stb)
    case_.append(case)
    g_.append(g)

df['d_N'] = d_N_
df['e_t'] = e_t_
df['e_b'] = e_b_
df['e_stt'] = e_stt_
df['e_stb'] = e_stb_
df['case'] = case_

# Calculating crack widths based on MATLAB calc results
df['Top steel stress'] = E_st * df['e_stt']
df['Bot steel stress'] = E_st * df['e_stb']

# Make a sub-dataframe just containing e_stt and e_stb
df_s = df[['e_stt','e_stb']]
s_min = df_s.min(axis=1)
s_max = df_s.max(axis=1)
zeros = [0] * n
zeros_s = pd.Series(zeros)
df_smin = pd.DataFrame({'Minimum steel strain': s_min, 'Zeros': zeros})
df_smax = pd.DataFrame({'Maximum steel strain': s_max, 'Zeros': zeros})

df['Minimum tensile strain'] = df_smin.max(axis=1)
df['Maximum tensile strain'] = df_smax.max(axis=1)
#df['Max tensile strain'] = max(df['Top steel stress'],df['Bot steel stress'],0)

est1 = df['Minimum tensile strain']
est2 = df['Maximum tensile strain']
k2_ = []
dist_ = []
hceff_top_ = []
hceff_bot_ = []
Area_top_ = []
Area_bot_ = []
st_ratio_t_ = []
st_ratio_b_ = []
srmax_t_ = []
srmax_b_ = []
strain_inc_t_ = []
strain_inc_b_ = []
crack_w_t_ = []
crack_w_b_ = []

for i in range(0,n):
    #Strain distribution coefficient (k2)
    k2 = 0.5 
    if est1[i] > 0 and est2[i] > 0:
        k = (est1[i]+est2[i])/2/est2[i]
    k2_.append(k2)
    
    # Distance, x
    dist = 0    
    if df['case'][i] == 1:
        dist = df['d_N'][i]
    if df['case'][i] == 2:
        dist == df['Liner Thickness'][i]-df['d_N'][i]
    dist_.append(dist)
    
    # H,ceff
    hceff_top = min(2.5*df['d top'][i],df['Liner Thickness'][i]/2,(df['Liner Thickness'][i]-dist)/3)
    if dist == 0:
        hceff_top = min(2.5*df['d top'][i],df['Liner Thickness'][i]/2)
    hceff_top_.append(hceff_top)
    
    hceff_bot = min(2.5*df['d bot'][i],df['Liner Thickness'][i]/2,(df['Liner Thickness'][i]-dist)/3)
    if dist == 0:
        hceff_bot = min(2.5*df['d bot'][i],df['Liner Thickness'][i]/2)
    hceff_bot_.append(hceff_bot)
    
    # Area, A c,eff
    Area_top = 0
    Area_bot = 0
    if df['case'][i] == 2 or df['case'][i] == 5 or df['case'][i] == 6:
        Area_top = hceff_top * 1000
    if df['case'][i] == 1 or df['case'][i] == 5 or df['case'][i] == 6:
        Area_bot = hceff_bot * 1000
    Area_top_.append(Area_top)
    Area_bot_.append(Area_bot)
    
    # Steel ratio P p,eff
    st_ratio_t = 0
    st_ratio_b = 0
    if Area_top > 0:
        st_ratio_t = df['Ast top'][i]/Area_top
    if Area_bot > 0:
        st_ratio_b = df['Ast bot'][i]/Area_bot
    st_ratio_t_.append(st_ratio_t)
    st_ratio_b_.append(st_ratio_b)
    
    # Maximum crack spacing
    srmax_t = 0
    srmax_b = 0
    if st_ratio_t > 0:
        srmax_t = k3*cover_top+k1*k2*k4*df['Reo Diameter Top'][i]/st_ratio_t
        if RILEM == 1:
            srmax_t = ((50+0.25*RILEM_K1*k2*df['Reo Diameter Top'][i]/st_ratio_t))*50/(RILEM_L/RILEM_D)
    if st_ratio_b > 0:
        srmax_b = k3*cover_bot+k1*k2*k4*df['Reo Diameter Bot'][i]/st_ratio_b
        if RILEM == 1:
            srmax_b = ((50+0.25*RILEM_K1*k2*df['Reo Diameter Bot'][i]/st_ratio_b))*50/(RILEM_L/RILEM_D)
    srmax_t_.append(srmax_t)
    srmax_b_.append(srmax_b)
    
    # Strain increment
    fcteff = max((1.6-(df['Liner Thickness'][i]/1000)*fctm),fctm)
    str_inc_t = 0.6*df['Top steel stress'][i]/E_st
    str_inc_b = 0.6*df['Bot steel stress'][i]/E_st
    if st_ratio_t > 0:
        if (df['Top steel stress'][i]-strain_ratio*(fcteff/st_ratio_t)*(1+kt*st_ratio_t))/E_st > 0.6*df['Top steel stress'][i]/E_st:
           str_inc_t = (df['Top steel stress'][i]-strain_ratio*(fcteff/st_ratio_t)*(1+kt*st_ratio_t))/E_st
    if st_ratio_b > 0:
        if (df['Bot steel stress'][i]-strain_ratio*(fcteff/st_ratio_b)*(1+kt*st_ratio_b))/E_st > 0.6*df['Bot steel stress'][i]/E_st:
           str_inc_t = (df['Bot steel stress'][i]-strain_ratio*(fcteff/st_ratio_b)*(1+kt*st_ratio_b))/E_st
    strain_inc_t_.append(str_inc_t)
    strain_inc_b_.append(str_inc_b)
    
    # Crack width
    crack_w_t = srmax_t*str_inc_t
    crack_w_b = srmax_b*str_inc_b   
    crack_w_t_.append(crack_w_t)
    crack_w_b_.append(crack_w_b)
    
df['Strain distribution coefficient'] = k2_
df['Distance'] = dist_
df['hceff top'] = hceff_top_
df['hceff bot'] = hceff_bot_
df['Area top'] = Area_top_
df['Area bot'] = Area_bot_
df['Steel ratio top'] = st_ratio_t_
df['Steel ratio bot'] = st_ratio_b_
df['Maximum crack spacing top'] = srmax_t_
df['Maximum crack spacing bot'] = srmax_b_
df['Strain increment top'] = strain_inc_t_
df['Strain increment bot'] = strain_inc_b_
df['Crack width top'] = crack_w_t_
df['Crack width bot'] = crack_w_b_
    

# Function for extracting unique values from a series while preserving original sequence order
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

stage_list = f7(df['Increment Letter'])

# Graphing results
cmap=plt.get_cmap('hsv')
imax = len(stage_list)
font = {'size': 16}

bins = [-10000,0,0.01,0.03,0.05,0.07,0.09,0.11,0.13,0.15,0.25,0.5,1,10000]
xlabels = ['Not Cracked', '< 0.01', '0.01 - 0.03', '0.03 - 0.05', '0.05 - 0.07', '0.07 - 0.09', '0.09 - 0.11', '0.11 - 0.13', '0.13 - 0.15', '0.15 - 0.25', '0.25 - 0.5', '0.5 - 1', '> 1']
x_int = range(0,len(xlabels))
df['Crack width top bin'] = pd.cut(df['Crack width top'], bins=bins, labels=xlabels)


f, (ax1,ax2) = plt.subplots(2,1,figsize=(15,15))
i = 0
legend_col = len(stage_list)
for stage in stage_list:
    data = df[df['Increment Letter'] == str(stage)]
    crack_width_top = data['Crack width top bin']
    
    bin_counts = []
    for label in xlabels:
        bin_count = data[data['Crack width top bin']==label].count()['Crack width top bin']/len(data['Crack width top bin'])
        bin_counts.append(bin_count)
        
    ax1.plot(bin_counts, c=cmap(i/imax), label=Load_Cases[stage])
    i = i+1
from matplotlib.ticker import PercentFormatter    
ax1.yaxis.set_major_formatter(PercentFormatter(1.0))
ax1.set_xlabel('Crack width (mm)', fontdict=font)
ax1.set_xticks(np.arange(len(xlabels)))
ax1.set_xticklabels(xlabels)
ax1.xaxis.set_tick_params(rotation=90,labelsize=14)
ax1.axvline(9.5, linewidth = 2, color='k', linestyle = '--')
ax1.set_yticks(np.arange(0, 1.1, 0.1))
ax1.yaxis.set_tick_params(labelsize=14)
ax1.set_ylim(0,1)
ax1.set_ylabel('Frequency (%)',fontdict=font)
ax1.set_title('SLS Crack Width - Extrados',fontsize=20)
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.65, box.height])
#legend=ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False,fontsize=14)
ax1.text(6.5,0.5, 'Serviceability \nDesign Crack \nWidth Limit',fontsize=14, bbox=dict(facecolor='white',alpha=1))
ax1.grid()
#plt.show()

bins = [-10000,0,0.01,0.03,0.05,0.07,0.09,0.11,0.13,0.15,0.3,0.5,1,10000]
xlabels = ['Not Cracked', '< 0.01', '0.01 - 0.03', '0.03 - 0.05', '0.05 - 0.07', '0.07 - 0.09', '0.09 - 0.11', '0.11 - 0.13', '0.13 - 0.15', '0.15 - 0.3', '0.3 - 0.5', '0.5 - 1', '> 1']
x_int = range(0,len(xlabels))
df['Crack width bot bin'] = pd.cut(df['Crack width bot'], bins=bins, labels=xlabels)


i = 0
for stage in stage_list:
    data = df[df['Increment Letter'] == str(stage)]
    crack_width_bot = data['Crack width bot bin']
    
    bin_counts = []
    for label in xlabels:
        bin_count = data[data['Crack width bot bin']==label].count()['Crack width bot bin']/len(data['Crack width bot bin'])
        bin_counts.append(bin_count)
        
    ax2.plot(bin_counts, c=cmap(i/imax), label=Load_Cases[stage])
    i = i+1
  
ax2.yaxis.set_major_formatter(PercentFormatter(1.0))
ax2.set_xlabel('Crack width (mm)', fontdict=font)
ax2.set_xticks(np.arange(len(xlabels)))
ax2.set_xticklabels(xlabels)
ax2.xaxis.set_tick_params(rotation=90,labelsize=14)
ax2.axvline(9.5, linewidth = 2, color='k', linestyle = '--')
ax2.set_yticks(np.arange(0, 1.1, 0.1))
ax2.yaxis.set_tick_params(labelsize=14)
ax2.set_ylim(0,1)
ax2.set_ylabel('Frequency (%)',fontdict=font)
ax2.set_title('SLS Crack Width - Intrados',fontsize=20)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.65, box.height])
#legend=ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False,fontsize=14)
ax2.text(6.5,0.5, 'Serviceability \nDesign Crack \nWidth Limit',fontsize=14, bbox=dict(facecolor='white',alpha=1))
ax2.grid()
# #plt.show()
ax2.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), frameon=False,ncol=legend_col)
f.subplots_adjust(hspace=2)
f.tight_layout(pad=5)

page = PSMA4("result2.pdf")
page.add_titleblock("Test Client","Test Project","Test Location","Description Line 1","Description Line 2","PSMTEST","FIGURE")
page.add_matplotlib_figure(plt)
page.save()