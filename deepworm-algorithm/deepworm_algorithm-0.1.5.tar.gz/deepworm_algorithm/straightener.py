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
        self.widths = widths

        # Pipeline:
        self.fit_spline()
        self.straighten()

    def fit_spline(self):
        # sample_widths are the widths between skeleton and contour
        sample_widths = [width/1.8+5 for width in self.widths]
        self.spine_tck = interpolate.fit_spline(
            [[y, x] for x, y in self.skeleton], smoothing=None)
        x_vals = np.linspace(0, 1, len(self.skeleton))
        self.width_tck = interpolate.fit_nonparametric_spline(
            x_vals, sample_widths, smoothing=None)

    def straighten(self):
        overlay_width = int(max(self.widths) * 1.2)
        self.img_straightened = resample.warp_image_to_standard_width(
            self.img,
            self.spine_tck,
            self.width_tck,
            self.width_tck,
            overlay_width)
        self.mask_straightened = resample.make_mask_for_sampled_spline(
            self.img_straightened.shape[0],
            self.img_straightened.shape[1],
            self.width_tck)
        self.img_straightened[~self.mask_straightened] = 0
        self.img_straightened = self.img_straightened.transpose()[::-1]
        self.mask_straightened = self.mask_straightened.transpose()[::-1]
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
