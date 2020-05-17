from .utils import index_to_slice
from .dataset import Dataset
from .enums import layouts_2dseq
from .ontology import *

import numpy as np
import copy

SUPPORTED_FG = ['FG_ISA','FG_IRMODE']

class Splitter(object):
    pass


class FrameGroupSplitter(Splitter):
    def __init__(self, fg):
        if fg not in SUPPORTED_FG:
            raise NotImplemented('Split operation for {} is not implemented'.format(fg))

        super(FrameGroupSplitter, self).__init__()
        self.fg = fg

    def split(self, dataset, index=None, write=False, path_out=None, **kwargs):
        """Split Bruker object along a dimension of specific frame group.
        Only the frame groups listed in SPLIT_FG_IMPLEMENTED can be used to split the object.

        Parameters
        ----------
        fg - list of fg's along which to split
        index - list of lists of indexes

        Returns
        -------
        List of objects incurred during splitting.

        """
        """
        CHECK if FG and index are valid
        """
        # If no index is specified, all elements of given dimension will be splited
        if index is None:
            index = []

        if isinstance(index, int):
            index = [index, ]

        if not self.fg in dataset.fg_scheme.dim_type:
            raise ValueError(f'Dataset does not contain {self.fg} frame group')

        fg_index = dataset.dim_type.index(self.fg)

        if not index:
            index = list(range(dataset.fg_scheme.dim_size(index=fg_index)))  # all items of given dimension

        if max(index) >= dataset.dim_size[fg_index]:
            raise IndexError(f'Index {index} out of bounds, size of {self.fg} dimension is {dataset.dim_size(index=fg_index)}')

        """
        PERFORM splitting
        """
        data = dataset.data
        visu_pars = dataset.parameters['visu_pars']
        fg_scheme = dataset.fg_scheme
        fg_ind = fg_scheme.dim_type.index(self.fg)

        datasets = []

        for index_ in index:
            if write and path_out:
                path = '{}_{}_{}/2dseq'.format(path_out, self.fg, index_)
            else:
                path = '{}_{}_{}/2dseq'.format(dataset.parent, self.fg, index_)

            # split visu_pars
            if self.fg == 'FG_ISA':
                visu_pars_ = self.split_params_FG_ISA(copy.deepcopy(visu_pars), fg_scheme, index_, fg_index)

            # split data array
            slc = index_to_slice(index_, data.shape, fg_ind)
            dataset_ = Dataset(path=path, load=False)
            dataset_.parameters = {'visu_pars': visu_pars_}
            dataset_.data = dataset.get_data(slc=slc, copy=True)
            dataset_.load_fg_scheme()
            datasets.append(dataset)

            if write:
                dataset_.write(dataset_.path, **kwargs)

        return datasets

    def split_params_FG_ISA(self, visu_pars, fg_scheme, index, fg_ind):

        visu_pars = split_VisuFGOrderDescDim(visu_pars)
        visu_pars = split_VisuFGOrderDesc(visu_pars, self.fg)
        visu_pars = split_VisuCoreFrameCount(visu_pars, fg_scheme.layout_shapes['frame_groups'][fg_ind])
        visu_pars = split_VisuCoreDataSlope(visu_pars, fg_scheme, index, fg_ind)
        visu_pars = split_VisuCoreDataOffs(visu_pars, fg_scheme, index, fg_ind)
        visu_pars = split_VisuCoreDataMin(visu_pars, fg_scheme, index, fg_ind)
        visu_pars = split_VisuCoreDataMax(visu_pars, fg_scheme, index, fg_ind)
        visu_pars = split_VisuCoreDataUnits(visu_pars, fg_scheme, index, fg_ind)
        visu_pars = split_VisuFGElemComment(visu_pars, fg_scheme, index, fg_ind)

        return visu_pars

    def split_params_FG_IRMODE(self, visu_pars):
        pass


class SlicePackageSplitter(Splitter):
    def __init__(self):
        pass

    def split(self, dataset):
        return dataset

    # def split_slice_packages(self) -> list:
    #     """Some data formats do not support separate orientation for individual parts, so"""
    #     # TODO find out, how to destroy object after split
    #
    #     if not self.fg_scheme:
    #         raise AttributeError('No fg_scheme found, cannot perform split_slice_packages')
    #
    #     try:
    #         VisuCoreSlicePacksSlices = self.parameters.get_list('VisuCoreSlicePacksSlices')
    #     except KeyError:
    #         print('Parameter VisuCoreSlicePacksSlices not found')
    #
    #     bruker_objs = []
    #     frame_range = [0,0]
    #
    #     fg_abs_index = self.fg_scheme.get_abs_fg_index(FG_TYPE.FG_SLICE)
    #     fg_rel_index = self.fg_scheme.get_rel_fg_index(FG_TYPE.FG_SLICE)
    #
    #     for sp_index in range(len(VisuCoreSlicePacksSlices)):
    #         """
    #         SPLIT data
    #         """
    #         slice_package = VisuCoreSlicePacksSlices[sp_index]
    #
    #         # getting range in the slice framegroup
    #         frame_range[0] = frame_range[1]
    #         frame_range[1] += slice_package[1]
    #
    #         data_slices = []
    #
    #         for dim_index in range(self.get_dim()):
    #             if dim_index == fg_abs_index:
    #                 data_slices.append(slice(frame_range[0], frame_range[1]))
    #             else:
    #                 data_slices.append(slice(0, self.get_size(index=dim_index)))
    #
    #
    #         data_slab = np.squeeze(self.data[tuple(data_slices)])
    #
    #         """
    #         SPLIT parameteres
    #         """
    #         parameters_copy = copy.deepcopy(self.parameters)
    #
    #         """
    #         MODIFY relevant parameters
    #         """
    #         VisuCoreOrientation = parameters_copy.get_float_array('VisuCoreOrientation', shape=(-1,9), order='C')
    #         parameters_copy.set_array('VisuCoreOrientation',VisuCoreOrientation[frame_range[0]:frame_range[1]], order='C')
    #
    #         VisuCorePosition = parameters_copy.get_float_array('VisuCorePosition', shape=(-1,3))
    #         parameters_copy.set_array('VisuCorePosition', VisuCorePosition[frame_range[0]:frame_range[1]])
    #
    #         VisuCoreDataMin = parameters_copy.get_float_array('VisuCoreDataMin')
    #         parameters_copy.set_array('VisuCoreDataMin', VisuCoreDataMin[frame_range[0]:frame_range[1]])
    #
    #         VisuCoreDataMax = parameters_copy.get_float_array('VisuCoreDataMax')
    #         parameters_copy.set_array('VisuCoreDataMax', VisuCoreDataMax[frame_range[0]:frame_range[1]])
    #
    #         VisuCoreDataOffs = parameters_copy.get_float_array('VisuCoreDataOffs')
    #         parameters_copy.set_array('VisuCoreDataOffs', VisuCoreDataOffs[frame_range[0]:frame_range[1]])
    #
    #         VisuCoreDataSlope = parameters_copy.get_float_array('VisuCoreDataSlope')
    #         parameters_copy.set_array('VisuCoreDataSlope', VisuCoreDataSlope[frame_range[0]:frame_range[1]])
    #
    #         # not sure about this one
    #         VisuFGOrderDesc = parameters_copy.get_nested_list('VisuFGOrderDesc') # ASSUMPTION
    #         VisuFGOrderDesc[fg_rel_index][0] = slice_package[1]
    #         parameters_copy.set_nested_list('VisuFGOrderDesc', VisuFGOrderDesc)
    #
    #         VisuCoreFrameCount = parameters_copy.get_int('VisuCoreFrameCount')
    #         VisuCoreFrameCount //= len(VisuCoreSlicePacksSlices)
    #         parameters_copy.set_int('VisuCoreFrameCount',VisuCoreFrameCount)
    #
    #         name = f'{self.name}_sp{sp_index}'
    #
    #         bruker_objs.append(Bruker(paths=self.paths, data=data_slab, params=parameters_copy, name=name))
    #
    #     return bruker_objs
