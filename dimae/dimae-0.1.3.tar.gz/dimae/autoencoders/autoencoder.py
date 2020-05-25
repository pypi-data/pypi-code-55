import numpy as np
import math
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras import Model


class AE(Model):
    def __init__(self,
                 n_input=None,
                 code_nodes=None,
                 summary=False,
                 _code_activation='relu',
                 _output_activation='sigmoid',
                 _inner_activation='tanh',
                 _code_kernel='he_uniform',
                 _output_kernel='truncated_normal',
                 _inner_kernel='glorot_uniform',
                 _red_factor=7.5,
                 *args,
                 **kwargs):
        """
        :param n_input: number of input features. If you are using a DataFrame, it will be equal to df.shape[1]
        :param code_nodes: number of required nodes for the encoder output. It will be set automatically depending on
        the reduction factor if not given by the user.
        :param summary: set to True if you want to print the AutoEncoder model structure.
        :param _code_activation: activation function at the code layer. Set to ReLu by default.
        :param _output_activation: activation function at the output layer. Set to Sigmoid by default.
        :param _inner_activation: activation function at Encoder and Decoder inner layers. Set to TanH by default.
        :param _code_kernel: kernel initializer at the code layer. Set to He Uniform by default.
        :param _output_kernel: kernel initializer at the output layer. Set to Truncated Normal by default.
        :param _inner_kernel: kernel initializer at Encoder and Decoder inner layers. Set to Glorot Uniform by default.
        :param _red_factor: reduction factor used to choose the number of code neurons if not explicitly given.
        :param args:
        :param kwargs:
        """

        self.input_nodes = n_input

        # either a number of code nodes or reduction factor can be specified
        self.code_nodes = __even__(self.input_nodes / _red_factor) if not code_nodes else code_nodes

        # number of layers
        n_layers = __layer_number__(n_input, code_nodes)

        # CHOSEN WAY TO SELECT CORRECT NUMBER OF LAYER NODES, BASED ON LOGSPACE
        a = np.log(self.code_nodes)
        b = np.log(self.input_nodes)

        encoder_layers = np.flip(np.logspace(a, b, n_layers, base=np.e))[1:-1]
        decoder_layers = np.logspace(a, b, n_layers, base=np.e)[1:-1]

        LAYERS = []

        # GENERATE LAYERS
        self.input_layer = Input(shape=(self.input_nodes,))
        LAYERS.append(self.input_layer)

        for n in encoder_layers:
            LAYERS.append(
                Dense(__even__(n), activation=_inner_activation, kernel_initializer=_inner_kernel)(LAYERS[-1])
            )

        self.code_layer = Dense(self.code_nodes, activation=_code_activation, kernel_initializer=_code_kernel)(LAYERS[-1])
        LAYERS.append(self.code_layer)

        for n in decoder_layers:
            LAYERS.append(
                Dense(__even__(n), activation=_inner_activation, kernel_initializer=_inner_kernel)(LAYERS[-1])
            )

        output_layer = Dense(self.input_nodes, activation=_output_activation, kernel_initializer=_output_kernel)(LAYERS[-1])

        # SETUP MODEL
        super().__init__(self.input_layer, output_layer, *args, **kwargs)

        # PRINT OUT MODEL STRUCTURE IF REQUIRED
        if summary:
            self.summary()

    def generate_encoder(self):
        """
        Creates the encoder model extracting it from the trained Autoencoder.
        :return: keras model of the encoder
        """
        encoder = Model(self.input_layer, self.code_layer)
        return encoder


def __layer_number__(a, b):
    """
    Calculates the proper number of hidden layers
    :param a: number of input nodes
    :param b: number of code nodes
    :return: number of layers from input to code
    """
    if a < b:
        raise Exception("The number of code neurons must be lower then input nodes number.")
    div = a / b

    if div > 1.5:
        div = math.log(div, 10)
        div = math.e**div
        div += 1

    return math.ceil(div)


def __even__(f):
    """
    Help function to round each number to even.
    :param f: given number
    :return: even approximation of the given number
    """
    return math.ceil(f / 2.) * 2
