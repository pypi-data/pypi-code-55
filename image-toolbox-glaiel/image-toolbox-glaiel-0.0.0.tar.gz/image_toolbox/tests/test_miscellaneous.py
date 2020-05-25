import unittest
import os
import numpy as np
from image_toolbox.miscellaneous.utils import ImageDataGenerator


filename_in = "image_toolbox/tests/data/imtest.png"

img_ref = np.array(
    [[[0., 0., 255.], [0., 255., 255.], [255., 0., 255.]],
     [[0., 255., 255.], [0., 255., 0.], [255., 255., 0.]],
     [[255., 0., 255.], [255., 255., 0.], [255., 0., 0.]]],
    dtype=np.float32)


class TestBasicFunction(unittest.TestCase):

    def test_image_data_generator(self):
        self.assertTrue(os.path.exists(filename_in))
        print("Creating image data generator...")
        gen = ImageDataGenerator([filename_in],
                                 batch_size=1,
                                 rotate=False, one_hot=True,
                                 crop_largest_rect=True,
                                 crop_center=True,
                                 input_shape=(3, 3, 3))
        print("Getting generator next image...")
        image_batch = gen.next()[0]
        print("Image batch size: %s" % str(image_batch.shape))
        image = image_batch[0]
        self.assertTrue((image == img_ref).all())


if __name__ == '__main__':
    unittest.main()
