import cv2
import matplotlib.pyplot as plt
import numpy as np


class EdgeEnhancing(object):
    """Enhancing edges by adding shadow
    
    Attributes:
        img (array): Input image
        img_gray (array): Gray scale image of input image
        img_denoise (array): Denoised image of img_gray
        img_edge_enhanced (array): Image with shadow on img_denoise
    """

    def __init__(self, img=None):
        super(EdgeEnhancing, self).__init__()
        self.img = img
        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Pipeline:
        self.remove_overexposure()
        self.denoise()
        self.add_shadow()

    def remove_overexposure(self):
        self.img_gray[self.img_gray == 255] = 127

    def denoise(self):
        self.img_denoise = cv2.fastNlMeansDenoising(
            self.img_gray, None, 10, 7, 21)

    def add_shadow(self):
        emboss_kernels = {
            'north_east':  [[0, 0, 1],
                            [0, 0, 0],
                            [-1, 0, 0]],
            'south_west': [[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]],
            'south_east': [[-1, -1, 0],
                           [-1, 0, 1],
                           [0, 1, 1]],
            'north_west': [[1, 0, 0],
                           [0, 0, 0],
                           [0, 0, -1]],
            'north':      [[1, 2, 1],
                           [0, 0, 0],
                           [-1, -2, -1]],
            'south':      [[-1, -2, -1],
                           [0, 0, 0],
                           [1, 2, 1]],
            'east':       [[-1, 0, 1],
                           [-2, 0, 2],
                           [-1, 0, 1]],
            'west':       [[1, 0, -1],
                           [2, 0, -2],
                           [1, 0, -1]],
        }

        self.img_edge_enhanced = self.img_denoise + 0
        for direction in emboss_kernels:
            kernel = np.array(emboss_kernels[direction])
            shadow = cv2.filter2D(self.img_denoise, -1, kernel)
            self.img_edge_enhanced = cv2.subtract(self.img_edge_enhanced, shadow)


if __name__ == '__main__':
    path = '1.jpg'
    img = cv2.imread(path)
    edge_enhancing = EdgeEnhancing(img)

    cv2.imshow('img', edge_enhancing.img_edge_enhanced)
    cv2.waitKey(0)
    cv2.imwrite('1_edge_enhanced.png',edge_enhancing.img_edge_enhanced)
