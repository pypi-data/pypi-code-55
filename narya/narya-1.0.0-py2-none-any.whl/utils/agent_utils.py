import numpy as np
import random

SMM_WIDTH = 96
SMM_HEIGHT = 72

channel_dimensions = (SMM_WIDTH, SMM_HEIGHT)

_MARKER_VALUE = 255


def _reverse_points(x, y):
    """Moves the left team to the right (and the right to the left)
    Args:
      x,y: Coordinates to reverse
    Returns:
      x,y: Reverse coordinates
    """
    x = channel_dimensions[0] - 1 - x
    y = channel_dimensions[1] - 1 - y
    return (x, y)


def _change(observation, observation_count, x, y, new_x, new_y):
    """Moves an entity from x,y to new_x,new_y
    Args:
      observation: np.array unstack of observations
      observation_count: np.array unstack of observations count
      x,y: old coordinates
      new_x,new_y: new coordinates
    Returns:
    """
    observation[new_y, new_x] = _MARKER_VALUE
    observation_count[new_y, new_x] += 1
    observation_count[y, x] = max(0, observation_count[y, x] - 1)
    if observation_count[y, x] == 0:
        observation[y, x] = 0


def change(observation, observation_count, x, y, new_x, new_y, entity):
    """Moves an entity from x,y to new_x,new_y on an entire observations
    Args:
      observation: np.array stacked observations
      observation_count: np.array stacked observations count
      x,y: old coordinates
      new_x,new_y: new coordinates
      entity: the entity to move (player or ball)
    Returns:
    """
    indx_init = 0 if entity == "player" else 2
    for i in range(indx_init, 16, 4):
        unstack_observation = observation[:, :, i]
        unstack_observation_count = observation_count[:, :, i]
        _change(unstack_observation, unstack_observation_count, x, y, new_x, new_y)


def _change_random(observation, observation_count, x, y):
    """Moves an entity from x,y randomly on the field
    Args:
      observation: np.array unstack observations
      observation_count: np.array unstacke observations count
      x,y: old coordinates
    Returns:
    """
    new_x = int(random.random() * channel_dimensions[0])
    new_y = int(random.random() * channel_dimensions[1])
    _change(observation, observation_count, x, y, new_x, new_y)


def _add_noise(observation, observation_count, x, y, x_std=5, y_std=5):
    """Moves an entity from x,y randomly on the field, with a gaussian noise
    Args:
      observation: np.array unstack observations
      observation_count: np.array unstacke observations count
      x,y: old coordinates
      x_std,y_std : std for the noises
    Returns:
    """
    new_x = min(max(int(np.random.normal(x, x_std, 1)[0]), 0), channel_dimensions[0])
    new_y = min(max(int(np.random.normal(y, y_std, 1)[0]), 0), channel_dimensions[1])
    _change(observation, observation_count, x, y, new_x, new_y)


def traverse(observation, observation_count, x, y, entity):
    """Moves an entityto its next possible position. Can be used to try the entire field
    Args:
      observation: np.array unstack observations
      observation_count: np.array unstacke observations count
      x,y: old coordinates
      entity: ball or player
    Returns:
      new_x,new_y: the Next available position
    """
    new_x = x + 1
    if new_x >= channel_dimensions[0]:
        new_x = 0
        new_y = y + 1
    else:
        new_y = y
    change(observation, observation_count, x, y, new_x, new_y, entity)
    return new_x, new_y
