import os
import tarfile

import cv2
import numpy as np
import tensorflow as tf


class DeepLab(object):
    """Class to load deeplab model and run inference."""

    def __init__(self, model_name='deeplabv3_pascal_trainval_2018_01_04.tar.gz'):
        self.graph = tf.Graph()
        graph_def = None
        # Extract frozen graph from tar archive.
        tar_file = tarfile.open(model_name)
        for tar_info in tar_file.getmembers():
            if 'frozen_inference_graph' in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.GraphDef.FromString(file_handle.read())
                break
        tar_file.close()

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)

    def predict(self, image, max_size=513, class_id=15):
        width, height = image.shape[:2][::-1]
        resize_ratio = 1.0 * max_size / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        new = cv2.resize(image, target_size, cv2.INTER_CUBIC)
        new = self.sess.run('SemanticPredictions:0', feed_dict={'ImageTensor:0': [new]})[0]
        new = cv2.resize(new.astype(np.uint8), (width, height), cv2.INTER_CUBIC)
        new = (new == class_id).astype(np.float32)

        return (255 * new).astype(np.uint8)
