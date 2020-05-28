import cv2
import matplotlib.pyplot as plt
import numpy as np
from .utils import geometry, interpolate, spline_geometry, resample


class Straightener(object):
    """Straighten a warped object by resampling along skeleton
    
    Attributes:
        img (array): Input image
        skeleton (list): Point sequence of skeleton which have no branch
        widths (list): Local width at each position along skeleton
        img_straightened: Result image after straightening
        mask_straightened: Mask of valid area in straightened image
    """

    def __init__(self, img, skeleton, widths):
        super(Straightener, self).__init__()
        self.img = img
        self.skeleton = skeleton  # skeleton is a point sequence(list)
        self.widths = [width/1.8+5 for width in widths]

        # Pipeline:
        self.warp_img()

    def warp_img(self):
        spine_tck = interpolate.fit_spline(
            [[y, x] for x, y in self.skeleton], smoothing=None)
        x_vals = np.linspace(0, 1, len(self.skeleton))
        width_tck = interpolate.fit_nonparametric_spline(
            x_vals, self.widths, smoothing=None)
        self.img_straightened = resample.warp_image_to_standard_width(
            self.img, spine_tck, width_tck, width_tck, 600)
        self.mask_straightened = resample.make_mask_for_sampled_spline(
            self.img_straightened.shape[0],
            self.img_straightened.shape[1],
            width_tck)
        self.img_straightened[~self.mask_straightened] = 0
        return self.img_straightened


if __name__ == '__main__':
    from skeleton_extractor import SkeletonExtractor
    from pixel_annotator import PixelAnnotator
    path = '1.jpg'
    img = cv2.imread(path, 0)
    mask = cv2.imread('mask_0.png', 0)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    skeleton_extractor = SkeletonExtractor(mask)
    skeleton = skeleton_extractor.skeleton
    pixel_annotator = PixelAnnotator(mask, skeleton)
    staightener = Straightener(img, skeleton, pixel_annotator.widths)
    cv2.imshow('img', staightener.img_straightened)
    cv2.waitKey(0)
