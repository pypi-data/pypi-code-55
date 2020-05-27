"""
DeepNetworkModel.py

DeepNetworkModel class that defines the gradient function to compute gradients from different paths for EIG.
Defines:
+ class DeepNetworkModel(object)
"""
import numpy as np
import tensorflow as tf


class DeepNetworkModel(object):
    """
    This is the DeepNetworkModel class that defines the gradient function to compute gradients for a tensorflow
    deep learning model.
    """
    def __init__(self, session, tensor_ops):
        """
        Initialize the tensorflow session and the tensor inputs/outputs.
        :param session: tensorflow session that contains the tensorflow graph for the model
        :param tensor_ops: The input and output tensors for the tensorflow model
        """
        self.sess = session
        self.grad_input_ph, self.other_input_ph, self.output_op = tensor_ops
        self.gradients_op = None

    def gradients(self, paths_inputs, other_input=None):
        """
        Compute gradients for the points in the paths_input.
        :param paths_inputs: list, data for all the grad_input_ph operations initialized in the init.
        :param other_input: list, All the additional input placeholders can go here.
        :return: gradients computed for all paths_inputs and (optionally other_input).
        """
        # Make sure data is provided for all path_inputs
        assert len(self.grad_input_ph) == len(paths_inputs), "provide values for all path input placeholders!"
        if other_input is not None:
            assert len(self.other_input_ph) == len(
                other_input), "provide values for all non gradient input placeholders"

        # Make dict to be fed to the tensorflow session run.
        input_dict = dict()
        for op, path in zip(self.grad_input_ph, paths_inputs):
            path_flattened = np.array(path, copy=True)
            path_flattened = path_flattened.reshape([path.shape[0] * path.shape[1]] + list(path.shape[2:]))
            input_dict[op] = path_flattened

        # If there are additional inputs, add them in the input dictionary to be fed to the tensorflow session run.
        if other_input is not None:
            for op, other_input in zip(self.other_input_ph, other_input):
                input_dict[op] = other_input

        # Make the gradient operation using the input and output operations
        gradients_op = tf.gradients(self.output_op, self.grad_input_ph)
        # Run gradient operation
        gradients = self.sess.run(gradients_op, input_dict)
        # Shape the gradients based on the shape of the paths_input.
        reshaped_gradients = []
        for gradient, path in zip(gradients, paths_inputs):
            reshaped_gradients.append(gradient.reshape(path.shape))
        return reshaped_gradients





