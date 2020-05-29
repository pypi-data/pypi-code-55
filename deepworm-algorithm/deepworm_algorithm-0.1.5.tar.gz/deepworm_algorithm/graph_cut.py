import cv2
import matplotlib.pyplot as plt
import numpy as np


class GraphCut(object):
    """Segmentation using GraphCut algorithm

    Attributes:
        img (array): Input image
        img_gray: Gray scale image of input image
        img_enhanced: Image of which edges is enhanced by adding shadow
        img_denoise: Image after denoise
        img_corrected (array): Image after illumination correction
        rough_seg_mask: Segmentation mask by Graphcut, edges as initial label
        mask_fuzzy_zone: Mask of fuzzy zone in image
        delicate_seg_mask: Description
        bgdModel: Backgroud model of GraphCut
        fgdModel: Foreground model of GraphCut
        GRAPHCUT_ITER_TIMES (int): Iteration times when applying GraphCUt
        INPAINT_RADIUS (int): Inpaint color is decided by the color of ajacent area
                              within a circle of which radius is INPAINT_RADIUS
        edges: Edges extracted by Canny operator, used as initial label for GraphCut
        init_label: Initial label for GraphCut
        img_enhance_fuzzy_zone: Image of which fuzzy zone is enhanced

    """

    def __init__(self, img=None, img_enhanced=None,
                 illumination_correction=False, delicate=True):
        super(GraphCut, self).__init__()
        self.img = img
        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.img_enhanced = self.img_gray if img_enhanced is None else img_enhanced
        self.img_denoise = cv2.fastNlMeansDenoising(
            self.img_gray, None, 7, 21, 21)
        self.img_corrected = self.img_denoise
        self.rough_seg_mask = np.zeros_like(self.img_gray)
        self.mask_fuzzy_zone = np.zeros_like(self.img_gray)
        self.delicate_seg_mask = np.zeros_like(self.img_gray)
        self.bgdModel = np.zeros((1, 65), np.float64)
        self.fgdModel = np.zeros((1, 65), np.float64)

        self.GRAPHCUT_ITER_TIMES = 1
        self.INPAINT_RADIUS = 30

        # Pipeline：
        self.init_labelling()
        self.rough_segment()
        if illumination_correction:
            self.illumination_correction()
        if delicate:
            self.pick_up_fuzzy_zone()
            self.delicate_segment()
            self.seg_mask = self.delicate_seg_mask
        else:
            self.seg_mask = self.rough_seg_mask

    def init_labelling(self):
        assert len(self.img_gray.shape) == 2
        self.edges = cv2.Canny(self.img_enhanced, 30, 150)

        self.init_label = np.zeros_like(self.img_gray)
        self.init_label[self.edges == 0] = 2  # 2 is PR_BGD
        self.init_label[self.edges == 255] = 3  # 3 is PR_FGD

    def rough_segment(self):
        label = self.init_label + 0
        cv2.grabCut(self.img, label, None, self.bgdModel, self.fgdModel,
                    self.GRAPHCUT_ITER_TIMES, cv2.GC_INIT_WITH_MASK)
        self.rough_seg_mask[label == 1] = 255
        self.rough_seg_mask[label == 3] = 255

    def illumination_correction(self):
        # Step 1: mask out objects
        kernel = np.ones((5, 5), np.uint8)
        mask_dilated = cv2.dilate(self.rough_seg_mask, kernel, iterations=2)
        img_inpaint = cv2.inpaint(self.img_gray, mask_dilated,
                                  self.INPAINT_RADIUS, cv2.INPAINT_NS)

        # Step 2: calculate light field and correct illumination
        blur_radius = max(self.img_gray.shape)//10
        blur = cv2.blur(img_inpaint, (blur_radius, blur_radius))
        mean = cv2.mean(blur)
        light_field = blur/mean[0]
        self.img_corrected = (self.img_denoise/light_field).astype(np.uint8)

    def pick_up_fuzzy_zone(self):
        backgournd_intensity = cv2.mean(self.img_gray,
                                        mask=255-self.rough_seg_mask)[0]
        img_backgroud = self.img_corrected+0
        img_backgroud[self.rough_seg_mask == 255] = int(backgournd_intensity)

        equ = cv2.equalizeHist(img_backgroud+0)
        ret2, th2 = cv2.threshold(equ, 30, 255, cv2.THRESH_BINARY)
        self.mask_fuzzy_zone[th2 == 0] = 255
        self.img_enhance_fuzzy_zone = cv2.addWeighted(
            equ, 0.5, self.img_denoise, 0.5, 0)

    def delicate_segment(self):
        label = np.zeros_like(self.img_gray)
        label[label == 0] = 2  # 2 is PR_BGD
        label[self.edges == 255] = 3  # 3 is PR_FGD
        label[self.mask_fuzzy_zone == 255] = 3  # 3 is PR_FGD

        img = cv2.cvtColor(self.img_enhance_fuzzy_zone, cv2.COLOR_GRAY2BGR)
        cv2.grabCut(img, label, None, self.bgdModel, self.fgdModel,
                    self.GRAPHCUT_ITER_TIMES, cv2.GC_INIT_WITH_MASK)
        self.delicate_seg_mask[label == 1] = 255
        self.delicate_seg_mask[label == 3] = 255


if __name__ == '__main__':
    path1 = '1.jpg'
    path2 = '1_edge_enhanced.png'
    img = cv2.imread(path1)
    img_enhanced = cv2.imread(path2, 0)
    graph_cut = GraphCut(img=img, img_enhanced=img_enhanced,
                         illumination_correction=False)
    cv2.imshow('img', graph_cut.delicate_seg_mask)
    cv2.waitKey(0)
    cv2.imwrite('1_mask.png', graph_cut.delicate_seg_mask)
