# coding=utf-8
from typing import Dict
import tensorflow_datasets as tfds
import tensorflow as tf
from tensorflow import keras as k
from tensorflow.python.ops import control_flow_util
"""
ref: https://github.com/tensorflow/tensorflow/issues/25414
Implement DCGAN using the new TF 2.0 API.

Also test tensorflow-datasets.

Celeb-A dataset.
"""


control_flow_util.ENABLE_CONTROL_FLOW_V2 = True


@tf.function
def bce(x, label, label_smoothing=0.0):
    """Returns the discrete binary cross entropy between x and the discrete label
    Args:
        x: a 2D tensor
        label: the discrete label, aka, the distribution to match
        label_smoothing: if greater than zero, smooth the labels

    Returns:
        The binary cros entropy
    """
    return k.losses.BinaryCrossentropy()(tf.ones_like(x) * label, x)


def min_max(positive, negative, label_smoothing=0.0):
    """Returns the discriminator (min max) loss
    Args:
        positive: the discriminator output for the positive class: 2D tensor
        negative: the discriminator output for the negative class: 2D tensor
        smooth: if greater than zero, appiles one-sided label smoothing
    Returns:
        The sum of 2 BCE
    """
    one = tf.constant(1.0)
    zero = tf.constant(0.0)
    d_loss = bce(positive, one, label_smoothing) + bce(negative, zero)
    return d_loss


class Generator(k.Model):

    def __init__(self):
        super(Generator, self).__init__()
        self.fc1 = k.layers.Dense(4 * 4 * 1024)
        self.batchnorm1 = k.layers.BatchNormalization()

        self.conv2 = k.layers.Conv2DTranspose(
            filters=512,
            kernel_size=(5, 5),
            strides=(2, 2),
            padding="same",
            use_bias=False,
        )
        self.batchnorm2 = k.layers.BatchNormalization()

        self.conv3 = k.layers.Conv2DTranspose(
            filters=256,
            kernel_size=(5, 5),
            strides=(2, 2),
            padding="same",
            use_bias=False,
        )
        self.batchnorm3 = k.layers.BatchNormalization()

        self.conv4 = k.layers.Conv2DTranspose(
            filters=128,
            kernel_size=(5, 5),
            strides=(2, 2),
            padding="same",
            use_bias=False,
        )
        self.batchnorm4 = k.layers.BatchNormalization()

        self.conv5 = k.layers.Conv2DTranspose(
            filters=3,
            kernel_size=(5, 5),
            strides=(2, 2),
            padding="same",
            use_bias=False,
        )
        self.batchnorm5 = k.layers.BatchNormalization()

    def call(self, x: tf.Tensor, training: bool = True) -> tf.Tensor:
        x = self.fc1(x)
        x = self.batchnorm1(x, training=training)
        x = tf.nn.relu(x)
        x = tf.reshape(x, shape=(-1, 4, 4, 1024))

        x = self.conv2(x)
        x = self.batchnorm2(x, training=training)
        x = tf.nn.relu(x)

        x = self.conv3(x)
        x = self.batchnorm3(x, training=training)
        x = tf.nn.relu(x)

        x = self.conv4(x)
        x = self.batchnorm4(x, training=training)
        x = tf.nn.relu(x)

        x = self.conv5(x)
        x = self.batchnorm5(x, training=training)

        x = tf.nn.tanh(x)
        return x


class Discriminator(k.Model):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.conv1 = k.layers.Conv2D(128, (5, 5), strides=(2, 2), padding="same")
        self.conv2 = k.layers.Conv2D(256, (5, 5), strides=(2, 2), padding="same")
        self.batchnorm2 = k.layers.BatchNormalization()
        self.conv3 = k.layers.Conv2D(512, (5, 5), strides=(2, 2), padding="same")
        self.batchnorm3 = k.layers.BatchNormalization()
        self.conv4 = k.layers.Conv2D(1024, (5, 5), strides=(2, 2), padding="same")
        self.batchnorm4 = k.layers.BatchNormalization()
        self.flatten = k.layers.Flatten()
        self.fc5 = k.layers.Dense(1)

    def call(self, x, training=True):
        x = self.conv1(x)
        x = tf.nn.leaky_relu(x)

        x = self.conv2(x)
        x = self.batchnorm2(x)
        x = tf.nn.leaky_relu(x)

        x = self.conv3(x)
        x = self.batchnorm3(x)
        x = tf.nn.leaky_relu(x)

        x = self.conv4(x)
        x = self.batchnorm4(x)
        x = tf.nn.leaky_relu(x)

        x = self.flatten(x)
        x = self.fc5(x)
        return x


class GAN:
    def __init__(self, generator, discriminator, encoder=None):
        """
        GAN initializer.

        Args:
            generator: A ``tensorflow.keras.Model`` to use as Generator.
            discriminator: A ``tensorflow.keras.Model`` to use as Discriminator.
            encoder: A ``tensorflow.keras.Model`` to use as Encoder.

        Returns:
            Trained GAN model (?).

        """
        self.G = generator()
        self.D = discriminator()
        # self.E = encoder() if encoder is not None else None
        self.latent_vector_dims = 100

    @tf.function()
    def train(self, dataset, opt1, opt2):
        """
        Train.
        """
        step = 0
        for f in dataset:
            x = f["image"]
            step += 1
            z = tf.random.normal((32, self.latent_vector_dims))

            # We record all the operations in the tape
            with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
                G_z = self.G(z, training=True)

                D_x = self.D(x, training=True)
                D_Gz = self.D(G_z, training=True)

                g_loss = bce(D_Gz, 1.0)
                d_loss = min_max(D_x, D_Gz, label_smoothing=0.0)

            # We retrieve the gradients from our records
            G_grads = gen_tape.gradient(g_loss, self.G.trainable_variables)
            D_grads = disc_tape.gradient(d_loss, self.D.trainable_variables)

            # Optimize and apply the gradients
            opt1.apply_gradients(zip(G_grads, self.G.trainable_variables))
            opt2.apply_gradients(zip(D_grads, self.D.trainable_variables))

            if step % 1 == 0:
                print("--------------------------")
                print("STEP", step)
                print("D_LOSS", d_loss)
                print("G_LOSS:", g_loss)
        return step


class InputPipeline:

    def __init__(self, dataset, batch_size, epochs, shuffle_buffer, prefetched_items, size):
        self.batch_size = batch_size
        self.dataset_name = dataset
        self.epochs = epochs
        self.prefetched_items = prefetched_items
        self.shuffle_buffer = shuffle_buffer
        self.size = size

    def get_input_fn(self):
        """Input fn."""
        return self.input_fn

    def load_public_dataset(self):
        """
        Load one of the publicly available datasets, will merge together all the splits.

        Args:
            chosen_dataset: dataset to use.

        Return:
            The chosen dataset as a ``tf.data.Dataset``

        """
        # Construct a tf.data.Dataset
        datasets = tfds.load(name=self.dataset_name, split=tfds.Split.ALL)
        return datasets

    def resize_images(self, features):
        """
        Overwrite the \"image\" feature in order to resize them.

        Args:
            features: features dictionary.
            size: desired target size.

        Returns:
            Features with \"image\" resized to the correct shape.

        """
        features["image"] = tf.image.resize(features["image"], self.size)
        return features

    def input_fn(self):
        dataset = self.load_public_dataset()
        dataset = (
            dataset.map(self.resize_images)
            .shuffle(self.shuffle_buffer)
            .batch(self.batch_size)
            .prefetch(self.prefetched_items)
            .repeat(self.epochs)
        )
        return dataset


def main():
    # See available datasets
    public_datasets = tfds.list_builders()
    print(public_datasets)

    gan = GAN(Generator, Discriminator)
    G_opt = k.optimizers.Adam(learning_rate=1e-5, beta_1=0.5)
    D_opt = k.optimizers.Adam(learning_rate=1e-5, beta_1=0.5)

    input_pipeline = InputPipeline(
        dataset="celeb_a",
        batch_size=32,
        epochs=2,
        prefetched_items=1,
        shuffle_buffer=1000,
        size=(64, 64),
    )
    dataset = input_pipeline.input_fn()
    _ = gan.train(dataset, G_opt, D_opt)


if __name__ == "__main__":
    main()

