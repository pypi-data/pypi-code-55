# standard library
import logging
# third party site-packages
import numpy as np
from scipy import interpolate
# this package
from aiolos_fluid_dynamics.physical_constants import GAMMA_AIR, R_AIR, R_H2O
from aiolos_cfd_tools import cfd_maths

import matplotlib.pyplot as plt


log = logging.getLogger(__name__)

# ====================================================================================================================================================================================================#
# FLUID PROPERTIES
# ====================================================================================================================================================================================================#


@np.vectorize
def ideal_gas_law(p=None, rho=None, T=None):
    """
    Solve the ideal gas law based on two thermodynamic parameters
    :param p:   <float> or <np.ndarray<float>> pressure in Pa
    :param rho: <float> or <np.ndarray<float>> density in kg/m**3
    :param T:   <float> or <np.ndarray<float>> temperature in Kelvin
    :return:
        returns the missing paramter
    """
    if p != None and rho != None and  T != None:
        errmsg = "ideal gas law over constrained: provide two of three parameters (P, rho T)"
        log.error(errmsg)
        raise ValueError(errmsg)

    if rho != None and  T != None and p == None:
        log.debug("calculating pressure from ideal gas law with density (%.2f kg/m**3) and temperature (%.2f K)" % (rho, T))
        return rho*R_AIR*T
    if p != None and T != None and rho == None:
        log.debug("calculating density from ideal gas law with pressure (%.2f kPa) and temperature (%.2f K)" % (p/1000, T))
        return p/R_AIR/T
    if p != None and rho != None and T == None:
        log.debug("calculating temperature from ideal gas law with pressure (%.2f kPa) and density (%.2f kg/m**3)" % (p/1000, rho))
        return p/R_AIR/rho
    else:
        errmsg  = "ideal gas law requires at least two of three paramters (P, rho, T)"
        log.error(errmsg)
        raise ValueError(errmsg)


def density_air_water_vapour(p, p_h2o, T):
    return (1 / T) * (p_h2o/R_H2O + (p - p_h2o)/R_AIR)


@np.vectorize
def water_vapour_pressure(dew_point_temperature, dry_bulb_temperature):
    """

        Hyland and Wexler relationship for water vapour pressure, Ph2o

    :param dew_point_temperature:      <float64 or np.ndarray<float64>> dew point temperature       [K]
    :param dry_bulb_temperature:       <float64 or np.ndarray<float64>> static temperature          [K]
    :return:

        partial pressure of water vapour in the air     [Pa]
    """

    tb = dry_bulb_temperature
    tdp = dew_point_temperature

    C1 = np.array([
        -5.6745359e3,
        6.3925247,
        -9.677843e-3,
        6.22115701e-7,
        2.0747825e-9,
        -9.484024e-13,
        4.1635019
    ])
    C2 = np.array([
        -5.8002206e3,
        1.3914993,
        -4.8640239e-2,
        4.1764768e-5,
        -1.4452093e-8,
        6.5459673
    ])

    if tb < 173.15:
        errmsg = "Dry Bulb Temperature Out of Range: Too low "
        log.error(errmsg)
        raise ValueError(errmsg)

    if tb > 473.15:
        errmsg = "Dry Bulb Temperature Out of Range: Too high"
        log.error(errmsg)
        raise ValueError(errmsg)

    if np.isnan(tb):
        errmsg = "Temperature data missing"
        log.error(errmsg)
        raise ValueError(errmsg)

    if tb <= 273.15:
        C = C1

    if 273.15 < tb <= 473.15:
        C = C2

    return np.exp(np.sum(C[i]*tdp**(i-1) for i in range(len(C)-1))+C[-1]*np.log(tdp))


def sutherland(T):
    """

    # =======================================================================#
    #
    #       FUNCTION:           sutherland(T)
    #
    #       DESCRIPTION:        Computes the dynamic viscosity (mu) from the absolute
    #                           temperautre (T) using the relationship established
    #                           by William Sutherland (1893)
    #                           
    #
    #
    #       ARGUMENTS
    #
    #           :param T:       <np.ndarray<np.float64> of size mx1> array or scalar    
    #                           of Temperature
    #
    #       OUTPUTS
    #
    #           :result x:      <np.ndarray<np.float64> of size T.size> results vector
    #
    # =======================================================================#

    """
    mu_o    = 1.716e-5      # kg/ms
    T_o     = 273.15        # Kelvin
    S       = 110.40        # Kelvin

    log.debug("Calculating viscosity using Sutherland's law for T = %.4f K" % T)
    return mu_o * ( T / T_o )**(3./2.) * ( T_o + S) / ( T + S)

# ====================================================================================================================================================================================================#
# ISENTROPIC RELATIONS
# ====================================================================================================================================================================================================#


def static_temperature(To, M, k=GAMMA_AIR):
    return To * (1 + (k - 1)/2.0*M**2)**(-1)


def total_temperature(T, M, k=GAMMA_AIR):
    return T * (1 + (k - 1)/2.0*M**2)


def static_pressure(Po, M, k=GAMMA_AIR):
    return Po * (1 + (k-1.)/2. * M**2)**(-k/(k-1))


def Mach_number(Po, p, k=GAMMA_AIR):
    return np.sqrt(2./(k-1.) * ((Po/p)**((k-1)/k) - 1))


def dynamic_pressure(p, M, k=GAMMA_AIR):
    return k/2.0*p*M**2

# todo: needs validation
def rayleigh_pitot_correction(Po2, p, tolerance=10e-6, MAXIT=1000, k=GAMMA_AIR):

    """
        This function is used to correct the supersonic measurement of a Pitot probe using the measured total pressure
        from the pitot and the measured true static pressure. Since the introduction of a probe into a supersonic flow
        results in the formation of a Bow shock at the probe tip, correction on the total pressure is required, and a
        specialized static pressure probe, which measures true static pressure even in supersonic flow is needed also.
        Since the bow shock just upstream of the central Pitot port on the probe, it can be treated as a normal shock.

        References:
                        [1] White, F.M. (2006) Fluid Mechanics. McGraw-Hill, 6th Edition

    :param Po2:         <float64 or np.ndarray<float64>> measured pitot pressure downstream of the shock          [Pa]
    :param p:           <float64 or np.ndarray<float64>> measured static pressure upstream of the shock          [Pa]
    :param tolerance:   <float65> Mach number error tolerance (default = 10e-6)
    :param MAXIT:       <int> maximum number of iterations before declaring non-convergence
    :param k:           <float64> ratio of specific heats k=cp/cv (default = 1.4 i.e. GAMMA_AIR)
    :return:
                M1      <float64 or np.ndarray<float64>> Mach number upstream of the shock (i.e. true Mach number)
                Po1     <float64 or np.ndarray<float64>> Total pressure upstream of the shock  (i.e. true total pressure)
    """

    # initial guess for Mach number upstream of the bow shock
    M1 = Mach_number(Po=Po2, p=p)

    for i in range(MAXIT):

        tmp1 = (k / (k - 1.0))
        tmp2 = (2.0 * k * M1**2.0 - k + 1.0) / (k + 1.0)
        tmp3 = (1.0 / (k - 1.0))

        M_tmp = (2.0 / (k + 1.0) * (Po2/p * tmp2**tmp3)**(1.0/tmp1))**0.5

        err = np.abs(M1-M_tmp)
        M1 = M_tmp

        if np.abs(err) >= tolerance:
            log.debug("Supersonic measurement corrected. Converged Mach number M = %.4f" % M1)

            Po1 = Po2 /  ((((k+1)*M1**2)/(2 + (k-1)*M1**2))**(k/(k-1))) / ( (k+1) / (2*k*M1**2 - (k-1)))**(1/(k-1))

            return M1, Po1

        if i == MAXIT:
            errmsg = "Maximum number of iterations reached: i = %8i" % i
            log.debug(errmsg)
            raise ValueError(errmsg)

# ====================================================================================================================================================================================================#
# BOUNDARY LAYER RELATIONSHIPS
# ====================================================================================================================================================================================================#


def dispacement_thickness(z, u, Ue=1.0, rho=1.0, rho_e=1.0):
    """

    :param z:       <np.array<float64>> height vector
    :param u:       <np.array<float64>> local velocity at locations corresponding to z vector
    :param Ue:      <float64> Freestream velocity (if velocity vector is already normalized, set Ue=1.0)
    :param rho:     <np.array<float64>> local density at locations corresponding to z vector (if incompressible set rho=1.0)
    :param rho_e:   <np.array<float64>> freestream density (if incompressible, or rho(z) is already normalized, set rho_e=1.0)
    :return:
        displacement thickness from the integral equation

    .. math::
        {\\delta}^* =


    """
    integrand = (1.0 - rho/rho_e * u/Ue)
    delta = boundary_layer_thickness(z=z, u=u, Ue=Ue)

    return cfd_maths.trapeziodalIntegraion(integrand, z, x0=0, x1=delta*1.1)


def momentum_thickness(z, u, Ue=1.0, rho=1.0, rho_e=1.0):
    """

    :param z:       <np.array<float64>> height vector
    :param u:       <np.array<float64>> local velocity at locations corresponding to z vector
    :param Ue:      <float64> Freestream velocity (if velocity vector is already normalized, set Ue=1.0)
    :param rho:     <np.array<float64>> local density at locations corresponding to z vector (if incompressible set rho=1.0)
    :param rho_e:   <np.array<float64>> freestream density (if incompressible, or rho(z) is already normalized, set rho_e=1.0)
    :return:
    """
    integrand = rho/rho_e * u/Ue * (1.0 -  u/Ue)
    delta = boundary_layer_thickness(z=z, u=u, Ue=Ue)
    
    return cfd_maths.trapeziodalIntegraion(integrand, z, x0=0, x1=delta)


def boundary_layer_thickness(z, u, Ue=1.0):
    """

    :param z:       <np.array<float64>> height vector
    :param u:       <np.array<float64>> local velocity at locations corresponding to z vector
    :param Ue:      <float64> Freestream velocity (if velocity vector is already normalized, set Ue=1.0)
    :return:
        linear interpolation of z vector where the normalized velocoty u(z)/Ue = 0.99
    """

    tck = interpolate.splrep(z, u/Ue, s = 0.001)
    z_smoothed = np.linspace(z[0], z[-1], 500)
    u_smoothed = interpolate.splev(z_smoothed, tck, der=0)

    return np.interp(0.99, np.squeeze(u_smoothed), np.squeeze(z_smoothed))    
