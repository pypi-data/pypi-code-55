import tensorflow as tf

from deepdialog.component.base import StochasticComponent
from deepdialog.distribution.distribution import MultiVarDiagonalGaussian

__ALL__ = ["PriorNet", "PosteriorNet"]


class PriorNet(StochasticComponent):
    """
    The :class:`PriorNet` class is the network for inferring prior distribution.
    It defines the prior distribution of a variable and supports stochastic sampling operation.
    """
    def __init__(self, latent_dim, n_samples=None, name="prior_net"):

        self._latent_dim = latent_dim
        self._n_samples = n_samples

        StochasticComponent.__init__(self, name, self._n_samples, dtype=tf.float32)

    @property
    def latent_dim(self):
        """The latent dimension of latent variable."""
        return self._latent_dim

    def __call__(self, context_states):
        with tf.variable_scope("prior_net"):
            prior_mulogvar = tf.layers.dense(inputs=context_states,
                                             units=self._latent_dim * 2,
                                             activation=tf.tanh, name="ctx_states2prior_network")
            prior_mu, prior_logvar = tf.split(prior_mulogvar, 2, axis=1)

            self._distribution = MultiVarDiagonalGaussian(
                prior_mu, prior_logvar, tf.float32, "prior_dist")
            z = self._distribution.sample(self._n_samples)
            return z


class PosteriorNet(StochasticComponent):
    """
    The :class:`PosteriorNet` class is the network for inferring posterior distribution.
    It defines the posterior distribution of a variable and supports stochastic sampling operation.
    """
    def __init__(self, latent_dim, n_samples=None, name="posterior_net"):

        self._latent_dim = latent_dim
        self._n_samples = n_samples

        StochasticComponent.__init__(self, name, self._n_samples, dtype=tf.float32)

    @property
    def latent_dim(self):
        """The latent dimension of latent variable."""
        return self._latent_dim

    def __call__(self, context_states, response_states):

        with tf.variable_scope("posterior_net"):
            posterior_input = tf.concat([context_states, response_states], 1)
            posterior_mulogvar = tf.layers.dense(inputs=posterior_input,
                                                 units=self._latent_dim * 2,
                                                 activation=tf.tanh, name="ctx_states2posterior_network")
            posterior_mu, posterior_logvar = tf.split(posterior_mulogvar, 2, axis=1)
            self._distribution = MultiVarDiagonalGaussian(
                posterior_mu, posterior_logvar, tf.float32, "posterior_dist")
            z = self._distribution.sample(self._n_samples)
            return z