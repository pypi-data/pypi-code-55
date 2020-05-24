import numpy as np

from npbrain import profile

if profile.get_backend().startswith('numba'):
    import numba as nb

__all__ = [
    'ode_generator',
    'forward_Euler', 'explicit_Euler',
    'rk2', 'RK2',
    'modified_Euler', 'explicit_midpoint_Euler',
    'rk3', 'RK3',
    'rk4', 'RK4',
    'RK4_alternative', 'rk4_alternative',
    'backward_Euler', 'implicit_Euler',
    'trapezoidal_rule',
]


def ode_generator(f, dt=None, method=None):
    """Generate the one-step ODE integration function.

    Parameters
    ----------
    f : callable
        The function at the right hand of the differential equation.
    dt : None, float
        Precision of numerical integration.
    method : None, str, callable
        Method of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    if dt is None:
        dt = profile.get_dt()
    if method is None:
        method = profile.get_ode_method()

    if isinstance(method, str):
        if method in ['euler', 'forward_Euler', 'explicit_Euler']:
            return forward_Euler(f, dt)
        if method in ['rk2', 'RK2']:
            return rk2(f, dt)
        if method in ['explicit_midpoint_Euler', 'modified_Euler']:
            return modified_Euler
        if method in ['rk3', 'RK3']:
            return rk3(f, dt)
        if method in ['rk4', 'RK4']:
            return rk4(f, dt)
        if method in ['RK4_alternative', 'rk4_alternative']:
            return rk4_alternative(f, dt)

        if method in ['backward_Euler', 'implicit_Euler']:
            return implicit_Euler(f, dt)
        if method in ['trapezoidal_rule']:
            return trapezoidal_rule(f, dt)
    elif callable(method):
        return method(f, dt)
    else:
        raise ValueError('Unknown method type.')


# euler-start
def forward_Euler(f, dt):
    """Forward Euler method. Also named as ``explicit_Euler``.

    The most unstable integrator known. Requires a very small timestep.
    Accuracy is O(dt).

    Parameters
    ----------
    f : callable
        The function at the right hand of the differential equation.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    def int_f(y0, t, *args):
        return y0 + dt * f(y0, t, *args)

    if profile.get_backend().startswith('numba'):
        int_f = nb.jit(**profile.get_numba_profile())(int_f)

    return int_f
# euler-end


explicit_Euler = forward_Euler


# rk2-start
def rk2(f, dt, beta=2 / 3):
    """Parametric second-order Runge-Kutta (RK2).
    Also named as ``RK2``.

    Popular choices for 'beta':
        1/2 :
            explicit midpoint method
        2/3 :
            Ralston's method
        1 :
            Heun's method, also known as the explicit trapezoid rule

    Parameters
    ----------
    f : callable
        The function at the right hand of the differential equation.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    def int_f(y0, t, *args):
        k1 = f(y0, t, *args)
        k2 = f(y0 + beta * dt * k1, t + beta * dt, *args)
        return y0 + dt * ((1 - 1 / (2 * beta)) * k1 + 1 / (2 * beta) * k2)

    if profile.get_backend().startswith('numba'):
        int_f = nb.jit(**profile.get_numba_profile())(int_f)

    return int_f
# rk2-end


RK2 = rk2


# modified_Euler-start
def explicit_midpoint_Euler(f, dt):
    """Explicit midpoint Euler method. Also named as ``modified_Euler``.

    Parameters
    ----------
    f : callable
        The function at the right hand of the differential equation.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    return rk2(f, dt, beta=0.5)
# modified_Euler-end


modified_Euler = explicit_midpoint_Euler


# rk3-start
def rk3(f, dt):
    """Kutta's third-order method (commonly known as RK3).
    Also named as ``RK3``.

    Parameters
    ----------
    f : callable
        The function at the right hand of the differential equation.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    def int_f(y0, t, *args):
        k1 = f(y0, t, *args)
        k2 = f(y0 + dt / 2 * k1, t + dt / 2, *args)
        k3 = f(y0 - dt * k1 + 2 * dt * k2, t + dt, *args)
        return y0 + dt / 6 * (k1 + 4 * k2 + k3)

    if profile.get_backend().startswith('numba'):
        int_f = nb.jit(**profile.get_numba_profile())(int_f)

    return int_f
# rk3-end


RK3 = rk3


# rk4-start
def rk4(f, dt):
    """Fourth-order Runge-Kutta (RK4). Also named as ``RK4``.

    Parameters
    ----------
    f : callable
        The function at the right hand of the differential equation.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    def int_f(y0, t, *args):
        k1 = f(y0, t, *args)
        k2 = f(y0 + dt / 2 * k1, t + dt / 2, *args)
        k3 = f(y0 + dt / 2 * k2, t + dt / 2, *args)
        k4 = f(y0 + dt * k3, t + dt, *args)
        return y0 + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    if profile.get_backend().startswith('numba'):
        int_f = nb.jit(**profile.get_numba_profile())(int_f)

    return int_f
# rk4-end


RK4 = rk4


# rk4_alternative-start
def rk4_alternative(f, dt):
    """An alternative of fourth-order Runge-Kutta method.
    Also named as ``RK4_alternative``.

    Parameters
    ----------
    f : callable
        The function at the right hand of the differential equation.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    def int_f(y0, t, *args):
        k1 = f(y0, t, *args)
        k2 = f(y0 + dt / 3 * k1, t + dt / 3, *args)
        k3 = f(y0 - dt / 3 * k1 + dt * k2, t + 2 * dt / 3, *args)
        k4 = f(y0 + dt * k1 - dt * k2 + dt * k3, t + dt, *args)
        return y0 + dt / 8 * (k1 + 3 * k2 + 3 * k3 + k4)

    if profile.get_backend().startswith('numba'):
        int_f = nb.jit(**profile.get_numba_profile())(int_f)

    return int_f
# rk4_alternative-end


RK4_alternative = rk4_alternative


# backward_Euler-start
def backward_Euler(f, dt, epsilon=1e-12):
    """Backward Euler method. Also named as ``implicit_Euler``.

    Parameters
    ----------
    f : callable
        The function at the right hand of the differential equation.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """
    def int_f(y0, t, *args):
        y1 = y0 + dt * f(y0, t, *args)
        y2 = y0 + dt * f(y1, t, *args)
        while not np.all(np.abs(y1 - y2) < epsilon):
            y1 = y2
            y2 = y0 + dt * f(y1, t, *args)
        return y2

    if profile.get_backend().startswith('numba'):
        int_f = nb.jit(**profile.get_numba_profile())(int_f)

    return int_f
# backward_Euler-end


implicit_Euler = backward_Euler


# trapezoidal_rule-start
def trapezoidal_rule(f, dt, epsilon=1e-12):
    """Trapezoidal rule.

    The trapezoidal rule is an implicit second-order method, which can
    be considered as both a Runge–Kutta method and a linear multistep method.

    Parameters
    ----------
    f : callable
        The function at the right hand of the differential equation.
    dt : None, float
        Precision of numerical integration.

    Returns
    -------
    func : callable
        The one-step numerical integration function.
    """

    def int_f(y0, t, *args):
        dy0 = f(y0, t, *args)
        y1 = y0 + dt * dy0
        y2 = y0 + dt / 2 * (dy0 + f(y1, t + dt, *args))
        while not np.all(np.abs(y1 - y2) < epsilon):
            y1 = y2
            y2 = y0 + dt / 2 * (dy0 + f(y1, t + dt, *args))
        return y2

    if profile.get_backend().startswith('numba'):
        int_f = nb.jit(**profile.get_numba_profile())(int_f)

    return int_f
# trapezoidal_rule-end

