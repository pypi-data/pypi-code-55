from PerceptionToolkit import Version
from PerceptionToolkit.PluginInterfaces import IClassificationPlugin
from PerceptionToolkit.DataModel import DataModel
from PerceptionToolkit.EyeMovements import Fixation

from typing import Sequence, Dict, Any, Union
import numpy as np
import matplotlib.pyplot as plt


class ClassificationNeedlemanWunsch(IClassificationPlugin):
    """
    Needleman-Wunsch (ScanMatch)
    Based on: https://link.springer.com/article/10.3758/BRM.42.3.692
    The scanpath is compared pairwise to every other scanpath in the set using the Needleman-Wunsch string
    alignment algorithm. Prediction is done via KNN.

    Attributes:
        gap_penalty: penalty score for each gap in the scanpath
        horizontal_alphabet_size: number of bins in the image along the x-axis
        vertical_alphabet_size: number of bins in the image along the y-axis
        image_dimensions: dimension of the image
        sampling: sampling size for the fixation duration
        enable_duration: specify whether the fixation should be repeated respective of its duration
        nearest_neighbors: the number of most similar scanpaths to the given scanpath
        enable_plot: specify whether to represent the data in graphical format
    """

    @staticmethod
    def version() -> Version:
        return Version(0, 0, 1)

    def __init__(self):
        super(ClassificationNeedlemanWunsch, self).__init__()
        # User determinable
        self.gap_penalty: int = 0
        self.horizontal_alphabet_size: int = 5
        self.vertical_alphabet_size: int = 3
        self.image_dimensions: tuple = None
        self.sampling: int = 100
        self.enable_duration: bool = True
        self.nearest_neighbors: int = 5
        self.enable_plot: bool = False

        self.substitution_matrix = np.array((1, 1))
        self.scoring_mats = []
        self.distance_matrix = []
        self.features = []
        self.labels = []
        # TODO just the default. The encoding boundaries are readjusted when find_boudaries is called
        self.encoding_boundaries_x = None
        self.encoding_boundaries_y = None
        # self.encoding_boundaries_x = np.linspace(0, self.image_dimensions[0], self.horizontal_alphabet_size + 1)[1:]
        # self.encoding_boundaries_y = np.linspace(0, self.image_dimensions[1], self.vertical_alphabet_size + 1)[1:]

    def apply_parameters(self, parameters: Dict[str, Any]) -> None:
        self.gap_penalty = parameters.get("gap_penalty", self.gap_penalty)
        self.horizontal_alphabet_size = parameters.get("horizontal_alphabet_size", self.horizontal_alphabet_size)
        self.vertical_alphabet_size = parameters.get("vertical_alphabet_size", self.vertical_alphabet_size)
        assert self.horizontal_alphabet_size > 0 and self.vertical_alphabet_size > 0, "Alphabet size must be greater than 0."
        self.image_dimensions = parameters.get("image_dimensions", self.image_dimensions)
        # assert 0 not in self.image_dimensions, "Inappropriate image dimension."
        self.sampling = parameters.get("sampling", self.sampling)
        assert self.sampling > 0, "Sampling must be greater than zero."
        self.enable_duration = parameters.get("enable_duration", self.enable_duration)
        self.nearest_neighbors = parameters.get("nearest_neighbors", self.nearest_neighbors)
        assert self.nearest_neighbors > 0, "Nearest neighbors must be greater than 0."
        self.enable_plot = parameters.get("enable_plot", self.enable_plot)

    def find_boundaries(self, data: Sequence[DataModel]) -> tuple:
       # if image dimensions not manually set, find the minimum/maximum x/y coordinates to determine the boundaries for
       # the image binning

        if self.image_dimensions is not None:
            print("Detected manually set image dimensions")
            self.encoding_boundaries_x = np.linspace(0, self.image_dimensions[0], self.horizontal_alphabet_size + 1)[1:]
            self.encoding_boundaries_y = np.linspace(0, self.image_dimensions[1], self.vertical_alphabet_size + 1)[1:]
            return 0, 0, self.image_dimensions[0], self.image_dimensions[1]

        print("Automatically determining image dimensions")
        min_x: int = 999
        min_y: int = 999
        max_x: int = -999
        max_y: int = -999

        # TODO update all the values
        for scanpath in data:
            # extracts a list of fixations from the datamodel. fixation := [centroid: (int, int), duration: int]
            fixations_centroid_duration = np.apply_along_axis(
                lambda f: Fixation(scanpath, f[1], f[2]).centroid, 1,
                scanpath.fixations())
            temp_minx = min(fixations_centroid_duration, key=lambda x: x[0])[0]
            temp_miny = min(fixations_centroid_duration, key=lambda x: x[1])[1]
            temp_maxx = max(fixations_centroid_duration, key=lambda x: x[0])[0]
            temp_maxy = max(fixations_centroid_duration, key=lambda x: x[1])[1]
            min_x = min(min_x, temp_minx)
            min_y = min(min_y, temp_miny)
            max_x = max(max_x, temp_maxx)
            max_y = max(max_y, temp_maxy)

        self.encoding_boundaries_x = np.linspace(min_x, max_x, self.horizontal_alphabet_size + 1)[1:]
        self.encoding_boundaries_y = np.linspace(min_y, max_y, self.vertical_alphabet_size + 1)[1:]

        print("Detected boundaries: ({}, {}) ({}, {})".format(min_x, min_y, max_x, max_y))
        return min_x, min_y, max_x, max_y

    def calculate_substitution_matrix(self, len_ROIs: int):
        # Takes the total number of ROIs and creates a substitution matrix of 1's and -1's

        self.substitution_matrix = np.full((len_ROIs, len_ROIs), -1)
        np.fill_diagonal(self.substitution_matrix, 1)

    def encode_fixation(self, fix) -> list:
        # Takes a fixation (centroid, duration) and encodes it into a repeating integer

        centroid, duration = 0, 1

        # assert all([fix[centroid][i] <= self.image_dimensions[i] for i in [0, 1]]), "Fixation going over image boundary"

        x = np.argmax(fix[centroid][0] <= self.encoding_boundaries_x)
        y = np.argmax(fix[centroid][1] <= self.encoding_boundaries_y)

        # calculate ROI position using 2D row-major order: offset = (row_index * TotalCols) + col_index
        roi: int = (y * self.horizontal_alphabet_size) + x

        repeat: int = int(fix[duration] / self.sampling)

        return [roi for _ in range(repeat)] if self.enable_duration else [roi]

    def encode(self, scanpath: DataModel) -> list:
        # Encodes a given scanpath into a list of integers

        # extracts a list of fixations from the datamodel. fixation := [centroid: (int, int), duration: int]
        fixations_centroid_duration = np.apply_along_axis(
            lambda f: [Fixation(scanpath, f[1], f[2]).centroid, Fixation(scanpath, f[1], f[2]).duration], 1,
            scanpath.fixations())

        scanpath_ = []

        # converts each fixation into a list of repeating (if duration enabled) integer and extends it to the scanpath
        for fix in fixations_centroid_duration:
            scanpath_.extend(self.encode_fixation(fix))

        return scanpath_

    def align(self, score_mat, sp1, sp2):
        # shows best alignment for two scanpaths given a scoring matrix. Must call compare_pairwise method beforehand
        # this method is solely used for the visual representation of the alignment of two scanpaths and does not really
        # play any role outside this script.

        align_a = ""
        align_b = ""
        offset = 1
        i = len(sp1)
        j = len(sp2)

        while i > 0 or j > 0:
            if i > 0 and j > 0 and \
               score_mat[j, i] == score_mat[j - 1, i - 1] + self.get_match_score(j - offset, i - offset, sp1, sp2):
                align_a = str(sp1[i-offset]) + align_a
                align_b = str(sp2[j-offset]) + align_b
                i -= 1
                j -= 1
            elif i > 0 and score_mat[j, i] == score_mat[j - 1, i] + self.gap_penalty:
                align_a = str(sp1[i-offset]) + align_a
                align_b = "--" + align_b
                i -= 1
            else:
                align_a = "--" + align_a
                align_b = str(sp2[j-offset]) + align_b
                j -= 1

        print("Alignment")
        # for i in range(0, len(alignA)):
        #     print(alignA[i] + " <-> " + alignB[i] )
        print(align_a)
        print(align_b)

    def compare_needlemanwunsch(self, scanpath1: Sequence[int], scanpath2: Sequence[int]) -> float:
        # after NMW comparison, the scoring matrix is then appended to the attribute self.scoring_mats

        m_width: int = len(scanpath1)
        m_height: int = len(scanpath2)
        scoring_matrix = np.zeros((m_height + 1, m_width + 1))

        # filling first col and row
        for c in range(1, m_width + 1):
            scoring_matrix[0, c] = scoring_matrix[0, c - 1] + self.gap_penalty
        for r in range(1, m_height + 1):
            scoring_matrix[r, 0] = scoring_matrix[r - 1, 0] + self.gap_penalty

        # filling the rest
        offset = 1  # with respect to theta in substitution matrix
        for c in range(offset, m_width + offset):
            for r in range(offset, m_height + offset):
                scoring_matrix[r, c] = max(
                      scoring_matrix[r-1, c-1] + self.get_match_score(r - offset, c - offset, scanpath1, scanpath2) # diagonal
                    , scoring_matrix[r-1, c] + self.gap_penalty                                               # up
                    , scoring_matrix[r, c-1] + self.gap_penalty                                               # left
                )

        self.scoring_mats.append(scoring_matrix)

        return self.get_score(scoring_matrix, scanpath1, scanpath2)

    def get_match_score(self, row: int, col: int, sp1: Sequence[int], sp2: Sequence[int]) -> int:
        return self.substitution_matrix[sp2[row], sp1[col]]

    def get_score(self, score_mat, sc1, sc2) -> float:
        # takes the maximum alignment score from the scoring matrix and returns the normalized score

        score = score_mat[-1, -1]
        max_sub_score = np.max(self.substitution_matrix)
        max_len = max(len(sc1), len(sc2))

        return score / (max_sub_score*max_len)

    def calculate_distance_matrix(self, data: Sequence[DataModel]) -> None:
        ### Creating a nxn distance matrix
        # Initialize an empty nxn distance matrix
        # Create substitution matrix
        # Fill up the distance matrix (commented out because not really useful. Might do away with distance_matrix)
        progress = ""
        print("Generating distance matrix:")

        self.distance_matrix = np.zeros((len(data), len(data)))
        self.calculate_substitution_matrix(self.horizontal_alphabet_size * self.vertical_alphabet_size)

        for scanpath in data:
            self.features.append(self.encode(scanpath))
            self.labels.append(scanpath.meta[DataModel.META.LABEL])

        for i, scanpath1 in enumerate(self.features):
            progress += "▉"
            print(progress)
            for j, scanpath2 in enumerate(self.features[i:]): # assume: commutative relationship
                self.distance_matrix[i+j,i] = self.compare_needlemanwunsch(scanpath1, scanpath2)

        if self.enable_plot:
            ticks = ["t{}_s{}_sb{}".format( sp.meta[DataModel.META.LABEL]
                                          , sp.meta[DataModel.META.STIMULUS]
                                          , sp.meta[DataModel.META.SUBJECT]
                                           ) for sp in data]
            plt.imshow(self.distance_matrix, cmap="nipy_spectral")
            plt.colorbar()
            plt.clim(0,1)
            plt.xticks(np.arange(len(data)), ticks, rotation="vertical")
            plt.yticks(np.arange(len(data)), ticks)

            ### add score to each cell
            # for i in range(len(self.distance_matrix)):
            #     for j in range(len(self.distance_matrix)):
            #         text = plt.text(j, i, round(self.distance_matrix[i, j], 2),
            #                        ha="center", va="center", color="w")

            plt.show()
            plt.close()

    def fit(self, data: Sequence[DataModel]) -> None:
        """
        Extracts and encodes the scanpath from each datamodel. Each scanpath and its corresponding label is stored
        for the prediction step.

        :param data: Sequence[DataModel]
        :return: None
        """
        # ------ Steps: ------
        # Reset the features and labels
        # Save features and labels of each scanpath in data

        self.find_boundaries(data)

        self.features = []
        self.labels = []

        for scanpath in data:
            self.features.append(self.encode(scanpath))
            self.labels.append(scanpath.meta[DataModel.META.LABEL])

    def predict(self, data: DataModel) -> int:
        """
        Predicts the label of given data based on set specified in fit-step (using NMW and KNN)

        :param
        data: DataModel
            The datamodel to be predicted
        :return:
        prediction: int
            The predicted label
        """

        # ------ Steps: ------
        # Initialize empty distance array
        # Encode the scanpath from the datamodel
        # Compare (using NMW) the scanpath to every other scanpath saved in the list, add score to the distance array
        # Get index of k-nearest neighbors to scanpath
        # Get most frequently occurring label =: prediction
        # Save prediction in datamodel metric

        self.calculate_substitution_matrix(self.horizontal_alphabet_size * self.vertical_alphabet_size)

        # array containing distances to scanpath in question
        dist_to_sp1 = np.zeros((1, len(self.features)))
        print("Features length {}".format(len(self.features)))

        sp1 = self.encode(data)

        for l, scanpath in enumerate(self.features):
            dist_to_sp1[0, l] = self.compare_needlemanwunsch(sp1, scanpath)

        # get index of k nearest scanpaths (biggest NMW score) !!! the result is unsorted
        k_nearest_index = np.argpartition(dist_to_sp1[0], -self.nearest_neighbors)[-self.nearest_neighbors:]

        nearest_distance = [dist_to_sp1[0][i] for i in k_nearest_index]
        nearest_labels = [self.labels[i] for i in k_nearest_index]
        print("k={} Nearest neighbors: {}".format(self.nearest_neighbors, nearest_labels))
        print("Nearest distance: {}".format(nearest_distance))

        # get the most frequently occurring label
        prediction = np.argmax(np.bincount(nearest_labels))
        data.metrics["prediction"] = int(prediction)
        print("Predicted label: {}".format(prediction))
        print("True label: {}".format(data.meta[DataModel.META.LABEL]))

        if self.enable_plot:
            plt.imshow(dist_to_sp1, cmap='cool')
            plt.colorbar(orientation='horizontal')
            plt.clim(min(dist_to_sp1[0]), max(dist_to_sp1[0]))
            plt.xticks(np.arange(len(self.features)), self.labels)
            plt.yticks(np.arange(1), [data.meta[DataModel.META.LABEL]])
            plt.ylabel("True label")
            plt.xlabel("Predicted label")
            plt.title("Prediction using KNN (k={})".format(self.nearest_neighbors))

            # show distance
            # for i in range(len(dist_to_sp1[0])):
            #     col = "r" if i in k_nearest_index else "w"
            #     text = plt.text(i, 0, round(dist_to_sp1[0, i], 2), ha="center", va="center", color=col)

            plt.show()
            plt.close()

        ################# test ######################
        # predictions = []
        # for i, sp in enumerate(self.features):
        #     for l, sp2 in enumerate(self.features):
        #         dist_to_sp1[0, l] = self.compare_needlemanwunsch(sp, sp2)
        #
        #     # leave out self comparison which is already equal to 1
        #     k_nearest_indices = np.argpartition(dist_to_sp1[0], -self.nearest_neighbors)[-self.nearest_neighbors:]
        #     nearest_labels = [self.labels[i] for i in k_nearest_indices]
        #
        #     most_common_label = np.argmax(np.bincount(nearest_labels))
        #
        #     predictions.append(most_common_label)
        #
        # truth = [int(i) for i in self.labels]
        #
        # print("Predictions %s" % predictions)
        # print("Truth       %s" % truth)
        #
        # c = confusion_matrix(truth, predictions)
        # normalized_c = c/c.astype(np.float).sum(axis=1)
        # print(normalized_c)
        #
        # plt.imshow(normalized_c, cmap='nipy_spectral')
        # plt.colorbar()
        # plt.clim(0, 1)
        # plt.xticks(np.arange(7), ['T{}'.format(t) for t in range(1,8)])
        # plt.yticks(np.arange(7), ['T{}'.format(t) for t in range(1,8)])
        # plt.xlabel("Predictions")
        # plt.ylabel("Ground Truth")
        #
        # plt.show()
        ################# end test ######################

        return int(prediction)