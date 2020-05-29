import cv2
import numpy as np
import networkx as nx
from itertools import combinations
from scipy import spatial
import networkx as nx
import matplotlib.pyplot as plt


class PixelAnnotator(object):
    """Annotating a segmentation mask by labelling the mapping relationship 
       between points

    Attributes:
        mask (array): Input segmentation mask
        skeleton (list): Sequence of points of skeleton which have no branches
        mask_labeled_skeleton (array): A mask on which points are labele with its
            index on skeleton sequence
        cnt (list): List of points of contour. Has a redundent dimention[0]
        gradient_x (array): Gradient derived from Scharr operator
        gradient_y (array): Gradient derived from Scharr operator
        curvature_heatmap (array): curverate on each pixel
        end_pt_1 (list): Coordinates(x,y) of one end of skeleton
        end_pt_2 (list): Coordinates(x,y) of another end of skeleton
        contour_graph (Graph): A graph representing the ring structure of contour
        side1 (list): Sequence of points(x,y) of one side on the contour
        side2 (list): Sequence of points(x,y) of another side on the contour
        labels_side1 (list): Labels of corresponding skeleton points of points on side1
        labels_side2 (list): Labels of corresponding skeleton points of points on side2
        widths (list): Local width at each position along skeleton
        side1_widths (list): Local width between skeleton and side1 at each position 
                             along skeleton
        side2_widths (list): Local width between skeleton and side2 at each position 
                             along skeleton
        is_head_ahead (bool): Is the skeleton in the order of head->tail 
        keypoint_dict (dict): Dict of skeleton,two sides, labels of two sides
    """

    def __init__(self, mask, skeleton):
        super(PixelAnnotator, self).__init__()
        self.mask = mask
        self.skeleton = skeleton  # skeleton is a point sequence(list)
        self.mask_labeled_skeleton = np.zeros(mask.shape)

        # Fraction of head/tail length,for estimating body orientation
        self.integral_span = 0.15  # Head(tail) length over body length

        # Pipeline:
        self.find_contour()
        self.label_skeleton()
        self.map_contour_to_skeleton()  # map outline to skeleton
        self.compute_gradients()  # Gradient derived from Scharr operator
        self.draw_curvature_heatmap()
        self.find_end_points()
        self.make_contour_graph()  # graph of the ring structure of contour
        self.cut_graph_to_2_sides()
        self.map_skeleton_to_2_sides()  # map each side of outline to skeleton
        self.compute_widths()
        self.estimate_body_orientation()

    def find_contour(self):
        image, contours, hierarchy = cv2.findContours(
            self.mask+0, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        assert len(contours) == 1
        self.cnt = contours[0].squeeze()

    def label_skeleton(self):
        for i, pt in enumerate(self.skeleton):
            self.mask_labeled_skeleton[pt[1], pt[0]] = i

    def map_contour_to_skeleton(self):
        tree = spatial.KDTree(np.array(self.skeleton))
        labels = tree.query(self.cnt)[1]
        for i, pt in enumerate(self.cnt):
            self.mask_labeled_skeleton[pt[1], pt[0]] = labels[i]

    def compute_gradients(self):
        self.gradient_x = cv2.Scharr(255-self.mask, cv2.CV_32F, 1, 0, scale=1)
        self.gradient_y = cv2.Scharr(255-self.mask, cv2.CV_32F, 0, 1, scale=1)
        self.gradient_x = self.gradient_x + 0.0001  # Avoid div by zero

    def compute_angle(self, x1, y1, x2, y2):
        # Angle between gradient vectors (gx1, gy1) and (gx2, gy2)
        gx1 = self.gradient_x[y1, x1]
        gy1 = self.gradient_y[y1, x1]
        gx2 = self.gradient_x[y2, x2]
        gy2 = self.gradient_y[y2, x2]
        cos_angle = gx1 * gx2 + gy1 * gy2
        cos_angle /= (np.linalg.norm((gx1, gy1)) * np.linalg.norm((gx2, gy2)))
        angle = np.arccos(cos_angle)
        if cos_angle < 0:
            angle = np.pi - angle
        return angle

    def draw_curvature_heatmap(self, n=5):
        self.curvature_heatmap = np.zeros_like(self.mask, dtype=np.float)
        contour = self.cnt.squeeze()
        N = len(contour)
        for i in range(N):
            x1, y1 = contour[i]
            x2, y2 = contour[(i + n) % N]
            angle = self.compute_angle(x1, y1, x2, y2)
            # Get the middle point between i and (i + n)
            x3, y3 = contour[((2*i + n) // 2) % N]
            # Use angle between gradient vectors as score
            self.curvature_heatmap[y3, x3] = angle

    # find body end point on contour. n is length of label span of end segment,
    def find_end_points(self, n=10):
        heatmap_end_1 = (self.curvature_heatmap
                         * [self.mask_labeled_skeleton < n+1]
                         ).squeeze()
        heatmap_end_2 = (self.curvature_heatmap
                         * [self.mask_labeled_skeleton
                            > len(self.skeleton)-n-1]
                         ).squeeze()
        self.end_pt_1 = np.unravel_index(
            np.argmax(heatmap_end_1), heatmap_end_1.shape)[::-1]  # (x,y)
        self.end_pt_2 = np.unravel_index(
            np.argmax(heatmap_end_2), heatmap_end_2.shape)[::-1]  # (x,y)

    def make_contour_graph(self):
        self.contour_graph = nx.Graph()
        self.contour_graph.add_nodes_from(
            ['%d,%d' % (pt[0], pt[1]) for pt in self.cnt])  # (x,y)
        for i, pt in enumerate(self.cnt):
            pt_1 = '%d,%d' % (self.cnt[i][0], self.cnt[i][1])  # (x,y)
            pt_2 = '%d,%d' % (self.cnt[i-1][0], self.cnt[i-1][1])  # (x,y)
            self.contour_graph.add_edge(pt_1, pt_2)

    def cut_graph_to_2_sides(self):
        break_pt_1 = list(
            self.contour_graph.edges(
                '%d,%d' % (self.end_pt_1)))[0][1]  # (x,y)
        break_pt_2 = list(
            self.contour_graph.edges('%d,%d' %
                                     (self.end_pt_2)))[0][1]  # (x,y)
        self.contour_graph.remove_edge('%d,%d' % (self.end_pt_1), break_pt_1)
        self.contour_graph.remove_edge('%d,%d' % (self.end_pt_2), break_pt_2)

        path1 = nx.all_simple_paths(self.contour_graph, source='%d,%d' % (
            self.end_pt_1), target=break_pt_2)  # this is a generator
        side1 = next(path1)
        self.side1 = [[int(pt.split(',')[0]), int(pt.split(',')[1])]
                      for pt in side1]
        path2 = nx.all_simple_paths(self.contour_graph,
                                    source=break_pt_1,
                                    target='%d,%d' % (self.end_pt_2)
                                    )  # this is a generator
        side2 = next(path2)
        self.side2 = [[int(pt.split(',')[0]), int(pt.split(',')[1])]
                      for pt in side2]

    def map_skeleton_to_2_sides(self):
        tree_side1 = spatial.KDTree(np.array(self.side1))
        tree_side2 = spatial.KDTree(np.array(self.side2))
        self.labels_side1 = tree_side1.query(np.squeeze(self.skeleton))[1]
        self.labels_side2 = tree_side2.query(np.squeeze(self.skeleton))[1]

    def compute_widths(self):
        self.widths = []
        self.side1_widths = []
        self.side2_widths = []
        for i in range(len(self.skeleton)):
            pt1 = np.array(self.side1[self.labels_side1[i]])
            pt2 = np.array(self.side2[self.labels_side2[i]])
            skeleton_pt = self.skeleton[i]
            self.widths.append(np.linalg.norm(pt1-pt2))
            self.side1_widths.append(np.linalg.norm(pt1-skeleton_pt))
            self.side2_widths.append(np.linalg.norm(pt2-skeleton_pt))

    def estimate_body_orientation(self):
        integral_length = int(self.integral_span*len(self.skeleton))
        area1 = sum(self.widths[:integral_length])
        area2 = sum(self.widths[-integral_length:])
        self.is_head_ahead = area1 > area2
        return area1 > area2

    def draw_2_sides(self):
        mask = np.zeros_like(self.mask)
        for i, pt in enumerate(self.side1):
            mask[pt[1], pt[0]] = 1  # label should start from 1, 0 is bg
        for i, pt in enumerate(self.side2):
            mask[pt[1], pt[0]] = 2  # label should start from 1, 0 is bg
        plt.imshow(mask)
        plt.colorbar()
        plt.show()


if __name__ == '__main__':
    path = "1.jpg"
    img = cv2.imread(path)
    img = cv2.resize(img, (200, 200))
    mask = cv2.imread('mask_0.png', 0)
    mask = cv2.resize(mask, (200, 200))
    from skeleton_extractor import SkeletonExtractor
    skeleton_extractor = SkeletonExtractor(mask)
    skeleton = skeleton_extractor.skeleton
    pixel_annotator = PixelAnnotator(mask, skeleton)
    pixel_annotator.draw_2_sides()
