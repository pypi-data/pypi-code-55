import cv2
import numpy as np
from collections import Counter


class MMSICHE(object):

    def __init__(self, img_path):
        self.img = cv2.imread(img_path, 0)
        self.h, self.w = self.img.shape
        self.freq_map = Counter(self.img.flatten())
        self.equalise_image()

    def calc_xe(self):
        self.xe = int(round(np.median(self.img)))

    def calc_xml_and_xmu(self):
        cnt_xml, cnt_xmu = 0, 0
        sum_xml, sum_xmu = 0, 0

        for i in range(self.h):
            for j in range(self.w):
                if self.img[i][j] < self.xe:
                    cnt_xml += 1
                    sum_xml += self.img[i][j]
                else:
                    cnt_xmu += 1
                    sum_xmu += self.img[i][j]

        self.xml = int(round(sum_xml / cnt_xml))
        self.xmu = int(round(sum_xmu / cnt_xmu))

    def equalize_hist(self, low, high):
        i_map = {}
        sum_t, L, prev_cum_p = 0, high - low, 0.0

        for it in range(low, high + 1):
            sum_t += self.freq_map[it]
        for it in range(low, high + 1):
            prev_cum_p += self.freq_map[it] / sum_t
            i_map[it] = round((L * prev_cum_p) + low)

        for i in range(self.h):
            for j in range(self.w):
                if low <= self.img[i][j] <= high:
                    self.img[i][j] = i_map[self.img[i][j]]

    def equalise_image(self):
        self.calc_xe()
        self.calc_xml_and_xmu()
        self.equalize_hist(0, self.xml)
        self.equalize_hist(self.xml + 1, self.xe)
        self.equalize_hist(self.xe + 1, self.xmu)
        self.equalize_hist(self.xmu + 1, 255)
