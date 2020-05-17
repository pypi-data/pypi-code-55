import tensorflow as tf
from typing import List


class Wrapper:
    def __init__(self, *gpu, log_device: bool = False):
        assert tf.__version__.startswith('2'), \
            f"Arkab Tensorflow Wrapper can only run in tf2.x"
        if len(gpu) == 0 or gpu[0] == -1:
            self.use_gpu = False
            self.device = tf.device("/cpu")
            self.gpu = []
        elif len(gpu) == 1 and tf.test.is_gpu_available():
            self.use_gpu = True
            self.device = tf.device(f"/gpu:{gpu[0]}")
            self.gpu = gpu
        tf.debugging.set_log_device_placement(log_device)

    def set_growth_memory(self):
        """
        Set growth memory for gpu
        """
        gpus = tf.config.experimental.list_physical_devices('GPU')
        try:
            # 设置GPU为增长式占用
            for gpu in gpus:
                index = int(gpu.name[-1])
                if index in self.gpu:
                    tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            # 打印异常
            print(e)

    def tensor(self, *data) -> List:
        """
        Convert list to a tensor
        :param data:
        :return:
        """
        result = list()
        with self.device:
            for d in data:
                result.append(tf.convert_to_tensor(d))
        return result

    def variable(self, *data):
        result = list()
        with self.device:
            for d in data:
                result.append(tf.Variable(d))
        return result
