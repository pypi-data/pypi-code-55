"""Runner to run on TLM."""

import logging
import pickle
from typing import Dict
from typing import Tuple

import numpy as np

from .runner import Runner

__all__ = [
    'TLMRunner'
]

LOGGER = logging.getLogger(__name__)


class TLMRunner(Runner):
    """TLM runner."""

    def __init__(self, tcf_debug_object_path: str):
        """
        TLM runner initialization.

        Parameters
        ----------
        tcf_debug_object_path
            path to the debug object pickled by `tcf`
        """
        # pylint: disable=import-outside-toplevel
        from tpu_tlm_is import Executable
        from tpu_tlm_is.base import TensorDescription

        with open(tcf_debug_object_path, 'rb') as file:
            obj: Tuple[Executable, Dict[str, TensorDescription]] = pickle.load(file)

        executable, tensor_descriptions = obj

        # NOTE: conversion from keys() to list is possible for Python > 3.6 guarantees dict item order
        super().__init__(source_path=tcf_debug_object_path,
                         input_nodes=list(executable.in_data.keys()),
                         output_nodes=list(executable.out_data.keys()))

        self._executable = executable
        self._tensor_descriptions = tensor_descriptions

    def _check_input_names(self, input_tensors: Dict[str, np.ndarray]):
        if input_tensors.keys() != self._executable.in_data.keys():
            raise ValueError(
                f'Expected inputs {self._executable.in_data.keys()} differs from the provided {input_tensors.keys()}')

    def _check_input_shapes(self, input_tensors: Dict[str, np.ndarray]):
        for name, tensor in input_tensors.items():
            expected_shape = self._tensor_descriptions[name].user_shape.nhwc
            if tensor.shape != expected_shape:
                raise ValueError(f'Invalid input shape {tensor.shape} for tensor "{name}": expected {expected_shape}')

    def __call__(self, input_tensors: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Perform TLM run for a given input."""
        # pylint: disable=import-outside-toplevel
        from tpu_compiler.core import Hardware
        from tpu_compiler_tests.tools.pced import _pad_to
        from tpu_compiler_tests.tools.pced import _encode
        from tpu_compiler_tests.tools.pced import _decode
        from tpu_compiler_tests.tools.pced import _crop_to
        from tpu_tlm import PythonModel

        LOGGER.debug('Input tensors: %s', str({name: tensor.shape for name, tensor in input_tensors.items()}))

        self._check_input_names(input_tensors)
        self._check_input_shapes(input_tensors)

        hardware = Hardware(self._executable.hardware_parameters)  # hardware proxy
        # compiler's inner dtype proxy classes:
        dtypes = {name: hardware.to_dtype(description.dtype) for name, description in self._tensor_descriptions.items()}

        # quantization (scaling) input
        input_scales = {name: self._tensor_descriptions[name].scale for name in input_tensors}
        quantized_input = {name: tensor * input_scales[name] for name, tensor in input_tensors.items()}

        LOGGER.debug('Input quantized with factors: %s', str(input_scales))

        # casting to int8
        integer_input = {name: tensor.astype(np.int8) for name, tensor in quantized_input.items()}
        LOGGER.debug('Input tensors are casted to int8 with max abs diff: %s',
                     str({name: np.max(np.abs(quantized_input[name] - integer_input[name]))
                          for name in quantized_input}))

        # padding to TPU shape
        padded_input = {name: _pad_to(integer_input[name], self._tensor_descriptions[name].tpu_shape)
                        for name in quantized_input}
        LOGGER.debug('Tensor padded to TPU shapes: %s',
                     str({name: tensor.shape for name, tensor in padded_input.items()}))

        # encode (integer tensor to uint8 binary tensor conversion)
        binary_input = _encode(hardware, padded_input, dtypes)
        LOGGER.debug('Binary input dictionary created: %s',
                     str({name: tensor.shape for name, tensor in binary_input.items()}))

        # execute on TLM
        binary_output = PythonModel.execute(self._executable, binary_input)
        LOGGER.debug('Binary output dictionary obtained: %s',
                     str({name: tensor.shape for name, tensor in binary_output.items()}))

        # decode
        decoded_output = _decode(
            hardware,
            binary_output,
            {name: self._tensor_descriptions[name].tpu_shape for name in binary_output},
            {name: dtype.dtype for name, dtype in dtypes.items()}  # tesor name to numpy's dtype dictionary (clumsy)
        )

        LOGGER.debug('Decoded dictionary obtained: %s',
                     str({name: tensor.shape for name, tensor in decoded_output.items()}))

        # cropping
        cropped_output = {name: _crop_to(tensor, self._tensor_descriptions[name].user_shape)
                          for name, tensor in decoded_output.items()}

        LOGGER.debug('Cropped tensors: %s',
                     str({name: tensor.shape for name, tensor in cropped_output.items()}))

        # de-quantization
        output_scales = {name: self._tensor_descriptions[name].scale for name in cropped_output}
        dequntized_output = {name: tensor * output_scales[name] for name, tensor in cropped_output.items()}
        LOGGER.debug('Output tensor de-quantized with scales: %s', str(output_scales))

        if len(dequntized_output) == 1:
            output = list(dequntized_output.values())[0]
            LOGGER.debug('TOP-5: %s', str(output.flatten().argsort()[::-1][:5]))

        return dequntized_output
