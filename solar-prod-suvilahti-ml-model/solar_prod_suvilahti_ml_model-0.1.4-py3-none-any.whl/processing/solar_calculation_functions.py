import numpy as np
import pandas as pd
# from http://sgemfinalreport.fi/files/WP611_photovoltaics%20HP%20Hellman.pdf
''' G_on and general'''
longtitude = 24.9693
latitude = 60.1867
lon = longtitude
phi = latitude
delta_GMT = 0
gamma = 0
beta=45

def calc_sun_azimuth_for_df(N, time, lon=longtitude, delta_GMT=3, phi=latitude):
    delta = calc_delta(N)
    omega = calc_omega(N, lon, delta_GMT, time)
    alpha_s = calc_alpha_s(phi, delta, omega)
    gamma_s = calc_gamma_s(alpha_s, phi, delta, omega)
    return gamma_s

def calc_alpha_s_for_df(N, time, lon=longtitude, delta_GMT=3, phi=latitude):
    delta = calc_delta(N)
    omega = calc_omega(N, lon, delta_GMT, time)
    alpha_s = calc_alpha_s(phi, delta, omega)
    return alpha_s

def calc_sol_time(N, lon, delta_GMT, time):
    sol_time_minus_st_time = calc_sol_time_minus_st_time(N, lon, delta_GMT)
    sol_time = time+sol_time_minus_st_time
    return(sol_time)

def calc_omega(N, lon, delta_GMT, time):
    sol_time = calc_sol_time(N, lon, delta_GMT, time)
    omega = 15 * (sol_time-12)
    return omega

def calc_sol_time_minus_st_time(N, lon, delta_GMT): # TEST PASSED!
    E = calc_eot(N)
    sol_time_minus_st_time = (4 * (lon-15*delta_GMT)+E)/60
    return sol_time_minus_st_time

def calc_eot(N):
    B = (N-1) * 360/365
    E = 229.2*(0.000075 + 0.001868*np.cos(B*np.pi/180) - 0.032077*np.sin(B*np.pi/180) - 0.014615*np.cos(2*B*np.pi/180) - 0.04089*np.sin(2*B*np.pi/180))
    return E

def calc_delta(N):
    delta = 23.45 * np.sin(360*(284+N)*np.pi/180/365)
    return delta

def calc_G_on(N):
    G_on = 1367 * (1 + 0.033 * np.cos(360*N/365*np.pi/180))
    return G_on

''' Direct below'''
def calc_alpha_s(phi, delta, omega):
    #sind(phi)*sind(delta(x))+cosd(phi)*cosd(delta(x))*cosd(h(x,k))
    #alfa_s(x,k)=asind(sind(phi)*sind(delta(x))+cosd(phi)*cosd(delta(x))*cosd(h(x,k)))
    part1 = np.sin(phi*np.pi/180) * np.sin(delta*np.pi/180)
    part2 = np.cos(phi*np.pi/180) * np.cos(delta*np.pi/180) * np.cos(omega*np.pi/180)
    in_arcsin = part1 + part2
    alpha_s = (np.arcsin(in_arcsin)*180)/np.pi #converting rad->deg
    return alpha_s

def calc_gamma_s(alpha_s, phi, delta, omega):
    top = np.sin(alpha_s*np.pi/180) * np.sin(phi*np.pi/180) - np.sin(delta*np.pi/180)
    bot = np.cos(alpha_s*np.pi/180) * np.cos(delta*np.pi/180)
    in_arccos = top / bot # this is in rad
    in_abs = np.arccos(in_arccos) * 180/np.pi #this is in degrees
    gamma_s = np.sign(omega) * np.absolute(in_abs)
    return gamma_s

def calc_cos_theta_i(alpha_s, gamma_s, beta=45, gamma=0):
    part1 = np.sin(alpha_s*np.pi/180) * np.cos(beta*np.pi/180)
    d_gamma = gamma_s-gamma
    part2 = np.cos(alpha_s*np.pi/180) * np.sin(beta*np.pi/180) * np.cos(d_gamma*np.pi/180)
    cos_theta_i =  part1 + part2 #this is in radian
    return cos_theta_i

def calc_m(alpha_s, z=-53):
    z_h = 8434.5
    pp0 = np.exp(-z/z_h)
    alpha_s_true = calc_alpha_s_true(alpha_s)
    bot = np.sin(alpha_s_true*np.pi/180) + 0.50572 * ((alpha_s_true + 6.07995)**(-1.6364))
    m = pp0/bot
    return m

def calc_alpha_s_true(alpha_s):
    d_alpha_ref = calc_d_alpha_ref(alpha_s)
    alpha_s_true = alpha_s + d_alpha_ref
    return alpha_s_true

def calc_d_alpha_ref(alpha_s):
    part1 = 0.061359 * (180/np.pi)
    top2 = 0.1594 + 1.123*(np.pi/180)*alpha_s + 0.065656*((np.pi/180)**2)*(alpha_s**2)
    bot3  = 1 + 28.9344*(np.pi/180)*alpha_s + 277.3971*((np.pi/180)**2)*(alpha_s**2)
    d_alpha_ref = part1 * (top2 / bot3)
    return d_alpha_ref

def calc_d_R(m):
    if m<=20:
        bot = 6.6296 + 1.7514*m - 0.1202*(m**2) + 0.0065*(m**3) - 0.00013*(m**4)
    else:
        bot = 10.4 + 0.718*m
    d_R = 1 / bot
    return d_R

def calc_direct_irrad(G_on, alpha_s, cos_theta_i, T_L=2):
    m = calc_m(alpha_s)
    d_R = calc_d_R(m)
    in_exp = -0.8662 * T_L * m * d_R
    G_beam = G_on * cos_theta_i * np.exp(in_exp)
    return G_beam

''' diffuse below'''

def calc_t_rd(T_L=2):
    T_rd = -0.015843 + 0.030543*T_L + 0.0003797*(T_L**2)
    return T_rd

def calc_f_d(T_rd, alpha_s, T_L=2):
    A0 = 0.26463 - 0.061581*T_L + 0.0031408*(T_L**2)
    if (A0*T_rd <0.002):
        A0 = 0.002/T_rd
    A1 = 2.0402 + 0.018945*T_L - 0.011161*(T_L**2)
    A2 = 1.3025 + 0.039231*T_L + 0.0085079*(T_L**2)
    F_d = A0 + A1*np.sin(alpha_s*np.pi/180) + A2*(np.sin(alpha_s*np.pi/180)**2)
    return F_d

def calc_diffuse_irrad(T_rd, alpha_s, G_on, beta):
    F_d = calc_f_d(T_rd, alpha_s, T_L=2)
    G_d = G_on * T_rd * F_d * ((1+np.cos(beta*np.pi/180))/2)
    return G_d


def calc_glob_irrad(N,time,lon=longtitude,delta_GMT=0,phi=latitude):
    gamma = 0
    beta=45
    omega = calc_omega(N, lon, delta_GMT, time)
    delta = calc_delta(N)
    alpha_s = calc_alpha_s(phi, delta, omega)
    if alpha_s>0:
        gamma_s = calc_gamma_s(alpha_s, phi, delta, omega)
        cos_theta_i = calc_cos_theta_i(alpha_s, gamma_s, gamma, beta)
        if cos_theta_i>0:
            G_on = calc_G_on(N)
            G_beam = calc_direct_irrad(G_on, alpha_s, cos_theta_i, T_L=2)
            T_rd = calc_t_rd(T_L=2)
            G_d = calc_diffuse_irrad(T_rd, alpha_s, G_on, beta)
            G_glob = G_beam + G_d
        else:
            G_glob = 0
    else:
        G_glob = 0
    return G_glob
