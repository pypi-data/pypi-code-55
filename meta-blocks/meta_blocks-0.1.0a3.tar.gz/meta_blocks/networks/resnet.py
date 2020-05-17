"""Resnets."""

from typing import Optional, Tuple

import tensorflow.compat.v1 as tf
from tensorflow.keras.applications import resnet

__all__ = ["build_resnet50"]

# Transition to V2 will happen in stages.
tf.disable_v2_behavior()
tf.enable_resource_variables()


def build_resnet50(
    input_shape: Tuple[int],
    input_type: str,
    *,
    pooling: Optional[str] = None,
    output_size: Optional[int] = None,
    output_activation: Optional[str] = None,
    name: str = "ResNet50",
):
    """Builds the standard ResNet50 network."""
    # Input node.
    inputs = tf.keras.layers.Input(shape=input_shape, dtype=input_type)
    # Transform inputs with ResNet50.
    x = resnet.ResNet50(
        include_top=False, weights=None, input_shape=input_shape, pooling=pooling,
    )(inputs)
    x = tf.keras.layers.Flatten(name="flatten")(x)
    # Add a fully connected output layer.
    if output_size is not None:
        OutputLayer = tf.keras.layers.Dense(
            output_size, activation=output_activation, name="fc"
        )
        x = OutputLayer(x)
    # Build and output the model.
    model = tf.keras.models.Model(inputs, x, name=name)
    return model
