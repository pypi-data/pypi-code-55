import numpy as np

from . import Optimiser


class SGD(Optimiser):
    """ Implementation of gradient descent. """

    def __init__(self, parameters, lr: float, momentum: float = 0.):

        """
        Parameters
        ----------
        momentum : float
            Momentum term for the gradient descent.
        """
        super().__init__(parameters, lr)
        self.mu = momentum
        self.lr = lr

        for i, p in enumerate(self.parameters):
            setattr(self, 'vm' + str(i), np.zeros_like(p))

        # if necessary, you can add state-variables here

    def step(self):

        for i, p in enumerate(self.parameters):
            d_p = p.grad
            vm = getattr(self, 'vm' + str(i))
            vm = self.mu * vm + (1 - self.mu) * d_p
            p -= self.lr * vm


class Adam(Optimiser):
    """Implementation of the Adam algorithm.
        https://arxiv.org/pdf/1412.6980.pdf
    """

    def __init__(self, parameters, lr: float = 1e-3, betas: tuple = (.9, .999),
                 epsilon: float = 1e-7, bias_correction=True):
        """
        Parameters
        ----------
        betas : tuple of 2 floats, optional
            Decay factors for the exponential averaging of mean, resp. variance.
        epsilon : float, optional
            Small number that is added to denominator for numerical stability.
        bias_correction : bool, optional
            Whether or not mean and bias estimates should be bias-corrected.
        """
        super().__init__(parameters, lr)

        beta1, beta2 = betas
        self.beta1 = float(beta1)
        self.beta2 = float(beta2)
        self.eps = float(epsilon)
        self.bias_correction = bias_correction
        self.lr = lr

        self.t = 0
        for i, p in enumerate(self.parameters):
            setattr(self, 'first_moment' + str(i), np.zeros_like(p))
            setattr(self, 'second_moment' + str(i), np.zeros_like(p))
        # if necessary, you can add state-variables here

    def step(self):
        self.t += 1
        for i, p in enumerate(self.parameters):
            d_p = p.grad
            first_moment = getattr(self, 'first_moment' + str(i))
            second_moment = getattr(self, 'second_moment' + str(i))
            first_moment = self.beta1 * first_moment + (1 - self.beta1) * d_p
            second_moment = self.beta2 * second_moment + (1 - self.beta2) * d_p * d_p
            m_t = first_moment / (1 - self.beta1 ** self.t)
            v_t = second_moment / (1 - self.beta2 ** self.t)
            p -= self.lr * m_t / (np.sqrt(v_t) + self.eps)


class AdaGrad(Optimiser):
    """Implementation of AdaGrad. """

    def __init__(self, parameters, lr: float):

        super().__init__(parameters, lr)
        self.lr = lr

        for i, p in enumerate(self.parameters):
            setattr(self, 'grad_squared' + str(i), np.zeros_like(p))

        # if necessary, you can add state-variables here

    def step(self):

        for i, p in enumerate(self.parameters):
            d_p = p.grad
            grad_squared = getattr(self, 'grad_squared' + str(i))
            grad_squared = grad_squared + d_p * d_p
            p -= self.lr * d_p / (np.sqrt(grad_squared) + 1e-7)


class RMSprop(Optimiser):
    """Implementation of RMSprop. """

    def __init__(self, parameters, lr: float = 1e-3, gamma: float = 0.0):

        super().__init__(parameters, lr)
        self.lr = lr
        self.gamma = gamma

        for i, p in enumerate(self.parameters):
            setattr(self, 'grad_squared' + str(i), np.zeros_like(p))

    def step(self):

        for i, p in enumerate(self.parameters):
            d_p = p.grad
            grad_squared = getattr(self, 'grad_squared' + str(i))
            grad_squared = self.gamma * grad_squared + (1 - self.gamma) * d_p * d_p
            p -= self.lr * d_p / (np.sqrt(grad_squared) + 1e-7)


class NesterovMomentum(Optimiser):

    def __init__(self, parameters, lr: float, momentum: float = 0.):
        """
        Parameters
        ----------
        momentum : float
            Momentum term for the gradient descent.
        """
        super().__init__(parameters, lr)
        self.rho = momentum
        self.lr = lr

        for i, p in enumerate(self.parameters):
            setattr(self, 'v' + str(i), np.zeros_like(p))

        # if necessary, you can add state-variables here

    def step(self):

        for i, p in enumerate(self.parameters):
            d_p = p.grad
            v = getattr(self, 'v' + str(i))
            old_v = v
            v = self.rho * v - self.lr * d_p
            p += -self.rho * old_v + (1 + self.rho) * v


# Not
class Adamax(Optimiser):
    """Implementation of the Adamax algorithm. https://arxiv.org/pdf/1412.6980.pdf"""

    def __init__(self, parameters, lr: float = 1e-3, betas: tuple = (.9, .999),
                 epsilon: float = 1e-7):
        """
        Parameters
        ----------
        betas : tuple of 2 floats, optional
            Decay factors for the exponential averaging of mean, resp. variance.
        """
        super().__init__(parameters, lr)

        beta1, beta2 = betas
        self.beta1 = float(beta1)
        self.beta2 = float(beta2)
        self.lr = lr

        self.t = 0
        for i, p in enumerate(self.parameters):
            setattr(self, 'm_t' + str(i), np.zeros_like(p))
            setattr(self, 'u_t' + str(i), 0)
        # if necessary, you can add state-variables here

    def step(self):
        self.t += 1
        for i, p in enumerate(self.parameters):
            d_p = p.grad
            m_t = getattr(self, 'm_t' + str(i))
            m_t = self.beta1 * m_t + (1 - self.beta1) * d_p
            u_t = getattr(self, 'u_t' + str(i))
            u_t = np.maximum(self.beta2 * u_t, np.linalg.norm(d_p, ord=1))
            p -= (self.lr / (1 - self.beta1 ** self.t)) * m_t / u_t


class RMSprop(Optimiser):
    """Implementation of RMSprop. """

    def __init__(self, parameters, lr: float = 1e-3, gamma: float = 0.0):

        super().__init__(parameters, lr)
        self.lr = lr
        self.gamma = gamma

        for i, p in enumerate(self.parameters):
            setattr(self, 'grad_squared' + str(i), np.zeros_like(p))

    def step(self):

        for i, p in enumerate(self.parameters):
            d_p = p.grad
            grad_squared = getattr(self, 'grad_squared' + str(i))
            grad_squared = self.gamma * grad_squared + (1 - self.gamma) * d_p * d_p
            p -= self.lr * d_p / (np.sqrt(grad_squared) + 1e-7)
