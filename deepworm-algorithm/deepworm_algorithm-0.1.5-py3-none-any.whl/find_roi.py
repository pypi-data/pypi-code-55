import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import data, filters, segmentation, measure, morphology, color, io
import thinning


class FindROI(object):
    """Find Eligible ROIs in a segmentation mask

    Attributes:
        mask (array): Input binary mask
        area_threshold (): Threshold of min area of an ROI
        markers (array): Label each pixel by the connected component it belongs
        valid_labels (list): Labels of Eligible ROIs
        valid_regions (list): Eligible ROIs

    Usage:
        yield_roi(): Return mask of a eligible ROI
    """

    def __init__(self, mask, area_threshold=200):
        super(FindROI, self).__init__()
        self.mask = mask
        self.area_threshold = area_threshold

        self.checklist = [
            self.check_area,
            self.check_extent,
            self.check_not_blob,
            self.check_shape,
        ]

        # Pipeline:
        self.mark()
        self.filter()

    def mark(self):
        self.markers = measure.label(self.mask)
        # self.image_label_overlay =color.label2rgb(self.markers, image=self.mask,bg_label=0)

    def check_area(self, region):  # prevent region is too small
        return region.area > self.area_threshold

    def check_extent(self, region):  # prevent region is a rectangle
        return region.extent < 0.8

    def check_not_blob(self, region):  # prevent region is a circular blob
        mask_region = np.zeros_like(self.mask)
        mask_region[self.markers == region.label] = 255
        image, contours, hierarchy = cv2.findContours(
            mask_region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        (x, y), radius = cv2.minEnclosingCircle(contours[0])
        circle_area = np.pi*radius**2
        return region.area/circle_area < 0.5

    def check_shape(self, region):
        mask_region = np.zeros_like(self.mask)
        mask_region[self.markers == region.label] = 255
        kernel = np.ones((5, 5), np.uint8)
        mask_region = cv2.dilate(mask_region, kernel, iterations=1)
        thinned = thinning.guo_hall_thinning(mask_region+0)
        length = cv2.countNonZero(thinned)
        ratio = region.area/length
        return ratio > 10 and length > 50

    def is_valid_region(self, region):
        for check in self.checklist:  # Return False if any condition not satisfied
            if not check(region):
                return False
        return True

    def filter(self):
        self.valid_labels = []
        self.valid_regions = []
        for i, region in enumerate(measure.regionprops(self.markers)):
            if self.is_valid_region(region):
                self.valid_labels.append(region.label)
                self.valid_regions.append(region)

    def yield_roi(self):  # Return a generator
        i = len(self.valid_regions)
        while i > 0:
            roi_mask = np.zeros(self.mask.shape, np.uint8)
            roi_mask[self.markers == self.valid_labels[i-1]] = 255
            i -= 1
            yield roi_mask


if __name__ == '__main__':
    mask = cv2.imread('1_mask.png', 0)
    find_roi = FindROI(mask)
    for roi in find_roi.yield_roi():
        cv2.imshow('img', roi)
        cv2.waitKey(0)
