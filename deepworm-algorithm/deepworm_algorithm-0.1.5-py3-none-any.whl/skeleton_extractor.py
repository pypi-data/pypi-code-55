import cv2
import numpy as np
import thinning
import networkx as nx
from itertools import combinations


class SkeletonExtractor(object):
    """Extract skeleton. First thinning, then make a graph to represent the branching
       structure. By searching longest path to find the path of skeleton

    Attributes:
        mask (array): Input segmentation mask
        thinned (array): Binary image. Skelton is 1-pixel width curve
        pixelpoints (list): List of points(y,x) on thinned image
        tip_pts (list): List of points that at end of curve
        fork_pts (list): List of points that connection multiple branches
        inter_pts (list): List of points that are in the middle of a branch
        graph (Graph): A graph representing the structure of branches on thinned image
        skeleton (list): Sequence of points on skeleton which do not have any branch
        mask_skeleton (array): Binary mask on which drawn the skeleton
    """

    def __init__(self, mask):
        super(SkeletonExtractor, self).__init__()
        self.mask = mask

        # Pipeline:
        self.thinning()
        self.classify_points()
        self.make_graph()
        self.find_skeleton()
        self.draw_skeleton()

    def thinning(self):
        self.thinned = thinning.guo_hall_thinning(self.mask+0)

    def classify_points(self):
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        dst = (cv2.filter2D(self.thinned/255, cv2.CV_64F, kernel))
        dst2 = np.uint8(dst)
        # only reserve pixels on thinned image
        dst2 = cv2.bitwise_and(dst2, dst2, mask=self.thinned)
        self.pixelpoints = np.transpose(np.nonzero(dst2))

        self.tip_pts = [[pt[0], pt[1]]
                        for pt in self.pixelpoints if dst2[pt[0]][pt[1]] == 1]
        self.fork_pts = [[pt[0], pt[1]]
                         for pt in self.pixelpoints if dst2[pt[0]][pt[1]] > 2]
        self.inter_pts = [[pt[0], pt[1]]
                          for pt in self.pixelpoints if dst2[pt[0]][pt[1]] == 2]

    def find_neighbors(self, x, y, mask):
        h, w = mask.shape
        neighbors = []
        for i in range(max(0, x-1), min(w, x+2)):
            for j in range(max(0, y-1), min(w, y+2)):
                if mask[j, i] > 0 and [i, j] != [x, y]:
                    neighbors.append([i, j])
        return neighbors

    def make_graph(self):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(['%d,%d' % (pt[1], pt[0])
                                   for pt in self.pixelpoints])
        for y, x in self.pixelpoints:
            neighbors = self.find_neighbors(x, y, self.thinned)
            for i in neighbors:
                self.graph.add_edge('%d,%d' % (x, y), '%d,%d' % (i[0], i[1]))

    def find_skeleton(self):
        paths = []
        for i in combinations(self.tip_pts, 2):
            paths += nx.all_simple_paths(self.graph, source='%d,%d' %
                                         (i[0][1], i[0][0]), target='%d,%d' % (i[1][1], i[1][0]))
        self.skeleton = max(paths, key=len)
        self.skeleton = [[int(pt.split(',')[0]), int(
            pt.split(',')[1])] for pt in self.skeleton]

    def draw_skeleton(self):
        self.mask_skeleton = np.zeros(self.mask.shape)
        skeleton_expend_dim = np.expand_dims(self.skeleton, axis=1)
        cv2.drawContours(self.mask_skeleton, np.array(
            skeleton_expend_dim), -1, 255, 1)


if __name__ == '__main__':
    mask = cv2.imread('mask_0.png', 0)
    skeleton_extractor = SkeletonExtractor(mask)
    cv2.imshow('img', skeleton_extractor.mask_skeleton)
    cv2.waitKey(0)
