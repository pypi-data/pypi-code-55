import unittest
import os
import numpy as np
from image_toolbox.io import read_image
from image_toolbox.io import write_image
from io import BytesIO


filename_in = "image_toolbox/tests/data/imtest.png"

img_ref = np.array(
    [[[0., 0., 255.], [0., 255., 255.], [255., 0., 255.]],
     [[0., 255., 255.], [0., 255., 0.], [255., 255., 0.]],
     [[255., 0., 255.], [255., 255., 0.], [255., 0., 0.]]],
    dtype=np.float32)


class TestBasicFunction(unittest.TestCase):

    def test_read_image(self):
        self.assertTrue(os.path.exists(filename_in))
        arr = read_image(filename_in)
        self.assertTrue(isinstance(arr, np.ndarray))
        self.assertTrue(arr.shape == (150, 150, 3))
        for i, j in zip([0, 1, 2], [0, 1, 2]):
            self.assertTrue((arr[i*50: (i+1)*50, j*50: (j+1)*50, :].reshape(50**2, 3).mean(axis=0) ==
                             img_ref[i, j, :]).all())

    def test_write_image(self):
        img = read_image(filename_in)
        # out_file = BytesIO()
        # write_image(out_file, img)
        # new_img = read_image(out_file)
        # write_image(out_file, img)
        # new_img = read_image(out_file)

        path_out = "/tmp/out.png"
        flag_create_tmp = not os.path.exists(os.path.dirname(path_out))
        try:
            if flag_create_tmp:
                os.makedirs(os.path.dirname(path_out))
            write_image(path_out, img)
            self.assertTrue(os.path.exists(path_out))
            new_img = read_image(path_out)
            self.assertTrue(img.shape == new_img.shape)
            self.assertTrue(np.allclose(img, new_img))
        finally:
            # pass
            os.remove(path_out)
            if flag_create_tmp:
                os.remove(os.path.dirname(path_out))


if __name__ == '__main__':
    unittest.main()
