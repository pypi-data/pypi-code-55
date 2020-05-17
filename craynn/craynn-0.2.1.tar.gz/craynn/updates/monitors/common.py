import numpy as np
import tensorflow as tf

from ..meta import as_stateful

__all__ = [
  'running_avg_loss'
]

@as_stateful
def running_avg_loss(
  initial_loss=0.0, half_life_slow=1024, half_life_fast=128, rho=0.99
):
  def monitor(loss):
    beta1 = np.exp(-np.log(2) / half_life_slow)
    beta2 = np.exp(-np.log(2) / half_life_fast)

    beta1 = tf.convert_to_tensor(beta1, dtype=loss.dtype)
    beta2 = tf.convert_to_tensor(beta2, dtype=loss.dtype)

    if rho is not None:
      _rho = tf.convert_to_tensor(rho, dtype=loss.dtype)
    else:
      _rho = None

    average_loss_slow = tf.Variable(
      initial_value=initial_loss,
      trainable=False,
      dtype=loss.dtype
    )

    average_loss_fast = tf.Variable(
      initial_value=0.0,
      trainable=False,
      dtype=loss.dtype
    )

    diff = average_loss_slow - average_loss_fast

    monitors_updates = [
      tf.assign(average_loss_slow, beta1 * average_loss_slow + (1 - beta1) * loss),
      tf.assign(average_loss_fast, beta2 * average_loss_fast + (1 - beta2) * loss),
    ]

    state = [average_loss_slow, average_loss_fast]

    if rho is not None:
      average_loss_diff = tf.Variable(
        initial_value=initial_loss,
        trainable=False,
        dtype=loss.dtype
      )

      monitors_updates.append(
        tf.assign(average_loss_diff, _rho * average_loss_diff + (1 - _rho) * diff)
      )

      observable = average_loss_diff

      state.append(average_loss_diff)
    else:
      observable = diff

    update_op = tf.group(monitors_updates)

    return state, update_op, dict(average_loss_change=observable)
  return monitor